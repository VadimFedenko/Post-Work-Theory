import { useEffect, useRef, useState, type CSSProperties } from 'react';
import { ArrowUpRight, Pin, X } from 'lucide-react';
import type { Lang, RecordDetail, Society, Source } from './types';
import type { Selection } from './Atlas';
import { allocationLabels, copy, levels, medium, regimes, societyTypeDescriptions, societyTypes, wageLabels } from './i18n';
import { controlLevel, guaranteeLevel, societySubtitle, utopiaColor, welfareLevel, workingPercent } from '../scripts/atlas-model.mjs';
import { familyName } from '../scripts/society-families.mjs';
import { recordText } from '../scripts/record-localization.mjs';
import SocietyIcon from './SocietyIcon';
import { layoutViewport } from './display-scale';

const cache = new Map<string, RecordDetail>();
let sourceRegistry: Promise<Source[]> | null = null;
function loadSources() {
  if (!sourceRegistry) sourceRegistry = Promise.all(['data/sources.json', 'data/supplemental-sources.json'].map(async path => {
    const response = await fetch(import.meta.env.BASE_URL + path); if (!response.ok) throw new Error(String(response.status)); return response.json();
  })).then(([main, supplemental]) => [...main.sources, ...(Array.isArray(supplemental) ? supplemental : Object.values(supplemental))] as Source[]).catch(error => { sourceRegistry = null; throw error; });
  return sourceRegistry;
}
const fieldNames: Record<string, string> = {
  scope: 'Контекст', axis_assessment: 'Обоснование координат', utopia_assessment: 'Обоснование благополучия',
  evidence: 'Подтверждения', uncertainties: 'Оговорки', canon_facts: 'Факты канона', editorial_assumptions: 'Редакторские допущения',
  assets: 'Изображение и происхождение', review: 'Внутренняя проверка', regime_primary: 'Уклад (нумерация базы)',
  regime_alternatives: 'Альтернативы (нумерация базы)', regime_analogy: 'Аналогия (нумерация базы)',
  record_type: 'Историческая категория', assessment_mode: 'Тип оценки', best_guess_axes: 'Оси с допущениями',
  qualification: 'Включение в базу', qualification_basis: 'Основание включения', qualification_confidence: 'Уверенность во включении',
  participation_definition: 'Определение участия в труде', reported_labor_statistics: 'Статистика занятости из лора',
  post_work_assessment: 'Оценка устройства экономики',
};
function readable(key: string) { return key.replaceAll('_', ' '); }
function Value({ value, depth = 0 }: { value: unknown; depth?: number }) {
  if (value == null) return <span className="muted">—</span>;
  if (typeof value === 'boolean') return <span>{String(value)}</span>;
  if (typeof value !== 'object') {
    const str = String(value);
    if (/^https?:\/\//.test(str)) return <a href={str} target="_blank" rel="noreferrer">{str}<ArrowUpRight size={10} /></a>;
    return <span>{str}</span>;
  }
  if (Array.isArray(value)) return <ul className="data-list">{value.map((v, i) => <li key={i}><Value value={v} depth={depth + 1} /></li>)}</ul>;
  return <dl className={`data-tree depth-${Math.min(depth, 3)}`}>{Object.entries(value).map(([k, v]) => <div key={k}><dt>{readable(k)}</dt><dd><Value value={v} depth={depth + 1} /></dd></div>)}</dl>;
}
export type FloatingPlacement = { left: number; top: number; width: number; height: number };
export default function Details({ selection, lang, familyMembers, visibleIds, onRelatedSelect, onClose, onPin, onEnter, onLeave, placement }: {
  selection: Selection; lang: Lang; onClose: () => void; onPin: () => void; onEnter: () => void; onLeave: () => void; placement?: FloatingPlacement;
  familyMembers: Society[]; visibleIds: Set<string>; onRelatedSelect: (record: Society) => void;
}) {
  const { record, pinned } = selection;
  const t = copy[lang];
  const [detail, setDetail] = useState<RecordDetail | null>(cache.get(record.id) || null);
  const [sources, setSources] = useState<Source[]>([]);
  const [error, setError] = useState(false);
  const [retry, setRetry] = useState(0);
  const cardElement = useRef<HTMLDivElement>(null);
  const contentElement = useRef<HTMLDivElement>(null);
  const [cardSize, setCardSize] = useState({ width: 0, height: 0 });
  const crop = record.poster_crop;
  const [canvasWidth, canvasHeight] = crop?.canvas || [320, 480];
  const [cropLeft, cropTop, cropRight, cropBottom] = crop?.content_box || [0, 0, canvasWidth, canvasHeight];
  const imageWidth = cropRight - cropLeft, imageHeight = cropBottom - cropTop;
  const aspect = imageWidth / imageHeight;
  const fullHeightPosterWidth = cardSize.height * aspect;
  const naturalCardWidth = fullHeightPosterWidth + 482;
  const stacked = cardSize.width > 0 && cardSize.width - fullHeightPosterWidth < 320;
  const posterWidth = stacked ? Math.min(cardSize.width * .42, cardSize.height * .55 * aspect) : fullHeightPosterWidth;
  const viewportWidth = placement ? layoutViewport().width : 0;
  const floatingWidth = placement ? Math.min(viewportWidth - 24, (placement.height - 2) * aspect + 482) : 0;
  const floatingPlacement = placement ? { ...placement, width: floatingWidth, left: Math.max(12, Math.min(placement.left, viewportWidth - floatingWidth - 12)) } : undefined;
  useEffect(() => {
    if (!cardElement.current) return;
    const observer = new ResizeObserver(([entry]) => {
      const { width, height } = entry.contentRect;
      setCardSize(old => old.width === width && old.height === height ? old : { width, height });
    });
    observer.observe(cardElement.current); return () => observer.disconnect();
  }, []);
  useEffect(() => {
    const controller = new AbortController();
    if (contentElement.current) contentElement.current.scrollTop = 0;
    if (cardElement.current) cardElement.current.scrollTop = 0;
    setDetail(cache.get(record.id) || null); setSources([]); setError(false);
    const fetchJSON = async (path: string) => { const response = await fetch(import.meta.env.BASE_URL + path, { signal: controller.signal }); if (!response.ok) throw new Error(String(response.status)); return response.json(); };
    (async () => {
      try {
        const data = cache.get(record.id) || await fetchJSON(`data/records/${record.id}.json`);
        if (controller.signal.aborted) return;
        cache.set(record.id, data); setDetail(data);
        const allSources = await loadSources();
        if (controller.signal.aborted) return;
        const ids = new Set<string>([...data.source_ids, ...(data.utopia_assessment?.source_ids || []), ...(data.utopia_assessment?.supplemental_source_ids || [])]);
        setSources(allSources.filter(s => ids.has(s.id)));
      } catch (e) { if (!controller.signal.aborted) setError(true); }
    })();
    return () => controller.abort();
  }, [record.id, retry]);
  const subtitle = societySubtitle(record);
  const text = detail ? recordText(detail, lang) : null;
  const core = new Set(['id', 'name', 'work', 'society', 'media', 'description', 'translations', 'axis', 'utopia_score', 'source_ids', 'popularity_score', 'popularity_assessment']);
  return <div ref={cardElement} className={`society-card ${pinned ? 'pinned' : ''} ${stacked ? 'stacked-card' : ''} ${placement ? 'floating-card' : record.axis.guarantees > .1 ? 'card-left' : ''}`} style={{ ...floatingPlacement, '--card-width': cardSize.height ? `${naturalCardWidth}px` : undefined, '--poster-width': posterWidth ? `${posterWidth}px` : undefined, '--poster-aspect': aspect } as CSSProperties} role="dialog" aria-label={record.name} onPointerEnter={onEnter} onPointerLeave={onLeave}>
    <div className="card-image"><svg key={record.poster} viewBox={`${cropLeft} ${cropTop} ${imageWidth} ${imageHeight}`} preserveAspectRatio="xMidYMid meet" role="img" aria-label={record.work}><image href={import.meta.env.BASE_URL + record.poster} width={canvasWidth} height={canvasHeight} /></svg><div className="card-regime"><span>{String(record.regime).padStart(2, '0')}</span><strong>{regimes[lang][record.regime]}</strong></div></div>
    <div className="card-content" ref={contentElement}>
      <header className="card-summary">
      <div className="card-topline"><span>{record.media.map(m => medium[lang][m]).join(' · ')}</span><div><button aria-label={lang === 'ru' ? 'Закрепить карточку' : 'Pin card'} title={lang === 'ru' ? 'Закрепить' : 'Pin'} aria-pressed={pinned} onClick={onPin}><Pin size={13} fill={pinned ? 'currentColor' : 'none'} /></button><button aria-label={t.close} onClick={onClose}><X size={16} /></button></div></div>
      <h3>{record.name}</h3>
      <div className="card-status-line"><span className="card-society-type" title={societyTypeDescriptions[lang][record.post_work_status]}>{societyTypes[lang][record.post_work_status]}</span><span className="card-welfare"><i className="score-dot" style={{ background: utopiaColor(record.utopia_score) }} />{levels[lang].welfare[welfareLevel(record.utopia_score)]}</span>{record.wage_dependence === 'structurally_displaced_without_replacement' && <span className="provision-status" title={t.noReplacement}>{t.insecureProvision}</span>}</div>
      {subtitle && <p className="card-society">{subtitle}</p>}
      <dl className="card-metrics"><div><dt>{t.controlAxis}</dt><dd>{levels[lang].control[controlLevel(record.axis.control)]}</dd></div><div><dt>{t.guaranteeAxis}</dt><dd>{levels[lang].guarantees[guaranteeLevel(record.axis.guarantees)]}</dd></div><div title={t.workingPopulationHint}><dt>{t.workingPopulation}</dt><dd>{workingPercent(record)}%</dd></div></dl>
      </header>
      <div className="card-body">
      {detail && text ? <>
        <div className="card-description" lang={text.language}>{text.description.split('\n').filter(Boolean).map((p, i) => <p key={i}>{p}</p>)}</div>
        {familyMembers.length > 1 && <section className="card-family" aria-label={t.workSeries}>
          <details className="related-societies" key={record.id}>
            <summary>{t.relatedSocieties} · {familyMembers.length}</summary>
            <div className="family-heading"><strong>{familyName(record)}</strong></div>
            <p className="related-note">{placement ? t.relatedTableHint : t.relatedMapHint}</p>
            <ul>{familyMembers.map(member => <li key={member.id}><button type="button" disabled={member.id === record.id} aria-current={member.id === record.id ? 'true' : undefined} onClick={() => onRelatedSelect(member)}>
              <SocietyIcon record={member} lazy />
              <span><b>{member.society}</b><small>{member.work}{member.id === record.id ? ' · ' + t.currentSociety : !visibleIds.has(member.id) ? ' · ' + t.hiddenByFilters : ''}</small></span>
            </button></li>)}</ul>
          </details>
        </section>}
        <details className="record-details economy-details"><summary>{t.economyDetails}</summary>
          <p>{societyTypeDescriptions[lang][record.post_work_status]}</p>
          <dl className="economy-facts"><div><dt>{t.wageAccess}</dt><dd>{wageLabels[lang][detail.post_work_assessment.wage_dependence] || detail.post_work_assessment.wage_dependence}</dd></div><div><dt>{t.allocation}</dt><dd>{detail.post_work_assessment.allocation_mechanisms.map(value => allocationLabels[lang][value] || value).join('; ')}</dd></div></dl>
          <p lang={text.language}>{text.economyBasis}</p>
        </details>
        <div className="estimate-note">{t.estimates}</div>
        <details className="record-details"><summary>{t.details}</summary><div className="full-record" lang="en">{Object.entries(detail).filter(([key]) => !core.has(key)).map(([key, value]) => <details key={key}><summary>{lang === 'ru' ? fieldNames[key] || readable(key) : readable(key)}</summary><Value value={value} /></details>)}</div></details>
        <details className="record-details"><summary>{t.sources} · {sources.length}</summary><ul className="source-list">{sources.map(s => <li key={s.id}><a href={s.url} target="_blank" rel="noreferrer">{s.title} <ArrowUpRight size={11} /></a>{s.read_scope && <p>{s.read_scope}</p>}{s.limitations && <p className="muted">{s.limitations}</p>}</li>)}</ul></details>
      </> : <p className="muted">{error ? t.error : t.loading}</p>}
      {error && <button className="text-button" onClick={() => setRetry(v => v + 1)}>{t.retry}</button>}
      </div>
    </div>
  </div>;
}
