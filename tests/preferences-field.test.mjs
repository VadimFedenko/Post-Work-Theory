import { test } from 'node:test';
import assert from 'node:assert/strict';
import { initialLanguage, initialTheme } from '../scripts/preferences.mjs';
import { atlasPalette } from '../scripts/atlas-style.mjs';
import { createColorField } from '../scripts/color-field.mjs';

test('first visit uses dark mode and the browser preferred language, with English fallback', () => {
  for (const languages of [[], ['en-US'], ['de-DE'], ['en', 'ru']]) assert.equal(initialLanguage(null, languages), 'en');
  for (const languages of [['ru'], ['ru-RU', 'en'], ['RU-ru']]) assert.equal(initialLanguage(null, languages), 'ru');
  assert.equal(initialTheme(null), 'dark');
  assert.equal(initialTheme('invalid'), 'dark');
  assert.equal(initialLanguage('en', ['ru-RU']), 'en');
  assert.equal(initialLanguage('ru', ['en-US']), 'ru');
  assert.equal(initialTheme('light'), 'light');
});

test('moving colour field retains all six palette centres and the grey sixth region', () => {
  const width = 120, height = 120, paint = createColorField(width, height), palette = atlasPalette();
  const a = new Uint8ClampedArray(width * height * 4), b = a.slice();
  paint(a, 0); paint(b, 20);
  const pixel = (frame, x, y) => [...frame.slice((y * width + x) * 4, (y * width + x) * 4 + 3)];
  const rgb = hex => [1, 3, 5].map(i => parseInt(hex.slice(i, i + 2), 16));
  for (const frame of [a, b]) for (const [side, x] of [['left', 18], ['right', 102]]) for (const [row, y] of [[0, 18], [1, 60], [2, 102]]) assert.deepEqual(pixel(frame, x, y), rgb(palette[side][row]));
  assert.notDeepEqual(a, b, 'seams should change over time');
  const still = a.slice(); paint(still, 0); assert.deepEqual(still, a, 'a fixed time produces a motion-free field');
  for (let p = 3; p < a.length; p += 4) assert.equal(a[p], 255);
});
