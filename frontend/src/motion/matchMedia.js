/**
 * Responsive + reduced-motion gateway. Replaces seven scattered matchMedia
 * checks from the pre-refactor codebase with a single helper.
 *
 * gsap.matchMedia() automatically reverts every tween / ScrollTrigger
 * created inside its callback when the query stops matching. That means
 * users toggling reduced-motion mid-session, or rotating between mobile
 * and desktop widths, both get clean cleanup without explicit code.
 */
import { gsap } from 'gsap'
import { ensurePlugins } from './registry'

let mmInstance = null

function getMM() {
  if (!mmInstance) {
    ensurePlugins()
    mmInstance = gsap.matchMedia()
  }
  return mmInstance
}

export const QUERIES = {
  isDesktop: '(min-width: 800px)',
  isMobile: '(max-width: 799px)',
  reduced: '(prefers-reduced-motion: reduce)',
  touch: '(hover: none)',
  hoverable: '(hover: hover)',
}

/**
 * Register a handler that runs whenever any of the QUERIES match.
 *
 *   motionMatch((ctx) => {
 *     const { isDesktop, reduced } = ctx.conditions
 *     if (reduced) return
 *     gsap.from('.box', { y: 60, ...entrance() })
 *   }, rootRef.value)   // optional scope ref for selector text
 */
export function motionMatch(handler, scope) {
  return getMM().add(QUERIES, handler, scope)
}

export function isReduced() {
  return (
    typeof window !== 'undefined' &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches
  )
}

export function isTouch() {
  return (
    typeof window !== 'undefined' &&
    (window.matchMedia('(hover: none)').matches || 'ontouchstart' in window)
  )
}

export function killMatchMedia() {
  mmInstance?.revert?.()
  mmInstance = null
}
