<template>
  <section class="kh-cards">
    <header class="kh-cards__head">
      <button type="button" class="kh-cards__back" @click="$emit('back')">
        <ArrowLeft :size="16" :stroke-width="2" /> Back
      </button>
      <div class="kh-cards__heading">
        <p ref="eyebrowRef" class="kh-cards__eyebrow">STEP 04 · DEEP-DIVE CARDS</p>
        <AnimatedHeading
          as="h2"
          class="kh-cards__title"
          text="Fourteen short reads — the numbers behind the slogans."
          :stagger="0.06"
          :delay="0.1"
        />
        <p ref="subtitleRef" class="kh-cards__subtitle">
          Tap any card to see the full story, the data, and where it comes from.
        </p>
      </div>
    </header>

    <!-- Theme filter chips -->
    <div class="kh-cards__filters" role="tablist" aria-label="Filter by theme">
      <button
        type="button"
        class="kh-chip"
        :class="{ 'kh-chip--active': activeTheme === 'all' }"
        role="tab"
        :aria-selected="activeTheme === 'all'"
        @click="activeTheme = 'all'"
      >
        All themes
      </button>
      <button
        v-for="theme in themes"
        :key="theme.key"
        type="button"
        class="kh-chip"
        :class="{ 'kh-chip--active': activeTheme === theme.key }"
        role="tab"
        :aria-selected="activeTheme === theme.key"
        @click="activeTheme = theme.key"
      >
        {{ theme.label }}
      </button>
    </div>

    <!-- Scrapbook masonry wall -->
    <div class="kh-cards__wall" ref="wallRef">
      <article
        v-for="card in visibleCards"
        :key="card.id"
        class="kh-card-tile"
        :class="[`kh-card-tile--theme-${card.theme}`, { 'kh-card-tile--no-image': !card.image }]"
        :style="{ '--tilt': tiltOf(card) + 'deg' }"
        tabindex="0"
        role="button"
        :aria-label="`Open: ${card.title}`"
        @click="openCard($event, card)"
        @keydown.enter.prevent="openCard($event, card)"
        @keydown.space.prevent="openCard($event, card)"
      >
        <div class="kh-card-tile__media">
          <!-- Pin lives inside the media (a position:relative box) so its
               absolute positioning isn't a direct child of the column item.
               That dodges a Chromium CSS-columns bug where the pin on the
               first card of column 2/3 got stretched to span the entire
               column height. -->
          <span class="kh-card-tile__pin" aria-hidden="true">
            {{ cardNum(card) }}
          </span>
          <img
            :src="card.image"
            :alt="card.title"
            loading="lazy"
            @error="handleImgError"
          />
          <span class="kh-card-tile__stamp">
            {{ themeLabel(card.theme) }}
          </span>
        </div>
        <div class="kh-card-tile__body">
          <h3 class="kh-card-tile__title">{{ card.title }}</h3>
          <p class="kh-card-tile__summary">{{ card.summary }}</p>
          <span class="kh-card-tile__more">
            Read more <ArrowRight :size="14" :stroke-width="2" />
          </span>
        </div>
      </article>
    </div>

    <JourneyNextCard
      to="/brand-search"
      eyebrow="STEP 3 · EVALUATE"
      title="Now apply it — which brands actually do this?"
      body="See the transparency score of any brand against what you just learned."
      cta="Search a brand"
    />

    <!-- Modal with GSAP-driven open choreography -->
    <Transition
      name="kh-modal"
      :css="false"
      @before-enter="onModalBeforeEnter"
      @enter="onModalEnter"
      @leave="onModalLeave"
    >
      <div
        v-if="activeCard"
        class="kh-modal__backdrop"
        role="dialog"
        aria-modal="true"
        :aria-label="activeCard.title"
        @click.self="closeCard"
        @keydown.esc="closeCard"
      >
        <div class="kh-modal__panel" tabindex="-1" ref="modalRef">
          <button
            type="button"
            class="kh-modal__close"
            aria-label="Close"
            @click="closeCard"
          >
            <X :size="18" :stroke-width="2" />
          </button>

          <div class="kh-modal__media">
            <img
              :src="activeCard.image"
              :alt="activeCard.title"
              @error="handleImgError"
            />
          </div>

          <div class="kh-modal__body" data-lenis-prevent>
            <span class="kh-modal__theme">
              {{ themeLabel(activeCard.theme) }}
            </span>
            <h3 class="kh-modal__title">{{ activeCard.title }}</h3>
            <p class="kh-modal__summary">{{ activeCard.summary }}</p>

            <div class="kh-modal__paragraphs">
              <p v-for="(p, i) in activeCard.body" :key="i">{{ p }}</p>
            </div>

            <p class="kh-modal__source">
              <BookOpen :size="13" :stroke-width="2" />
              <span><strong>Source:</strong> {{ activeCard.source }}</span>
            </p>
          </div>
        </div>
      </div>
    </Transition>
  </section>
