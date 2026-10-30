import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

const read = async path => JSON.parse(await readFile(new URL('../' + path, import.meta.url), 'utf8'));
const { societies } = await read('data/societies.json');
const overlay = await read('data/society-popularity.json');

test('all society scores inherit one complete explicitly reviewed recognition unit', () => {
  assert.equal(societies.length, 893);
  assert.equal(Object.keys(overlay.assignments).length, 893);
  const seen = new Map();
  for (const record of societies) {
    const score = record.popularity_score;
    assert.ok(Number.isFinite(score) && score >= 0 && score <= 1, record.id);
    assert.ok(Math.abs(score * 20 - Math.round(score * 20)) < 1e-8);
    const subjectId = overlay.assignments[record.id].subject_id;
    const subject = overlay.subjects[subjectId];
    assert.equal(record.popularity_assessment.subject_id, subjectId);
    assert.equal(score, subject.score);
    assert.ok(subject.work_labels.includes(record.work));
    if (seen.has(record.work)) assert.equal(subjectId, seen.get(record.work));
    seen.set(record.work, subjectId);
  }
  assert.equal(seen.size, 675);
  assert.equal(overlay.subjects['star-wars'].score, 1);
  assert.equal(overlay.subjects['culture'].score, .55);
});

test('web index and every detail export preserve the original popularity score', async () => {
  const index = await read('public/data/index.json');
  assert.equal(index.length, societies.length);
  const byId = new Map(index.map(r => [r.id, r]));
  await Promise.all(societies.map(async r => {
    assert.equal(byId.get(r.id).popularity_score, r.popularity_score);
    const detail = await read(`public/data/records/${r.id}.json`);
    assert.equal(detail.popularity_score, r.popularity_score);
    assert.deepEqual(detail.popularity_assessment, r.popularity_assessment);
  }));
});
