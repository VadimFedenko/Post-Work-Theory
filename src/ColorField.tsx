import { useEffect, useRef } from 'react';
import { createColorField } from '../scripts/color-field.mjs';

export default function ColorField({ width, height }: { width: number; height: number }) {
  const canvas = useRef<HTMLCanvasElement>(null);
  useEffect(() => {
    const element = canvas.current; if (!element) return;
    element.width = Math.max(2, Math.min(512, Math.ceil(width / 3)));
    element.height = Math.max(2, Math.min(384, Math.ceil(height / 3)));
    const ctx = element.getContext('2d'); if (!ctx) return;
    const frame = ctx.createImageData(element.width, element.height);
    const paint = createColorField(element.width, element.height);
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
    let request = 0, previous = -Infinity;
    const render = (now: number) => {
      if (previous === -Infinity || (!document.hidden && now - previous >= 40)) {
        paint(frame.data, reduced.matches ? 0 : now / 1000 * 10);
        ctx.putImageData(frame, 0, 0); previous = now;
      }
      if (!reduced.matches) request = requestAnimationFrame(render);
    };
    const restart = () => { cancelAnimationFrame(request); previous = -Infinity; render(performance.now()); };
    render(performance.now()); reduced.addEventListener('change', restart);
    return () => { cancelAnimationFrame(request); reduced.removeEventListener('change', restart); };
  }, [width, height]);
  return <canvas ref={canvas} className="color-field" aria-hidden="true" />;
}
