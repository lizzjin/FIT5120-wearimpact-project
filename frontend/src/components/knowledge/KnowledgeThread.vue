<template>
  <svg
    ref="svgRef"
    class="kh-thread"
    viewBox="0 0 100 100"
    preserveAspectRatio="none"
    aria-hidden="true"
  >
    <path
      ref="basePathRef"
      class="kh-thread__base"
      :d="pathD"
      pathLength="1"
      fill="none"
    />
    <path
      v-for="(_, i) in pulseSlots"
      :key="`pulse-${i}`"
      :ref="(el) => (pulsePathRefs[i] = el)"
      class="kh-thread__pulse"
      :d="pathD"
      pathLength="1"
      fill="none"
      stroke="transparent"
    />
  </svg>
</template>

<script setup>
import { inject, onBeforeUnmount, onMounted, ref } from 'vue'

// Path is normalized inside a 100×100 viewBox; preserveAspectRatio="none"
// stretches it to the full document height of the .knowledge-page wrapper.
// S-curve hand-tuned to roughly weave near each section centroid.
const pathD =
  'M 18 4 ' +
  'C 5 12, 92 18, 76 26 ' +
  'C 60 34, 12 42, 30 50 ' +
  'C 46 58, 92 62, 70 70 ' +
  'C 48 78, 14 82, 32 90 ' +
  'C 50 96, 72 98, 64 100'

const svgRef = ref(null)
const basePathRef = ref(null)
const pulseSlots = [0, 1, 2]
const pulsePathRefs = ref([null, null, null])
let nextPulseSlot = 0

let rafId = null
let gsapLib = null
const unsubscribers = []

function prefersReducedMotion() {
  return (
    typeof window !== 'undefined' &&
    window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches
  )
}

function updateScrollProgress() {
  const docH = Math.max(
    document.documentElement.scrollHeight,
    document.body?.scrollHeight ?? 0,
    window.innerHeight,
  )
  const max = Math.max(1, docH - window.innerHeight)
  const progress = Math.min(1, Math.max(0, window.scrollY / max))
  if (basePathRef.value) {
    basePathRef.value.style.strokeDashoffset = String(1 - progress)
  }
}

function onScroll() {
  if (rafId != null) return
  rafId = requestAnimationFrame(() => {
    rafId = null
    updateScrollProgress()
  })
}

function pulse(strokeColor, glowColor, durationMs = 850) {
  if (prefersReducedMotion() || !gsapLib) return
  const slot = nextPulseSlot
  nextPulseSlot = (nextPulseSlot + 1) % pulsePathRefs.value.length
  const path = pulsePathRefs.value[slot]
  if (!path) return

  path.style.strokeDasharray = '0.05 1'
  path.setAttribute('stroke', strokeColor)
  path.style.filter = `drop-shadow(0 0 6px ${glowColor})`
  gsapLib.killTweensOf(path)
  gsapLib.fromTo(
    path,
    { strokeDashoffset: 1 },
    {
      strokeDashoffset: -0.05,
      duration: durationMs / 1000,
      ease: 'power1.inOut',
      onComplete: () => path.setAttribute('stroke', 'transparent'),
    },
  )
}

const bus = inject('quizBus', null)

onMounted(async () => {
  updateScrollProgress()
  window.addEventListener('scroll', onScroll, { passive: true })
  window.addEventListener('resize', updateScrollProgress, { passive: true })

  try {
    const mod = await import('gsap')
    gsapLib = mod.gsap ?? mod.default ?? mod
  } catch {
    gsapLib = null
  }

  if (bus) {
    unsubscribers.push(
      bus.on('pick:correct', () =>
        pulse('var(--color-kh-pulse-correct)', 'rgba(159,232,112,0.55)', 850),
      ),
    )
    unsubscribers.push(
      bus.on('pick:wrong', () =>
        pulse('var(--color-kh-pulse-wrong)', 'rgba(255,192,145,0.55)', 900),
      ),
    )
    unsubscribers.push(
      bus.on('advance', () =>
        pulse('var(--color-kh-pulse-neutral)', 'rgba(226,246,213,0.5)', 1100),
      ),
    )
  }
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', onScroll)
  window.removeEventListener('resize', updateScrollProgress)
  if (rafId != null) cancelAnimationFrame(rafId)
  unsubscribers.forEach((u) => u && u())
})
</script>

<style scoped>
.kh-thread {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
  overflow: visible;
}

.kh-thread__base {
  stroke: var(--color-kh-accent);
  stroke-width: 1.4;
  stroke-linecap: round;
  vector-effect: non-scaling-stroke;
  filter: drop-shadow(0 0 6px var(--color-kh-glow-blue));
  stroke-dasharray: 1;
  opacity: 0.75;
}

.kh-thread__pulse {
  stroke-width: 2.4;
  stroke-linecap: round;
  vector-effect: non-scaling-stroke;
  stroke-dasharray: 0.05 1;
  stroke-dashoffset: 1;
}
</style>
