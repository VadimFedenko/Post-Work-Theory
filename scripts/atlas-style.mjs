export const GRID_STEP = 28;
export function atlasPalette() {
  return { left: ['#a1e8b7', '#f4cd7c', '#b799ec'], right: ['#8acdf1', '#f19a9b', '#afb7bf'] };
}
export function verticalStops(colors) {
  return [[0, colors[0]], [.27, colors[0]], [.39, colors[1]], [.61, colors[1]], [.73, colors[2]], [1, colors[2]]];
}
export function gradientCSS(colors) {
  return 'linear-gradient(180deg,' + verticalStops(colors).map(([stop, color]) => color + ' ' + Math.round(stop * 100) + '%').join(',') + ')';
}
