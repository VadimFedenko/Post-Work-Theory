import { Check } from 'lucide-react';
import type { Lang, SocietyStatusFilter } from './types';
import { copy, societyFilterOptions } from './i18n';

export type StatusCounts = Record<SocietyStatusFilter, number>;
export type SocietyFilterProps = { value: SocietyStatusFilter; counts: StatusCounts; onChange: (value: SocietyStatusFilter) => void };

export default function SocietyFilter({ lang, value, counts, onChange }: SocietyFilterProps & { lang: Lang }) {
  const t = copy[lang];
  const options: SocietyStatusFilter[] = ['zero_variant', 'transition', 'post_work', 'all'];
  return <div className="society-filter filter-buttons" role="group" aria-label={t.societyType}>
    {options.map(status => <button key={status} type="button" className={value === status ? 'selected' : ''} aria-pressed={value === status} title={`${status === 'all' ? t.allSocieties : societyFilterOptions[lang][status]}: ${counts[status]}`} onClick={() => onChange(status)}>{value === status && <Check size={11} />}{status === 'all' ? t.allSocieties : societyFilterOptions[lang][status]}</button>)}
  </div>;
}
