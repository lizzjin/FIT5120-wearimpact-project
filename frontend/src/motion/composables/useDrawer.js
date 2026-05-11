/**
 * Side drawer primitive. Slides a panel in from the right (default) with
 * a backdrop fade. Same isOpen-watch contract as useModal — bind a ref
 * that flips true/false, the composable owns the choreography.
 *
 *   useDrawer(isOpen, { backdropRef, panelRef, side: 'right', onClose })
 */
import { watch, onBeforeUnmount } from 'vue'
import { gsap } from 'gsap'
import { ensurePlugins } from '../registry'
import { isReduced } from '../matchMedia'
import { EASE } from '../tokens'

export function useDrawer(isOpen, options = {}) {
  const {
    backdropRef,
    panelRef,
    side = 'right',
    onClose = null,
    enterDuration = 0.28,
    leaveDuration = 0.22,
  } = options

  ensurePlugins()

  function fromX() {
    return side === 'right' ? '100%' : '-100%'
  }

  function animateIn() {
    const backdrop = backdropRef?.value
    const panel = panelRef?.value
    if (!panel) return
    if (isReduced()) {
      gsap.set(panel, { xPercent: 0 })
      if (backdrop) gsap.set(backdrop, { opacity: 1 })
      return
    }
    if (backdrop) {
      gsap.fromTo(backdrop, { opacity: 0 }, { opacity: 1, duration: 0.2, ease: EASE.entrance })
    }
    gsap.fromTo(panel,
      { xPercent: side === 'right' ? 100 : -100 },
      { xPercent: 0, duration: enterDuration, ease: EASE.entrance },
    )
  }

  function animateOut() {
    const backdrop = backdropRef?.value
    const panel = panelRef?.value
    if (!panel) return
    if (isReduced()) return
    if (backdrop) {
      gsap.to(backdrop, { opacity: 0, duration: leaveDuration, ease: 'power2.in' })
    }
    gsap.to(panel, {
      xPercent: side === 'right' ? 100 : -100,
      duration: leaveDuration,
      ease: 'power2.in',
    })
  }

  function onKey(e) {
    if (e.key === 'Escape' && isOpen.value) onClose?.()
  }

  watch(isOpen, (value) => {
    if (value) {
      document.addEventListener('keydown', onKey)
      requestAnimationFrame(() => animateIn())
    } else {
      document.removeEventListener('keydown', onKey)
      animateOut()
    }
  })

  onBeforeUnmount(() => {
    document.removeEventListener('keydown', onKey)
  })
}
