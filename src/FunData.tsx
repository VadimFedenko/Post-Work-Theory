import { useMemo, type ReactNode } from 'react';
import { BookOpen, Gamepad2, Clapperboard } from 'lucide-react';
import type { Lang, Society } from './types';
import { buildFunData } from '../scripts/fun-data.mjs';
import { atlasPalette } from '../scripts/atlas-style.mjs';
import { funDataCopy } from './fun-data-copy';
import './fun-data.css';

type Row = { label: string; percent: number | null };
const pct = (value: number | null) => value === null ? '—' : `${value}%`;
const palette = atlasPalette();
const regimeColors: Record<number, string> = { 1: palette.left[1], 2: palette.right[1], 3: palette.left[0], 4: palette.right[0], 5: palette.left[2], 6: palette.right[2] };
const mediaIcons = { book: BookOpen, anime: Clapperboard, game: Gamepad2 };

function Columns({ rows }: { rows: Row[] }) {
  return <dl className="fun-columns">{rows.map(row => <div key={row.label}>
    <dt>{row.label}</dt>
    <dd className="fun-column"><span className="fun-column-number">{pct(row.percent)}</span><i aria-hidden="true" style={{ height: `${(row.percent ?? 0) * 1.4}px` }} /></dd>
  </div>)}</dl>;
}
function Stripes({ rows }: { rows: Row[] }) {
  return <dl className="fun-stripes">{rows.map(row => <div key={row.label}>
    <dt>{row.label}</dt><dd><strong>{pct(row.percent)}</strong><i aria-hidden="true" style={{ width: `${row.percent ?? 0}%` }} /></dd>
  </div>)}</dl>;
}
function Insight({ id, title, metric, explanation, note, children }: { id: string; title: string; metric?: string; explanation?: string; note?: string; children: ReactNode }) {
  return <article className={`fun-insight fun-insight-${id}`} aria-labelledby={`fun-title-${id}`}>
    <h3 id={`fun-title-${id}`}>{title}</h3>
    <div className="fun-figure">{children}<div className="fun-notes">{metric && <p className="fun-metric" title={note}>{metric}</p>}{explanation && <p className="fun-explanation">{explanation}</p>}</div></div>
  </article>;
}
export default function FunData({ data, lang }: { data: Society[]; lang: Lang }) {
  const stats = useMemo(() => buildFunData(data), [data]);
  const t = funDataCopy[lang];
  return <section className="fun-section" id="fun-data" aria-labelledby="fun-data-title">
    <header className="fun-heading"><h2 id="fun-data-title">{t.title}</h2></header>
    <div className="fun-grid">
      <Insight id="guarantees" title={t.guaranteeTitle} explanation={t.guaranteeExplanation.replace('{ratio}', String(stats.dystopiaRatio ?? '—'))}>
        <Columns rows={[{ label: t.without, ...stats.guarantees.without }, { label: t.with, ...stats.guarantees.with }]} />
      </Insight>
      <Insight id="control" title={t.controlTitle} metric={t.controlMetric}>
        <Stripes rows={stats.control.map(row => ({ ...row, label: t.controls[row.regime] }))} />
      </Insight>
      <Insight id="media" title={t.mediaTitle} metric={t.mediaMetric}>
        <Columns rows={stats.media.map(row => ({ ...row, label: t.mediaLabels[row.media] }))} />
      </Insight>
      <Insight id="stages" title={t.stageTitle} explanation={t.stageExplanation} metric={t.stageMetric}>
        <div className="fun-pies">{stats.stages.map(stage => {
          let offset = 0;
          return <div className="fun-pie-group" key={stage.stage}>
            <div className="fun-pie"><svg viewBox="0 0 100 100" role="img" aria-label={`${t.stages[stage.stage]}: ${stage.regimes.map(row => `${t.regimeLabels[row.regime]} ${pct(row.percent)}`).join('; ')}`}>
              {stage.regimes.map(row => {
                const length = 100 * row.count / (stage.total || 1), start = offset; offset += length;
                return <circle key={row.regime} cx="50" cy="50" r="40" pathLength="100" fill="none" stroke={regimeColors[row.regime]} strokeWidth="15" strokeDasharray={`${length} ${100 - length}`} strokeDashoffset={-start} transform="rotate(-90 50 50)"><title>{t.regimeLabels[row.regime]}: {pct(row.percent)}</title></circle>;
              })}
            </svg><strong aria-label={`${t.stageMetric}: ${pct(stage.elite.percent)}`}>{pct(stage.elite.percent)}</strong></div>
            <p>{t.stages[stage.stage]}</p>
          </div>;
        })}</div>
      </Insight>
      <Insight id="leaders" title={t.leaderTitle} metric={t.leaderMetric}>
        <dl className="fun-models">{stats.mediaLeaders.map(row => {
          const Icon = mediaIcons[row.media as keyof typeof mediaIcons];
          return <div key={row.media}><dt><Icon size={16} strokeWidth={1.4} aria-hidden="true" />{t.mediaLabels[row.media]}</dt><dd>{row.leaders.map(leader => <div key={leader.regime}><span>{t.regimeLabels[leader.regime]}</span><strong>{pct(leader.percent)}</strong></div>)}</dd></div>;
        })}</dl>
      </Insight>
      <Insight id="work" title={t.workTitle} metric={t.workMetric} note={t.workNote}>
        <dl className="fun-work-rings">{stats.participation.map(row => <div key={row.stage}>
          <dt>{t.stages[row.stage]}</dt><dd><svg viewBox="0 0 120 120" aria-hidden="true"><circle className="fun-ring-rest" cx="60" cy="60" r="53" /><circle className="fun-ring-value" cx="60" cy="60" r="53" pathLength="100" strokeDasharray={`${row.percent ?? 0} 100`} transform="rotate(-90 60 60)" /></svg><strong>{pct(row.percent)}</strong></dd>
        </div>)}</dl>
      </Insight>
    </div>
    <p className="fun-caption">{t.caption}</p>
  </section>;
}
