/** Select text at render time so cached and pinned cards follow the language switch. */
export function recordText(record, language) {
  const translation = language === 'ru' ? record.translations?.ru : undefined;
  return translation
    ? { description: translation.description, economyBasis: translation.economy_basis, language: 'ru' }
    : { description: record.description, economyBasis: record.post_work_assessment.basis, language: 'en' };
}
