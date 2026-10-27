import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { layoutAtlasLabels } from '../scripts/atlas-labels.mjs';
import { familyKey, familyConnections, groupFamilies } from '../scripts/society-families.mjs';

test('hover reserves the hidden label, so every other label retains its position and visibility', () => {
  const points = Array.from({ length: 220 }, (_, i) => ({ x: 40 + (i % 20) * 90, y: 60 + Math.floor(i / 20) * 55, radius: 8, record: { id: 's-' + i, work: 'Work ' + i, popularity_score: 1 - i / 250 } }));
  const place = selected => layoutAtlasLabels(points, 1860, 740, text => text.length * 5, { selected });
  const ordinary = place(null), geometry = labels => labels.map(({ hidden, ...rest }) => rest);
  assert.equal(ordinary.length, 160, 'label limit must also reserve a selected label');
  for (const selected of [ordinary[0].id, ordinary[14].id, ordinary.at(-1).id, 'no-label']) {
    const hovered = place(selected);
    assert.deepEqual(geometry(hovered), geometry(ordinary));
    assert.equal(hovered.filter(label => label.hidden).length, selected === 'no-label' ? 0 : 1);
  }
});

test('family groups use reviewed work/series IDs, not a shared image or title prefix', async () => {
  const { societies } = JSON.parse(await readFile(new URL('../data/societies.json', import.meta.url), 'utf8'));
  const groups = groupFamilies(societies);
  assert.equal(groups.get('subject:star-trek').length, 28);
  assert.equal(groups.get('subject:culture').length, 9);
  assert.ok(groups.get('subject:star-trek').some(record => record.work === 'Star Trek: Voyager'));
  const synthetic = [
    { id: 'a', work: 'Same title', society: 'One', icon: 'shared.png', family: { id: 'one' } },
    { id: 'b', work: 'Same title', society: 'Two', icon: 'shared.png', family: { id: 'two' } },
    { id: 'c', work: 'Episode', society: 'Three', family: { id: 'one' } },
  ];
  assert.notEqual(familyKey(synthetic[0]), familyKey(synthetic[1]));
  assert.equal(groupFamilies(synthetic).get('subject:one').length, 2);
  assert.equal(synthetic[0].id, 'a', 'grouping must not reorder the source array');
});

test('connections join only visible members, stop outside circles, and have no self-links', () => {
  const point = (id, x, y, family) => ({ x, y, radius: 10, record: { id, work: id, family: { id: family } } });
  const active = point('a', 50, 50, 'series'), target = point('b', 150, 50, 'series');
  const links = familyConnections(active, [active, target, point('c', 50, 150, 'unrelated')]);
  assert.deepEqual(links, [{ id: 'b', x1: 65, y1: 50, x2: 135, y2: 50 }]);
  assert.deepEqual(familyConnections(active, [active]), []);
  assert.deepEqual(familyConnections(null, [target]), []);
});

test('web export keeps every reviewed family ID and display name', async () => {
  const { societies } = JSON.parse(await readFile(new URL('../data/societies.json', import.meta.url), 'utf8'));
  const index = JSON.parse(await readFile(new URL('../public/data/index.json', import.meta.url), 'utf8'));
  const source = new Map(societies.map(record => [record.id, record]));
  for (const record of index) {
    assert.equal(record.family.id, source.get(record.id).popularity_assessment.subject_id);
    assert.equal(record.family.name, source.get(record.id).popularity_assessment.subject);
  }
});
