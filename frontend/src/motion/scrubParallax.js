/**
 * Single-element scrub parallax. Mirrors the subtle scaleX scrub seen on
 * shelby.ashfall.studio's hero artwork (`scale(0.9932, 1)` driven by scrollY).
 *
 * Usage:
 *   useScrubParallax(elRef, { yPercent: -10 })
 */
import { onMounted, onBeforeUnmount } from 'vue'
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

const REDUCED = () =>
  typeof window !== 'undefined' &&
  window.matchMedia('(prefers-reduced-motion: reduce)').matches

export function useScrubParallax(elRef, options = {}) {
  const { yPercent = 0, scaleX = null, start = 'top bottom', end = 'bottom top', scrub = true } = options
  let tween = null

  onMounted(() => {
    const el = elRef?.value
    if (!el || REDUCED()) return

    const to = {}
    if (yPercent) to.yPercent = yPercent
    if (scaleX !== null) to.scaleX = scaleX

    tween = gsap.to(el, {
      ...to,
      ease: 'none',
      scrollTrigger: { trigger: el, start, end, scrub },
    })
  })

  onBeforeUnmount(() => {
    tween?.scrollTrigger?.kill?.()
    tween?.kill?.()
  })
}
