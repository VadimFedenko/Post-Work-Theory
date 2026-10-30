import { useEffect, useMemo, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { ArrowDown, ArrowUp, ArrowUpDown, Download, ChevronLeft, ChevronRight, Search, X } from 'lucide-react';
import type { FamilyIndex, Lang, Society } from './types';
import { copy, levels, medium, regimes, societyTypeDescriptions, societyTypes } from './i18n';
import { controlLevel, controlScore, guaranteeLevel, guaranteeScore, utopiaColor, welfareLevel, welfareScore, workingPercent } from '../scripts/atlas-model.mjs';
import Details, { type FloatingPlacement } from './Details';
import type { Selection } from './Atlas';
import { familyKey } from '../scripts/society-families.mjs';
import SocietyIcon from './SocietyIcon';
import SocietyFilter, { type SocietyFilterProps } from './SocietyFilter';
import { displayScale, layoutViewport } from './display-scale';
type SortKey = 'work' | 'status' | 'guarantees' | 'control' | 'working' | 'utopia' | 'popularity' | 'regime';
export default function DataTable({ data, families, lang, query, onQuery, societyFilter }: { data: Society[]; families: FamilyIndex; lang: Lang; query: string; onQuery: (q: string) => void; societyFilter: SocietyFilterProps }) {
  const t = copy[lang];
  const [sort, setSort] = useState<{ key: SortKey; direction: number }>({ key: 'work', direction: 1 });
  const [page, setPage] = useState(0);
  const [card, setCard] = useState<{ selection: Selection; placement: FloatingPlacement } | null>(null);
  const visibleIds = useMemo(() => new Set(data.map(record => record.id)), [data]);
  const closeTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const cancelClose = () => { if (closeTimer.current) clearTimeout(closeTimer.current); };
  const closeSoon = () => { cancelClose(); closeTimer.current = setTimeout(() => setCard(old => old?.selection.pinned ? old : null), 250); };
  const showCard = (record: Society, target: HTMLElement, pinned: boolean) => {
    cancelClose();
    const bounds = target.getBoundingClientRect();
    const viewport = layoutViewport(), scale = displayScale();
    const width = Math.min(700, viewport.width - 24), height = Math.min(480, viewport.height - 110);
    const left = Math.max(12, Math.min(viewport.width - width - 12, bounds.right / scale + 12));
    const top = Math.max(80, Math.min(viewport.height - height - 12, bounds.top / scale - 40));
    setCard(old => old?.selection.pinned && !pinned ? old : { selection: { record, pinned }, placement: { left, top, width, height } });
  };
  useEffect(() => { setCard(null); }, [data, sort, page]);
  useEffect(() => {
    const onKey = (event: KeyboardEvent) => { if (event.key === 'Escape') setCard(null); };
    const onScroll = () => {
      const bounds = document.getElementById('table')?.getBoundingClientRect();
      setCard(old => bounds && bounds.top < window.innerHeight && bounds.bottom > 0 && old?.selection.pinned ? old : null);
    };
    const onResize = () => setCard(null);
    window.addEventListener('keydown', onKey); window.addEventListener('scroll', onScroll); window.addEventListener('resize', onResize);
    return () => { cancelClose(); window.removeEventListener('keydown', onKey); window.removeEventListener('scroll', onScroll); window.removeEventListener('resize', onResize); };
  }, []);
  useEffect(() => setPage(0), [data, sort]);
  const sorted = useMemo(() => [...data].sort((a, b) => {
    if (sort.key === 'work') return a.work.localeCompare(b.work) * sort.direction || a.id.localeCompare(b.id);
    if (sort.key === 'status') return societyTypes[lang][a.post_work_status].localeCompare(societyTypes[lang][b.post_work_status]) * sort.direction || a.name.localeCompare(b.name);
    const value = (s: Society) => sort.key === 'working' ? workingPercent(s) : sort.key === 'utopia' ? welfareScore(s.utopia_score) : sort.key === 'regime' ? s.regime : sort.key === 'popularity' ? s.popularity_score : sort.key === 'guarantees' ? guaranteeScore(s.axis.guarantees) : controlScore(s.axis.control);
    return (value(a) - value(b)) * sort.direction || a.name.localeCompare(b.name);
  }), [data, sort, lang]);
  const pages = Math.max(1, Math.ceil(sorted.length / 40));
  const current = Math.min(page, pages - 1);
  const download = () => {
    const headers = ['id', 'name', 'work', 'society', 'media', 'guarantees_raw', 'control_raw', 'working_percent', 'utopia_raw', 'article_regime', 'record_type', 'popularity_100', 'guarantees_100', 'guarantees_label', 'control_100', 'control_label', 'utopia_100', 'utopia_label', 'post_work_status', 'society_type', 'wage_dependence'];
    const escape = (value: unknown) => { let str = String(value); if (/^[=+@\t\r]/.test(str) || /^-[^\d]/.test(str)) str = "'" + str; return '"' + str.replaceAll('"', '""') + '"'; };
    const csv = [headers, ...sorted.map(s => [s.id, s.name, s.work, s.society, s.media.join(';'), s.axis.guarantees, s.axis.control, workingPercent(s), s.utopia_score, s.regime, s.record_type, Math.round(s.popularity_score * 100), guaranteeScore(s.axis.guarantees), levels[lang].guarantees[guaranteeLevel(s.axis.guarantees)], controlScore(s.axis.control), levels[lang].control[controlLevel(s.axis.control)], welfareScore(s.utopia_score), levels[lang].welfare[welfareLevel(s.utopia_score)], s.post_work_status, societyTypes[lang][s.post_work_status], s.wage_dependence])].map(row => row.map(escape).join(',')).join('\r\n');
    const url = URL.createObjectURL(new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8' }));
    const a = document.createElement('a'); a.href = url; a.download = 'after-work-societies.csv'; a.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
  };
  const heading = (key: SortKey, title: string) => <button onClick={() => setSort({ key, direction: sort.key === key ? -sort.direction : 1 })}>{title}{sort.key === key ? sort.direction === 1 ? <ArrowUp size={11} /> : <ArrowDown size={11} /> : <ArrowUpDown size={11} />}</button>;
  return <section id="table" className="table-section" aria-label={t.table}>
    <div className="table-heading"><div><h2>{t.tableTitle}</h2><p>{t.tableSub}</p></div><button className="outline-button" onClick={download}><Download size={14} />{t.download}</button></div>
    <p className="table-scales">{t.scales}</p>
    <div className="table-tools"><label className="search-box"><Search size={15} /><input value={query} onChange={e => onQuery(e.target.value)} placeholder={t.searchShort} aria-label={t.search} />{query && <button onClick={() => onQuery('')} aria-label={t.clear}><X size={13} /></button>}</label><SocietyFilter lang={lang} {...societyFilter} /><span>{data.length} {t.of} 890</span></div>
    <div className="table-scroll"><table><thead><tr>
      <th scope="col" aria-sort={sort.key === 'work' ? sort.direction === 1 ? 'ascending' : 'descending' : 'none'}>{heading('work', t.work)}</th><th scope="col">{t.media}</th>
      <th scope="col" aria-sort={sort.key === 'status' ? sort.direction === 1 ? 'ascending' : 'descending' : 'none'}>{heading('status', t.societyType)}</th>
      {(['guarantees', 'control', 'working', 'utopia', 'popularity', 'regime'] as SortKey[]).map((key, i) => <th scope="col" key={key} aria-sort={sort.key === key ? sort.direction === 1 ? 'ascending' : 'descending' : 'none'}>{heading(key, [t.guaranteeAxis, t.controlAxis, t.works, t.welfare, t.popularity, t.regime][i])}</th>)}
    </tr></thead><tbody>{sorted.slice(current * 40, current * 40 + 40).map(s => <tr key={s.id}>
      <td><button className="table-society" onPointerEnter={e => { if (e.pointerType !== 'touch') showCard(s, e.currentTarget, false); }} onPointerLeave={closeSoon} onFocus={e => showCard(s, e.currentTarget, false)} onBlur={closeSoon} onClick={e => showCard(s, e.currentTarget, true)}><SocietyIcon record={s} lazy /><span><b>{s.work}</b><small>{s.society}</small></span></button></td>
      <td><span className="medium-tag">{s.media.map(m => medium[lang][m]).join(' / ')}</span></td><td className="table-society-type" title={societyTypeDescriptions[lang][s.post_work_status]}>{societyTypes[lang][s.post_work_status]}</td><td><span className="table-rating"><b>{guaranteeScore(s.axis.guarantees)}<small>/100</small></b><span>{levels[lang].guarantees[guaranteeLevel(s.axis.guarantees)]}</span></span></td><td><span className="table-rating"><b>{controlScore(s.axis.control)}<small>/100</small></b><span>{levels[lang].control[controlLevel(s.axis.control)]}</span></span></td>
      <td className="numeric"><div className="working-value"><span className="mini-bar"><i style={{ width: workingPercent(s) + '%' }} /></span>{workingPercent(s)}%</div></td>
      <td><span className="table-rating"><b><i className="score-dot" style={{ background: utopiaColor(s.utopia_score) }} />{welfareScore(s.utopia_score)}<small>/100</small></b><span>{levels[lang].welfare[welfareLevel(s.utopia_score)]}</span></span></td>
      <td className="numeric">{Math.round(s.popularity_score * 100)}<small className="rating-total">/100</small></td>
      <td><span className="table-regime" title={regimes[lang][s.regime]}>{String(s.regime).padStart(2, '0')}</span></td>
    </tr>)}</tbody></table>{!data.length && <div className="empty-table"><Search size={24} /><h3>{t.noResults}</h3><p>{t.noMatches}</p><button className="text-button" onClick={() => { onQuery(''); societyFilter.onChange('all'); }}>{t.allSocieties}</button></div>}</div>
    <div className="table-pagination"><span>{data.length ? current * 40 + 1 : 0}–{Math.min((current + 1) * 40, data.length)} {t.of} {data.length}</span><div><button aria-label={t.prev} disabled={current === 0} onClick={() => setPage(p => p - 1)}><ChevronLeft size={16} /></button><span>{current + 1} / {pages}</span><button aria-label={t.next} disabled={current >= pages - 1} onClick={() => setPage(p => p + 1)}><ChevronRight size={16} /></button></div></div>
    <p className="data-footnote">{t.estimates} {t.legacy}</p>
    {card && createPortal(<Details selection={card.selection} placement={card.placement} lang={lang} familyMembers={families.get(familyKey(card.selection.record)) || [card.selection.record]} visibleIds={visibleIds} onRelatedSelect={record => { cancelClose(); setCard(old => old ? { ...old, selection: { record, pinned: true } } : null); }} onClose={() => setCard(null)} onPin={() => setCard(old => old ? { ...old, selection: { ...old.selection, pinned: !old.selection.pinned } } : null)} onEnter={cancelClose} onLeave={closeSoon} />, document.body)}
  </section>;
}
