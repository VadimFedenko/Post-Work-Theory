import { GRID_STEP } from '../scripts/atlas-style.mjs';
import { traceMarker } from '../scripts/society-status.mjs';
import { displayScale } from './display-scale';

async function settleWithin(promise: Promise<unknown>, milliseconds: number) {
  let timer = 0;
  try { await Promise.race([promise.catch(() => {}), new Promise<void>(resolve => { timer = window.setTimeout(resolve, milliseconds); })]); }
  finally { window.clearTimeout(timer); }
}
function drawField(ctx: CanvasRenderingContext2D, width: number, height: number, field: HTMLCanvasElement) {
  ctx.save();
  ctx.drawImage(field, 0, 0, width, height);
  ctx.lineWidth = 1; ctx.strokeStyle = 'rgba(255,255,255,.133)';
  ctx.beginPath();
  for (let x = 0; x <= width; x += GRID_STEP) { ctx.moveTo(x, 0); ctx.lineTo(x, height); }
  for (let y = 0; y <= height; y += GRID_STEP) { ctx.moveTo(0, y); ctx.lineTo(width, y); }
  ctx.stroke();
  ctx.strokeStyle = 'rgba(53,86,77,.4)';
  ctx.beginPath();
  ctx.moveTo(width / 2, 0); ctx.lineTo(width / 2, height);
  ctx.moveTo(0, height / 3); ctx.lineTo(width, height / 3);
  ctx.moveTo(0, height * 2 / 3); ctx.lineTo(width, height * 2 / 3);
  ctx.setLineDash([6, 6]);
  ctx.stroke();
  ctx.restore();
}

function drawTextElement(ctx: CanvasRenderingContext2D, element: HTMLElement, origin: DOMRect, box = false, coordinateScale = 1) {
  const rect = element.getBoundingClientRect(), css = getComputedStyle(element);
  const bounds = new DOMRect((rect.left - origin.left) / coordinateScale, (rect.top - origin.top) / coordinateScale, rect.width / coordinateScale, rect.height / coordinateScale);
  if (!bounds.width || !bounds.height) return;
  const scale = element.offsetWidth ? bounds.width / element.offsetWidth : 1;
  const fontSize = parseFloat(css.fontSize) * scale;
  const x = bounds.left, y = bounds.top;
  const paddingX = (parseFloat(css.paddingLeft) || 0) * scale;
  const paddingY = (parseFloat(css.paddingTop) || 0) * scale;
  if (box) {
    ctx.save(); ctx.translate(x, y); ctx.scale(scale, scale);
    ctx.beginPath(); ctx.roundRect(0, 0, bounds.width / scale, bounds.height / scale, 2);
    ctx.fillStyle = css.backgroundColor; ctx.fill(); ctx.restore();
  }
  if (element.matches('.regime-label,.regime-label-box')) {
    const arrow = element.querySelector<SVGSVGElement>(':scope > .regime-arrow');
    const polygon = arrow?.querySelector('polygon'), matrix = arrow?.getScreenCTM();
    if (polygon && matrix) {
      ctx.save(); ctx.transform(matrix.a / coordinateScale, matrix.b / coordinateScale, matrix.c / coordinateScale, matrix.d / coordinateScale, (matrix.e - origin.left) / coordinateScale, (matrix.f - origin.top) / coordinateScale);
      ctx.beginPath();
      for (let i = 0; i < polygon.points.numberOfItems; i++) {
        const point = polygon.points.getItem(i);
        if (i) ctx.lineTo(point.x, point.y); else ctx.moveTo(point.x, point.y);
      }
      ctx.closePath(); ctx.fillStyle = getComputedStyle(polygon).fill; ctx.fill(); ctx.restore();
    }
    for (const child of element.querySelectorAll<HTMLElement>(':scope > span')) {
      drawTextElement(ctx, child, origin, element.classList.contains('direction-label'), coordinateScale);
    }
    return;
  }
  ctx.font = css.fontWeight + ' ' + fontSize + 'px ' + css.fontFamily;
  ctx.fillStyle = css.color; ctx.textBaseline = 'top';
  const text = (element.textContent || '').trim().replace(/\s+/g, ' ').replace(/([^\s])([↑↓])/g, '$1 $2');
  const lines: string[] = [];
  let line = '';
  const available = Math.max(10, bounds.width - paddingX * 2);
  const lineHeight = (parseFloat(css.lineHeight) || fontSize * 1.35) * scale;
  const maxLines = Math.max(1, Math.round((bounds.height - paddingY * 2) / lineHeight));
  if (css.whiteSpace === 'pre') lines.push(...(element.textContent || '').split('\n'));
  else if (maxLines === 1 || css.whiteSpace === 'nowrap') lines.push(text);
  else {
    for (const word of text.split(' ')) {
      const next = line ? line + ' ' + word : word;
      if (line && ctx.measureText(next).width > available && lines.length < maxLines - 1) { lines.push(line); line = word; } else line = next;
      if (css.overflowWrap === 'anywhere') while (ctx.measureText(line).width > available && lines.length < maxLines - 1) {
        let split = line.length;
        while (split > 1 && ctx.measureText(line.slice(0, split)).width > available) split--;
        lines.push(line.slice(0, split)); line = line.slice(split);
      }
    }
    if (line) lines.push(line);
  }
  const centred = css.textAlign === 'center' || css.justifyContent === 'center';
  ctx.textAlign = centred ? 'center' : css.textAlign === 'right' ? 'right' : 'left';
  const tx = centred ? x + bounds.width / 2 : css.textAlign === 'right' ? x + bounds.width - paddingX : x + paddingX;
  const ty = box ? y + paddingY : y + (bounds.height - lines.length * lineHeight) / 2;
  lines.forEach((value, i) => ctx.fillText(value, tx, ty + i * lineHeight + 1, available));
}

