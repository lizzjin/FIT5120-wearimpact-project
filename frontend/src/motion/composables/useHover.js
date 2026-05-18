/**
 * Hover-press micro-interaction primitive. Three preset modes that match
 * the recipes in §2.2.1 / 2.2.2 / 2.2.3 of the motion plan:
 *
 *   mode='button'  scale 1 → 1.02 on enter, scale 0.97 on press
 *   mode='card'    y 0 → -4 lift on enter, scale 0.99 on press
 *   mode='link'    inner indicator scaleX 0 → 1 (origin left) — used for
 *                  nav-link underlines. Pass `indicator` option to target
 *                  a child element instead of the link itself.
 *
 * Touch devices skip the hover path entirely (matchMedia '(hover: none)'),
 * but press still runs so taps still get tactile feedback. Reduced-motion
 * bypasses tweens but leaves the element fully interactive.
 */
import { onMounted, onBeforeUnmount } from 'vue'
import { gsap } from 'gsap'
import { ensurePlugins } from '../registry'
import { isReduced, isTouch } from '../matchMedia'
import { DUR, EASE } from '../tokens'

export function useHover(elRef, options = {}) {
  const {
    mode = 'button',
    scaleEnter = mode === 'button' ? 1.02 : 1,
    yEnter = mode === 'card' ? -4 : 0,
    scalePress = mode === 'card' ? 0.99 : 0.97,
    indicator = null,
  } = options

  ensurePlugins()

  let cleanup = null

  onMounted(() => {
    const el = elRef?.value
    if (!el) return
    if (isReduced()) return

    const indicatorEl = mode === 'link' && indicator
      ? el.querySelector(indicator)
      : null
    if (indicatorEl) {
      gsap.set(indicatorEl, { scaleX: 0, transformOrigin: '0 50%' })
    }

    const enter = () => {
      if (isTouch()) return
      if (indicatorEl) {
        gsap.to(indicatorEl, { scaleX: 1, duration: DUR.hover, ease: 'power2.out' })
        return
      }
      gsap.to(el, {
        scale: scaleEnter,
        y: yEnter,
        duration: DUR.hover,
        ease: EASE.entrance,
      })
    }

    const leave = () => {
      if (isTouch()) return
      if (indicatorEl) {
        gsap.to(indicatorEl, { scaleX: 0, duration: DUR.hover, ease: 'power2.out' })
        return
      }
      gsap.to(el, { scale: 1, y: 0, duration: DUR.hover, ease: EASE.entrance })
    }

    const press = () => {
      if (indicatorEl) return
      gsap.to(el, { scale: scalePress, duration: DUR.press / 2 / 1000, ease: EASE.spring })
    }

    const release = () => {
      if (indicatorEl) return
      // Restore to the hover-end state if pointer is still over the element,
      // otherwise back to identity. Cheap heuristic: pointermove after the
      // press will overwrite this anyway, so always go to hover-end first.
      gsap.to(el, { scale: scaleEnter, duration: DUR.press / 1000, ease: EASE.spring })
    }

    el.addEventListener('pointerenter', enter)
    el.addEventListener('pointerleave', leave)
    el.addEventListener('pointerdown', press)
    el.addEventListener('pointerup', release)
    el.addEventListener('pointercancel', release)

    cleanup = () => {
      el.removeEventListener('pointerenter', enter)
      el.removeEventListener('pointerleave', leave)
      el.removeEventListener('pointerdown', press)
      el.removeEventListener('pointerup', release)
      el.removeEventListener('pointercancel', release)
      gsap.set(el, { clearProps: 'transform' })
      if (indicatorEl) gsap.set(indicatorEl, { clearProps: 'transform' })
    }
  })

  onBeforeUnmount(() => cleanup?.())
}
