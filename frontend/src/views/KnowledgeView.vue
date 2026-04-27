<template>
  <div class="knowledge-page">
    <QuizBackground />

    <div
      class="kh-edge-flash"
      :class="{ 'kh-edge-flash--active': edgeFlashActive }"
      :style="{ '--kh-edge-color': edgeFlashColor }"
      aria-hidden="true"
    >
      <span class="kh-edge-flash__bar kh-edge-flash__bar--top"></span>
      <span class="kh-edge-flash__bar kh-edge-flash__bar--bottom"></span>
    </div>

    <Navbar />

    <main class="knowledge-page__main">
      <QuizHero />
      <QuizFlow @complete="onQuizComplete" />
      <QuizSummary v-if="answers.length > 0" :answers="answers" />
      <WardrobeAdvisorTeaser />
    </main>

    <!-- Page section rail — tracks the user's vertical position through
         the page (Intro → Quiz → Result → Next), not quiz progress. The
         Result dot only appears once the quiz has been completed. -->
    <aside class="page-rail" aria-label="Page sections">
      <button
        v-for="s in visibleSections"
        :key="s.id"
        type="button"
        class="page-rail__dot"
        :class="{ 'page-rail__dot--active': activeSection === s.id }"
        @click="jumpToSection(s.id)"
      >
        <span class="page-rail__num" aria-hidden="true">{{ s.num }}</span>
        <span class="page-rail__core" aria-hidden="true" />
        <span class="page-rail__label">{{ s.label }}</span>
      </button>
    </aside>

    <!-- Shared floor rail — same SVG flow used on Home, footer-aware. -->
    <div class="floor-rail" aria-hidden="true">
      <svg class="floor-rail__wave" viewBox="0 0 1440 24" preserveAspectRatio="none">
        <path
          d="M 0 12 Q 60 2 120 12 T 240 12 T 360 12 T 480 12 T 600 12 T 720 12 T 840 12 T 960 12 T 1080 12 T 1200 12 T 1320 12 T 1440 12"
          stroke="#9fe870"
          stroke-width="2"
          fill="none"
          stroke-linecap="round"
          opacity="0.7"
        />
      </svg>
      <div class="floor-flow">
        <img
          v-for="(src, i) in floorIcons"
          :key="i"
          :src="src"
          class="floor-item"
          :style="{ '--i': i }"
          alt=""
          aria-hidden="true"
        />
      </div>
    </div>

    <FooterSection />
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, provide, ref } from 'vue'
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import Navbar from '../components/Navbar.vue'
import FooterSection from '../components/FooterSection.vue'
import QuizBackground from '../components/knowledge/QuizBackground.vue'
import QuizHero from '../components/knowledge/QuizHero.vue'
import QuizFlow from '../components/knowledge/QuizFlow.vue'
import QuizSummary from '../components/knowledge/QuizSummary.vue'
import WardrobeAdvisorTeaser from '../components/knowledge/WardrobeAdvisorTeaser.vue'

import floorClothing from '../assets/illustrations/floor-clothing.svg'
import floorHandbag from '../assets/illustrations/floor-handbag.svg'
import floorLeaf from '../assets/illustrations/floor-leaf.svg'
import floorLightBulb from '../assets/illustrations/floor-light-bulb.svg'
import floorRecycle from '../assets/illustrations/floor-recycle.svg'
import floorShoes from '../assets/illustrations/floor-shoes.svg'
import floorTag from '../assets/illustrations/floor-tag.svg'

gsap.registerPlugin(ScrollTrigger)

const floorIcons = [
  floorClothing,
  floorTag,
  floorLeaf,
  floorHandbag,
  floorRecycle,
  floorShoes,
  floorLightBulb,
]

const answers = ref([])
const triggers = []
let scrollLockAttached = false

