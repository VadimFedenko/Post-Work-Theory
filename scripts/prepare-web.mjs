import { readFile, writeFile, mkdir, copyFile, stat } from 'node:fs/promises';
import { resolve, dirname, relative, isAbsolute } from 'node:path';
import { fileURLToPath } from 'node:url';
import { articleRegime } from './atlas-model.mjs';
import { SOCIETY_STATUSES } from './society-status.mjs';
const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const { societies, taxonomy_version } = JSON.parse(await readFile(resolve(root, 'data/societies.json'), 'utf8'));
const output = resolve(root, 'public');
await mkdir(resolve(output, 'data/records'), { recursive: true });
const ids = new Set();
const images = new Set();
const index = [];
for (const record of societies) {
  if (!/^[a-z0-9][a-z0-9_-]*$/i.test(record.id) || ids.has(record.id)) throw new Error(`Invalid/duplicate ID: ${record.id}`);
  ids.add(record.id);
  if (!SOCIETY_STATUSES.includes(record.post_work_assessment?.status)) throw new Error(`Invalid society status: ${record.id}`);
  for (const [key, value] of Object.entries(record.axis)) {
    const min = key === 'nonworking' ? 0 : -1;
    if (!Number.isFinite(value) || value < min || value > 1) throw new Error(`Invalid ${key}: ${record.id}`);
  }
  if (!Number.isFinite(record.utopia_score)) throw new Error(`Missing score: ${record.id}`);
  if (!Number.isFinite(record.popularity_score) || record.popularity_score < 0 || record.popularity_score > 1 ||
      Math.abs(record.popularity_score * 20 - Math.round(record.popularity_score * 20)) > 1e-8 ||
      !record.popularity_assessment?.subject_id) throw new Error(`Invalid popularity: ${record.id}`);
  index.push({
    id: record.id, name: record.name, work: record.work, society: record.society,
    media: record.media, axis: record.axis, utopia_score: record.utopia_score,
    popularity_score: record.popularity_score,
    family: { id: record.popularity_assessment.subject_id, name: record.popularity_assessment.subject, kind: record.popularity_assessment.subject_type },
    regime: articleRegime(record, taxonomy_version), record_type: record.record_type,
    post_work_status: record.post_work_assessment.status, wage_dependence: record.post_work_assessment.wage_dependence,
    icon: record.assets.icon, poster: record.assets.poster,
    poster_crop: record.assets.crop.poster,
  });
  await writeFile(resolve(output, `data/records/${record.id}.json`), JSON.stringify(record));
  images.add(record.assets.icon); images.add(record.assets.poster);
}
for (const asset of images) {
  const source = resolve(root, asset);
  const rel = relative(resolve(root, 'assets'), source);
  if (isAbsolute(rel) || rel.startsWith('..')) throw new Error(`Unsafe asset path: ${asset}`);
  const destination = resolve(output, asset);
  await mkdir(dirname(destination), { recursive: true });
  const [a, b] = await Promise.all([stat(source), stat(destination).catch(() => null)]);
  if (!b || a.size !== b.size || a.mtimeMs > b.mtimeMs) await copyFile(source, destination);
}
await writeFile(resolve(output, 'data/index.json'), JSON.stringify(index));
await copyFile(resolve(root, 'data/sources.json'), resolve(output, 'data/sources.json'));
const utopia = JSON.parse(await readFile(resolve(root, 'data/society-utopia.json'), 'utf8'));
await writeFile(resolve(output, 'data/supplemental-sources.json'), JSON.stringify(utopia.supplemental_sources || {}));
const popularity = JSON.parse(await readFile(resolve(root, 'data/society-popularity.json'), 'utf8'));
await writeFile(resolve(output, 'data/popularity-references.json'), JSON.stringify(popularity.references));
console.log(`Prepared ${index.length} distinct societies and ${images.size} display assets. Research files unchanged.`);
