import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFile, access } from 'node:fs/promises';
import { coordinates, matchesMedia, societySubtitle, workingPercent, ARTICLE_REGIME, articleRegime, MEDIA_GROUPS } from '../scripts/atlas-model.mjs';
const { societies } = JSON.parse(await readFile(new URL('../data/societies.json', import.meta.url), 'utf8'));

test('card subtitles omit repeated titles while preserving a distinct population or period', () => {
  const octopuses = societies.find(record => record.id === 'childrenofruin-octopus-habitats-zero');
  assert.equal(societySubtitle(octopuses), '');
  assert.equal(societySubtitle({ ...octopuses, society: octopuses.society.toUpperCase() + '.' }), '');
  const geonosis = societies.find(record => record.id === 'starwars-geonosis-automated-hives');
  assert.equal(societySubtitle(geonosis), 'Living Geonosian hive society during the Clone Wars');
});
test('guarantees go left, human control up, AI control down', () => {
  assert.deepEqual(coordinates({ guarantees: -1, control: 1 }, 800, 600), { x: 0, y: 0 });
  assert.deepEqual(coordinates({ guarantees: 1, control: -1 }, 800, 600), { x: 800, y: 600 });
  assert.deepEqual(coordinates({ guarantees: 0, control: 0 }, 800, 600), { x: 400, y: 300 });
});
test('all media, multiple media and an intentionally empty map', () => {
  const bookAndGame = { media: ['book', 'game'] };
  assert.equal(matchesMedia(bookAndGame, ['all']), true);
  assert.equal(matchesMedia(bookAndGame, []), false);
  assert.equal(matchesMedia(bookAndGame, ['movies', 'games']), true);
  assert.equal(matchesMedia(bookAndGame, ['movies', 'anime']), false);
  const media = new Set(Object.values(MEDIA_GROUPS).flat());
  for (const record of societies) for (const m of record.media) assert.ok(media.has(m), `Uncovered medium ${m}`);
});
test('article numbering is adapted without reclassifying historical zeros', () => {
  assert.equal(ARTICLE_REGIME[2], 3); assert.equal(ARTICLE_REGIME[3], 2); assert.equal(ARTICLE_REGIME[0], 0);
  for (const record of societies.filter(s => s.regime_primary === 0)) assert.equal(ARTICLE_REGIME[record.regime_primary], 0);
  assert.equal(articleRegime({ regime_primary: 2 }), 3);
  assert.equal(articleRegime({ regime_primary: 3, taxonomy_version: 'article-2026-10-21' }), 3);
  assert.equal(articleRegime({ regime_primary: 2 }, 'article-2026-10-21'), 2);
  assert.throws(() => articleRegime({ regime_primary: 2 }, 'unknown'));
});
test('working participation has the correct denominator and direction', () => {
  assert.equal(workingPercent({ axis: { nonworking: .6 } }), 40);
  assert.equal(workingPercent({ axis: { nonworking: 0 } }), 100);
  assert.equal(workingPercent({ axis: { nonworking: 1 } }), 0);
});
test('all 890 separate societies have valid coordinates, scores and local display assets', async () => {
  assert.equal(societies.length, 890); assert.equal(new Set(societies.map(s => s.id)).size, 890);
  const assets = new Set();
  for (const record of societies) {
    assert.ok(Number.isFinite(record.axis.guarantees) && Math.abs(record.axis.guarantees) <= 1);
    assert.ok(Number.isFinite(record.axis.control) && Math.abs(record.axis.control) <= 1);
    assert.ok(Number.isFinite(record.axis.nonworking) && record.axis.nonworking >= 0 && record.axis.nonworking <= 1);
    assert.ok(Number.isFinite(record.utopia_score) && Math.abs(record.utopia_score) <= 1);
    assets.add(record.assets.icon); assets.add(record.assets.poster);
  }
  await Promise.all([...assets].map(asset => access(new URL('../' + asset, import.meta.url))));
});
