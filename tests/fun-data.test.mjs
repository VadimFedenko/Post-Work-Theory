import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { buildFunData, compositionRegime, median, percent } from '../scripts/fun-data.mjs';

const { societies } = JSON.parse(await readFile(new URL('../data/societies.json', import.meta.url), 'utf8'));
const stats = buildFunData(societies);
test('fun data reproduces the catalogue comparisons with the correct denominators', () => {
  assert.equal(stats.total, 890);
  assert.deepEqual(stats.guarantees.without, { count: 302, total: 520, percent: 58 });
  assert.deepEqual(stats.guarantees.with, { count: 51, total: 370, percent: 14 });
  assert.equal(stats.dystopiaRatio, 4);
  assert.deepEqual(stats.control.map(row => [row.regime, row.count, row.total, row.percent]), [[3, 116, 128, 91], [5, 66, 94, 70], [1, 53, 126, 42]]);
  assert.deepEqual(stats.media.map(row => [row.media, row.count, row.total, row.percent]), [['book', 187, 362, 52], ['anime', 54, 73, 74], ['tv', 87, 108, 81]]);
  assert.deepEqual(stats.mediaLeaders.map(row => [row.media, ...row.leaders.map(leader => [leader.regime, leader.count, leader.total, leader.percent])]), [['book', [3, 75, 189, 40]], ['anime', [1, 13, 33, 39]], ['game', [5, 19, 64, 30]]]);
  assert.deepEqual(stats.participation.map(row => [row.stage, row.total, row.percent]), [['zero_variant', 345, 75], ['post_work', 470, 60]]);
});
test('stage pies reproduce the slide, projecting only zero regimes and preserving all counts', () => {
  assert.deepEqual(stats.stages.map(row => row.regimes.map(regime => regime.count)), [[17, 226, 11, 42, 1, 48], [11, 29, 12, 10, 5, 8], [115, 80, 116, 11, 89, 59]]);
  assert.deepEqual(stats.stages.map(row => row.elite.percent), [66, 39, 17]);
  for (const stage of stats.stages) assert.equal(stage.regimes.reduce((sum, row) => sum + row.count, 0), stage.total);
  for (const control of [-1 / 3, 0, 1 / 3, 1]) for (const guarantees of [-.1, 0]) {
    const record = { regime_primary: 0, axis: { control, guarantees } };
    const expected = (control > 1 / 3 ? 3 : control <= -1 / 3 ? 5 : 1) + (guarantees < 0 ? 0 : 1);
    assert.equal(compositionRegime(record), expected);
    assert.equal(compositionRegime({ ...record, regime_primary: 3 }), 3);
  }
});
test('web index gives the same summaries as source records without mutating them', () => {
  const before = JSON.stringify(societies);
  const index = societies.map(record => ({ ...record, regime: record.regime_primary, post_work_status: record.post_work_assessment.status, post_work_assessment: undefined, regime_primary: undefined }));
  assert.deepEqual(buildFunData(index), stats);
  assert.equal(JSON.stringify(societies), before);
});
test('cutoffs include severe dystopia boundary, exclude neutral utopia, and assign zero guarantees to without', () => {
  const base = { axis: { guarantees: 0, control: 0, nonworking: .4 }, media: ['book', 'anime'], regime: 1, post_work_status: 'post_work' };
  const result = buildFunData([-.5, -.49, 0, .1].map(utopia_score => ({ ...base, utopia_score })));
  assert.deepEqual(result.guarantees.without, { count: 1, total: 4, percent: 25 });
  assert.equal(result.control.find(row => row.regime === 1).percent, 25);
  assert.deepEqual(result.media.map(row => row.percent), [50, 50, null]);
  assert.equal(result.mediaLeaders[0].total, 4);
});
test('medians are numeric and taken before rounding; empty samples are not labelled zero percent', () => {
  assert.equal(median([2, 11, 3, 8]), 5.5);
  assert.equal(median([10, 2, 5]), 5);
  assert.equal(median([]), null);
  assert.equal(percent(0, 0), null);
  const empty = buildFunData([]);
  assert.equal(empty.guarantees.with.percent, null);
  assert.equal(empty.dystopiaRatio, null);
  assert.equal(empty.participation[0].percent, null);
  assert.deepEqual(empty.mediaLeaders[0].leaders, []);
});
test('most frequent models preserve ties rather than silently choosing one winner', () => {
  const record = { axis: { guarantees: -.5, control: .5, nonworking: .5 }, media: ['book'], utopia_score: .1, post_work_status: 'post_work' };
  const result = buildFunData([1, 3].map(regime => ({ ...record, regime })));
  assert.deepEqual(result.mediaLeaders[0].leaders.map(row => [row.regime, row.percent]), [[1, 50], [3, 50]]);
});
