/**
 * Tooltip primitive. Shows a tooltip element on hover (after a 400ms
 * delay to filter out drive-by mouse-overs) and hides it on leave. The
 * tooltip element itself is rendered by the parent — useTooltip only
 * controls visibility + animation.
 *
 *   const triggerRef = ref(null)
 *   const tooltipRef = ref(null)
 *   useTooltip(triggerRef, tooltipRef, { delay: 400 })
 */
import { onMounted, onBeforeUnmount } from 'vue'
import { gsap } from 'gsap'
import { ensurePlugins } from '../registry'
import { isReduced, isTouch } from '../matchMedia'
import { EASE } from '../tokens'

export function useTooltip(triggerRef, tooltipRef, options = {}) {
  const {
    delay = 400,
    enterDuration = 0.18,
    leaveDuration = 0.12,
  } = options

  ensurePlugins()

  let showTimer = null
  let cleanup = null

  onMounted(() => {
    const trigger = triggerRef?.value
    const tooltip = tooltipRef?.value
    if (!trigger || !tooltip) return

    // Default state: hidden, ready to fade in.
    gsap.set(tooltip, { opacity: 0, y: 4, pointerEvents: 'none' })

    const show = () => {
      if (isTouch()) return
      clearTimeout(showTimer)
      showTimer = setTimeout(() => {
        if (isReduced()) {
          gsap.set(tooltip, { opacity: 1, y: 0 })
          return
        }
        gsap.to(tooltip, { opacity: 1, y: 0, duration: enterDuration, ease: EASE.entrance })
      }, delay)
    }
    const hide = () => {
      clearTimeout(showTimer)
      if (isReduced()) {
        gsap.set(tooltip, { opacity: 0, y: 4 })
        return
      }
      gsap.to(tooltip, { opacity: 0, y: 4, duration: leaveDuration, ease: 'power2.in' })
    }

    trigger.addEventListener('pointerenter', show)
    trigger.addEventListener('pointerleave', hide)
    trigger.addEventListener('focus', show)
    trigger.addEventListener('blur', hide)

    cleanup = () => {
      clearTimeout(showTimer)
      trigger.removeEventListener('pointerenter', show)
      trigger.removeEventListener('pointerleave', hide)
      trigger.removeEventListener('focus', show)
      trigger.removeEventListener('blur', hide)
    }
  })

  onBeforeUnmount(() => cleanup?.())
}
