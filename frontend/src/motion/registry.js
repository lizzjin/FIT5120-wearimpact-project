/**
 * Centralised GSAP plugin registration. Every composable calls
 * ensurePlugins() at first use; only the first call actually registers.
 *
 * Plugins added in later phases:
 *   Phase 2 — SplitText
 *   Phase 3 — ScrollSmoother
 *   Phase 7 — Flip, Draggable, InertiaPlugin
 */
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

let registered = false

export function ensurePlugins() {
  if (registered) return
  gsap.registerPlugin(ScrollTrigger)
  registered = true
}

export { gsap, ScrollTrigger }
