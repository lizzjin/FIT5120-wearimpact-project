/**
 * Dropdown / popover primitive. Animates a menu open from y:8 + opacity:0
 * + scale:0.96, with optional item stagger. Direction-aware: pass a
 * `direction` of 'up' to flip the entrance origin.
 *
 *   useDropdown(isOpen, { panelRef, itemsSelector: '.menu-item', direction: 'down' })
 */
import { watch, onBeforeUnmount } from 'vue'
import { gsap } from 'gsap'
import { ensurePlugins } from '../registry'
import { isReduced } from '../matchMedia'
import { EASE, STAGGER } from '../tokens'

export function useDropdown(isOpen, options = {}) {
  const {
    panelRef,
    itemsSelector = null,
    direction = 'down',
    onClose = null,
    enterDuration = 0.18,
    leaveDuration = 0.12,
  } = options

  ensurePlugins()

  function animateIn() {
    const panel = panelRef?.value
    if (!panel) return
    const yFrom = direction === 'up' ? -8 : 8
    if (isReduced()) {
      gsap.set(panel, { opacity: 1, y: 0, scale: 1 })
      return
    }
    gsap.fromTo(panel,
      { opacity: 0, y: yFrom, scale: 0.96 },
      { opacity: 1, y: 0, scale: 1, duration: enterDuration, ease: EASE.entrance, transformOrigin: direction === 'up' ? 'bottom center' : 'top center' },
    )
    if (itemsSelector) {
      const items = panel.querySelectorAll(itemsSelector)
      if (items.length) {
        gsap.fromTo(items,
          { opacity: 0, y: 6 },
          { opacity: 1, y: 0, duration: enterDuration, stagger: STAGGER.list * 0.4, ease: EASE.entrance },
        )
      }
    }
  }

  function animateOut() {
    const panel = panelRef?.value
    if (!panel || isReduced()) return
    gsap.to(panel, { opacity: 0, duration: leaveDuration, ease: 'power2.in' })
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
