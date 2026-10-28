import { createHash } from 'node:crypto';

export function translationSourceHash(record) {
  return createHash('sha256').update(JSON.stringify([record.description, record.post_work_assessment.basis])).digest('hex');
}

/** Refuse incomplete or stale translations before publishing the web data. */
export function validateTranslations(societies, catalog) {
  if (catalog.language !== 'ru' || !catalog.translations) throw new Error('Invalid Russian translation catalog');
  const ids = new Set(societies.map(record => record.id));
  for (const id of Object.keys(catalog.translations)) {
    if (!ids.has(id)) throw new Error(`Unknown translation ID: ${id}`);
  }
  for (const record of societies) {
    const translation = catalog.translations[record.id];
    if (!translation) throw new Error(`Missing Russian translation: ${record.id}`);
    if (translation.translation_method !== 'direct_from_english') throw new Error(`Russian description still needs direct translation: ${record.id}`);
    if (translation.source_sha256 !== translationSourceHash(record)) throw new Error(`Stale Russian translation: ${record.id}`);
    for (const field of ['description', 'economy_basis']) {
      if (typeof translation[field] !== 'string' || !/[А-Яа-яЁё]/u.test(translation[field])) {
        throw new Error(`Missing Russian ${field}: ${record.id}`);
      }
    }
  }
}
