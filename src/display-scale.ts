/** CSS zoom changes layout units; pointer and bounding-rect coordinates stay in viewport units. */
export function displayScale(): number {
  return parseFloat(getComputedStyle(document.documentElement).zoom) || 1;
}

export function layoutViewport() {
  const scale = displayScale();
  return { width: document.documentElement.clientWidth / scale, height: window.innerHeight / scale };
}
