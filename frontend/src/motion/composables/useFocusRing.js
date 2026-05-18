/**
 * Focus-visible ring primitive. Renders an animated box-shadow ring when
 * the element receives keyboard focus (via :focus-visible), then fades it
 * out on blur. Pointer focus (clicking a button) does not trigger the
 * ring — the browser's :focus-visible heuristic decides.
 *
 * style.css already ships a generic :focus-visible outline rule, so
 * useFocusRing is for components that want a tinted/animated ring instead
 * of the default 2px outline (CTA buttons, leaderboard cards, form
 * inputs with rounded borders that look bad with offset outlines).
 */
import { onMounted, onBeforeUnmount } from 'vue'
import { gsap } from 'gsap'
import { ensurePlugins } from '../registry'
import { isReduced } from '../matchMedia'
import { DUR, EASE } from '../tokens'

export function useFocusRing(elRef, options = {}) {
  const {
    color = 'var(--color-primary-text)',
    ringWidth = 2,
    offset = 3,
  } = options

  ensurePlugins()

  let cleanup = null

  onMounted(() => {
    const el = elRef?.value
    if (!el) return

    const on = () => {
      // matches(':focus-visible') filters out pointer-initiated focus.
      if (!el.matches(':focus-visible')) return
      if (isReduced()) {
        el.style.boxShadow = `0 0 0 ${offset}px transparent, 0 0 0 ${offset + ringWidth}px ${color}`
        return
      }
      gsap.fromTo(
        el,
        { boxShadow: `0 0 0 ${offset}px transparent, 0 0 0 ${offset}px transparent` },
        {
          boxShadow: `0 0 0 ${offset}px transparent, 0 0 0 ${offset + ringWidth}px ${color}`,
          duration: DUR.hover,
          ease: EASE.entrance,
          overwrite: 'auto',
        },
      )
    }

    const off = () => {
      if (isReduced()) {
        el.style.boxShadow = ''
        return
      }
      gsap.to(el, {
        boxShadow: `0 0 0 ${offset}px transparent, 0 0 0 ${offset}px transparent`,
        duration: DUR.hover * 0.7,
        ease: 'power2.in',
        overwrite: 'auto',
        onComplete: () => { el.style.boxShadow = '' },
      })
    }

    el.addEventListener('focus', on)
    el.addEventListener('blur', off)

    cleanup = () => {
      el.removeEventListener('focus', on)
      el.removeEventListener('blur', off)
      el.style.boxShadow = ''
    }
  })

  onBeforeUnmount(() => cleanup?.())
}
