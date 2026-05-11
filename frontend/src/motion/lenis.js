/**
 * Lenis singleton, bridged to GSAP's ticker so ScrollTrigger stays in sync
 * with the smoothed scroll position. Mounted once from App.vue.
 *
 * - Disabled on touch devices (iOS momentum scroll fights smooth-scroll JS).
 * - Disabled when the user prefers reduced motion.
 * - Idempotent: repeated startLenis() calls return the same instance.
 *
 * Phase 3 (revised) note: the plan called for swapping Lenis for the
 * official GSAP ScrollSmoother, but the project has four `position: sticky`
 * elements (Navbar, EcoShopFilterBar, KnowledgeMaterials sidebar) and an
 * App.vue comment warning that any transformed/filtered ancestor breaks
 * sticky. ScrollSmoother applies a transform to its `#smooth-content`
 * wrapper, which would silently break every one of those — most visibly
 * the navbar. Keeping Lenis (which uses a scroll-position bridge, not a
 * transform) preserves sticky and is the lower-risk path; this Phase 3
 * instead harmonises Lenis with the shared motion infrastructure so the
 * reduced-motion / touch gates flow through the same matchMedia helper
 * the rest of the module uses.
 */
import Lenis from 'lenis'
import { gsap } from 'gsap'
import { ensurePlugins, ScrollTrigger } from './registry'
import { isReduced, isTouch } from './matchMedia'

let instance = null

export function startLenis() {
  if (instance || typeof window === 'undefined') return instance
  if (isTouch() || isReduced()) return null

  ensurePlugins()

  instance = new Lenis({
    duration: 1.1,
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    smoothWheel: true,
  })

  // Make ScrollTrigger read the smoothed scroll position on every tick.
  instance.on('scroll', ScrollTrigger.update)
  gsap.ticker.add((time) => instance.raf(time * 1000))
  gsap.ticker.lagSmoothing(0)

  document.documentElement.classList.add('has-lenis')
  return instance
}

export function stopLenis() {
  if (!instance) return
  instance.destroy()
  instance = null
  document.documentElement.classList.remove('has-lenis')
}

export function getLenis() {
  return instance
}

export function scrollToTopImmediate() {
  if (instance) {
    instance.scrollTo(0, { immediate: true })
  } else if (typeof window !== 'undefined') {
    window.scrollTo(0, 0)
  }
}
