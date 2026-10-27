// Descriptive, unweighted catalogue summaries. Always pass the entire catalogue,
// never the map's filtered records. Both source records and the web index work.
export const FUN_STAGES = ['zero_variant', 'transition', 'post_work'];
export const FUN_REGIMES = [1, 2, 3, 4, 5, 6];
const status = record => record.post_work_status ?? record.post_work_assessment.status;
const regime = record => record.regime ?? record.regime_primary;
export function percent(count, total) { return total ? Math.round(100 * count / total) : null; }
function share(records, predicate) {
  const count = records.filter(predicate).length;
  return { count, total: records.length, percent: percent(count, records.length) };
}
export function median(values) {
  if (!values.length) return null;
  const sorted = [...values].sort((a, b) => a - b), middle = Math.floor(sorted.length / 2);
  return sorted.length % 2 ? sorted[middle] : (sorted[middle - 1] + sorted[middle]) / 2;
}
// As in the research slide: only zero variants are projected onto the six
// coordinate regions. Preserve the editorial regimes of all other records.
export function compositionRegime(record) {
  if (regime(record) !== 0) return regime(record);
  const base = record.axis.control > 1 / 3 ? 3 : record.axis.control <= -1 / 3 ? 5 : 1;
  return base + (record.axis.guarantees < 0 ? 0 : 1);
}
export function buildFunData(records) {
  const withGuarantees = records.filter(record => record.axis.guarantees < 0);
  const withoutGuarantees = records.filter(record => record.axis.guarantees >= 0);
  const guarantees = {
    without: share(withoutGuarantees, record => record.utopia_score <= -.5),
    with: share(withGuarantees, record => record.utopia_score <= -.5),
  };
  const ratio = guarantees.with.count && guarantees.without.total
    ? Math.round((guarantees.without.count / guarantees.without.total) / (guarantees.with.count / guarantees.with.total)) : null;
  return {
    total: records.length, guarantees, dystopiaRatio: ratio,
    control: [3, 5, 1].map(id => ({ regime: id, ...share(records.filter(record => regime(record) === id), record => record.utopia_score > 0) })),
    media: ['book', 'anime', 'tv'].map(media => ({ media, ...share(records.filter(record => record.media.includes(media)), record => record.utopia_score < 0) })),
    stages: FUN_STAGES.map(stage => {
      const group = records.filter(record => status(record) === stage);
      const counts = FUN_REGIMES.map(id => ({ regime: id, ...share(group, record => compositionRegime(record) === id) }));
      return { stage, total: group.length, regimes: counts, elite: counts.find(row => row.regime === 2) };
    }),
    mediaLeaders: ['book', 'anime', 'game'].map(media => {
      const group = records.filter(record => record.media.includes(media) && status(record) === 'post_work');
      const counts = FUN_REGIMES.map(id => ({ regime: id, ...share(group, record => regime(record) === id) }));
      const maximum = Math.max(...counts.map(row => row.count));
      return { media, total: group.length, leaders: counts.filter(row => row.count === maximum && maximum > 0) };
    }),
    participation: ['zero_variant', 'post_work'].map(stage => {
      const group = records.filter(record => status(record) === stage);
      // Take the median before rounding; do not reuse the rounded card value.
      const value = median(group.map(record => 100 * (1 - record.axis.nonworking)));
      return { stage, total: group.length, percent: value === null ? null : Math.round(value) };
    }),
  };
}
