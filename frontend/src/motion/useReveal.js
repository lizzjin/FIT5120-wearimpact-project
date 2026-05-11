/**
 * Section reveal composable. Drives one section's enter animation; chosen
 * by the `mode` option:
 *
 *   mode='char'      — eyebrow / tag: per-character fade stagger.
 *   mode='word'      — heading word-mask rise (yPercent: 110 → 0).
 *   mode='inline'    — heading containing <strong>/<em>/<span>/<br>;
 *                      SplitText preserves inline markup natively.
 *   mode='fade-up'   — generic block: y:28 + opacity 0 → 1.
 *   mode='fade-blur' — paragraph: y:60 + filter blur(8px) → 0.
 *
 * Set `replay: true` to reset on leave-back and re-play each time the
 * user scrolls into the element again.
 *
 * Phase 2 rewrite: the underlying text splitting now uses the official
 * GSAP SplitText plugin via `splitElement`. Easings and durations read
 * from the shared motion tokens so a CSS-token tweak propagates here.
 */
import { onMounted, onBeforeUnmount } from 'vue'
import { gsap } from 'gsap'
import { ScrollTrigger, ensurePlugins } from './registry'
import { isReduced } from './matchMedia'
import { DUR, EASE, STAGGER, Y, entrance, entranceLg } from './tokens'
import { splitElement } from './composables/useTextSplit'

export function useReveal(elRef, options = {}) {
  const {
    mode = 'fade-up',
    start = 'top 82%',
    stagger,
    duration,
    y = Y.body,
    delay = 0,
    replay = false,
    ease = EASE.entrance,
  } = options

  ensurePlugins()

  let trigger = null
  let targets = null
  let initialState = null
  let animatedState = null
  let originalFilter = ''
  let revertSplit = () => {}

  onMounted(() => {
    const el = elRef?.value
    if (!el) return

    if (isReduced()) {
      el.style.opacity = '1'
      return
    }

    if (mode === 'word') {
      const split = splitElement(el, { type: 'words', mask: 'words' })
      revertSplit = split.revert
      if (!split.words.length) return
      targets = split.words
      initialState = { yPercent: 110 }
      animatedState = {
        yPercent: 0,
        duration: duration ?? DUR.entranceLg,
        stagger: stagger ?? 0.07,
        delay,
        ease,
      }
    } else if (mode === 'inline') {
      // SplitText handles inline markup (<strong>, <em>, <br>) natively,
      // so the same word-mask config works for headings with mixed inline
      // content as it does for plain strings.
      const split = splitElement(el, { type: 'words', mask: 'words' })
      revertSplit = split.revert
      if (!split.words.length) return
      targets = split.words
      initialState = { yPercent: 110 }
      animatedState = {
        yPercent: 0,
        duration: duration ?? DUR.entranceLg,
        stagger: stagger ?? 0.07,
        delay,
        ease,
      }
    } else if (mode === 'char') {
      const split = splitElement(el, { type: 'chars, words' })
      revertSplit = split.revert
      if (!split.chars.length) return
      targets = split.chars
      initialState = { opacity: 0, y: 12 }
      animatedState = {
        opacity: 1,
        y: 0,
        duration: duration ?? 0.5,
        stagger: stagger ?? STAGGER.char,
        delay,
        ease,
      }
    } else if (mode === 'fade-blur') {
      targets = [el]
      originalFilter = el.style.filter || ''
      initialState = { opacity: 0, y: y || Y.heading, filter: 'blur(8px)' }
      animatedState = {
        opacity: 1,
        y: 0,
        filter: 'blur(0px)',
        duration: duration ?? DUR.entrance,
        delay,
        ease,
      }
    } else {
      targets = [el]
      initialState = { opacity: 0, y }
      animatedState = {
        opacity: 1,
        y: 0,
        duration: duration ?? DUR.entrance,
        stagger: stagger ?? STAGGER.list,
        delay,
        ease,
      }
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
    revertSplit()
    const el = elRef?.value
    if (el && originalFilter !== '') el.style.filter = originalFilter
  })
}

// Re-exports keep backward-compatible imports (some components import
// these names from this file rather than from the motion barrel).
export { entrance, entranceLg, DUR, EASE, STAGGER, Y }