// Page section rail — IntersectionObserver picks the section closest to
// viewport center as active. Result dot appears once the quiz completes.
const PAGE_SECTIONS = [
  { id: 'quiz-hero', num: '01', label: 'Intro' },
  { id: 'quiz-flow', num: '02', label: 'Quiz' },
  { id: 'quiz-summary', num: '03', label: 'Result', requiresAnswers: true },
  { id: 'wardrobe-teaser', num: '04', label: 'Next' },
]
const activeSection = ref('quiz-hero')
const visibleSections = computed(() =>
  PAGE_SECTIONS.filter((s) => !s.requiresAnswers || answers.value.length > 0)
    .map((s, i) => ({ ...s, num: String(i + 1).padStart(2, '0') })),
)
let sectionObserver = null

function jumpToSection(id) {
  const el = document.getElementById(id)
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

// Page-level scroll lock — engaged on mount, fully detached on quiz
// completion. preventDefault on wheel/touch/keys blocks user-initiated
// scroll while leaving programmatic scrollIntoView free.
//
// CRITICAL: we DETACH these listeners on unlock rather than just no-op.
// A non-passive wheel listener (even one that does nothing) forces the
// browser to wait for it before processing each scroll tick — that's
// what was making post-quiz scrolling feel choppy.
function preventScroll(e) { e.preventDefault() }
function preventKeyScroll(e) {
  const blocked = ['ArrowUp', 'ArrowDown', 'PageUp', 'PageDown', 'Home', 'End', ' ', 'Spacebar']
  if (blocked.includes(e.key)) e.preventDefault()
}

function attachScrollLock() {
  if (scrollLockAttached) return
  window.addEventListener('wheel', preventScroll, { passive: false })
  window.addEventListener('touchmove', preventScroll, { passive: false })
  window.addEventListener('keydown', preventKeyScroll, { passive: false })
  scrollLockAttached = true
}

function detachScrollLock() {
  if (!scrollLockAttached) return
  window.removeEventListener('wheel', preventScroll)
  window.removeEventListener('touchmove', preventScroll)
  window.removeEventListener('keydown', preventKeyScroll)
  scrollLockAttached = false
}

const edgeFlashActive = ref(false)
const edgeFlashColor = ref('var(--color-kh-pulse-correct)')
let flashTimer = null

function flashEdges(color) {
  if (window.matchMedia?.('(prefers-reduced-motion: reduce)').matches) return
  edgeFlashColor.value = color
  edgeFlashActive.value = true
  if (flashTimer) clearTimeout(flashTimer)
  flashTimer = setTimeout(() => {
    edgeFlashActive.value = false
  }, 200)
}

const handlers = new Map()
const bus = {
  emit(event, payload) {
    const set = handlers.get(event)
    if (set) set.forEach((h) => h(payload))
  },
  on(event, fn) {
    if (!handlers.has(event)) handlers.set(event, new Set())
    handlers.get(event).add(fn)
    return () => handlers.get(event)?.delete(fn)
  },
}
provide('quizBus', bus)

const unsubscribers = []

function onQuizComplete(finalAnswers) {
  answers.value = finalAnswers
  // Quiz finished — fully detach the scroll lock listeners so post-quiz
  // scrolling has no per-tick handler overhead. Auto-scroll to summary.
  detachScrollLock()
  requestAnimationFrame(() => {
    const el = document.getElementById('quiz-summary')
    if (el) {
      // Summary only mounts after the quiz completes — observe it now so
      // the page rail's Result dot tracks scroll position correctly.
      sectionObserver?.observe(el)
      el.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  })
}

onMounted(() => {
  attachScrollLock()
  // Always start at the hero on /knowledge entry.
  window.scrollTo({ top: 0, behavior: 'instant' })

  unsubscribers.push(
    bus.on('pick:correct', () => flashEdges('var(--color-kh-pulse-correct)')),
  )
  unsubscribers.push(
    bus.on('pick:wrong', () => flashEdges('var(--color-kh-pulse-wrong)')),
  )

  // Footer fade for floor rail (mirrors HomeView).
  const railEl = document.querySelector('.knowledge-page .floor-rail')
  const footerEl = document.querySelector('.knowledge-page footer')
  const prefersReduced = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches
  if (footerEl && railEl && !prefersReduced) {
    const updateRail = () => {
      const vh = window.innerHeight
      const footerTop = footerEl.getBoundingClientRect().top
      const fadeStart = vh * 0.95
      const fadeEnd   = vh * 0.7
      let railOpacity
      if (footerTop >= fadeStart)      railOpacity = 1
      else if (footerTop <= fadeEnd)   railOpacity = 0
      else                             railOpacity = (footerTop - fadeEnd) / (fadeStart - fadeEnd)
      gsap.set(railEl, { opacity: railOpacity, y: 150 * (1 - railOpacity) })
    }
    const t = ScrollTrigger.create({
      start: 0,
      end: 'max',
      onUpdate: updateRail,
      onRefresh: updateRail,
    })
    triggers.push(t)
    updateRail()
  }

  // Track which page section the user is currently looking at. The
  // intersection root margin keeps the active dot in sync with viewport
  // center rather than the very top of the section.
  const ids = ['quiz-hero', 'quiz-flow', 'quiz-summary', 'wardrobe-teaser']
  const visibility = new Map(ids.map((id) => [id, 0]))
  sectionObserver = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        visibility.set(entry.target.id, entry.intersectionRatio)
      }
      let bestId = activeSection.value
      let bestRatio = -1
      for (const [id, ratio] of visibility) {
        if (ratio > bestRatio) {
          bestRatio = ratio
          bestId = id
        }
      }
      if (bestRatio > 0) activeSection.value = bestId
    },
    { threshold: [0.15, 0.4, 0.65, 0.9], rootMargin: '-20% 0px -20% 0px' },
  )
  ids.forEach((id) => {
    const el = document.getElementById(id)
    if (el) sectionObserver.observe(el)
  })
})

