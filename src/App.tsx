import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { ArrowDown, Check, ChevronDown, Globe2, Moon, Sun } from 'lucide-react';
import Atlas, { type AtlasHandle, type Selection } from './Atlas';
import Article from './Article';
import DataTable from './DataTable';
import Details from './Details';
import MapTools from './MapTools';
import Credits from './Credits';
import SocietyFilter from './SocietyFilter';
import FunData from './FunData';
import brandMark from './brand-mark.svg?no-inline';
import type { FamilyIndex, Lang, Society, SocietyStatusFilter } from './types';
import { copy } from './i18n';
import { matchesMedia } from '../scripts/atlas-model.mjs';
import { initialLanguage, initialTheme } from '../scripts/preferences.mjs';
import { familyKey, groupFamilies } from '../scripts/society-families.mjs';
import { countSocietyStatuses, pentagonPoints } from '../scripts/society-status.mjs';
const filters = ['all', 'movies', 'tv', 'anime', 'books', 'games', 'comics', 'other'] as const;
type Mode = 'societies' | 'article' | 'funData' | 'table';
const stored = (key: string, fallback: string) => { try { return localStorage.getItem(key) || fallback; } catch { return fallback; } };
export default function App() {
  const [lang, setLang] = useState<Lang>(() => initialLanguage(stored('atlas-lang', ''), navigator.languages?.length ? navigator.languages : [navigator.language]));
  const [theme, setTheme] = useState<'light' | 'dark'>(() => initialTheme(stored('atlas-theme', '')));
  const [mode, setMode] = useState<Mode>('societies');
  const [data, setData] = useState<Society[]>([]);
  const [loadState, setLoadState] = useState<'loading' | 'ready' | 'error'>('loading');
  const [retry, setRetry] = useState(0);
  const [selectedMedia, setSelectedMedia] = useState<string[]>(['all']);
  const [societyStatus, setSocietyStatus] = useState<SocietyStatusFilter>('all');
  const [query, setQuery] = useState('');
  const atlasRef = useRef<AtlasHandle | null>(null);
  const [zoom, setZoom] = useState(1);
  const [region, setRegion] = useState(0);
  const [selection, setSelection] = useState<Selection | null>(null);
  const modeRef = useRef(mode); modeRef.current = mode;
  const closeTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const t = copy[lang];
  useEffect(() => { document.documentElement.dataset.theme = theme; try { localStorage.setItem('atlas-theme', theme); } catch {} }, [theme]);
  useEffect(() => { document.documentElement.lang = lang; document.title = copy[lang].title; try { localStorage.setItem('atlas-lang', lang); } catch {} }, [lang]);
  useEffect(() => {
    const controller = new AbortController(); setLoadState('loading');
    fetch(`${import.meta.env.BASE_URL}data/index.json`, { signal: controller.signal }).then(r => { if (!r.ok) throw Error(String(r.status)); return r.json(); }).then(d => { setData(d); setLoadState('ready'); }).catch(() => { if (!controller.signal.aborted) setLoadState('error'); });
    return () => controller.abort();
  }, [retry]);
  useEffect(() => {
    const onKey = (event: KeyboardEvent) => { if (event.key === 'Escape') setSelection(null); };
    window.addEventListener('keydown', onKey); return () => window.removeEventListener('keydown', onKey);
  }, []);
  const matching = useMemo(() => {
    const words = query.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    return data.filter(s => matchesMedia(s, selectedMedia) && (!words.length || words.every(q => `${s.name} ${s.work} ${s.society}`.toLocaleLowerCase().includes(q))));
  }, [data, selectedMedia, query]);
  const statusCounts = useMemo(() => countSocietyStatuses(matching), [matching]);
  const visible = useMemo(() => matching.filter(record => societyStatus === 'all' || record.post_work_status === societyStatus), [matching, societyStatus]);
  const families = useMemo<FamilyIndex>(() => groupFamilies(data), [data]);
  const visibleIds = useMemo(() => new Set(visible.map(record => record.id)), [visible]);
  const cancelClose = useCallback(() => { if (closeTimer.current) clearTimeout(closeTimer.current); }, []);
  const scheduleClose = useCallback(() => { cancelClose(); closeTimer.current = setTimeout(() => setSelection(s => s?.pinned ? s : null), 250); }, [cancelClose]);
  useEffect(() => () => cancelClose(), [cancelClose]);
  const select = useCallback((next: Selection | null) => {
    cancelClose();
    setSelection(current => current?.pinned && next && !next.pinned ? current : next);
  }, [cancelClose]);
  const navigate = (next: Mode) => {
    setMode(next); setSelection(null);
    if (next === 'societies') setRegion(0);
    const behavior = window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth';
    requestAnimationFrame(() => {
      if (next === 'table' || next === 'funData') document.getElementById(next === 'table' ? 'table' : 'fun-data')?.scrollIntoView({ behavior, block: 'start' });
      else window.scrollTo({ top: 0, behavior });
    });
  };
  useEffect(() => {
    if (mode === 'article') return;
    const sections = [document.getElementById('fun-data'), document.getElementById('table')].filter((section): section is HTMLElement => section !== null);
    let frame = 0;
    const update = () => {
      frame = 0;
      if (modeRef.current === 'article') return;
      const line = Math.max(90, window.innerHeight * .3);
      const current = [...sections].reverse().find(section => section.getBoundingClientRect().top <= line);
      setMode(current?.id === 'table' ? 'table' : current?.id === 'fun-data' ? 'funData' : 'societies');
    };
    const schedule = () => { if (!frame) frame = requestAnimationFrame(update); };
    window.addEventListener('scroll', schedule, { passive: true });
    window.addEventListener('resize', schedule);
    schedule();
    return () => { cancelAnimationFrame(frame); window.removeEventListener('scroll', schedule); window.removeEventListener('resize', schedule); };
  }, [mode === 'article', loadState]);
  const toggleFilter = (key: string) => {
    setSelection(null);
    setSelectedMedia(previous => key === 'all' ? previous.includes('all') ? [] : ['all'] : previous.includes('all') ? [key] : previous.includes(key) ? previous.filter(v => v !== key) : [...previous, key]);
  };
  const queryChange = (value: string) => { setQuery(value); setSelection(null); };
  const statusChange = (value: SocietyStatusFilter) => { setSocietyStatus(value); setSelection(null); };
  const selectRelated = (record: Society) => {
    cancelClose();
    if (!visibleIds.has(record.id)) { setSelectedMedia(['all']); setQuery(''); setSocietyStatus('all'); }
    setSelection({ record, pinned: true });
  };
  return <>
    <a className="skip-link" href="#main">{lang === 'ru' ? 'К содержимому' : 'Skip to content'}</a>
    <header className="site-header">
      <a className="brand" href="#" onClick={e => { e.preventDefault(); navigate('societies'); }} aria-label={t.brand}><img className="brand-symbol" src={brandMark} width="28" height="28" alt="" aria-hidden="true" /><h1>{t.title}</h1></a>
      <nav className="main-nav" aria-label={lang === 'ru' ? 'Главная навигация' : 'Main navigation'}>{(['societies', 'article', 'funData', 'table'] as Mode[]).map(item => <button key={item} className={mode === item ? 'active' : ''} aria-current={mode === item ? 'page' : undefined} disabled={item === 'funData' && loadState !== 'ready'} onClick={() => navigate(item)}>{t[item]}{item === 'societies' && <span className="nav-dot" />}</button>)}</nav>
      <div className="header-settings"><button className="language-switch" onClick={() => setLang(v => v === 'ru' ? 'en' : 'ru')} aria-label={lang === 'ru' ? 'Switch to English' : 'Переключить на русский'}><Globe2 size={14} /><span>{lang.toUpperCase()}</span><ChevronDown size={11} /></button><i /><button className="theme-switch" onClick={() => setTheme(v => v === 'light' ? 'dark' : 'light')} aria-label={theme === 'light' ? t.dark : t.light} title={theme === 'light' ? t.dark : t.light}>{theme === 'light' ? <Moon size={17} /> : <Sun size={18} />}</button></div>
    </header>
    <main id="main" className={mode === 'article' ? 'reading-mode' : ''}>
      {mode !== 'article' && <section className="atlas-section" id="societies">
        <div className="atlas-workspace">
          <div className="map-column">
            <div className="filter-bar"><div className="filter-strip"><div className="media-filters" role="group" aria-label={t.media}>{filters.map(key => <button key={key} className={selectedMedia.includes(key) ? 'selected' : ''} aria-pressed={selectedMedia.includes(key)} onClick={() => toggleFilter(key)}>{selectedMedia.includes(key) && <Check size={11} />}{t[key]}</button>)}</div><SocietyFilter lang={lang} value={societyStatus} counts={statusCounts} onChange={statusChange} /></div><MapTools atlas={atlasRef} zoom={zoom} ready={loadState === 'ready'} lang={lang} /></div>
            <div className="map-frame">
              {loadState === 'ready' ? <Atlas ref={atlasRef} data={visible} lang={lang} theme={theme} emptyMessage={selectedMedia.length ? t.noMatches : t.emptySub} selected={selection?.record.id || null} onZoomChange={setZoom} onRegion={setRegion} onSelect={select} cancelClose={cancelClose} scheduleClose={scheduleClose} /> : <div className="map-loading"><img className="brand-symbol" src={brandMark} width="28" height="28" alt="" aria-hidden="true" /><p>{loadState === 'loading' ? t.loading : t.error}</p>{loadState === 'error' && <button className="outline-button" onClick={() => setRetry(v => v + 1)}>{t.retry}</button>}</div>}
              {selection && <Details selection={selection} lang={lang} familyMembers={families.get(familyKey(selection.record)) || [selection.record]} visibleIds={visibleIds} onRelatedSelect={selectRelated} onClose={() => setSelection(null)} onPin={() => setSelection(s => s ? { ...s, pinned: !s.pinned } : null)} onEnter={cancelClose} onLeave={scheduleClose} />}
            </div>
            <div className="map-legend"><div className="color-legend"><span>{t.dystopia}</span><i /><span>{t.utopia}</span></div><div className="shape-key" aria-label={t.statusKey}><span><svg viewBox="0 0 14 14" aria-hidden="true"><circle cx="7" cy="7" r="5.5" /></svg>{t.shapePostWork}</span><span><svg viewBox="0 0 14 14" aria-hidden="true"><polygon points={pentagonPoints(7, 7, 6)} /></svg>{t.shapeOther}</span></div><div className="size-legend"><span className="size-circles"><i /><i /><i /></span><span>{t.size}</span></div><button className="table-jump" onClick={() => navigate('table')}>{t.table}<ArrowDown size={13} /></button></div>
          </div>
          <Article lang={lang} expanded={false} region={region} onExpand={() => navigate('article')} onBack={() => navigate('societies')} />
        </div>
      </section>}
      {mode === 'article' ? <Article lang={lang} expanded region={region} onExpand={() => {}} onBack={() => navigate('societies')} /> : <>
        {loadState === 'ready' && <FunData data={data} lang={lang} />}
        <DataTable data={visible} families={families} lang={lang} query={query} onQuery={queryChange} societyFilter={{ value: societyStatus, counts: statusCounts, onChange: statusChange }} />
      </>}
    </main>
    {mode !== 'article' && <footer className="site-footer"><Credits /><span>{t.estimates}</span></footer>}
    <div className="sr-only" role="status" aria-live="polite">{visible.length} {t.shown}</div>
  </>;
}
