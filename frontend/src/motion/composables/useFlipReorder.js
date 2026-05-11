/**
 * List reorder / filter primitive. Uses the Flip plugin to animate items
 * from their old positions to their new ones when the underlying array
 * changes. Mirrors the BrandLeaderboard / WardrobeMain re-sort flow.
 *
 *   const { capture, animate } = useFlipReorder(containerRef, {
 *     itemSelector: '.rank-card',
 *   })
 *
 *   watch(sortedBrands, () => {
 *     capture()                  // snapshot before Vue updates
 *     nextTick(() => animate())  // animate after DOM settles
 *   })
 */
import { Flip, ensurePlugins } from '../registry'
import { isReduced } from '../matchMedia'

export function useFlipReorder(containerRef, options = {}) {
  const {
    itemSelector = '> *',
    duration = 0.5,
    ease = 'power2.inOut',
    absolute = true,
  } = options

  ensurePlugins()

  let prevState = null

  function capture() {
    const container = containerRef?.value
    if (!container) return
    const items = container.querySelectorAll(itemSelector.startsWith('>') ? `:scope ${itemSelector}` : itemSelector)
    if (!items.length) return
    prevState = Flip.getState(items)
  }

  function animate() {
    if (!prevState || isReduced()) {
      prevState = null
      return
    }
    Flip.from(prevState, {
      duration,
      ease,
      absolute,
      stagger: 0.02,
    })
    prevState = null
  }

  return { capture, animate }
}
