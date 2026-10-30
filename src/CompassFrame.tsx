import type { Lang } from './types';

/** The compact, bilingual coordinate frame is also rendered in PNG exports. */
export default function CompassFrame({ width, height, lang }: { width: number; height: number; lang: Lang }) {
  const left = 34, top = 36, fieldWidth = width - left, row = (height - top) / 3;
  const mid = left + fieldWidth / 2;
  const colors = ['#94edb8', '#f4cd7c', '#b799ec'];
  const names = lang === 'ru' ? ['ОБЩЕСТВО', 'ЭЛИТЫ', 'АВТОНОМНЫЙ ИИ'] : ['SOCIETY', 'ELITES', 'AUTONOMOUS AI'];
  const controlLength = lang === 'ru' ? 92 : 82;
  const controlEnd = 8 + controlLength;
  return <svg className="compass-frame" xmlns="http://www.w3.org/2000/svg" viewBox={`0 0 ${width} ${height}`} aria-label={lang === 'ru' ? 'Шкалы гарантий и контроля над ИИ' : 'Guarantees and control over AI'}>
    <g fontFamily="Arial, sans-serif" fontWeight="700" fill="#f5f7f6">
      <path d={`M62 0H${width}V36H62Z M0 0H62V36L34 64V${height}H0Z`} fill="#101f22" />
      <text x="38" y="28" fill={colors[0]} fontSize="24" textAnchor="middle">{lang === 'ru' ? 'ИИ' : 'AI'}</text>
      <text transform="translate(18 8) rotate(-90)" textAnchor="end" fontSize="10" textLength={controlLength} lengthAdjust="spacingAndGlyphs">{lang === 'ru' ? 'КТО КОНТРОЛИРУЕТ' : 'WHO CONTROLS'}</text>
      <path d="M38 35V46" stroke={colors[0]} strokeWidth="1.5" strokeLinecap="round" fill="none" />
      <path d="M34 44L38 51L42 44Z" fill={colors[0]} />
      <text x="108" y="16" fontSize="12">{lang === 'ru' ? 'Широкие гарантии' : 'Broad guarantees'}</text>
      <text x={width - 46} y="16" fontSize="12" textAnchor="end">{lang === 'ru' ? 'Без гарантий' : 'No guarantees'}</text>
      <text x={mid} y="16" fontSize="10" textAnchor="middle">{lang === 'ru' ? 'Гарантировано ли материальное обеспечение?' : 'Are material needs guaranteed?'}</text>
      <path d={`M76 25H${mid - 4}`} stroke={colors[0]} strokeWidth="1.7" />
      <path d={`M${mid + 4} 25H${width - 12}`} stroke="#7ecdf3" strokeWidth="1.7" />
      <path d="M72 25L84 20V30Z" fill={colors[0]} />
      <path d={`M${width - 8} 25L${width - 21} 20V30Z`} fill="#7ecdf3" />
      <path d={`M${mid} 21V29`} stroke="#afc4ca" strokeWidth="1.5" />
      {names.map((name, i) => {
        const y = top + i * row, center = y + row * .5;
        const textLength = name.length * 8.1, half = textLength / 2 + 13;
        const ribbonStart = i === 0 ? controlEnd + 8 : y + 2;
        const ribbonEnd = center - half;
        return <g key={name}>
          {ribbonEnd > ribbonStart + 16 && <path d={`M9 ${ribbonStart + 12}L31 ${ribbonStart}V${ribbonEnd - 12}L9 ${ribbonEnd + 2}Z`} fill={colors[i]} />}
          <path d={`M9 ${center + half - 2}L31 ${center + half + 12}V${y + row - 5}Q31 ${y + row - 2} 27 ${y + row - 2}H13Q9 ${y + row - 2} 9 ${y + row - 6}Z`} fill={colors[i]} />
          <text transform={`translate(24 ${center}) rotate(-90)`} textAnchor="middle" fontSize="15">{name}</text>
        </g>;
      })}
    </g>
  </svg>;
}
