import { forwardRef, useEffect, useImperativeHandle, useMemo, useRef, useState } from 'react';
import type { Lang, Society } from './types';
import { copy, societyTypes } from './i18n';
import { utopiaColor } from '../scripts/atlas-model.mjs';
import { layoutSocieties } from '../scripts/atlas-layout.mjs';
import { layoutAtlasLabels } from '../scripts/atlas-labels.mjs';
import { familyConnections, familyKey, familyName } from '../scripts/society-families.mjs';
import { layoutFamilyLabels } from '../scripts/family-labels.mjs';
import { GRID_STEP } from '../scripts/atlas-style.mjs';
import { createAtlasPng } from './atlas-export';
import { displayScale } from './display-scale';
import ColorField from './ColorField';
import CompassFrame from './CompassFrame';
import SocietyIcon from './SocietyIcon';
import { markerShape, pentagonPoints } from '../scripts/society-status.mjs';

export type Selection = { record: Society; pinned: boolean };
export type AtlasHandle = { saveImage: () => Promise<void> };
type Props = { data: Society[]; lang: Lang; theme: string; emptyMessage: string; onRegion: (n: number) => void; onSelect: (s: Selection | null) => void; selected: string | null; cancelClose: () => void; scheduleClose: () => void };
type Point = { x: number; y: number; anchorX: number; anchorY: number; radius: number; record: Society };
type FamilyLabel = { id: string; text: string; lines: string[]; x: number; y: number; w: number; h: number; leader: { x1: number; y1: number; x2: number; y2: number } | null };
const regionOrder = [3, 4, 1, 2, 5, 6];
const Atlas = forwardRef<AtlasHandle, Props>(function Atlas({ data, lang, theme, emptyMessage, onRegion, onSelect, selected, cancelClose, scheduleClose }, ref) {
  const t = copy[lang];
  const host = useRef<HTMLDivElement>(null);
  const canvas = useRef<HTMLCanvasElement>(null);
  const [size, setSize] = useState({ width: 1000, height: 700 });
  const hovered = useRef<string | null>(null);
  const region = useRef(-1);
  useEffect(() => {
    if (!host.current) return;
    const observer = new ResizeObserver(([entry]) => {
      const width = Math.round(entry.contentRect.width), height = Math.round(entry.contentRect.height);
      setSize(old => old.width === width && old.height === height ? old : { width, height });
    });
    observer.observe(host.current); return () => observer.disconnect();
  }, []);
  useEffect(() => { hovered.current = null; }, [data]);
  const points: Point[] = useMemo(() => {
    return layoutSocieties(data, size.width, size.height, []);
  }, [data, size]);
  const activePoint = points.find(p => p.record.id === selected);
  const activeFamily = activePoint ? familyKey(activePoint.record) : null;
  const familyPoints = activeFamily ? points.filter(p => familyKey(p.record) === activeFamily) : [];
  const hasFamily = familyPoints.length > 1;
  const familyLabels = useMemo<FamilyLabel[]>(() => {
    if (!hasFamily) return [];
    const ctx = document.createElement('canvas').getContext('2d'); if (!ctx) return [];
    ctx.font = '500 10px Arial, sans-serif';
    return layoutFamilyLabels(familyPoints, size.width, size.height, (text: string) => ctx.measureText(text).width, t.societyLabel);
  }, [points, activeFamily, size.width, size.height, lang]);
  const connections: { id: string; x1: number; y1: number; x2: number; y2: number }[] = familyConnections(activePoint, points);
  const activeLabelWidth = activePoint ? Math.min(size.width - 8, 360, activePoint.record.work.length * 6.4 + 16) : 0;
  const pointAt = (x: number, y: number) => {
    let closest: Point | null = null, distance = Infinity;
    for (const p of points) { const d = Math.hypot(p.x - x, p.y - y); if (d <= Math.max(p.radius + 2, 6) && d < distance) { closest = p; distance = d; } }
    return closest;
  };
  useEffect(() => {
    const element = canvas.current; if (!element) return;
    const dpr = Math.min((window.devicePixelRatio || 1) * displayScale(), 2);
    element.width = Math.round(size.width * dpr); element.height = Math.round(size.height * dpr);
    const ctx = element.getContext('2d'); if (!ctx) return;
    const css = getComputedStyle(element);
    const labelBackground = css.getPropertyValue('--map-label-background').trim();
    const labelForeground = css.getPropertyValue('--map-label-foreground').trim();
    ctx.scale(dpr, dpr); ctx.clearRect(0, 0, size.width, size.height);
    ctx.font = '500 10px Arial, sans-serif'; ctx.textBaseline = 'top'; ctx.textAlign = 'left';
    const labels = layoutAtlasLabels(points, size.width, size.height, (title: string) => ctx.measureText(title).width, { total: data.length, selected });
    const familyIds = new Set(hasFamily ? familyPoints.map(p => p.record.id) : []);
    for (const label of labels) {
      if (label.hidden || familyIds.has(label.id)) continue;
      ctx.fillStyle = labelBackground; ctx.beginPath(); ctx.roundRect(label.x, label.y - 1, label.w, label.h, 2); ctx.fill();
      ctx.fillStyle = labelForeground; ctx.fillText(label.title, label.x + 3, label.y);
    }
  }, [points, size, theme, selected, data.length]);
  useImperativeHandle(ref, () => ({
    saveImage: async () => {
      if (!host.current || !canvas.current) return;
      const blob = await createAtlasPng(host.current, canvas.current);
      const url = URL.createObjectURL(blob), link = document.createElement('a');
      link.href = url; link.download = 'post-work-societies.png'; link.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
    },
  }));
  const setRegionAt = (x: number, y: number) => {
    const wx = x / size.width, wy = y / size.height;
    const n = regionOrder[Math.max(0, Math.min(2, Math.floor(wy * 3))) * 2 + (wx < .5 ? 0 : 1)];
    if (n !== region.current) { region.current = n; onRegion(n); }
  };
  return <div className="map-shell compass-shell" data-theme={theme}>
    <CompassFrame width={size.width + 34} height={size.height + 36} lang={lang} theme={theme} />
    <div className={'plot' + (hasFamily ? ' has-family' : '')} ref={host}>
      <ColorField width={size.width} height={size.height} />
      <div className="plot-grid" data-grid-step={GRID_STEP} aria-hidden="true" style={{ backgroundSize: `${GRID_STEP}px ${GRID_STEP}px` }} />
      <svg className="zone-guides" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><path d="M50 0V100 M0 33.333H100 M0 66.667H100" /></svg>
      {hasFamily && <svg className="family-graph" aria-hidden="true" viewBox={`0 0 ${size.width} ${size.height}`}>
        {connections.map(link => <g key={link.id} data-related-id={link.id}><line className="family-link-halo" x1={link.x1} y1={link.y1} x2={link.x2} y2={link.y2} /><line className="family-link" x1={link.x1} y1={link.y1} x2={link.x2} y2={link.y2} /></g>)}
        {familyPoints.map(p => <g key={p.record.id}>{markerShape(p.record.post_work_status) === 'circle' ? <><circle className="family-ring-halo" cx={p.x} cy={p.y} r={p.radius + 4} /><circle className="family-ring" cx={p.x} cy={p.y} r={p.radius + 4} /></> : <><polygon className="family-ring-halo" points={pentagonPoints(p.x, p.y, p.radius + 4)} /><polygon className="family-ring" points={pentagonPoints(p.x, p.y, p.radius + 4)} /></>}</g>)}
        {familyLabels.filter(label => label.leader).map(label => <line className="family-label-link" key={'label-' + label.id} x1={label.leader!.x1} y1={label.leader!.y1} x2={label.leader!.x2} y2={label.leader!.y2} />)}
      </svg>}
      <canvas ref={canvas} role="img" aria-label={lang === 'ru' ? 'Карта: ' + data.length + ' отдельных обществ. ' + t.hint : 'Map: ' + data.length + ' individual societies. ' + t.hint} data-point-count={points.length}
        onPointerMove={e => {
          const r = e.currentTarget.getBoundingClientRect(), x = (e.clientX - r.left) * size.width / r.width, y = (e.clientY - r.top) * size.height / r.height;
          setRegionAt(x, y);
          const point = pointAt(x, y);
          if (point) { cancelClose(); if (hovered.current !== point.record.id) { hovered.current = point.record.id; onSelect({ record: point.record, pinned: false }); } }
          else { hovered.current = null; scheduleClose(); }
        }}
        onPointerLeave={scheduleClose}
        onPointerUp={e => { const r = e.currentTarget.getBoundingClientRect(); const p = pointAt((e.clientX - r.left) * size.width / r.width, (e.clientY - r.top) * size.height / r.height); if (p) onSelect({ record: p.record, pinned: true }); }}
      />
      <div className="sprite-layer" role="group" aria-label={t.societies}>{[...points].reverse().map((p, index) => <button
        className={'map-sprite ' + (p.record.id === selected ? 'is-selected' : '') + (p.radius < 4.5 ? ' small-dot' : '') + (hasFamily && familyKey(p.record) === activeFamily ? ' family-member' : '')}
        key={p.record.id} data-society-id={p.record.id} data-anchor-x={p.anchorX.toFixed(1)} data-anchor-y={p.anchorY.toFixed(1)} data-popularity={p.record.popularity_score} data-shape={markerShape(p.record.post_work_status)}
        tabIndex={index === points.length - 1 ? 0 : -1} aria-label={p.record.work + ' — ' + p.record.society + ' — ' + societyTypes[lang][p.record.post_work_status]}
        style={{ left: p.x, top: p.y, width: p.radius * 2, height: p.radius * 2, color: utopiaColor(p.record.utopia_score) }}
        onPointerEnter={() => { cancelClose(); hovered.current = p.record.id; onSelect({ record: p.record, pinned: false }); setRegionAt(p.anchorX, p.anchorY); }}
        onPointerLeave={scheduleClose}
        onFocus={() => { cancelClose(); onSelect({ record: p.record, pinned: true }); }}
        onClick={() => { cancelClose(); onSelect({ record: p.record, pinned: true }); }}
        onKeyDown={e => { const direction = ['ArrowRight', 'ArrowDown'].includes(e.key) ? 1 : ['ArrowLeft', 'ArrowUp'].includes(e.key) ? -1 : 0; if (direction) { e.preventDefault(); (e.currentTarget.parentElement?.children[(index + direction + points.length) % points.length] as HTMLElement)?.focus(); } }}
      ><SocietyIcon record={p.record} showImage={p.radius >= 4.5} /></button>)}</div>
      {!data.length && <div className="empty-map-note">{emptyMessage}</div>}
      {activePoint && !hasFamily && <span className="active-name" style={{ left: Math.max(4, Math.min(size.width - activeLabelWidth - 4, activePoint.x - activeLabelWidth / 2)), top: activePoint.y + activePoint.radius + 23 < size.height ? activePoint.y + activePoint.radius + 4 : activePoint.y - activePoint.radius - 23, maxWidth: Math.min(360, size.width - 8) }}>{activePoint.record.work}</span>}
      <div className="family-society-labels">{familyLabels.map(label => <span className={'family-society-label' + (label.id === selected ? ' is-active' : '')} key={label.id} data-society-id={label.id} aria-label={label.text} title={label.text} style={{ left: label.x, top: label.y, width: label.w, height: label.h }}>{label.lines.join('\n')}</span>)}</div>
      {hasFamily && activePoint && <span className="family-map-caption">{familyName(activePoint.record)} · {familyPoints.length} {t.relatedOnMap}</span>}
    </div>
  </div>;
});
export default Atlas;