onBeforeUnmount(() => {
  unsubscribers.forEach((u) => u && u())
  if (flashTimer) clearTimeout(flashTimer)
  triggers.forEach((t) => t?.kill?.())
  triggers.length = 0
  sectionObserver?.disconnect()
  sectionObserver = null
  detachScrollLock()
})
</script>

<style scoped>
.knowledge-page {
  position: relative;
  min-height: 100vh;
  color: var(--color-kh-text);
  background: transparent;
  font-family: 'Inter', system-ui, -apple-system, Arial, sans-serif;
  overflow-x: hidden;
}

.knowledge-page__main {
  position: relative;
  z-index: 1;
  padding-bottom: 160px;          /* leave room for the global floor rail */
}

/* Edge flash — kept for reveal feedback */
.kh-edge-flash {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 3;
  --kh-edge-color: var(--color-kh-pulse-correct);
}

.kh-edge-flash__bar {
  position: absolute;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(
    to right,
    transparent 0%,
    var(--kh-edge-color) 50%,
    transparent 100%
  );
  filter: blur(1.5px);
  opacity: 0;
  transition: opacity 80ms ease-out;
}

.kh-edge-flash__bar--top {
  top: 0;
  box-shadow: 0 8px 30px var(--kh-edge-color);
}

.kh-edge-flash__bar--bottom {
  bottom: 0;
  box-shadow: 0 -8px 30px var(--kh-edge-color);
}

.kh-edge-flash--active .kh-edge-flash__bar {
  opacity: 0.85;
  transition: opacity 80ms ease-out;
}

/* ── Floor rail — same as HomeView ── */
.floor-rail {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  height: 130px;
  pointer-events: none;
  z-index: 5;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(
    to bottom,
    transparent 0%,
    rgba(246, 240, 230, 0.35) 30%,
    rgba(246, 240, 230, 0.85) 70%,
    rgba(246, 240, 230, 0.95) 100%
  );
}

.floor-rail__wave {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 38px;
  width: 100%;
  height: 24px;
  pointer-events: none;
}

