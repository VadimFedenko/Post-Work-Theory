import { useEffect, useRef, useState, type RefObject } from 'react';
import { Camera, Info } from 'lucide-react';
import type { AtlasHandle } from './Atlas';
import type { Lang } from './types';
import { copy } from './i18n';

export default function MapTools({ atlas, ready, lang }: { atlas: RefObject<AtlasHandle | null>; ready: boolean; lang: Lang }) {
  const t = copy[lang];
  const [help, setHelp] = useState(false), [saving, setSaving] = useState(false), [error, setError] = useState(false);
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const cancel = () => { if (timer.current) clearTimeout(timer.current); };
  useEffect(() => () => cancel(), []);
  const save = async () => {
    if (!atlas.current || saving) return;
    setSaving(true); setError(false);
    try { await atlas.current.saveImage(); } catch { setError(true); } finally { setSaving(false); }
  };
  return <div className="map-tools" role="group" aria-label={t.mapTools}>
    <div className="map-help" onPointerEnter={e => { if (e.pointerType !== 'touch') { cancel(); setHelp(true); } }} onPointerLeave={() => { cancel(); timer.current = setTimeout(() => setHelp(false), 180); }} onKeyDown={e => { if (e.key === 'Escape') setHelp(false); }}>
      <button className="tool-button" aria-label={t.methodology} aria-expanded={help} aria-describedby={help ? 'map-key' : undefined} onClick={() => setHelp(true)} onFocus={() => { cancel(); setHelp(true); }} onBlur={() => setHelp(false)}><Info size={16} /></button>
      {help && <div className="map-help-popover" id="map-key" role="tooltip"><h3>{t.methodology}</h3><p>{t.methodologyText}</p><p>{t.estimates}</p><p>{t.legacy}</p></div>}
    </div>
    <button className="tool-button" aria-label={t.screenshot} title={t.screenshot} disabled={!ready || saving} onClick={save}><Camera size={16} className={saving ? 'saving-icon' : ''} /></button>
    {error && <span role="alert" className="export-error">{t.exportError}</span>}
  </div>;
}
