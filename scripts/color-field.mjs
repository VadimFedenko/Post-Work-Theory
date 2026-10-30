import { atlasPalette, verticalStops } from './atlas-style.mjs';

/** A small raster is sufficient for a smooth field; labels and the grid stay sharp. */
export function createColorField(width, height) {
  const palette = atlasPalette(), steps = 4096;
  const lookup = colors => {
    const stops = verticalStops(colors).map(([position, hex]) => [position, [1, 3, 5].map(i => parseInt(hex.slice(i, i + 2), 16))]);
    const result = new Float32Array(steps * 3);
    let segment = 0;
    for (let i = 0; i < steps; i++) {
      const y = i / (steps - 1);
      while (segment < stops.length - 2 && y > stops[segment + 1][0]) segment++;
      const [a, ac] = stops[segment], [b, bc] = stops[segment + 1];
      const t = Math.min(1, Math.max(0, (y - a) / (b - a)));
      for (let c = 0; c < 3; c++) result[i * 3 + c] = ac[c] + (bc[c] - ac[c]) * t;
    }
    return result;
  };
  const left = lookup(palette.left), right = lookup(palette.right);
  const columnX = new Float32Array(width), columnY = new Float32Array(width);
  const rowX = new Float32Array(height), rowY = new Float32Array(height);
  const distortionStrength = 1.4, distortionSize = 1.25;
  return (pixels, seconds = 0) => {
    // Broader waves bend colour seams without moving data coordinates or zone centres.
    for (let x = 0; x < width; x++) {
      const u = x / (width - 1) / distortionSize;
      columnX[x] = distortionStrength * .003 * Math.sin(u * 13 + seconds * .11);
      columnY[x] = distortionStrength * (.018 * Math.sin(u * 10 + seconds * .14) + .007 * Math.sin(u * 23 - seconds * .09));
    }
    for (let y = 0; y < height; y++) {
      const v = y / (height - 1) / distortionSize;
      rowX[y] = distortionStrength * (.013 * Math.sin(v * 12 - seconds * .12) + .005 * Math.sin(v * 25 + seconds * .08));
      rowY[y] = distortionStrength * .004 * Math.sin(v * 17 + seconds * .1);
    }
    for (let y = 0, p = 0; y < height; y++) for (let x = 0; x < width; x++, p += 4) {
      const u = x / (width - 1) + rowX[y] + columnX[x];
      const v = Math.max(0, Math.min(1, y / (height - 1) + (columnY[x] + rowY[y]) * .2));
      const at = Math.round(v * (steps - 1)) * 3;
      const mix = Math.max(0, Math.min(1, (u - .44) / .12));
      for (let c = 0; c < 3; c++) pixels[p + c] = left[at + c] + (right[at + c] - left[at + c]) * mix;
      pixels[p + 3] = 255;
    }
  };
}
