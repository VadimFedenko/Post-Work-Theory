import { useEffect, useMemo, useRef, type ReactNode } from 'react';
import { ArrowUpRight, ArrowLeft, BookOpen } from 'lucide-react';
import ruArticle from '../article-ru.md?raw';
import enArticle from '../article-en.md?raw';
import referenceRu from '../reference.png';
import referenceEn from '../reference-en.png';
import technologyWorkRu from '../assets/infographics/article/02-technology-work-ru.png';
import technologyWorkEn from '../assets/infographics/article/02-technology-work-en.png';
import regimeCompositionRu from '../assets/infographics/article/05-regime-composition-ru.png';
import regimeCompositionEn from '../assets/infographics/article/05-regime-composition-en.png';
import guaranteesRu from '../assets/infographics/article/06-guarantees-ru.png';
import guaranteesEn from '../assets/infographics/article/06-guarantees-en.png';
import controlDystopiaRu from '../assets/infographics/article/07-control-dystopia-ru.png';
import controlDystopiaEn from '../assets/infographics/article/07-control-dystopia-en.png';
import type { Lang } from './types';
import { copy } from './i18n';
import Credits from './Credits';

type ImageBlock = { kind: 'image'; alt: string; src: string };
type TextBlock = { kind: 'paragraph' | 'blockquote'; text: string };
type HeadingBlock = { kind: 'heading'; level: number; text: string };
type ListBlock = { kind: 'list'; ordered: boolean; items: string[] };
type Block = ImageBlock | TextBlock | HeadingBlock | ListBlock;
type Chapter = { id: string; title: string; number: number | null; blocks: Block[] };

const localImages: Record<string, string> = {
  'reference.png': referenceRu,
  'reference-en.png': referenceEn,
  'assets/infographics/article/02-technology-work-ru.png': technologyWorkRu,
  'assets/infographics/article/02-technology-work-en.png': technologyWorkEn,
  'assets/infographics/article/05-regime-composition-ru.png': regimeCompositionRu,
  'assets/infographics/article/05-regime-composition-en.png': regimeCompositionEn,
  'assets/infographics/article/06-guarantees-ru.png': guaranteesRu,
  'assets/infographics/article/06-guarantees-en.png': guaranteesEn,
  'assets/infographics/article/07-control-dystopia-ru.png': controlDystopiaRu,
  'assets/infographics/article/07-control-dystopia-en.png': controlDystopiaEn,
};

function imageUrl(path: string) {
  const normalized = path.trim().replace(/^\.\//, '');
  return localImages[normalized] || normalized;
}

function chapterId(title: string, index: number) {
  const number = title.match(/^(\d+)\./)?.[1];
  return number ? 'regime-' + number : 'chapter-' + index;
}

function parseImage(line: string): ImageBlock | null {
  const match = line.trim().match(/^!\[([^\]]*)\]\(([^)]+)\)$/);
  return match ? { kind: 'image', alt: match[1], src: imageUrl(match[2]) } : null;
}

function parseArticle(source: string): Chapter[] {
  const lines = source.replace(/\r/g, '').split('\n');
  const chapters: Chapter[] = [{ id: 'intro', title: '', number: null, blocks: [] }];
  let current = chapters[0];
  let i = 0;
  const isBoundary = (line: string) => !line.trim() || /^(#{1,6})\s+/.test(line) || /^!\[[^\]]*\]\([^)]+\)$/.test(line) || /^\s*(?:[-*+]\s+|\d+[.)]\s+)/.test(line) || /^>\s?/.test(line);
  while (i < lines.length) {
    const line = lines[i];
    if (!line.trim()) { i += 1; continue; }
    const heading = line.match(/^(#{1,6})\s+(.+?)\s*#*$/);
    if (heading) {
      if (heading[1].length === 1) {
        const title = heading[2].trim();
        current = { id: chapterId(title, chapters.length), title, number: Number(title.match(/^(\d+)\./)?.[1] || 0) || null, blocks: [] };
        chapters.push(current);
      } else {
        current.blocks.push({ kind: 'heading', level: heading[1].length, text: heading[2].trim() });
      }
      i += 1;
      continue;
    }
    const image = parseImage(line);
    if (image) { current.blocks.push(image); i += 1; continue; }
    if (/^\s*(?:[-*+]\s+|\d+[.)]\s+)/.test(line)) {
      const ordered = /^\s*\d+[.)]\s+/.test(line);
      const items: string[] = [];
      while (i < lines.length && lines[i].trim() && /^\s*(?:[-*+]\s+|\d+[.)]\s+)/.test(lines[i])) {
        items.push(lines[i].replace(/^\s*(?:[-*+]\s+|\d+[.)])\s+/, '').trim());
        i += 1;
      }
      current.blocks.push({ kind: 'list', ordered, items });
      continue;
    }
    if (/^>\s?/.test(line)) {
      const quote: string[] = [];
      while (i < lines.length && /^>\s?/.test(lines[i])) { quote.push(lines[i].replace(/^>\s?/, '').trim()); i += 1; }
      current.blocks.push({ kind: 'blockquote', text: quote.join(' ') });
      continue;
    }
    const paragraph: string[] = [line.trim()];
    i += 1;
    while (i < lines.length && lines[i].trim() && !isBoundary(lines[i])) { paragraph.push(lines[i].trim()); i += 1; }
    current.blocks.push({ kind: 'paragraph', text: paragraph.join(' ') });
  }
  return chapters;
}

function safeHref(url: string) {
  return /^(?:https?:|mailto:)/i.test(url) ? url : undefined;
}

