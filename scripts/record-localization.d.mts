import type { Lang, RecordDetail } from '../src/types';

export function recordText(record: RecordDetail, language: Lang): {
  description: string;
  economyBasis: string;
  language: Lang;
};
