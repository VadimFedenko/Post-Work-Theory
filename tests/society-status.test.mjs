import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { countSocietyStatuses, markerShape } from '../scripts/society-status.mjs';

const { societies } = JSON.parse(await readFile(new URL('../data/societies.json', import.meta.url), 'utf8'));
const index = JSON.parse(await readFile(new URL('../public/data/index.json', import.meta.url), 'utf8'));

test('the web index preserves the three assessed statuses, including the 75 partial transitions', () => {
  const byId = new Map(index.map(record => [record.id, record]));
  for (const record of societies) {
    assert.equal(byId.get(record.id).post_work_status, record.post_work_assessment.status, record.id);
    assert.equal(byId.get(record.id).wage_dependence, record.post_work_assessment.wage_dependence, record.id);
  }
  assert.deepEqual(countSocietyStatuses(index), { all: 893, post_work: 470, transition: 75, zero_variant: 348 });
  const partial = index.filter(record => record.post_work_status === 'transition');
  assert.equal(partial.length, 75);
  assert.ok(partial.every(record => record.record_type === 'post_work' && markerShape(record.post_work_status) === 'pentagon'));
  assert.deepEqual(countSocietyStatuses([]), { all: 0, post_work: 0, transition: 0, zero_variant: 0 });
});

test('shape follows the current assessment even for historical zero IDs and insecure provision', () => {
  const historicalZeros = index.filter(record => record.id.endsWith('-zero') && record.post_work_status === 'post_work');
  assert.ok(historicalZeros.length > 0);
  assert.ok(historicalZeros.every(record => markerShape(record.post_work_status) === 'circle'));
  const insecure = index.filter(record => record.wage_dependence === 'structurally_displaced_without_replacement');
  assert.equal(insecure.length, 23);
  assert.ok(insecure.every(record => record.post_work_status === 'post_work' && markerShape(record.post_work_status) === 'circle'));
  assert.ok(index.filter(record => record.post_work_status === 'zero_variant').every(record => markerShape(record.post_work_status) === 'pentagon'));
});
