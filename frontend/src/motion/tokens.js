/**
 * Motion tokens — single source of truth for durations, easings, staggers.
 *
 * Values mirror the `--motion-*` custom properties in `style.css` so a
 * change there propagates to every GSAP tween. GSAP accepts CSS
 * `cubic-bezier(x,y,x,y)` strings directly as `ease`, so the same curves
 * drive both CSS transitions and GSAP tweens.
 *
 * Reads happen lazily on first access; results are cached for the lifetime
 * of the page. Fallback values match the CSS hardcoded numbers so very
 * early boot reads (before the stylesheet is parsed) still produce sane
 * values.
 */

const FALLBACK = {
  durHover: 150,
  durPress: 200,
  durEntrance: 600,
  durEntranceLg: 800,
  durOdometer: 1200,
  durStroke: 850,
  staggerList: 60,
  staggerChar: 30,
  easeEntrance: 'cubic-bezier(0.22, 1, 0.36, 1)',
  easeSpring: 'cubic-bezier(0.34, 1.56, 0.64, 1)',
  easeStrokeDraw: 'cubic-bezier(0.65, 0, 0.35, 1)',
}

let cache = null

function readCssMs(name, fallback) {
  if (typeof document === 'undefined') return fallback
  const raw = getComputedStyle(document.documentElement)
    .getPropertyValue(name)
    .trim()
  if (!raw) return fallback
  const num = parseFloat(raw)
  return Number.isFinite(num) ? num : fallback
}

function readCssString(name, fallback) {
  if (typeof document === 'undefined') return fallback
  const raw = getComputedStyle(document.documentElement)
    .getPropertyValue(name)
    .trim()
  return raw || fallback
}

function load() {
  if (cache) return cache
  cache = {
    durHover: readCssMs('--motion-dur-hover', FALLBACK.durHover),
    durPress: readCssMs('--motion-dur-press', FALLBACK.durPress),
    durEntrance: readCssMs('--motion-dur-entrance', FALLBACK.durEntrance),
    durEntranceLg: readCssMs('--motion-dur-entrance-lg', FALLBACK.durEntranceLg),
    durOdometer: readCssMs('--motion-dur-odometer', FALLBACK.durOdometer),
    durStroke: readCssMs('--motion-dur-stroke', FALLBACK.durStroke),
    staggerList: readCssMs('--motion-stagger-list', FALLBACK.staggerList),
    staggerChar: readCssMs('--motion-stagger-char', FALLBACK.staggerChar),
    easeEntrance: readCssString('--motion-entrance', FALLBACK.easeEntrance),
    easeSpring: readCssString('--motion-spring', FALLBACK.easeSpring),
    easeStrokeDraw: readCssString('--motion-stroke-draw', FALLBACK.easeStrokeDraw),
  }
  return cache
}

const toSec = (ms) => ms / 1000

export const DUR = {
  get hover() { return toSec(load().durHover) },
  get press() { return toSec(load().durPress) },
  get entrance() { return toSec(load().durEntrance) },
  get entranceLg() { return toSec(load().durEntranceLg) },
  get odometer() { return toSec(load().durOdometer) },
  get stroke() { return toSec(load().durStroke) },
}

export const STAGGER = {
  get list() { return toSec(load().staggerList) },
  get char() { return toSec(load().staggerChar) },
}

export const EASE = {
  get entrance() { return load().easeEntrance },
  get spring() { return load().easeSpring },
  get strokeDraw() { return load().easeStrokeDraw },
}

export const Y = {
  body: 28,
  heading: 60,
  blur: 16,
}

export function entrance(extra = {}) {
  return { duration: DUR.entrance, ease: EASE.entrance, ...extra }
}

export function entranceLg(extra = {}) {
  return { duration: DUR.entranceLg, ease: EASE.entrance, ...extra }
}

export function resetTokenCache() {
  cache = null
}
