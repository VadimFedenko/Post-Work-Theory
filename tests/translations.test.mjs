import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { recordText } from '../scripts/record-localization.mjs';
import { validateTranslations } from '../scripts/translation-data.mjs';

const readJSON = async path => JSON.parse(await readFile(new URL(path, import.meta.url), 'utf8'));
const { societies } = await readJSON('../data/societies.json');
const catalog = await readJSON('../data/society-translations.ru.json');

test('every society has a Russian description matching the current English source', async () => {
  validateTranslations(societies, catalog);
  assert.equal(Object.keys(catalog.translations).length, societies.length);
  for (const source of societies) {
    const record = await readJSON(`../public/data/records/${source.id}.json`);
    assert.equal(record.description, source.description, `${source.id}: English source preserved`);
    assert.equal(record.post_work_assessment.basis, source.post_work_assessment.basis);
    const ru = recordText(record, 'ru');
    assert.equal(ru.description, catalog.translations[source.id].description, source.id);
    assert.equal(ru.economyBasis, catalog.translations[source.id].economy_basis, source.id);
    assert.equal(ru.language, 'ru');
    assert.equal(ru.description.split(/\n\s*\n/).length, source.description.split(/\n\s*\n/).length, `${source.id}: all paragraphs retained`);
    assert.notEqual(ru.description, source.description);
    assert.equal(recordText(record, 'en').description, source.description);
  }
});

test('a cached record switches RU → EN → RU without mutating either text', async () => {
  const record = await readJSON(`../public/data/records/${societies[0].id}.json`);
  const before = structuredClone(record);
  const ru = recordText(record, 'ru');
  const en = recordText(record, 'en');
  assert.equal(en.language, 'en');
  assert.equal(en.description, record.description);
  assert.equal(en.economyBasis, record.post_work_assessment.basis);
  assert.deepEqual(recordText(record, 'ru'), ru);
  assert.deepEqual(record, before);
  const legacy = { ...record, translations: undefined };
  assert.deepEqual(recordText(legacy, 'ru'), en, 'old cached records keep an honestly labelled English fallback');
});

test('incomplete, orphaned or stale translations cannot enter the web build', () => {
  const first = societies[0];
  const one = { language: 'ru', translations: { [first.id]: catalog.translations[first.id] } };
  assert.throws(() => validateTranslations(societies, one), /Missing Russian translation/);
  assert.throws(() => validateTranslations([first], { ...one, translations: { ...one.translations, unknown: one.translations[first.id] } }), /Unknown translation ID/);
  assert.throws(() => validateTranslations([{ ...first, description: first.description + ' New evidence.' }], one), /Stale Russian translation/);
  const empty = { ...one.translations[first.id], description: '' };
  assert.throws(() => validateTranslations([first], { ...one, translations: { [first.id]: empty } }), /Missing Russian description/);
});
