export const ARTICLE_REGIME = { 0: 0, 1: 1, 2: 3, 3: 2, 4: 4, 5: 5, 6: 6 };
export function articleRegime(record, taxonomyVersion) {
  const version = record.taxonomy_version || taxonomyVersion;
  if (!version || version === 'pre-article-2026-10-21') return ARTICLE_REGIME[record.regime_primary];
  if (version === 'article-2026-10-21') return record.regime_primary;
  throw new Error(`Unsupported taxonomy version: ${version}`);
}
export const MEDIA_GROUPS = {
  books: ['book', 'short_story', 'web_fiction'], movies: ['movie'],
  tv: ['tv'], anime: ['anime'], games: ['game', 'tabletop'],
  comics: ['comic', 'manga', 'webcomic'], other: ['cartoon', 'play', 'audio'],
};
export function matchesMedia(record, selected) {
  return selected.includes('all') || selected.some(key => MEDIA_GROUPS[key]?.some(m => record.media.includes(m)));
}
export function coordinates(axis, width, height) {
  return { x: (axis.guarantees + 1) / 2 * width, y: (1 - axis.control) / 2 * height };
}
export function workingPercent(record) { return Math.round((1 - record.axis.nonworking) * 100); }
export function societySubtitle(record) {
  const normalize = text => text.normalize('NFKC').toLocaleLowerCase().replace(/[^\p{L}\p{N}]+/gu, ' ').trim();
  const name = normalize(record.name), society = normalize(record.society);
  return society && !(` ${name} `).includes(` ${society} `) ? record.society : '';
}
export function utopiaColor(score) {
  const from = [190, 155, 77];
  const to = score < 0 ? [222, 53, 75] : [9, 177, 145];
  const t = Math.min(1, Math.abs(score) / .7);
  return `rgb(${from.map((c, i) => Math.round(c + (to[i] - c) * t)).join(',')})`;
}
export function guaranteeScore(value) { return Math.round((1 - value) * 50); }
export function controlScore(value) { return Math.round((value + 1) * 50); }
export function welfareScore(value) { return Math.round((value + 1) * 50); }
export function guaranteeLevel(value) {
  const score = guaranteeScore(value);
  return score >= 80 ? 4 : score >= 60 ? 3 : score >= 40 ? 2 : score >= 20 ? 1 : 0;
}
export function controlLevel(value) { return value <= -.65 ? 0 : value < -.25 ? 1 : value <= .25 ? 2 : value < .65 ? 3 : 4; }
export function welfareLevel(value) { return value <= -.7 ? 0 : value <= -.4 ? 1 : value < -.15 ? 2 : value <= .15 ? 3 : value < .4 ? 4 : value < .7 ? 5 : 6; }
