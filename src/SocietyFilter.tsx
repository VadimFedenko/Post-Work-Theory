import type { Lang, SocietyStatusFilter } from './types';
import { copy, societyFilterOptions } from './i18n';

export type StatusCounts = Record<SocietyStatusFilter, number>;
export type SocietyFilterProps = { value: SocietyStatusFilter; counts: StatusCounts; onChange: (value: SocietyStatusFilter) => void };

export default function SocietyFilter({ lang, value, counts, onChange }: SocietyFilterProps & { lang: Lang }) {
  const t = copy[lang];
  const options: SocietyStatusFilter[] = ['all', 'post_work', 'zero_variant', 'transition'];
  return <div className="society-filter" role="group" aria-label={t.postWorkSociety}>
    {options.map(status => <button key={status} type="button" className={value === status ? 'selected' : ''} aria-pressed={value === status} title={`${status === 'all' ? t.allSocieties : societyFilterOptions[lang][status]}: ${counts[status]}`} onClick={() => onChange(status)}>{status === 'all' ? t.allSocieties : societyFilterOptions[lang][status]}</button>)}
  </div>;
}