/** Exports the chart itself; controls, popovers and application panels are excluded. */
export async function createAtlasPng(plot: HTMLDivElement, labels: HTMLCanvasElement): Promise<Blob> {
  await settleWithin(document.fonts.ready, 1200);
  const shell = plot.closest('.map-shell') as HTMLDivElement;
  const shellRect = shell.getBoundingClientRect(), plotRect = plot.getBoundingClientRect();
  const scale = displayScale(), shellWidth = shellRect.width / scale, shellHeight = shellRect.height / scale;
  const output = document.createElement('canvas');
  const resolution = Math.min(2, 4096 / Math.max(shellRect.width, shellRect.height));
  output.width = Math.round(shellRect.width * resolution); output.height = Math.round(shellRect.height * resolution);
  const ctx = output.getContext('2d'); if (!ctx) throw new Error('Canvas is unavailable');
  ctx.scale(resolution * scale, resolution * scale);
  ctx.fillStyle = getComputedStyle(shell).backgroundColor; ctx.fillRect(0, 0, shellWidth, shellHeight);
  const sprites = [...plot.querySelectorAll<HTMLButtonElement>('.map-sprite')];
  await settleWithin(Promise.all(sprites.flatMap(element => { const img = element.querySelector('img'); return img && !img.complete ? [img.decode().catch(() => {})] : []; })), 1800);
  const x = (plotRect.left - shellRect.left) / scale + plot.clientLeft, y = (plotRect.top - shellRect.top) / scale + plot.clientTop;
  const width = plot.clientWidth, height = plot.clientHeight;
  ctx.save(); ctx.translate(x, y); ctx.beginPath(); ctx.rect(0, 0, width, height); ctx.clip();
  const field = plot.querySelector<HTMLCanvasElement>('.color-field');
  if (!field) throw new Error('The colour field is unavailable');
  drawField(ctx, width, height, field);
  for (const element of plot.querySelectorAll<SVGLineElement | SVGCircleElement | SVGPolygonElement>('.family-graph line,.family-graph circle,.family-graph polygon')) {
    const css = getComputedStyle(element), value = (name: string) => Number(element.getAttribute(name));
    ctx.strokeStyle = css.stroke; ctx.lineWidth = parseFloat(css.strokeWidth); ctx.lineCap = 'round'; ctx.beginPath();
    if (element.tagName === 'circle') ctx.arc(value('cx'), value('cy'), value('r'), 0, Math.PI * 2);
    else if (element.tagName === 'polygon') {
      const points = (element as SVGPolygonElement).points;
      for (let i = 0; i < points.numberOfItems; i++) { const point = points.getItem(i); if (i) ctx.lineTo(point.x, point.y); else ctx.moveTo(point.x, point.y); }
      ctx.closePath();
    }
    else { ctx.moveTo(value('x1'), value('y1')); ctx.lineTo(value('x2'), value('y2')); }
    ctx.stroke();
  }
  ctx.drawImage(labels, 0, 0, width, height);
  for (const element of sprites.sort((a, b) => Number(a.classList.contains('is-selected')) - Number(b.classList.contains('is-selected')))) {
    const box = element.getBoundingClientRect(), style = getComputedStyle(element), radius = box.width / scale / 2;
    ctx.save(); ctx.globalAlpha = Number(style.opacity);
    const cx = (box.left - plotRect.left) / scale - plot.clientLeft + radius, cy = (box.top - plotRect.top) / scale - plot.clientTop + radius;
    const icon = element.querySelector<HTMLElement>('.society-icon'); if (!icon) { ctx.restore(); continue; }
    const iconStyle = getComputedStyle(icon), shape = element.dataset.shape || 'circle';
    ctx.fillStyle = iconStyle.backgroundColor; traceMarker(ctx, shape, cx, cy, radius); ctx.fill();
    const img = element.querySelector('img'), border = parseFloat(iconStyle.paddingLeft) || 0;
    if (img?.complete && img.naturalWidth) {
      ctx.save(); traceMarker(ctx, shape, cx, cy, Math.max(0, radius - border)); ctx.clip();
      ctx.drawImage(img, cx - radius + border, cy - radius + border, (radius - border) * 2, (radius - border) * 2); ctx.restore();
    }
    ctx.restore();
  }
  const localOrigin = new DOMRect(plotRect.left + plot.clientLeft * scale, plotRect.top + plot.clientTop * scale, width, height);
  const regimeLayer = plot.querySelector<HTMLElement>('.region-labels');
  if (regimeLayer && Number(getComputedStyle(regimeLayer).opacity) > 0) for (const element of plot.querySelectorAll<HTMLElement>('.regime-label')) drawTextElement(ctx, element, localOrigin, true, scale);
  for (const element of plot.querySelectorAll<HTMLElement>('.active-name,.family-map-caption,.family-society-label')) drawTextElement(ctx, element, localOrigin, true, scale);
  ctx.restore();
  const frame = shell.querySelector<SVGSVGElement>('.compass-frame');
  if (frame) {
    const clone = frame.cloneNode(true) as SVGSVGElement;
    clone.setAttribute('width', String(shellWidth)); clone.setAttribute('height', String(shellHeight));
    const url = URL.createObjectURL(new Blob([new XMLSerializer().serializeToString(clone)], { type: 'image/svg+xml' }));
    try {
      const img = new Image(); img.src = url; await img.decode();
      ctx.drawImage(img, 0, 0, shellWidth, shellHeight);
    } finally { URL.revokeObjectURL(url); }
  }
  return new Promise((resolve, reject) => output.toBlob(blob => blob ? resolve(blob) : reject(new Error('PNG export failed')), 'image/png'));
}
