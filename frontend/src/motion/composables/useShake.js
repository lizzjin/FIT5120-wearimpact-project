/**
 * Error-shake primitive. Triggers a horizontal ±4px shake for ~0.4s.
 * Imperative — return { shake } and callers invoke it after validation
 * failure or any other "no, try again" moment.
 *
 *   const passwordRef = ref(null)
 *   const { shake } = useShake(passwordRef)
 *   function submit() {
 *     if (!isValid.value) { shake(); return }
 *     ...
 *   }
 */
import { gsap } from 'gsap'
import { ensurePlugins } from '../registry'
import { isReduced } from '../matchMedia'

export function useShake(elRef) {
  ensurePlugins()

  function shake() {
    const el = elRef?.value
    if (!el || isReduced()) return
    gsap.fromTo(
      el,
      { x: -4 },
      {
        x: 4,
        duration: 0.08,
        repeat: 5,
        yoyo: true,
        ease: 'power1.inOut',
        overwrite: 'auto',
        onComplete: () => gsap.set(el, { x: 0 }),
      },
    )
  }

  return { shake }
}