</template>

<script setup>
import { ref, computed, watch, nextTick, onBeforeUnmount } from 'vue'
import { gsap } from 'gsap'
import { ArrowLeft, ArrowRight, BookOpen, X } from 'lucide-vue-next'
import data from '../../data/knowledge-cards.json'
import AnimatedHeading from '../AnimatedHeading.vue'
import JourneyNextCard from '../journey/JourneyNextCard.vue'
import { useReveal } from '../../motion/useReveal'
import { isReduced } from '../../motion'

defineEmits(['back'])

const eyebrowRef = ref(null)
const subtitleRef = ref(null)
const wallRef = ref(null)
useReveal(eyebrowRef, { mode: 'char', stagger: 0.022, duration: 0.5 })
useReveal(subtitleRef, { mode: 'fade-blur', y: 40, delay: 0.25 })

const themes = data.themes
const cards = data.cards

const activeTheme = ref('all')
const activeCard = ref(null)
const modalRef = ref(null)

const themeMap = Object.fromEntries(themes.map((t) => [t.key, t.label]))
function themeLabel(key) { return themeMap[key] || key }

const visibleCards = computed(() => {
  if (activeTheme.value === 'all') return cards
  return cards.filter((c) => c.theme === activeTheme.value)
})

// Deterministic per-card tilt — each card always lands at the same angle so
// the wall feels like 14 hand-stuck polaroids rather than random noise.
const TILTS = [-1.2, 1.4, -0.8, 1.1, -1.5, 0.9, -1.0, 1.3, -0.7, 1.5, -1.1, 0.8, -1.4, 1.2]
function tiltOf(card) {
  const i = cards.indexOf(card)
  return TILTS[i] ?? 0
}

const TOTAL = String(cards.length).padStart(2, '0')
function cardNum(card) {
  const i = cards.indexOf(card)
  return `${String(i + 1).padStart(2, '0')} / ${TOTAL}`
}

// Stagger-reveal visible tiles whenever the filter list changes (initial
// mount + every theme switch). Uses gsap.context to scope and clean up.
let wallCtx = null
watch(
  () => visibleCards.value.map((c) => c.id).join('|'),
  async () => {
    if (isReduced()) return
    await nextTick()
    wallCtx?.revert()
    const tiles = wallRef.value?.querySelectorAll('.kh-card-tile')
    if (!tiles || !tiles.length) {
      wallCtx = null
      return
    }
    wallCtx = gsap.context(() => {
      gsap.fromTo(
        tiles,
        { opacity: 0, y: 24 },
        { opacity: 1, y: 0, duration: 0.55, stagger: 0.05, ease: 'power3.out' },
      )
    }, wallRef.value)
  },
  { immediate: true },
)

// `overflow: hidden` on <html>/<body> was insufficient in some browsers (the
// page kept scrolling under the modal). Pinning <body> with `position: fixed`
// and restoring the scroll position on close is the bulletproof pattern.
let lockedScrollY = 0
function lockScroll() {
  lockedScrollY = window.scrollY
  const b = document.body.style
  b.position = 'fixed'
  b.top = `-${lockedScrollY}px`
  b.left = '0'
  b.right = '0'
  b.width = '100%'
}
function unlockScroll() {
  const b = document.body.style
  b.position = ''
  b.top = ''
  b.left = ''
  b.right = ''
  b.width = ''
  if (lockedScrollY) {
    window.scrollTo(0, lockedScrollY)
    lockedScrollY = 0
  }
}

// Capture the click coordinates so the modal can scale-up from where the
// user actually tapped — a subtle "the card grew" feeling.
const clickOrigin = ref({ x: null, y: null })
function openCard(evt, card) {
  if (evt && evt.clientX != null) {
    clickOrigin.value = { x: evt.clientX, y: evt.clientY }
  } else {
    clickOrigin.value = { x: null, y: null }
  }
  activeCard.value = card
  lockScroll()
  nextTick(() => modalRef.value?.focus())
}
function closeCard() {
  activeCard.value = null
  unlockScroll()
}

function handleImgError(e) {
  e.target.style.opacity = '0'
}

