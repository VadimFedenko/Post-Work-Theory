import coordinateFont from './exo-2-coordinate.woff2?inline';

// Keep the frame self-contained: SVG images used by PNG export cannot load external fonts.
export const compassFontCss = `
@font-face {
  font-family: 'Exo 2'; font-style: normal; font-weight: 500 700; font-display: swap;
  src: url('${coordinateFont}') format('woff2');
}`;
