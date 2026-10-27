/** Hover hides a label only after placement: its space and label limit stay reserved. */
export function layoutAtlasLabels(points, width, height, measureText, { total = points.length, selected = null } = {}) {
  const occupied = [], labels = [], labelWidth = Math.min(280, width * .43);
  for (const side of [0, 1]) for (const y of [0, height / 2 - 16, height - 34]) occupied.push({ x: side ? width - labelWidth - 8 : 8, y, w: labelWidth, h: 34 });
  for (const p of [...points].sort((a, b) => b.record.popularity_score - a.record.popularity_score)) {
    if (labels.length >= 160 || (p.radius < 4.5 && total > 40)) continue;
    const title = p.record.work.length > 27 ? p.record.work.slice(0, 26) + '…' : p.record.work;
    const w = measureText(title) + 6, h = 13;
    const options = [
      { x: p.x - w / 2, y: p.y + p.radius + 3, w, h },
      { x: p.x - w / 2, y: p.y - p.radius - 16, w, h },
      { x: p.x + p.radius + 4, y: p.y - 6, w, h },
      { x: p.x - p.radius - w - 4, y: p.y - 6, w, h },
    ];
    const box = options.find(b => b.x > 2 && b.y > 2 && b.x + b.w < width - 2 && b.y + b.h < height - 2 && !occupied.some(o => b.x < o.x + o.w + 3 && b.x + b.w + 3 > o.x && b.y < o.y + o.h + 2 && b.y + b.h + 2 > o.y) && !points.some(o => o !== p && o.x + o.radius > b.x && o.x - o.radius < b.x + b.w && o.y + o.radius > b.y && o.y - o.radius < b.y + b.h));
    if (!box) continue;
    occupied.push(box);
    labels.push({ ...box, id: p.record.id, title, hidden: p.record.id === selected });
  }
  return labels;
}