// ── Modal motion (Vue Transition JS hooks → GSAP timeline) ────────
// `:css="false"` on the <Transition> tells Vue to skip its CSS classes and
// wait for the JS hooks to call `done()`. The hooks below choreograph a
// spring-pop on the panel + a staggered fade-up on every inner block.
function onModalBeforeEnter(el) {
  if (isReduced()) return
  const panel = el.querySelector('.kh-modal__panel')
  const targets = el.querySelectorAll(
    '.kh-modal__theme, .kh-modal__title, .kh-modal__summary, .kh-modal__paragraphs p, .kh-modal__source',
  )
  // Lock initial state so there's no flash of fully-rendered content before
  // the timeline kicks in.
  gsap.set(el, { opacity: 0 })
  gsap.set(panel, {
    opacity: 0,
    y: 30,
    scale: 0.92,
    transformOrigin: originString(panel),
  })
  gsap.set(targets, { opacity: 0, y: 14 })
  gsap.set(el.querySelector('.kh-modal__media img'), { scale: 1.08 })
}

function onModalEnter(el, done) {
  if (isReduced()) {
    el.style.opacity = '1'
    el.querySelector('.kh-modal__panel').style.opacity = '1'
    done()
    return
  }

  const panel = el.querySelector('.kh-modal__panel')
  const targets = el.querySelectorAll(
    '.kh-modal__theme, .kh-modal__title, .kh-modal__summary, .kh-modal__paragraphs p, .kh-modal__source',
  )

  const tl = gsap.timeline({ onComplete: done })

  tl.to(el, { opacity: 1, duration: 0.25, ease: 'power2.out' }, 0)
    .to(panel, {
      opacity: 1, y: 0, scale: 1,
      duration: 0.55,
      ease: 'cubic-bezier(0.34, 1.56, 0.64, 1)',
    }, 0)
    .to(el.querySelector('.kh-modal__media img'), {
      scale: 1,
      duration: 0.9,
      ease: 'power3.out',
    }, 0.05)
    .to(targets, {
      opacity: 1, y: 0,
      duration: 0.45,
      stagger: 0.05,
      ease: 'power3.out',
    }, 0.18)
}

function onModalLeave(el, done) {
  if (isReduced()) { done(); return }
  const panel = el.querySelector('.kh-modal__panel')
  gsap.timeline({ onComplete: done })
    .to(panel, {
      opacity: 0, y: 12, scale: 0.97,
      duration: 0.22,
      ease: 'power2.in',
    }, 0)
    .to(el, { opacity: 0, duration: 0.22, ease: 'power2.in' }, 0)
}

// Pick a transform-origin near the click point so the spring pop visually
// connects to where the user tapped. Falls back to centre if we don't have
// coordinates (keyboard activation).
function originString(panel) {
  const { x, y } = clickOrigin.value
  if (x == null || y == null) return '50% 50%'
  const r = panel.getBoundingClientRect()
  const ox = ((x - r.left) / r.width) * 100
  const oy = ((y - r.top) / r.height) * 100
  return `${Math.max(0, Math.min(100, ox))}% ${Math.max(0, Math.min(100, oy))}%`
}

// Esc-to-close at document level so modal closes even if focus has drifted.
function onKey(e) { if (e.key === 'Escape') closeCard() }
watch(activeCard, (v) => {
  if (v) document.addEventListener('keydown', onKey)
  else document.removeEventListener('keydown', onKey)
})
onBeforeUnmount(() => {
  document.removeEventListener('keydown', onKey)
  unlockScroll()
  wallCtx?.revert()
  wallCtx = null
})
</script>

<style scoped>
.kh-cards {
  position: relative;
  max-width: 1200px;
  margin: 0 auto;
  padding: 64px 32px 80px;
}

