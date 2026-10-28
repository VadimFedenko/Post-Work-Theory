import { readFile, writeFile } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { translationSourceHash } from './translation-data.mjs';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const { societies } = JSON.parse(await readFile(resolve(root, 'data/societies.json'), 'utf8'));
const records = new Map(societies.map(record => [record.id, record]));
const catalogPath = resolve(root, 'data/society-translations.ru.json');
const catalog = JSON.parse(await readFile(catalogPath, 'utf8'));
const bases = JSON.parse(await readFile(resolve(root, 'data/translation-bases.ru.json'), 'utf8'));
for (const input of process.argv.slice(2)) {
  const batch = JSON.parse(await readFile(resolve(root, input), 'utf8'));
  for (const [id, description] of Object.entries(batch)) {
    const source = records.get(id);
    if (!source) throw new Error(`Unknown society: ${id}`);
    if (typeof description !== 'string' || !/[А-Яа-яЁё]/u.test(description)) throw new Error(`Invalid translation: ${id}`);
    catalog.translations[id] = {
      ...catalog.translations[id],
      source_sha256: translationSourceHash(source),
      description,
      translation_method: 'direct_from_english',
    };
  }
}
for (const record of societies) {
  const basis = bases[record.post_work_assessment.basis];
  if (!basis) throw new Error(`Missing direct economy translation: ${record.id}`);
  catalog.translations[record.id].economy_basis = basis;
  if (catalog.translations[record.id].translation_method === 'direct_from_english') {
    // The English taxonomy conclusion is identical for every occurrence of a
    // basis. Use its separately authored direct translation consistently.
    const text = catalog.translations[record.id].description;
    const conclusions = [...text.matchAll(/(?:По классификации статьи[,:]|Классификация в соответствии со стать[её]й:|Классификация по статье:|Согласно классификации статьи[,:])/gu)];
    if (!conclusions.length) throw new Error(`Missing taxonomy conclusion: ${record.id}`);
    catalog.translations[record.id].description = text.slice(0, conclusions.at(-1).index).trimEnd()
      + ' Классификация по статье: ' + basis + ' Полезная деятельность и доля неработающих оцениваются отдельно.';
  }
}
const done = societies.filter(record => catalog.translations[record.id]?.translation_method === 'direct_from_english').length;
catalog.method = done === societies.length
  ? 'Direct translation of every description from its English original by the assistant; no translation service or local translation model.'
  : 'Direct retranslation from English is in progress. Only entries marked direct_from_english have been replaced; other entries still contain the rejected machine-translation draft.';
catalog.direct_translation_progress = { complete: done, total: societies.length };
if (done === societies.length) {
  delete catalog.model;
  delete catalog.model_license;
  delete catalog.attribution;
  catalog.authors = ['Assistant', 'GPT-6.1 Terra agents'];
}
await writeFile(catalogPath, JSON.stringify(catalog, null, 2) + '\n');
console.log(`Direct translations: ${done}/${societies.length}`);
