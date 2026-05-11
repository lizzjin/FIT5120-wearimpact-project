/**
 * Skeleton shimmer primitive. Applies a moving linear-gradient sweep on
 * a skeleton placeholder element while a `loading` ref is true; stops
 * when loading flips false.
 *
 *   const isLoading = ref(true)
 *   const skeletonRef = ref(null)
 *   useSkeletonShimmer(skeletonRef, isLoading)
 *
 * Implementation: uses backgroundPositionX on a 200%-wide linear-gradient
 * background applied to the element via inline style. Reduced-motion
 * shows a static placeholder colour.
 */
import { watch, onBeforeUnmount } from 'vue'
import { gsap } from 'gsap'
import { ensurePlugins } from '../registry'
import { isReduced } from '../matchMedia'

export function useSkeletonShimmer(elRef, isLoading, options = {}) {
  const {
    baseColor = 'var(--color-surface-alt)',
    highlightColor = 'rgba(255, 255, 255, 0.7)',
    duration = 1.4,
  } = options

  ensurePlugins()

  let tween = null

  watch(isLoading, (loading) => {
    const el = elRef?.value
    if (!el) return

    if (!loading) {
      tween?.kill()
      tween = null
      el.style.background = ''
      return
    }

    el.style.background = `linear-gradient(90deg, ${baseColor} 0%, ${highlightColor} 50%, ${baseColor} 100%)`
    el.style.backgroundSize = '200% 100%'
    el.style.backgroundPosition = '100% 0'

    if (isReduced()) return

    tween = gsap.to(el, {
      backgroundPosition: '-100% 0',
      duration,
      ease: 'none',
      repeat: -1,
    })
  }, { immediate: true })

  onBeforeUnmount(() => {
    tween?.kill()
    tween = null
  })
}
