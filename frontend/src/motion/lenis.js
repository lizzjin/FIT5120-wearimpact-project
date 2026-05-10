/**
 * Lenis singleton, bridged to GSAP's ticker so ScrollTrigger stays in sync
 * with the smoothed scroll position. Mounted once from App.vue.
 *
 * - Disabled on touch devices (iOS momentum scroll fights smooth-scroll JS).
 * - Disabled when the user prefers reduced motion.
 * - Idempotent: repeated startLenis() calls return the same instance.
 */
import Lenis from 'lenis'
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

let instance = null

function isTouch() {
  return (
    typeof window !== 'undefined' &&
    (window.matchMedia('(hover: none)').matches || 'ontouchstart' in window)
  )
}

function prefersReducedMotion() {
  return (
    typeof window !== 'undefined' &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches
  )
}

export function startLenis() {
  if (instance || typeof window === 'undefined') return instance
  if (isTouch() || prefersReducedMotion()) return null

  instance = new Lenis({
    duration: 1.1,
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    smoothWheel: true,
  })

  // Make sure GSAP ScrollTrigger reads the smoothed position.
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
