export function familyKey(record) {
  const id = record.family?.id || record.popularity_assessment?.subject_id;
  return id ? 'subject:' + id : 'work:' + record.work.normalize('NFKC').trim().toLocaleLowerCase('en');
}
export function familyName(record) {
  return record.family?.name || record.popularity_assessment?.subject || record.work;
}
export function groupFamilies(records) {
  const groups = new Map();
  for (const record of records) {
    const key = familyKey(record);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(record);
  }
  for (const records of groups.values()) records.sort((a, b) => a.society.localeCompare(b.society, 'en') || a.work.localeCompare(b.work, 'en') || a.id.localeCompare(b.id));
  return groups;
}
/** A star of undirected links avoids an all-to-all mesh for large series. */
export function familyConnections(active, points) {
  if (!active) return [];
  const key = familyKey(active.record);
  return points.filter(p => p.record.id !== active.record.id && familyKey(p.record) === key).flatMap(p => {
    const dx = p.x - active.x, dy = p.y - active.y, distance = Math.hypot(dx, dy);
    const start = active.radius + 5, end = p.radius + 5;
    if (distance <= start + end) return [];
    return [{ id: p.record.id, x1: active.x + dx / distance * start, y1: active.y + dy / distance * start, x2: p.x - dx / distance * end, y2: p.y - dy / distance * end }];
  });
}
