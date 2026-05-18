/**
 * Stagger reveal for a list/grid of children. Each direct match of
 * `selector` inside the container animates in turn when the container
 * enters the viewport.
 *
 * Used for bullet lists, leaderboard cards, wardrobe grid items, the
 * lifecycle timeline nodes, and any batch of siblings that should arrive
 * one after another.
 *
 * Phase 2 rewrite: durations, easings, and the default stagger now read
 * from shared motion tokens. Reduced-motion check delegates to the
 * matchMedia helper. The API surface (containerRef + options) is
 * unchanged so existing call sites stay intact.
 */
import { onMounted, onBeforeUnmount } from 'vue'
import { gsap } from 'gsap'
import { ScrollTrigger, ensurePlugins } from './registry'
import { isReduced } from './matchMedia'
import { DUR, EASE, STAGGER, Y } from './tokens'

export function useStagger(containerRef, options = {}) {
  const {
    selector = ':scope > *',
    start = 'top 82%',
    stagger = STAGGER.list,
    duration = DUR.entrance,
    y = Y.body,
    delay = 0,
    replay = false,
    ease = EASE.entrance,
  } = options

  ensurePlugins()

  let trigger = null

  onMounted(() => {
    const root = containerRef?.value
    if (!root) return

    // querySelectorAll rejects a leading ">"; normalise to `:scope >` form.
    const safeSelector = selector.startsWith('>') ? `:scope ${selector}` : selector
    const items = Array.from(root.querySelectorAll(safeSelector))
    if (!items.length) return

    if (isReduced()) {
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
