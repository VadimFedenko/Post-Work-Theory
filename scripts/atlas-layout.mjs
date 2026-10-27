import { coordinates } from './atlas-model.mjs';

function hash(text) {
  let n = 2166136261;
  for (let i = 0; i < text.length; i++) n = Math.imul(n ^ text.charCodeAt(i), 16777619);
  return n >>> 0;
}
export function popularityRadius(score, width, height, count) {
  const scale = Math.max(.65, Math.min(1.45, Math.sqrt(width * height / 700000)));
  return Math.max(2, (2.7 + 11.8 * Math.pow(Math.max(0, Math.min(1, score)), 1.9)) * scale * (count < 60 ? 1.25 : 1));
}
/** Individual visual positions; anchors and the source records never change. */
export function layoutSocieties(records, width, height, reserved = []) {
  if (!records.length || width < 20 || height < 20) return [];
  const nodes = records.map(record => {
    const anchor = coordinates(record.axis, width, height);
    const angle = hash(record.id) / 0xffffffff * Math.PI * 2;
    const radius = popularityRadius(record.popularity_score ?? .1, width, height, records.length);
    return { record, radius, anchorX: anchor.x, anchorY: anchor.y, x: anchor.x + Math.cos(angle), y: anchor.y + Math.sin(angle) };
  }).sort((a, b) => b.radius - a.radius || a.record.id.localeCompare(b.record.id));
  const buckets = new Map();
  for (const node of nodes) {
    const key = `${Math.round(node.anchorX / 12)},${Math.round(node.anchorY / 12)}`;
    const count = buckets.get(key) || 0; buckets.set(key, count + 1);
    const spread = Math.sqrt(count) * (node.radius + 3) * 1.3;
    const angle = count * 2.399963 + hash(key) / 0xffffffff;
    node.x += Math.cos(angle) * spread; node.y += Math.sin(angle) * spread;
  }
  const cell = Math.max(...nodes.map(n => n.radius)) * 2 + 3;
  const columns = Math.ceil(width / cell) + 3;
  const constrain = node => {
    const margin = node.radius + 1.5;
    node.x = Math.max(margin, Math.min(width - margin, node.x));
    node.y = Math.max(margin, Math.min(height - margin, node.y));
    for (const box of reserved) {
      if (node.x + margin <= box.x || node.x - margin >= box.x + box.width || node.y + margin <= box.y || node.y - margin >= box.y + box.height) continue;
      const moves = [
        { d: Math.abs(node.x - (box.x - margin)), x: box.x - margin, y: node.y },
        { d: Math.abs(node.x - (box.x + box.width + margin)), x: box.x + box.width + margin, y: node.y },
        { d: Math.abs(node.y - (box.y - margin)), x: node.x, y: box.y - margin },
        { d: Math.abs(node.y - (box.y + box.height + margin)), x: node.x, y: box.y + box.height + margin },
      ].filter(p => p.x >= margin && p.x <= width - margin && p.y >= margin && p.y <= height - margin);
      moves.sort((a, b) => a.d - b.d);
      if (moves[0]) { node.x = moves[0].x; node.y = moves[0].y; }
    }
  };
  for (let iteration = 0; iteration < 520; iteration++) {
    const grid = new Map();
    const spring = iteration < 170 ? .018 * (1 - iteration / 170) : 0;
    for (let i = 0; i < nodes.length; i++) {
      const n = nodes[i]; n.x += (n.anchorX - n.x) * spring; n.y += (n.anchorY - n.y) * spring; constrain(n);
      const key = Math.floor(n.x / cell) + Math.floor(n.y / cell) * columns;
      const bucket = grid.get(key) || []; bucket.push(i); grid.set(key, bucket);
    }
    let maxOverlap = 0;
    for (let i = 0; i < nodes.length; i++) {
      const a = nodes[i], cx = Math.floor(a.x / cell), cy = Math.floor(a.y / cell);
      for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) {
        const neighbors = grid.get(cx + dx + (cy + dy) * columns); if (!neighbors) continue;
        for (const j of neighbors) {
          if (j <= i) continue;
          const b = nodes[j]; let vx = b.x - a.x, vy = b.y - a.y;
          let distance = Math.hypot(vx, vy); const target = a.radius + b.radius + 1.6;
          if (distance >= target) continue;
          if (distance < .001) { vx = .01; vy = .007; distance = Math.hypot(vx, vy); }
          const overlap = target - distance; maxOverlap = Math.max(maxOverlap, overlap);
          const shift = overlap * .57;
          const shareA = b.radius * b.radius / (a.radius * a.radius + b.radius * b.radius);
          const nx = vx / distance * shift, ny = vy / distance * shift;
          a.x -= nx * shareA; a.y -= ny * shareA; b.x += nx * (1 - shareA); b.y += ny * (1 - shareA);
        }
      }
    }
    nodes.forEach(constrain);
    if (iteration > 180 && maxOverlap < .15) break;
  }
  return nodes;
}
