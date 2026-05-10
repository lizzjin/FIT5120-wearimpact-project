/**
 * Vue composable that drives one section's enter animation. Modelled on
 * shelby.ashfall.studio's "section-intro" contract:
 *
 *   mode='char'      — eyebrow / tag: per-character fade stagger.
 *   mode='word'      — heading word-mask rise (yPercent: 110 → 0).
 *   mode='inline'    — heading containing <strong>/<em>/<span>/<br>;
 *                      preserves inline markup.
 *   mode='fade-up'   — generic block: y:28 + opacity 0 → 1.
 *   mode='fade-blur' — paragraph: y:60 + filter blur(8px) → 0.
 *
 * Set `replay: true` so the animation reverses on leave-back and re-plays
 * each time the user scrolls into the element again — matches Shelby's
 * "every section enters fresh" feel.
 */
import { onMounted, onBeforeUnmount } from 'vue'
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { splitText, splitInlineHTML, revert, prefersReducedMotion } from './splitText'

export function useReveal(elRef, options = {}) {
  const {
    mode = 'fade-up',
    start = 'top 82%',
    stagger = 0.06,
    duration = 0.9,
    y = 28,
    delay = 0,
    replay = false,
    ease = 'power3.out',
  } = options

  let trigger = null
  let targets = null
  let initialState = null
  let animatedState = null
  let originalFilter = ''

  onMounted(() => {
    const el = elRef?.value
    if (!el) return

    if (prefersReducedMotion()) {
      el.style.opacity = '1'
      return
    }

    if (mode === 'word') {
      const { inners } = splitText(el, 'word')
      if (!inners.length) return
      targets = inners
      initialState = { yPercent: 110 }
      animatedState = { yPercent: 0, duration, stagger, delay, ease }
    } else if (mode === 'inline') {
      const { inners } = splitInlineHTML(el)
      if (!inners.length) return
      targets = inners
      initialState = { yPercent: 110 }
      animatedState = { yPercent: 0, duration, stagger, delay, ease }
    } else if (mode === 'char') {
      const { chars } = splitText(el, 'char')
      if (!chars.length) return
      targets = chars
      initialState = { opacity: 0, y: 12 }
      animatedState = { opacity: 1, y: 0, duration: duration || 0.5, stagger, delay, ease }
    } else if (mode === 'fade-blur') {
      targets = [el]
      originalFilter = el.style.filter || ''
      initialState = { opacity: 0, y: y || 60, filter: 'blur(8px)' }
      animatedState = { opacity: 1, y: 0, filter: 'blur(0px)', duration, delay, ease }
    } else {
      targets = [el]
      initialState = { opacity: 0, y }
      animatedState = { opacity: 1, y: 0, duration, stagger, delay, ease }
    }

    gsap.set(targets, initialState)

    const play = () => gsap.to(targets, animatedState)
    const reset = () => gsap.set(targets, initialState)

    trigger = ScrollTrigger.create({
      trigger: el,
      start,
      once: !replay,
      onEnter: play,
      onEnterBack: replay ? play : undefined,
      onLeave: replay ? reset : undefined,
      onLeaveBack: replay ? reset : undefined,
    })
  })

  onBeforeUnmount(() => {
    trigger?.kill?.()
    const el = elRef?.value
    if (el?.dataset?.split) revert(el)
    if (el && originalFilter !== '') el.style.filter = originalFilter
  })
}
