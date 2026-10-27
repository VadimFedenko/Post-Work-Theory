export type Lang = 'ru' | 'en';
export type SocietyStatus = 'post_work' | 'transition' | 'zero_variant';
export type SocietyStatusFilter = SocietyStatus | 'all';
export type PosterCrop = { canvas: [number, number]; content_box: [number, number, number, number] };
export type Society = {
  id: string; name: string; work: string; society: string; media: string[];
  axis: { guarantees: number; control: number; nonworking: number };
  utopia_score: number; popularity_score: number; regime: number; record_type: string; icon: string; poster: string; poster_crop?: PosterCrop;
  family?: { id: string; name: string; kind: string };
  post_work_status: SocietyStatus; wage_dependence: string;
};
export type FamilyIndex = Map<string, Society[]>;
export type RecordDetail = Society & {
  description: string; scope: Record<string, unknown>; assets: Record<string, unknown>;
  translations: { ru: { description: string; economy_basis: string } };
  axis_assessment: Record<string, { interval: number[]; confidence: string; basis: string }>;
  utopia_assessment: { basis: string; confidence: string; supplemental_source_ids?: string[] };
  popularity_assessment: { subject_id: string; subject: string; basis: string; confidence: string; reference_ids: string[] };
  post_work_assessment: { status: SocietyStatus; wage_dependence: string; allocation_mechanisms: string[]; basis: string; confidence: string };
  source_ids: string[]; uncertainties: string[]; [key: string]: unknown;
};
export type Source = { id: string; title: string; url: string; read_scope?: string; limitations?: string };
