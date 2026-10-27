export function initialLanguage(saved, languages = []) {
  if (saved === 'ru' || saved === 'en') return saved;
  return /^ru(?:-|$)/i.test(languages[0] || '') ? 'ru' : 'en';
}
export function initialTheme(saved) {
  return saved === 'light' ? 'light' : 'dark';
}
