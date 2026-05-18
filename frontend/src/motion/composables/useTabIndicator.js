/**
 * Tab/toggle active indicator that slides from the old position to the
 * new one using the Flip plugin. Pass an indicator element ref and a
 * reactive ref of the active key; the composable measures the position
 * before the active class swaps, applies the new state, then animates.
 *
 *   const activeKey = ref('list')
 *   const containerRef = ref(null)
 *   useTabIndicator(containerRef, activeKey, {
 *     indicatorSelector: '.tab--active',
 *   })
 *
 * The container must already render `.tab--active` on whichever tab is
 * current. When `activeKey` changes, Vue updates the class, and this
 * composable's Flip.from() animates the indicator's bounds.
 */
import { watch, onBeforeUnmount } from 'vue'
import { Flip, ensurePlugins } from '../registry'
import { isReduced } from '../matchMedia'

export function useTabIndicator(containerRef, activeKey, options = {}) {
  const {
    indicatorSelector = '[data-tab-active]',
    duration = 0.32,
    ease = 'power3.inOut',
  } = options

  ensurePlugins()

  let prevState = null

  function snapshot() {
    const container = containerRef?.value
    if (!container) return null
    const el = container.querySelector(indicatorSelector)
    return el ? Flip.getState(el) : null
  }

  function animate() {
    if (!prevState || isReduced()) return
    Flip.from(prevState, { duration, ease, absolute: true })
    prevState = null
  }

  // Capture the snapshot synchronously when activeKey changes (i.e. before
  // Vue applies the new active class), then animate after the DOM updates.
  watch(activeKey, () => {
    prevState = snapshot()
    queueMicrotask(animate)
  })

  onBeforeUnmount(() => {
    prevState = null
  })
}
