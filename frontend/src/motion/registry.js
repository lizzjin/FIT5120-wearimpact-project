/**
 * Centralised GSAP plugin registration. Every composable calls
 * ensurePlugins() at first use; only the first call actually registers.
 *
 * Plugins registered:
 *   ScrollTrigger    Phase 1 — scroll-driven animation
 *   SplitText        Phase 2 — char/word/line text splitting
 *   Flip             Phase 7 — tab indicator slide + list reorder
 *   Draggable        Phase 7 — touch swipe + drag interactions
 *   InertiaPlugin    Phase 7 — drag inertia / snap-to-rest
 */
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { SplitText } from 'gsap/SplitText'
import { Flip } from 'gsap/Flip'
import { Draggable } from 'gsap/Draggable'
import { InertiaPlugin } from 'gsap/InertiaPlugin'

let registered = false

export function ensurePlugins() {
  if (registered) return
  gsap.registerPlugin(ScrollTrigger, SplitText, Flip, Draggable, InertiaPlugin)
  registered = true
}

export { gsap, ScrollTrigger, SplitText, Flip, Draggable, InertiaPlugin }
