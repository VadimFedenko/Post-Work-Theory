import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { layoutSocieties, popularityRadius } from '../scripts/atlas-layout.mjs';
import { guaranteeScore, controlScore, welfareScore, guaranteeLevel, controlLevel, welfareLevel, utopiaColor } from '../scripts/atlas-model.mjs';

const { societies } = JSON.parse(await readFile(new URL('../data/societies.json', import.meta.url), 'utf8'));
test('readable scales preserve the meaning and direction of both axes', () => {
  assert.equal(guaranteeScore(-1), 100); assert.equal(guaranteeScore(1), 0); assert.equal(guaranteeScore(-.7), 85);
  assert.equal(controlScore(-1), 0); assert.equal(controlScore(0), 50); assert.equal(controlScore(1), 100);
  assert.equal(welfareScore(0), 50);
  assert.equal(guaranteeLevel(-.7), 4); assert.equal(guaranteeLevel(.9), 0);
  assert.equal(controlLevel(-.9), 0); assert.equal(controlLevel(-.15), 2); assert.equal(controlLevel(.9), 4);
  assert.equal(welfareLevel(-.7), 0); assert.equal(welfareLevel(0), 3); assert.equal(welfareLevel(.7), 6);
  assert.equal(utopiaColor(-.7), utopiaColor(-1)); assert.equal(utopiaColor(.7), utopiaColor(1));
});
test('popularity, rather than participation in work, determines circle size', () => {
  const radii = [0, .2, .5, .8, 1].map(score => popularityRadius(score, 1100, 700, 890));
  assert.ok(radii.every((radius, i) => !i || radius > radii[i - 1]));
  assert.ok(radii[4] / radii[0] > 4);
});
test('all societies keep their own unchanged data and independent visual positions', () => {
  const before = JSON.stringify(societies);
  const nodes = layoutSocieties(societies, 1100, 700);
  assert.equal(nodes.length, societies.length);
  assert.equal(new Set(nodes.map(n => n.record.id)).size, societies.length);
  assert.equal(JSON.stringify(societies), before);
  let severeOverlaps = 0;
  for (let i = 0; i < nodes.length; i++) {
    const n = nodes[i];
    assert.ok(n.x >= n.radius && n.x <= 1100 - n.radius && n.y >= n.radius && n.y <= 700 - n.radius);
    assert.equal(n.anchorX, (n.record.axis.guarantees + 1) / 2 * 1100);
    assert.equal(n.anchorY, (1 - n.record.axis.control) / 2 * 700);
    for (let j = i + 1; j < nodes.length; j++) if (n.radius + nodes[j].radius - Math.hypot(n.x - nodes[j].x, n.y - nodes[j].y) > 2) severeOverlaps++;
  }
  assert.equal(severeOverlaps, 0);
  assert.ok(nodes.some(n => Math.hypot(n.x - n.anchorX, n.y - n.anchorY) > 10));
  assert.deepEqual(layoutSocieties([], 1100, 700), []);
});
test('records at identical coordinates remain separate and can be selected individually', () => {
  const input = Array.from({ length: 60 }, (_, i) => ({ id: 'same-' + i, axis: { guarantees: .9, control: 0, nonworking: i / 60 }, popularity_score: .3 }));
  const nodes = layoutSocieties(input, 900, 600);
  assert.equal(nodes.length, input.length);
  assert.equal(new Set(nodes.map(n => n.x.toFixed(2) + ',' + n.y.toFixed(2))).size, input.length);
  assert.ok(nodes.every(n => n.anchorX === 855 && n.anchorY === 300));
});
