import { readFile, readdir, writeFile, mkdir } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { translationSourceHash } from './translation-data.mjs';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const { societies } = JSON.parse(await readFile(resolve(root, 'data/societies.json'), 'utf8'));
const catalog = JSON.parse(await readFile(resolve(root, 'data/society-translations.ru.json'), 'utf8'));
const pending = [], issues = [], numberDifferences = [];
const numbers = text => [...text.matchAll(/\d+(?:[.,]\d+)?/g)].map(match => match[0]);
for (const [index, source] of societies.entries()) {
  const target = catalog.translations[source.id];
  if (target?.translation_method !== 'direct_from_english') { pending.push({ index, id: source.id }); continue; }
  if (target.source_sha256 !== translationSourceHash(source)) issues.push({ index, id: source.id, issue: 'stale source' });
  const paragraphs = text => text.split(/\n\s*\n/).length;
  if (paragraphs(target.description) !== paragraphs(source.description)) issues.push({ index, id: source.id, issue: 'paragraph count' });
  if (/материальн\w* этаж|контрольн\w* вес|выбранное окончание/iu.test(target.description)) issues.push({ index, id: source.id, issue: 'literal translation jargon' });
  if (!/[А-Яа-яЁё]/u.test(target.description)) issues.push({ index, id: source.id, issue: 'no Russian text' });
  if (target.description.length < source.description.length * .6) issues.push({ index, id: source.id, issue: 'suspiciously short' });
  if (JSON.stringify(numbers(source.description)) !== JSON.stringify(numbers(target.description))) {
    numberDifferences.push({ index, id: source.id, english: numbers(source.description), russian: numbers(target.description) });
  }
}
const report = { total: societies.length, complete: societies.length - pending.length, pending, issues, numberDifferences };
await mkdir(resolve(root, 'tmp'), { recursive: true });
await writeFile(resolve(root, 'tmp/direct-translation-audit.json'), JSON.stringify(report, null, 2) + '\n');
console.log(JSON.stringify({ total: report.total, complete: report.complete, pending: pending.length, issues, numberDifferences }));
if (issues.length) process.exitCode = 1;
