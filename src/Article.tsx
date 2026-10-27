import { useEffect, useRef } from 'react';
import { ArrowUpRight, ArrowLeft, BookOpen } from 'lucide-react';
import article from '../article.md?raw';
import type { Lang } from './types';
import { copy, regimes } from './i18n';
import Credits from './Credits';

const sections = article.split(/^## /m).map((text, index) => {
  if (index === 0) return { id: 0, title: '', body: text };
  const [title, ...body] = text.split('\n');
  return { id: index, title: title.trim(), body: body.join('\n') };
});
const subheads = new Set(['Машины могут всех заменить, но люди всё равно продолжают работать', 'Что на самом деле ломается, когда машины заменяют людей?', 'Век Изобилия']);
function linked(text: string) {
  return text.split(/(https?:\/\/[^\s)]+)/g).map((piece, i) => /^https?:\/\//.test(piece) ? <a href={piece} key={i} target="_blank" rel="noreferrer">{new URL(piece).hostname.replace('www.', '')} ↗</a> : piece);
}
function Body({ body }: { body: string }) {
  return <>{body.split(/\r?\n\s*\r?\n/).filter(p => p.trim() && p.trim() !== 'картинка координат').map((p, i) => subheads.has(p.trim()) ? <h3 key={i}>{p.trim()}</h3> : <p key={i}>{linked(p.trim())}</p>)}</>;
}
export default function Article({ lang, expanded, region, onExpand, onBack }: { lang: Lang; expanded: boolean; region: number; onExpand: () => void; onBack: () => void }) {
  const t = copy[lang];
  const scroll = useRef<HTMLDivElement>(null);
  const targets = useRef<Record<number, HTMLElement | null>>({});
  const manual = useRef(0);
  const moveTo = (id: number) => {
    const node = targets.current[id];
    if (!node || !scroll.current) return;
    scroll.current.scrollTo({ top: node.getBoundingClientRect().top - scroll.current.getBoundingClientRect().top + scroll.current.scrollTop - 28, behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' });
  };
  useEffect(() => { if (!expanded && Date.now() > manual.current) { if (region > 0) moveTo(region); else scroll.current?.scrollTo({ top: 0 }); } }, [region, expanded, lang]);
  return <aside className={`article-panel ${expanded ? 'expanded' : ''}`} aria-label={t.article}>
    <div className="article-bar"><span><BookOpen size={13} /> {t.read}</span><button onClick={expanded ? onBack : onExpand} aria-label={expanded ? t.back : t.full} title={expanded ? t.back : t.full}>{expanded ? <ArrowLeft size={17} /> : <ArrowUpRight size={18} />}</button></div>
    <div className="article-scroll" ref={scroll} onWheel={() => { manual.current = Date.now() + 1800; }} onTouchStart={() => { manual.current = Date.now() + 1800; }}>
      <div className="article-inner">
        <header className="essay-heading"><h2>{t.articleTitle}</h2><p>{t.articleDesc}</p><div className="essay-rule" /></header>
        {lang === 'en' ? <div className="translation-placeholder"><span>EN / COMING SOON</span><h3>{t.translation}</h3><p>{t.translationSub}</p><ol>{regimes.en.slice(1).map((title, i) => <li key={title}><b>0{i + 1}</b>{title}</li>)}</ol></div> : <>
          <nav className="essay-toc" aria-label={t.contents}><span className="eyebrow">{t.contents}</span>{[t.intro, ...sections.slice(1).map(s => s.title)].map((title, i) => <button key={i} onClick={() => { manual.current = Date.now() + 2500; moveTo(i); }}><span>{String(i).padStart(2, '0')}</span>{title.replace(/^\d\. /, '')}<ArrowUpRight size={12} /></button>)}</nav>
          {sections.map(s => <section key={s.id} ref={node => { targets.current[s.id] = node; }} className={`essay-section ${region === s.id ? 'current' : ''}`} data-chapter={s.id}>{s.title && <h2><span>{s.id < 7 ? `0${s.id}` : '↗'}</span>{s.title.replace(/^\d\. /, '')}</h2>}<Body body={s.body} /></section>)}
        </>}
        <footer className="essay-footer">{t.estimates}<br />{t.enData}{expanded && <p><Credits /></p>}</footer>
      </div>
    </div>
  </aside>;
}
