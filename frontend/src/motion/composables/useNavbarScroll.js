/**
 * Navbar scroll-state primitive. Toggles a `is-scrolled` class on the
 * nav element when the page is scrolled past a threshold, and drives
 * the bg-opacity + shadow transition via CSS (cheaper than animating
 * those properties in JS).
 *
 *   const navRef = ref(null)
 *   useNavbarScroll(navRef, { threshold: 40 })
 *
 * The CSS rule that responds to .is-scrolled is the parent's
 * responsibility; this composable only owns the class toggle.
 */
import { onMounted, onBeforeUnmount } from 'vue'
import { ScrollTrigger, ensurePlugins } from '../registry'

export function useNavbarScroll(navRef, options = {}) {
  const {
    threshold = 40,
    activeClass = 'is-scrolled',
  } = options

  ensurePlugins()

  let trigger = null

  onMounted(() => {
    const nav = navRef?.value
    if (!nav) return

    trigger = ScrollTrigger.create({
      start: threshold,
      end: 'max',
      onEnter: () => nav.classList.add(activeClass),
      onLeaveBack: () => nav.classList.remove(activeClass),
    })
  })

  onBeforeUnmount(() => {
    trigger?.kill?.()
  })
}
