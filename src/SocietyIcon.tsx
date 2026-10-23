import type { Society } from './types';
import { utopiaColor } from '../scripts/atlas-model.mjs';
import { markerShape, PENTAGON_CLIP } from '../scripts/society-status.mjs';

export default function SocietyIcon({ record, showImage = true, lazy = false }: { record: Society; showImage?: boolean; lazy?: boolean }) {
  const shape = markerShape(record.post_work_status);
  return <i className={'society-icon' + (showImage ? '' : ' dot-icon')} aria-hidden="true" style={{ backgroundColor: utopiaColor(record.utopia_score), clipPath: shape === 'circle' ? 'circle(50%)' : PENTAGON_CLIP }}>
    {showImage && <img src={'/' + record.icon} alt="" draggable={false} loading={lazy ? 'lazy' : undefined} />}
  </i>;
}
