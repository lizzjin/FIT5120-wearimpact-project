/**
 * Carousel slide-change primitive. Animates one slide out (x + fade)
 * and the next slide in. Direction-aware: forward (-100% / +100%) or
 * backward (+100% / -100%).
 *
 *   const { goTo } = useCarouselSlide(trackRef, { slideSelector: '.slide' })
 *   goTo(2)   // animate to slide index 2
 *
 * The track element holds N slides; the composable measures the slide
 * width and translates the track. Caller is responsible for tracking
 * which slide is active in reactive state.
 */
import { gsap } from 'gsap'
import { ensurePlugins } from '../registry'
import { isReduced } from '../matchMedia'

export function useCarouselSlide(trackRef, options = {}) {
  const {
    duration = 0.45,
    ease = 'power3.inOut',
  } = options

  ensurePlugins()

  let currentIndex = 0

  function goTo(index, opts = {}) {
    const track = trackRef?.value
    if (!track) return
    const { animate = true } = opts

    if (isReduced() || !animate) {
      gsap.set(track, { xPercent: -100 * index })
      currentIndex = index
      return
    }

    gsap.to(track, {
      xPercent: -100 * index,
      duration,
      ease,
    })
    currentIndex = index
  }

  function current() {
    return currentIndex
  }

  return { goTo, current }
}
