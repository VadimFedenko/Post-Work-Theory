import type { Lang } from './types';
import { compassFontCss } from './fonts/compass-font';

/** The compact, bilingual coordinate frame is also rendered in PNG exports. */
export default function CompassFrame({ width, height, lang, theme }: { width: number; height: number; lang: Lang; theme: string }) {
  const left = 34, top = 36, fieldWidth = width - left, row = (height - top) / 3;
  const mid = left + fieldWidth / 2;
  const colors = ['#94edb8', '#f4cd7c', '#b799ec'];
  const frameColors = theme === 'dark'
    ? { background: '#101f22', text: '#f5f7f6', green: '#94edb8', blue: '#7ecdf3', tick: '#afc4ca' }
    : { background: '#f6f6f1', text: '#25372f', green: '#27744e', blue: '#267c9f', tick: '#697c73' };
  const names = lang === 'ru' ? ['ОБЩЕСТВО', 'ЭЛИТЫ', 'АВТОНОМНЫЙ ИИ'] : ['SOCIETY', 'ELITES', 'AUTONOMOUS AI'];
  const controlLength = Math.min(lang === 'ru' ? 92 : 82, row / 2);
  const controlEnd = 8 + controlLength;
  const compact = width < 660;
  const arrowY = compact ? 19 : 25;
  return <svg className="compass-frame" xmlns="http://www.w3.org/2000/svg" viewBox={`0 0 ${width} ${height}`} aria-label={lang === 'ru' ? 'Шкалы гарантий и контроля над ИИ' : 'Guarantees and control over AI'}>
    <defs><style>{compassFontCss}</style></defs>
    <g fontFamily="'Exo 2', sans-serif" fontWeight="600" fill={frameColors.text}>
      <path d={`M62 0H${width}V36H62Z M0 0H62V36L34 64V${height}H0Z`} fill={frameColors.background} />
      <text x="38" y="28" fill={frameColors.green} fontSize="24" fontWeight="700" textAnchor="middle">{lang === 'ru' ? 'ИИ' : 'AI'}</text>
      <text transform="translate(18 8) rotate(-90)" textAnchor="end" fontSize="9" letterSpacing=".6" textLength={controlLength} lengthAdjust="spacingAndGlyphs">{lang === 'ru' ? 'КТО КОНТРОЛИРУЕТ' : 'WHO CONTROLS'}</text>
      <path d="M38 35V46" stroke={frameColors.green} strokeWidth="1.5" strokeLinecap="round" fill="none" />
      <path d="M34 44L38 51L42 44Z" fill={frameColors.green} />
      <text x={compact ? 76 : 108} y={compact ? 33 : 16} fontSize={compact ? 9 : 12} fontWeight="650" letterSpacing=".15">{lang === 'ru' ? 'Широкие гарантии' : 'Broad guarantees'}</text>
      <text x={width - (compact ? 8 : 46)} y={compact ? 33 : 16} fontSize={compact ? 9 : 12} fontWeight="650" letterSpacing=".15" textAnchor="end">{lang === 'ru' ? 'Без гарантий' : 'No guarantees'}</text>
      <text x={compact ? (76 + width - 8) / 2 : mid} y={compact ? 9 : 16} fontSize={compact ? 8 : 10} fontWeight="500" textAnchor="middle">{lang === 'ru' ? 'Гарантировано ли материальное обеспечение?' : 'Are material needs guaranteed?'}</text>
      <path d={`M76 ${arrowY}H${mid - 4}`} stroke={frameColors.green} strokeWidth="1.7" />
      <path d={`M${mid + 4} ${arrowY}H${width - 12}`} stroke={frameColors.blue} strokeWidth="1.7" />
      <path d={`M72 ${arrowY}L84 ${arrowY - 5}V${arrowY + 5}Z`} fill={frameColors.green} />
      <path d={`M${width - 8} ${arrowY}L${width - 21} ${arrowY - 5}V${arrowY + 5}Z`} fill={frameColors.blue} />
      <path d={`M${mid} ${arrowY - 4}V${arrowY + 4}`} stroke={frameColors.tick} strokeWidth="1.5" />
      {names.map((name, i) => {
        const y = top + i * row;
        const textLength = name.length * 9, half = textLength / 2 + 13;
        const center = i === 0 ? Math.max(y + row * .5, controlEnd + half + 6) : y + row * .5;
        const ribbonStart = i === 0 ? controlEnd + 8 : y + 2;
        const ribbonEnd = center - half;
        return <g key={name}>
          {ribbonEnd > ribbonStart + 16 && <path d={`M9 ${ribbonStart + 12}L31 ${ribbonStart}V${ribbonEnd - 12}L9 ${ribbonEnd + 2}Z`} fill={colors[i]} />}
          {y + row - 5 > center + half + 12 && <path d={`M9 ${center + half - 2}L31 ${center + half + 12}V${y + row - 5}Q31 ${y + row - 2} 27 ${y + row - 2}H13Q9 ${y + row - 2} 9 ${y + row - 6}Z`} fill={colors[i]} />}
          <text transform={`translate(24 ${center}) rotate(-90)`} textAnchor="middle" fontSize="14" fontWeight="650" letterSpacing=".65">{name}</text>
        </g>;
      })}
    </g>
  </svg>;
}
