/**
 * Filter chip add/remove primitive. Returns enter/exit functions for
 * spring-based scale + opacity animation. Call enter() after adding a
 * chip's DOM node (e.g. in nextTick), exit(node, onDone) before
 * removing.
 *
 *   const { enterChip, exitChip } = useChip()
 *   function addTag(tag) {
 *     tags.value.push(tag)
 *     nextTick(() => enterChip(chipRefs.value.at(-1)))
 *   }
 *   function removeTag(idx) {
 *     exitChip(chipRefs.value[idx], () => tags.value.splice(idx, 1))
 *   }
 */
import { gsap } from 'gsap'
import { ensurePlugins } from '../registry'
import { isReduced } from '../matchMedia'
import { EASE } from '../tokens'

export function useChip(options = {}) {
  const {
    enterDuration = 0.25,
    exitDuration = 0.18,
  } = options

  ensurePlugins()

  function enterChip(el) {
    if (!el) return
    if (isReduced()) {
      gsap.set(el, { opacity: 1, scale: 1 })
      return
    }
    gsap.fromTo(el,
      { opacity: 0, scale: 0.8 },
      { opacity: 1, scale: 1, duration: enterDuration, ease: EASE.spring },
    )
  }

  function exitChip(el, onDone) {
    if (!el) {
      onDone?.()
      return
    }
    if (isReduced()) {
      onDone?.()
      return
    }
    gsap.to(el, {
      opacity: 0,
      scale: 0.8,
      duration: exitDuration,
      ease: 'power2.in',
      onComplete: () => onDone?.(),
    })
  }

  return { enterChip, exitChip }
}
