/**
 * Stagger reveal for a list/grid of children. Each direct match of `selector`
 * inside the container animates in turn when the container enters viewport.
 *
 * Used for: bullet lists, leaderboard cards, wardrobe grid items, the
 * lifecycle timeline nodes, etc. — anywhere a batch of siblings should
 * arrive one after another.
 */
import { onMounted, onBeforeUnmount } from 'vue'
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { prefersReducedMotion } from './splitText'

export function useStagger(containerRef, options = {}) {
  const {
    selector = ':scope > *',
    start = 'top 82%',
    stagger = 0.08,
    duration = 0.7,
    y = 28,
    delay = 0,
    replay = false,
    ease = 'power3.out',
  } = options

  let trigger = null

  onMounted(() => {
    const root = containerRef?.value
    if (!root) return

    // querySelectorAll does not accept the relative ">" syntax on its own;
    // a leading ">" must be normalised to a `:scope >` form, otherwise the
    // call throws SyntaxError and the rest of the composable never runs.
    const safeSelector = selector.startsWith('>') ? `:scope ${selector}` : selector
    const items = Array.from(root.querySelectorAll(safeSelector))
    if (!items.length) return

    if (prefersReducedMotion()) {
      items.forEach((it) => (it.style.opacity = '1'))
      return
    }

    gsap.set(items, { opacity: 0, y })

    const play = () => gsap.to(items, { opacity: 1, y: 0, duration, stagger, delay, ease })
    const reset = () => gsap.set(items, { opacity: 0, y })

    trigger = ScrollTrigger.create({
      trigger: root,
      start,
      once: !replay,
      onEnter: play,
      onEnterBack: replay ? play : undefined,
      onLeave: replay ? reset : undefined,
      onLeaveBack: replay ? reset : undefined,
    })
  })

  onBeforeUnmount(() => {
    trigger?.kill?.()
  })
}
