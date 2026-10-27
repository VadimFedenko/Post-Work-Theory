export type Share = { count: number; total: number; percent: number | null };
export type RegimeShare = Share & { regime: number };
type Stage = 'zero_variant' | 'transition' | 'post_work';
type RecordInput = {
  axis: { guarantees: number; control: number; nonworking: number };
  utopia_score: number; media: string[]; regime?: number; regime_primary?: number;
  post_work_status?: Stage; post_work_assessment?: { status: Stage };
};
export const FUN_STAGES: Stage[];
export const FUN_REGIMES: number[];
export function percent(count: number, total: number): number | null;
export function median(values: number[]): number | null;
export function compositionRegime(record: RecordInput): number;
export function buildFunData(records: RecordInput[]): {
  total: number; guarantees: { without: Share; with: Share }; dystopiaRatio: number | null;
  control: RegimeShare[];
  media: (Share & { media: string })[];
  stages: { stage: Stage; total: number; regimes: RegimeShare[]; elite: RegimeShare }[];
  mediaLeaders: { media: string; total: number; leaders: RegimeShare[] }[];
  participation: { stage: Stage; total: number; percent: number | null }[];
};
