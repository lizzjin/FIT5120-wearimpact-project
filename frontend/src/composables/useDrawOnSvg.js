/**
 * useDrawOnSvg — animate inline SVG paths via stroke-dasharray draw-on.
 *
 * The motion vocabulary forbids fade-in for illustrations (see
 * openspec/changes/wise-aesthetic-redesign/specs/motion-vocabulary/spec.md).
 * Illustrations enter by drawing their outline from 0 → full length over
 * ~850ms with cubic-bezier(0.65, 0, 0.35, 1).
 *
 * Usage:
 *   const svgRef = ref(null)
 *   const { play, reset } = useDrawOnSvg(svgRef, { duration: 850 })
 *   onMounted(() => play())
 *
 * `play()` sets dashoffset to the path length (invisible) then animates to 0.
 * IntersectionObserver-based auto-play is opt-in via { auto: true }.
 */
import { onBeforeUnmount, onMounted, watch } from 'vue'

const DEFAULT_DURATION = 850
const DEFAULT_EASING = 'cubic-bezier(0.65, 0, 0.35, 1)'

export function useDrawOnSvg(targetRef, options = {}) {
  const {
    duration = DEFAULT_DURATION,
    easing = DEFAULT_EASING,
    delay = 0,
    auto = false,             // auto-play on mount
    observe = false,          // auto-play when scrolled into view
    rootMargin = '-10%',
  } = options

  let observer = null

  function getPaths() {
    const svg = targetRef.value
    if (!svg) return []
    // Animate every drawn primitive — paths, lines, polylines, polygons, circles, rects
    return svg.querySelectorAll('path, line, polyline, polygon, circle, rect, ellipse')
  }

  /** Reset every path to invisible (dashoffset = full length). */
  function reset() {
    getPaths().forEach((el) => {
      // getTotalLength works for path/line/polyline/polygon/circle/ellipse;
      // for rect we approximate with bounding-box perimeter.
      const len = computeLength(el)
      el.style.transition = 'none'
      el.style.strokeDasharray = String(len)
      el.style.strokeDashoffset = String(len)
    })
    // Force reflow so the next transition starts from the reset state.
    void targetRef.value?.getBoundingClientRect()
  }

  /** Animate every path from invisible → drawn. */
  function play() {
    getPaths().forEach((el, i) => {
      const len = computeLength(el)
      el.style.strokeDasharray = String(len)
      el.style.strokeDashoffset = String(len)
      // One frame later, transition to 0 so the browser registers the start state.
      requestAnimationFrame(() => {
        el.style.transition = `stroke-dashoffset ${duration}ms ${easing} ${delay + i * 30}ms`
        el.style.strokeDashoffset = '0'
      })
    })
  }

  /** Compute path length, falling back to bounding-box perimeter for rects. */
  function computeLength(el) {
    if (typeof el.getTotalLength === 'function') {
      try {
        return el.getTotalLength() || 0
      } catch {
        // fall through
      }
    }
    const box = el.getBBox?.()
    return box ? 2 * (box.width + box.height) : 0
  }

  function setupObserver() {
    if (!observe || !targetRef.value || typeof IntersectionObserver === 'undefined') return
    observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            play()
            observer?.disconnect()
            observer = null
            break
          }
        }
      },
      { rootMargin },
    )
    observer.observe(targetRef.value)
  }

  onMounted(() => {
    // Honor prefers-reduced-motion: skip the entrance animation entirely,
    // leaving the SVG fully drawn at rest.
    if (window.matchMedia?.('(prefers-reduced-motion: reduce)').matches) return

    if (auto) {
      reset()
      requestAnimationFrame(() => play())
    } else if (observe) {
      reset()
      setupObserver()
    }
  })

  onBeforeUnmount(() => {
    observer?.disconnect()
    observer = null
  })

  // Re-bind observer if the ref's element changes after mount.
  watch(targetRef, (el) => {
    if (observe && el) setupObserver()
  })

  return { play, reset }
}