/* ── Header ───────────────────────────────────────────────────── */
.kh-cards__head {
  display: flex;
  align-items: flex-start;
  gap: 24px;
  margin-bottom: 28px;
}
.kh-cards__back {
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  background: var(--color-surface, #fff);
  border: 1px solid var(--color-border, rgba(0, 0, 0, 0.08));
  border-radius: var(--radius-btn, 999px);
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text);
  cursor: pointer;
  transition: transform var(--transition-base), background var(--transition-base);
}
.kh-cards__back:hover { transform: translateX(-2px); background: var(--color-bg-soft, #f5f1e8); }

.kh-cards__heading { flex: 1; }
.kh-cards__eyebrow {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 2px;
  color: var(--color-primary-text);
  margin: 0 0 10px;
}
.kh-cards__title {
  font-size: clamp(28px, 3.4vw, 40px);
  font-weight: 800;
  letter-spacing: -1px;
  line-height: 1.1;
  color: var(--color-text);
  margin: 0 0 12px;
}
.kh-cards__subtitle {
  font-size: 15.5px;
  line-height: 1.55;
  color: var(--color-text-muted);
  max-width: 620px;
  margin: 0;
}

/* ── Filter chips ─────────────────────────────────────────────── */
.kh-cards__filters {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 36px;
}
.kh-chip {
  padding: 8px 16px;
  border-radius: 999px;
  border: 1px solid var(--color-border, rgba(0, 0, 0, 0.1));
  background: var(--color-surface, #fff);
  color: var(--color-text-muted);
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.2px;
  cursor: pointer;
  transition: all var(--transition-base);
}
.kh-chip:hover { background: var(--color-bg-soft, #f5f1e8); color: var(--color-text); }
.kh-chip--active {
  background: var(--color-primary);
  color: var(--color-primary-text);
  border-color: transparent;
}

/* ── Scrapbook wall (CSS columns masonry) ─────────────────────── */
.kh-cards__wall {
  column-count: 3;
  column-gap: 28px;
  /* Small horizontal padding lets the rotated cards' corners breathe
     without getting clipped by the column edges. */
  padding: 4px 6px;
}

.kh-card-tile {
  --tilt: 0deg;
  /* Per-theme accent — overridden by .kh-card-tile--theme-* below.
     Drives pin background, stamp border, Read more text, hover border. */
  --accent: #2d6b35;
  position: relative;
  display: block;
  break-inside: avoid;
  -webkit-column-break-inside: avoid;
  page-break-inside: avoid;
  margin-bottom: 28px;
  background: var(--color-surface, #fff);
  border: 1.5px solid var(--color-border-light, rgba(0, 0, 0, 0.06));
  border-radius: 18px;
  overflow: hidden;
  cursor: pointer;
  transform: rotate(var(--tilt));
  transition:
    transform 320ms var(--motion-spring),
    box-shadow 240ms var(--motion-entrance),
    border-color 240ms var(--motion-entrance);
  will-change: transform;
}

/* Seven themes, seven earthy accent tones — keeps the cream + green frame
   while giving every card a distinct personality. */
.kh-card-tile--theme-pollution   { --accent: #2d7a3e; }
.kh-card-tile--theme-materials   { --accent: #b3823a; }
.kh-card-tile--theme-production  { --accent: #b04a35; }
.kh-card-tile--theme-consumption { --accent: #3d7e8a; }
.kh-card-tile--theme-care        { --accent: #8167a3; }
.kh-card-tile--theme-waste       { --accent: #7a5a39; }
.kh-card-tile--theme-brand       { --accent: #b14a6a; }

.kh-card-tile:hover {
  /* Stand up to greet the cursor. */
  transform: rotate(0deg) translateY(-6px) scale(1.015);
  box-shadow: 0 20px 40px -18px rgba(22, 51, 0, 0.2);
  border-color: var(--accent);
}
.kh-card-tile:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 4px;
}

/* Numbered "01 / 14" pin badge — sits inside the media so it doesn't trip
   the CSS-columns absolute-positioning fragmentation bug. */
.kh-card-tile__pin {
  position: absolute;
  top: 12px;
  left: 12px;
  z-index: 2;
  padding: 4px 11px;
  border-radius: 999px;
  background: var(--accent);
  color: #fff;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 1.2px;
  font-variant-numeric: tabular-nums;
  border: 1.5px solid rgba(255, 255, 255, 0.7);
  box-shadow: 0 4px 10px -4px rgba(0, 0, 0, 0.32);
  transform: rotate(-4deg);
}

/* Media slot — rounded image with the pin + a tilted "stamp" tag on top. */
.kh-card-tile__media {
  position: relative;
  margin: 0;
  overflow: hidden;
  border-radius: 16px 16px 0 0;
  background: linear-gradient(135deg, #d9f4b9 0%, #9fe870 100%);
}
.kh-card-tile__media img {
  display: block;
  width: 100%;
  height: auto;
  object-fit: cover;
  transition: opacity 200ms ease, transform 700ms var(--motion-entrance);
}
.kh-card-tile:hover .kh-card-tile__media img {
  transform: scale(1.03);
}
.kh-card-tile__stamp {
  position: absolute;
  top: 14px;
  right: 14px;
  padding: 5px 11px;
  background: var(--color-surface);
  color: var(--accent);
  font-size: 10.5px;
  font-weight: 800;
  letter-spacing: 0.6px;
  text-transform: uppercase;
  border-radius: 4px;
  border: 1.5px solid var(--accent);
  box-shadow: 0 2px 6px -2px rgba(0, 0, 0, 0.18);
  /* Stamp tilt — slightly off-axis like a postmark. */
  transform: rotate(-3deg);
}

.kh-card-tile__body { padding: 20px 22px 22px; }
.kh-card-tile__title {
  font-size: 17.5px;
  font-weight: 800;
  line-height: 1.32;
  color: var(--color-text);
  margin: 0 0 10px;
  letter-spacing: -0.25px;
}
.kh-card-tile__summary {
  font-size: 13.5px;
  line-height: 1.6;
  color: var(--color-text-muted);
  margin: 0 0 16px;
}
.kh-card-tile__more {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 12.5px;
  font-weight: 800;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  color: var(--accent);
}
.kh-card-tile__more svg {
  transition: transform var(--transition-base);
}
.kh-card-tile:hover .kh-card-tile__more svg { transform: translateX(4px); }

/* ── Modal ────────────────────────────────────────────────────── */
.kh-modal__backdrop {
  position: fixed;
  inset: 0;
  z-index: 100;
  background: rgba(22, 51, 0, 0.45);
  backdrop-filter: blur(6px);
  display: grid;
  place-items: center;
  padding: 24px;
  overflow-y: auto;
}

.kh-modal__panel {
  position: relative;
  width: 100%;
  max-width: 720px;
  max-height: calc(100vh - 48px);
  background: var(--color-surface, #fff);
  border-radius: 24px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  outline: none;
  box-shadow: 0 28px 70px rgba(0, 0, 0, 0.24);
  will-change: transform;
}

.kh-modal__close {
  position: absolute;
  top: 16px; right: 16px;
  z-index: 2;
  width: 36px; height: 36px;
  border-radius: 999px;
  border: none;
  background: rgba(255, 255, 255, 0.92);
  color: var(--color-text);
  cursor: pointer;
  display: grid; place-items: center;
  transition: background var(--transition-base), transform var(--transition-base);
}
.kh-modal__close:hover { background: #fff; transform: scale(1.05); }

.kh-modal__media {
  background: linear-gradient(135deg, #d9f4b9 0%, #9fe870 100%);
  flex-shrink: 0;
  overflow: hidden;
}
.kh-modal__media img {
  display: block;
  width: 100%;
  height: 280px;
  object-fit: cover;
}

.kh-modal__body {
  padding: 28px 36px 32px;
  overflow-y: auto;
}

.kh-modal__theme {
  display: inline-block;
  padding: 4px 12px;
  background: var(--color-surface);
  color: var(--color-primary-text);
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 1px;
  border-radius: 4px;
  border: 1.2px solid var(--color-primary-text);
  margin-bottom: 14px;
  text-transform: uppercase;
  transform: rotate(-2deg);
}
.kh-modal__title {
  font-size: clamp(22px, 2.6vw, 28px);
  font-weight: 800;
  line-height: 1.2;
  letter-spacing: -0.5px;
  color: var(--color-text);
  margin: 0 0 12px;
}
.kh-modal__summary {
  font-size: 15.5px;
  line-height: 1.55;
  color: var(--color-text-muted);
  font-style: italic;
  margin: 0 0 22px;
  padding-left: 14px;
  border-left: 3px solid var(--color-primary);
}
.kh-modal__paragraphs p {
  font-size: 15px;
  line-height: 1.7;
  color: var(--color-text);
  margin: 0 0 14px;
}
.kh-modal__paragraphs p:last-child { margin-bottom: 20px; }
.kh-modal__source {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  margin: 12px 0 0;
  padding: 14px 16px;
  background: var(--color-bg-soft, #f5f1e8);
  border-radius: 12px;
  font-size: 12.5px;
  line-height: 1.5;
  color: var(--color-text-muted);
}
.kh-modal__source svg {
  flex-shrink: 0;
  margin-top: 2px;
  color: var(--color-primary-text);
}

/* prefers-reduced-motion: kill all the scrapbook flourishes. */
@media (prefers-reduced-motion: reduce) {
  .kh-card-tile {
    transform: none;
  }
  .kh-card-tile:hover {
    transform: translateY(-3px);
  }
  .kh-card-tile__pin,
  .kh-card-tile__stamp,
  .kh-modal__theme {
    transform: none;
  }
}

/* ── Responsive ──────────────────────────────────────────────── */
@media (max-width: 1024px) {
  .kh-cards__wall { column-count: 2; }
}
@media (max-width: 640px) {
  .kh-cards { padding: 48px 20px 64px; }
  .kh-cards__head { flex-direction: column; gap: 16px; }
  .kh-cards__wall { column-count: 1; column-gap: 0; }
  .kh-modal__media img { height: 200px; }
  .kh-modal__body { padding: 22px 22px 26px; }
}
</style>