.floor-flow {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 100%;
  pointer-events: none;
}

.floor-item {
  position: absolute;
  bottom: 18px;
  left: 0;
  width: 56px;
  height: 56px;
  object-fit: contain;
  pointer-events: none;
  animation: floor-travel 36s linear infinite;
  animation-delay: calc(var(--i, 0) * -5.2s);
  will-change: transform, opacity;
}

.floor-item:nth-child(2) { animation-duration: 40s; bottom: 26px; width: 52px; height: 52px; }
.floor-item:nth-child(3) { animation-duration: 32s; }
.floor-item:nth-child(4) { animation-duration: 38s; bottom: 22px; width: 60px; height: 60px; }
.floor-item:nth-child(5) { animation-duration: 42s; bottom: 30px; }
.floor-item:nth-child(6) { animation-duration: 35s; bottom: 24px; width: 50px; height: 50px; }
.floor-item:nth-child(7) { animation-duration: 39s; bottom: 28px; }

@keyframes floor-travel {
  0%   { transform: translateX(-10vw) scale(0.7) rotate(-4deg); opacity: 0; }
  8%   { opacity: 0.85; }
  50%  { transform: translateX(50vw) scale(1) rotate(0deg);     opacity: 0.9; }
  92%  { opacity: 0.85; }
  100% { transform: translateX(110vw) scale(0.7) rotate(4deg);  opacity: 0; }
}

@media (prefers-reduced-motion: reduce) {
  .kh-edge-flash__bar,
  .floor-item {
    animation: none;
  }
  .floor-item {
    transform: translateX(calc(8vw + var(--i, 0) * 16vw)) scale(1);
    opacity: 0.85;
  }
}

@media (max-width: 768px) {
  .floor-rail { height: 90px; }
  .floor-item { width: 44px; height: 44px; }
}

/* ── Page section rail ─────────────────────────────────────────────── */
.page-rail {
  position: fixed;
  top: 50%;
  right: 20px;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  gap: 6px;
  z-index: 50;
  padding: 12px 8px;
  background: rgba(246, 240, 230, 0.4);
  backdrop-filter: blur(8px);
  border-radius: var(--radius-pill);
  border: 1px solid rgba(22, 51, 0, 0.08);
}

.page-rail__dot {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 10px;
  padding: 8px 12px 8px 8px;
  background: transparent;
  border: none;
  cursor: pointer;
  font-family: inherit;
  color: var(--color-text-subtle);
  transition: color 240ms var(--motion-entrance);
}

.page-rail__dot:hover {
  color: var(--color-primary-text);
}

.page-rail__num {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.12em;
  width: 18px;
  text-align: right;
  opacity: 0.6;
  transition: opacity 240ms var(--motion-entrance);
}

.page-rail__core {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgba(22, 51, 0, 0.25);
  transition: all 280ms var(--motion-entrance);
}

.page-rail__label {
  position: absolute;
  right: calc(100% + 8px);
  top: 50%;
  transform: translateY(-50%) translateX(8px);
  white-space: nowrap;
  background: var(--color-text);
  color: var(--color-warm-cream);
  padding: 6px 12px;
  border-radius: var(--radius-pill);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.08em;
  opacity: 0;
  pointer-events: none;
  transition:
    opacity 240ms var(--motion-entrance),
    transform 240ms var(--motion-entrance);
}

.page-rail__dot:hover .page-rail__label,
.page-rail__dot--active .page-rail__label {
  opacity: 1;
  transform: translateY(-50%) translateX(0);
}

.page-rail__dot--active .page-rail__core {
  background: var(--color-primary);
  width: 14px;
  height: 14px;
  box-shadow: 0 0 0 4px rgba(159, 232, 112, 0.25);
}

.page-rail__dot--active .page-rail__num {
  opacity: 1;
  color: var(--color-primary-text);
}

@media (max-width: 1024px) {
  .page-rail {
    display: none;
  }
}
</style>