function inline(text: string): ReactNode[] {
  const token = /(!?\[[^\]]+\]\((?:https?:\/\/|mailto:)[^)]+\)|\[[^\]]+\]\([^)]+\)|\*\*[^*]+\*\*|__[^_]+__|\*[^*]+\*|_[^_]+_|\x60[^\x60]+\x60|https?:\/\/[^\s)]+)/g;
  const pieces: ReactNode[] = [];
  let last = 0;
  let match: RegExpExecArray | null;
  let key = 0;
  const addText = (value: string) => { if (value) pieces.push(value); };
  while ((match = token.exec(text))) {
    addText(text.slice(last, match.index));
    const value = match[0];
    const image = value.match(/^!\[([^\]]*)\]\(([^)]+)\)$/);
    const link = value.match(/^\[([^\]]+)\]\(([^)]+)\)$/);
    if (image) pieces.push(<img key={key++} className="essay-inline-image" src={imageUrl(image[2])} alt={image[1]} />);
    else if (link && safeHref(link[2])) pieces.push(<a key={key++} href={link[2]} target="_blank" rel="noreferrer">{link[1]} ↗</a>);
    else if (/^https?:\/\//.test(value)) pieces.push(<a key={key++} href={value} target="_blank" rel="noreferrer">{new URL(value).hostname.replace(/^www\./, '')} ↗</a>);
    else if (/^\*\*|^__/.test(value)) pieces.push(<strong key={key++}>{value.slice(2, -2)}</strong>);
    else if (/^\*|^_/.test(value)) pieces.push(<em key={key++}>{value.slice(1, -1)}</em>);
    else if (value[0] === String.fromCharCode(96)) pieces.push(<code key={key++}>{value.slice(1, -1)}</code>);
    else addText(value);
    last = match.index + value.length;
  }
  addText(text.slice(last));
  return pieces;
}

function displayChapterTitle(chapter: Chapter, lang: Lang) {
  return chapter.id === 'chapter-1' ? (lang === 'ru' ? 'Термины' : 'Terms') : chapter.title;
}
function renderBlock(block: Block, index: number) {
  if (block.kind === 'image') return <figure className="essay-figure" key={index}><img src={block.src} alt={block.alt} loading="lazy" /></figure>;
  if (block.kind === 'blockquote') return <blockquote key={index}>{inline(block.text)}</blockquote>;
  if (block.kind === 'list') {
    const Tag = block.ordered ? 'ol' : 'ul';
    return <Tag key={index}>{block.items.map((item, itemIndex) => <li key={itemIndex}>{inline(item)}</li>)}</Tag>;
  }
  if (block.kind === 'heading') return <h3 key={index} className={block.level >= 5 ? 'essay-caption' : undefined}>{inline(block.text)}</h3>;
  return <p key={index}>{inline(block.text)}</p>;
}

export default function Article({ lang, expanded, region, onExpand, onBack }: { lang: Lang; expanded: boolean; region: number; onExpand: () => void; onBack: () => void }) {
  const t = copy[lang];
  const scroll = useRef<HTMLDivElement>(null);
  const targets = useRef<Record<string, HTMLElement | null>>({});
  const manual = useRef(0);
  const chapters = useMemo(() => parseArticle(lang === 'ru' ? ruArticle : enArticle), [lang]);
  const moveTo = (id: string) => {
    const node = targets.current[id];
    if (!node || !scroll.current) return;
    node.scrollIntoView({ block: 'start', behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' });
  };
  useEffect(() => {
    if (expanded || Date.now() <= manual.current) return;
    if (region > 0) moveTo('regime-' + region);
    else scroll.current?.scrollTo({ top: 0, behavior: 'instant' });
  }, [region, expanded, lang, chapters]);
  return <aside className={'article-panel ' + (expanded ? 'expanded' : '')} aria-label={t.article}>
    <div className="article-bar"><span><BookOpen size={13} /> {t.read}</span><button onClick={expanded ? onBack : onExpand} aria-label={expanded ? t.back : t.full} title={expanded ? t.back : t.full}>{expanded ? <ArrowLeft size={17} /> : <ArrowUpRight size={18} />}</button></div>
    <div className="article-scroll" ref={scroll} onWheel={() => { manual.current = Date.now() + 1800; }} onTouchStart={() => { manual.current = Date.now() + 1800; }}>
      <div className="article-inner">
        <header className="essay-heading"><h2>{t.articleTitle}</h2><p>{t.articleDesc}</p><div className="essay-rule" /></header>
        <nav className="essay-toc" aria-label={t.contents}><span className="eyebrow">{t.contents}</span>{chapters.map((chapter, index) => <button key={chapter.id} onClick={() => { manual.current = Date.now() + 2500; moveTo(chapter.id); }}><span>{chapter.number ? String(chapter.number).padStart(2, '0') : String(index).padStart(2, '0')}</span>{displayChapterTitle(chapter, lang) || t.intro}<ArrowUpRight size={12} /></button>)}</nav>
        {chapters.map(chapter => <section key={chapter.id} ref={node => { targets.current[chapter.id] = node; }} className={'essay-section ' + (chapter.number === region ? 'current' : '')} data-chapter={chapter.id}>{displayChapterTitle(chapter, lang) && <h2><span>{chapter.number ? String(chapter.number).padStart(2, '0') : '↗'}</span>{displayChapterTitle(chapter, lang)}</h2>}{chapter.blocks.map(renderBlock)}</section>)}
        <footer className="essay-footer">{t.estimates}<br />{t.enData}{expanded && <p><Credits /></p>}</footer>
      </div>
    </div>
  </aside>;
}
