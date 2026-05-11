/**
 * Accordion / collapsible primitive. Uses the `grid-template-rows` trick
 * (0fr ↔ 1fr) to animate variable-height content without ever animating
 * `height` directly — no layout thrashing, no manual height calculation.
 *
 * The wrapper element must use grid layout with one row that animates;
 * the content element is the only child of that row. Container CSS:
 *
 *   .accordion { display: grid; grid-template-rows: 0fr; transition: ... }
 *   .accordion > * { overflow: hidden; }
 *
 * useAccordion swaps the grid-template-rows between '0fr' and '1fr' and
 * fades the inner content. Works on any block-level wrapper.
 */
import { watch } from 'vue'
import { gsap } from 'gsap'
import { ensurePlugins } from '../registry'
import { isReduced } from '../matchMedia'
import { EASE } from '../tokens'

export function useAccordion(isOpen, wrapperRef, options = {}) {
  const {
    contentSelector = ':scope > *',
    enterDuration = 0.3,
    leaveDuration = 0.22,
  } = options

  ensurePlugins()

  watch(isOpen, (value) => {
    const wrapper = wrapperRef?.value
    if (!wrapper) return
    const content = wrapper.querySelector(contentSelector)

    if (isReduced()) {
      wrapper.style.gridTemplateRows = value ? '1fr' : '0fr'
      if (content) content.style.opacity = value ? '1' : '0'
      return
    }

    if (value) {
      gsap.to(wrapper, {
        gridTemplateRows: '1fr',
        duration: enterDuration,
        ease: 'power2.inOut',
      })
      if (content) {
        gsap.fromTo(content,
          { opacity: 0 },
          { opacity: 1, duration: enterDuration * 0.8, delay: enterDuration * 0.2, ease: EASE.entrance },
        )
      }
    } else {
      if (content) {
        gsap.to(content, { opacity: 0, duration: leaveDuration * 0.5, ease: 'power2.in' })
      }
      gsap.to(wrapper, {
        gridTemplateRows: '0fr',
        duration: leaveDuration,
        ease: 'power2.inOut',
      })
    }
  }, { immediate: false })
}
