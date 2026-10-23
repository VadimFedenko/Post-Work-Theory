const intersection = (a, b) => Math.max(0, Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x)) * Math.max(0, Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y));
function wrap(text, width, measure) {
  const lines = [], words = text.split(/\s+/);
  let line = '';
  for (const word of words) {
    const next = line ? line + ' ' + word : word;
    if (line && measure(next) > width) { lines.push(line); line = word; } else line = next;
  }
  if (line) lines.push(line);
  const visible = lines.slice(0, 3);
  for (let i = 0; i < visible.length; i++) {
    let value = visible[i], shortened = i === 2 && lines.length > 3;
    while (value && measure(value + (shortened ? '…' : '')) > width) { value = value.slice(0, -1); shortened = true; }
    visible[i] = value + (shortened ? '…' : '');
  }
  return visible;
}

/** Temporary labels use society names, without changing ordinary label reservations. */
export function layoutFamilyLabels(points, width, height, measureText, prefix) {
  const labels = [], maximumWidth = Math.max(60, Math.min(236, width * .45, width - 8));
  const icons = points.map(p => ({ x: p.x - p.radius - 3, y: p.y - p.radius - 3, w: p.radius * 2 + 6, h: p.radius * 2 + 6 }));
  for (const p of [...points].sort((a, b) => b.y - a.y || a.x - b.x || a.record.id.localeCompare(b.record.id))) {
    const text = prefix + ': ' + p.record.society;
    const w = Math.min(maximumWidth, Math.max(80, measureText(text) + 14));
    const lines = wrap(text, w - 14, measureText), h = lines.length * 13 + 10;
    const below = p.y + p.radius + 7, above = p.y - p.radius - h - 7;
    const candidates = [], rows = [below, below + h + 4, below + (h + 4) * 2];
    if (below + h > height - 4) rows.push(above);
    for (const y of rows) for (const offset of [0, -.6, .6, -1, 1]) {
      const box = { x: Math.max(4, Math.min(width - w - 4, p.x - w / 2 + offset * w)), y: Math.max(4, Math.min(height - h - 4, y)), w, h };
      const overlap = labels.reduce((sum, label) => sum + intersection(box, { x: label.x - 3, y: label.y - 3, w: label.w + 6, h: label.h + 6 }), 0);
      const iconOverlap = icons.reduce((sum, icon) => sum + intersection(box, icon), 0);
      const distance = Math.hypot(box.x + w / 2 - p.x, box.y - below);
      candidates.push({ ...box, cost: overlap * 20 + iconOverlap * 4 + distance + (box.y < p.y ? 35 : 0) });
    }
    candidates.sort((a, b) => a.cost - b.cost);
    const { cost, ...box } = candidates[0];
    const isBelow = box.y + h / 2 >= p.y;
    const x1 = p.x, y1 = p.y + (isBelow ? p.radius + 4 : -p.radius - 4);
    const x2 = Math.max(box.x + 5, Math.min(box.x + w - 5, p.x)), y2 = isBelow ? box.y : box.y + h;
    labels.push({ ...box, id: p.record.id, text, lines, leader: Math.hypot(x2 - x1, y2 - y1) > 13 ? { x1, y1, x2, y2 } : null });
  }
  return labels;
}
