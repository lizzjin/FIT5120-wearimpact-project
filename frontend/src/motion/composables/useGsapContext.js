/**
 * Vue composable that owns a gsap.context() for a component subtree.
 *
 * Any tween or ScrollTrigger created inside setupFn is scoped to the
 * rootRef element and reverted automatically when the component unmounts.
 * This replaces the `triggers.push(...) / triggers.forEach(kill)` pattern
 * that previously lived in HomeView, KnowledgeLifecycle, and FloorRail.
 *
 *   const root = ref(null)
 *   useGsapContext(root, (ctx) => {
 *     gsap.from('.card', { y: 24, opacity: 0, stagger: 0.06 })
 *     ScrollTrigger.create({ trigger: '.hero', start: 'top top', ... })
 *   })
 */
import { onBeforeUnmount, onMounted } from 'vue'
import { gsap } from 'gsap'
import { ensurePlugins } from '../registry'

export function useGsapContext(rootRef, setupFn) {
  ensurePlugins()
  let ctx = null

  onMounted(() => {
    const scope = rootRef?.value
    if (!scope) return
    ctx = gsap.context(setupFn, scope)
  })

  onBeforeUnmount(() => {
    ctx?.revert()
    ctx = null
  })

  return {
    rebuild() {
      ctx?.revert()
      const scope = rootRef?.value
      if (!scope) return
      ctx = gsap.context(setupFn, scope)
    },
    revert() {
      ctx?.revert()
      ctx = null
    },
  }
}
