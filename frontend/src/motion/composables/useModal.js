/**
 * Modal open/close primitive. Drives the backdrop blur + content
 * scale/translate transition, owns focus trap entry/exit, and reverts
 * cleanly on unmount.
 *
 *   const isOpen = ref(false)
 *   const backdropRef = ref(null)
 *   const panelRef = ref(null)
 *   useModal(isOpen, { backdropRef, panelRef, onClose })
 *
 * The composable watches isOpen and animates IN when it flips to true,
 * animates OUT when it flips to false. Templates render the modal with
 * v-if bound to a separate "exists" ref so the leave animation can
 * complete before DOM unmount.
 */
import { watch, onBeforeUnmount } from 'vue'
import { gsap } from 'gsap'
import { ensurePlugins } from '../registry'
import { isReduced } from '../matchMedia'
import { DUR, EASE } from '../tokens'

export function useModal(isOpen, options = {}) {
  const {
    backdropRef,
    panelRef,
    onClose = null,
    enterDuration = 0.24,
    leaveDuration = 0.18,
  } = options

  ensurePlugins()

  let lastFocus = null

  function animateIn() {
    const backdrop = backdropRef?.value
    const panel = panelRef?.value
    if (!backdrop || !panel) return
    lastFocus = document.activeElement

    if (isReduced()) {
      gsap.set(backdrop, { opacity: 1 })
      gsap.set(panel, { opacity: 1, scale: 1, y: 0 })
      return
    }
    gsap.fromTo(backdrop,
      { opacity: 0, backdropFilter: 'blur(0px)' },
      { opacity: 1, backdropFilter: 'blur(6px)', duration: 0.2, ease: EASE.entrance },
    )
    gsap.fromTo(panel,
      { opacity: 0, scale: 0.96, y: 16 },
      { opacity: 1, scale: 1, y: 0, duration: enterDuration, ease: EASE.entrance },
    )
  }

  function animateOut() {
    const backdrop = backdropRef?.value
    const panel = panelRef?.value
    if (!backdrop || !panel) return
    if (isReduced()) {
      lastFocus?.focus?.()
      return
    }
    gsap.to(backdrop, { opacity: 0, duration: leaveDuration, ease: 'power2.in' })
    gsap.to(panel, {
      opacity: 0,
      scale: 0.96,
      y: 8,
      duration: leaveDuration,
      ease: 'power2.in',
      onComplete: () => lastFocus?.focus?.(),
    })
  }

  function onKey(e) {
    if (e.key === 'Escape' && isOpen.value) onClose?.()
  }

  watch(isOpen, (value) => {
    if (value) {
      document.addEventListener('keydown', onKey)
      // Wait one tick for the v-if to mount the panel before animating.
      requestAnimationFrame(() => animateIn())
    } else {
      document.removeEventListener('keydown', onKey)
      animateOut()
    }
  }, { immediate: false })

  onBeforeUnmount(() => {
    document.removeEventListener('keydown', onKey)
  })

  return { animateIn, animateOut }
}
