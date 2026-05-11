/**
 * Image / Lottie lazy-load reveal primitive. Animates an element from
 * opacity:0 + scale:0.98 to opacity:1 + scale:1 when it enters the
 * viewport. Single ScrollTrigger per element with `once: true` so it
 * only fires on first appearance.
 *
 * Use for lazy-loaded `<img>`, vue3-lottie wrappers, or any media node
 * that should fade in rather than pop into existence.
 */
import { onMounted, onBeforeUnmount } from 'vue'
import { gsap } from 'gsap'
import { ScrollTrigger, ensurePlugins } from '../registry'
import { isReduced } from '../matchMedia'
import { DUR, EASE } from '../tokens'

export function useImageReveal(elRef, options = {}) {
  const {
    start = 'top 90%',
    duration,
    delay = 0,
  } = options

  ensurePlugins()

  let trigger = null

  onMounted(() => {
    const el = elRef?.value
    if (!el) return
    if (isReduced()) {
      el.style.opacity = '1'
      return
    }

    gsap.set(el, { opacity: 0, scale: 0.98 })
    trigger = ScrollTrigger.create({
      trigger: el,
      start,
      once: true,
      onEnter: () => gsap.to(el, {
        opacity: 1,
        scale: 1,
        duration: duration ?? DUR.entrance,
        delay,
        ease: EASE.entrance,
      }),
    })
  })

  onBeforeUnmount(() => {
    trigger?.kill?.()
  })
}
