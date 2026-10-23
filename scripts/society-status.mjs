export const SOCIETY_STATUSES = ['post_work', 'transition', 'zero_variant'];

export function countSocietyStatuses(records) {
  const counts = { all: records.length, post_work: 0, transition: 0, zero_variant: 0 };
  for (const record of records) counts[record.post_work_status]++;
  return counts;
}

export function markerShape(status) { return status === 'post_work' ? 'circle' : 'pentagon'; }

export function pentagonVertices(cx, cy, radius) {
  return Array.from({ length: 5 }, (_, i) => {
    const angle = -Math.PI / 2 + i * Math.PI * 2 / 5;
    return [cx + Math.cos(angle) * radius, cy + Math.sin(angle) * radius];
  });
}

export function pentagonPoints(cx, cy, radius) {
  return pentagonVertices(cx, cy, radius).map(point => point.join(',')).join(' ');
}

export const PENTAGON_CLIP = 'polygon(' + pentagonVertices(50, 50, 50).map(point => point.map(value => value + '%').join(' ')).join(',') + ')';

export function traceMarker(ctx, shape, cx, cy, radius) {
  ctx.beginPath();
  if (shape === 'circle') ctx.arc(cx, cy, radius, 0, Math.PI * 2);
  else {
    pentagonVertices(cx, cy, radius).forEach(([x, y], i) => i ? ctx.lineTo(x, y) : ctx.moveTo(x, y));
    ctx.closePath();
  }
}
