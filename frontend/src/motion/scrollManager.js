/**
 * ScrollTrigger lifecycle controller — the single entry point for refresh
 * calls. Replaces the four scattered ScrollTrigger.refresh() sites that
 * existed before this refactor (three in App.vue, one in HomeView.vue).
 *
 * The two public hooks:
 *
 *   armScrollTriggers()  — call once after the first route is mounted.
 *     Wires deferred refreshes so triggers do not bind to stale layout:
 *       1. document.fonts.ready  (SplitText measures real font metrics)
 *       2. window 'load'         (last images / iframes settle)
 *       3. requestIdleCallback   (Lottie or other heavy mounts)
 *
 *   onRouteSettled()     — call from the router's after-enter hook so
 *     newly mounted views recompute trigger positions against their own
 *     layout instead of the outgoing page's.
 */
import { ScrollTrigger, ensurePlugins } from './registry'

let armed = false

function refreshOnIdle() {
  if (typeof window === 'undefined') return
  if (typeof window.requestIdleCallback === 'function') {
    window.requestIdleCallback(() => ScrollTrigger.refresh())
  } else {
    setTimeout(() => ScrollTrigger.refresh(), 0)
  }
}

export function armScrollTriggers() {
  ensurePlugins()
  if (typeof window === 'undefined') return

  if (typeof document !== 'undefined' && document.fonts?.ready) {
    document.fonts.ready
      .then(() => ScrollTrigger.refresh())
      .catch(() => {})
  }

  if (!armed) {
    window.addEventListener('load', () => ScrollTrigger.refresh(), { once: true })
    armed = true
  }

  refreshOnIdle()
}

export function onRouteSettled() {
  ensurePlugins()
  ScrollTrigger.refresh()
}

export function refreshNow() {
  ensurePlugins()
  ScrollTrigger.refresh()
}

export { ScrollTrigger }
