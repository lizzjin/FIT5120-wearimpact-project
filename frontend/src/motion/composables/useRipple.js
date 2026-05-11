/**
 * Click ripple primitive. On pointerdown, creates a circular span at the
 * pointer location, scales it from 0 to cover the element, fades to 0,
 * removes the node. Element should have `position: relative` and
 * `overflow: hidden` so the ripple is clipped to its bounds — useRipple
 * applies them defensively only if they are missing.
 *
 * Reduced-motion bypasses ripple creation entirely.
 */
import { onMounted, onBeforeUnmount } from 'vue'
import { gsap } from 'gsap'
import { ensurePlugins } from '../registry'
import { isReduced } from '../matchMedia'

export function useRipple(elRef, options = {}) {
  const {
    color = 'rgba(255, 255, 255, 0.4)',
    duration = 0.55,
  } = options

  ensurePlugins()

  let cleanup = null

  onMounted(() => {
    const el = elRef?.value
    if (!el || isReduced()) return

    // Ensure the element clips the ripple.
    const cs = getComputedStyle(el)
    const restorePosition = cs.position === 'static' ? '' : null
    const restoreOverflow = cs.overflow !== 'hidden' && cs.overflow !== 'clip' ? cs.overflow : null
    if (restorePosition === '') el.style.position = 'relative'
    if (restoreOverflow !== null) el.style.overflow = 'hidden'

    const handler = (event) => {
      const rect = el.getBoundingClientRect()
      const x = (event.clientX ?? rect.left + rect.width / 2) - rect.left
      const y = (event.clientY ?? rect.top + rect.height / 2) - rect.top
      const size = Math.max(rect.width, rect.height) * 2

      const ring = document.createElement('span')
      ring.setAttribute('aria-hidden', 'true')
      ring.style.cssText = `
        position: absolute;
        left: ${x - size / 2}px;
        top: ${y - size / 2}px;
        width: ${size}px;
        height: ${size}px;
        border-radius: 50%;
        background: ${color};
        pointer-events: none;
        transform: scale(0);
        opacity: 0.6;
      `
      el.appendChild(ring)
      gsap.to(ring, {
        scale: 1,
        opacity: 0,
        duration,
        ease: 'power2.out',
        onComplete: () => ring.remove(),
      })
    }

    el.addEventListener('pointerdown', handler)

    cleanup = () => {
      el.removeEventListener('pointerdown', handler)
      // Remove any in-flight ripples.
      el.querySelectorAll(':scope > span[aria-hidden="true"]').forEach((n) => {
        if (n.style.borderRadius === '50%') n.remove()
      })
    }
  })

  onBeforeUnmount(() => cleanup?.())
}
