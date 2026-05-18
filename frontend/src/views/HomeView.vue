<template>
  <div class="home" ref="pageRef">
    <Navbar />

    <!-- Fixed background canvas — does NOT scroll with content.
         Unified backdrop across all sections so there are no visible seams.
         Two soft lime/mint blobs drift, three abstract shapes orbit slowly,
         and a faint mint grid anchors the depth. Each element has its own
         period so they never pulse together. -->
    <div class="home-canvas" aria-hidden="true">
      <!-- One soft full-screen tint sheet replaces the four-corner blob
           "headlights". Per-section palette swaps drive a 800ms CSS
           transition between two diagonal stops, so the page feels lit by
           a different ambient colour in each section without any visible
           light pucks. -->
      <span class="canvas-tint" />
      <span class="canvas-grid" />
    </div>

    <!-- §1 Hero — wardrobe illustration, headline reveals on scroll-progress. -->
    <section class="story story--hero" data-section="hero">
      <span class="section-index" aria-hidden="true">01</span>
      <span class="section-label" aria-hidden="true">SECTION 01 — THE PROMISE</span>
      <span class="sprinkle sprinkle--tag-1" aria-hidden="true"><Tag :size="18" :stroke-width="1.6" /></span>
      <span class="sprinkle sprinkle--leaf-1" aria-hidden="true"><Leaf :size="20" :stroke-width="1.6" /></span>
      <span class="sprinkle sprinkle--sparkle-1" aria-hidden="true"><Sparkles :size="16" :stroke-width="1.6" /></span>
      <div class="story-grid">
        <div class="story-text" data-reveal>
          <p class="eyebrow" data-line>FOR SUSTAINABLE FASHION IN AUSTRALIA</p>
          <AnimatedHeading
            as="h1"
            class="hero-headline"
            mode="flip"
            :lines="[
              'Wear it longer.',
              'Waste it less.',
              'Look better doing both.',
            ]"
            :stagger="0.12"
            :delay="0.15"
            :duration="1.05"
          />
          <p class="hero-sub" data-line>
            Fashion leaves a footprint long before it reaches your wardrobe.
            WearImpact helps you choose better, buy second-hand, and make
            more of what you already own.
          </p>
          <p class="hero-sub hero-sub--solution" data-line>
            <strong>Start with what you already have.</strong>
            Catalogue your closet first — then we'll help you decide what's next.
          </p>
          <div class="hero-cta-row" data-line>
            <CtaButton to="/wardrobe" class="hero-cta-primary">
              Start with my wardrobe
              <ArrowRight :size="17" :stroke-width="2.5" class="cta-arrow" />
            </CtaButton>
            <button
              type="button"
              class="hero-cta-secondary"
              @click="jumpToSection('sol-2')"
            >
              Or see how the journey works
              <span class="hero-cta-secondary__arrow" aria-hidden="true">↓</span>
            </button>
          </div>
        </div>
        <!-- safe: trusted internal SVG string from this component, never user input -->
        <div class="story-art story-art--hero" data-art v-html="artHero" aria-hidden="true" />
      </div>

      <!-- Hexagon scroll-cue button: anchored to the bottom of the hero
           viewport, scrolls smoothly to the first solution section. The
           shape is built with clip-path; bounces gently to invite a click. -->
      <button
        type="button"
        class="hero-scroll-down"
        aria-label="Scroll to next section"
        @click="jumpToSection('sol-2')"
      >
        <span class="hero-scroll-down__hex" aria-hidden="true" />
        <ChevronDown :size="18" :stroke-width="2.4" class="hero-scroll-down__icon" />
      </button>
    </section>

    <div class="story-divider" aria-hidden="true"><span /><span /><span /></div>

    <!-- §5–7 Solutions — each pairs copy with an animated illustration. -->
    <template v-for="(sol, i) in solutions" :key="sol.id">
      <section class="story story--solution" :data-section="`sol-${sol.id}`">
        <span class="section-index" :class="{ 'section-index--right': i % 2 === 1 }" aria-hidden="true">0{{ sol.id }}</span>
        <span class="section-label" :class="{ 'section-label--right': i % 2 === 1 }" aria-hidden="true">SECTION 0{{ sol.id }} — {{ sol.labelTag }}</span>
        <span class="sprinkle sprinkle--sol-1" aria-hidden="true"><component :is="sol.sprinkleA" :size="18" :stroke-width="1.6" /></span>
        <span class="sprinkle sprinkle--sol-2" aria-hidden="true"><component :is="sol.sprinkleB" :size="16" :stroke-width="1.6" /></span>
        <div class="story-grid" :class="{ 'story-grid--reverse': i % 2 === 1 }">
          <div class="story-text" data-reveal>
            <p class="sol-problem" data-line>{{ sol.problem }}</p>
            <h2 data-line>{{ sol.title }}</h2>
            <p class="sol-desc" data-line>{{ sol.description }}</p>
            <CtaButton :to="sol.link" class="sol-cta" data-line>
              {{ sol.cta }}
              <ArrowRight :size="17" :stroke-width="2.5" class="cta-arrow" />
            </CtaButton>
          </div>
          <!-- safe: trusted internal SVG string from the solutions array, never user input -->
          <div class="story-art story-art--solution" data-art v-html="sol.art" aria-hidden="true" />
        </div>
      </section>
      <div v-if="i < solutions.length - 1" class="story-divider" aria-hidden="true"><span /><span /><span /></div>
    </template>

    <!-- Global floor rail — fixed at viewport bottom. Single shared set of
         SVG icons flowing left → right continuously, identical across all
         sections. Footer fade hides the whole rail when reaching footer. -->
    <div class="floor-rail" aria-hidden="true">
      <!-- Lime "river" — two parallax water layers under a bright surface line. -->
      <div class="floor-river">
        <svg class="river-layer river-layer--back" viewBox="0 0 2880 80" preserveAspectRatio="none">
          <defs>
            <linearGradient id="home-river-back" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0"    stop-color="#bff0a0" stop-opacity="0.45"/>
              <stop offset="0.55" stop-color="#a8e394" stop-opacity="0.22"/>
              <stop offset="1"    stop-color="#9fe870" stop-opacity="0"/>
            </linearGradient>
          </defs>
          <path :d="riverBackPathD" fill="url(#home-river-back)" />
        </svg>
        <svg class="river-layer river-layer--front" viewBox="0 0 2880 80" preserveAspectRatio="none">
          <defs>
            <linearGradient id="home-river-front" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0"    stop-color="#b6ea90" stop-opacity="0.62"/>
              <stop offset="0.55" stop-color="#9fe870" stop-opacity="0.34"/>
              <stop offset="1"    stop-color="#9fe870" stop-opacity="0"/>
            </linearGradient>
          </defs>
          <path :d="riverFrontPathD" fill="url(#home-river-front)" />
        </svg>
        <svg class="river-edge" viewBox="0 0 1440 24" preserveAspectRatio="none">
          <path
            d="M 0 12 Q 60 2 120 12 T 240 12 T 360 12 T 480 12 T 600 12 T 720 12 T 840 12 T 960 12 T 1080 12 T 1200 12 T 1320 12 T 1440 12"
            stroke="#9fe870"
            stroke-width="2"
            fill="none"
            stroke-linecap="round"
            opacity="0.85"
          />
        </svg>
      </div>
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
      <span class="floor-rail__caption">{{ activeSectionLabel }}</span>
    </div>

    <!-- Side progress rail — fixed right, vertical 7-dot indicator that
         tracks the current section in view. Click a dot to jump. -->
    <aside class="progress-rail" aria-label="Page progress">
      <button
        v-for="(s, i) in railSections"
        :key="s.key"
        type="button"
        class="rail-dot"
        :class="{ 'rail-dot--active': activeSectionKey === s.key }"
        @click="jumpToSection(s.key)"
      >
        <span class="rail-dot__num" aria-hidden="true">0{{ i + 1 }}</span>
        <span class="rail-dot__core" aria-hidden="true" />
        <span class="rail-dot__label">{{ s.label }}</span>
      </button>
    </aside>

    <FooterSection />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { gsap } from 'gsap'
import { ScrollTrigger, splitElement, isReduced } from '../motion'
import Navbar from '../components/Navbar.vue'
import FooterSection from '../components/FooterSection.vue'
import AnimatedHeading from '../components/AnimatedHeading.vue'
import CtaButton from '../components/CtaButton.vue'
import {
  ArrowRight,
  ChevronDown,
  Tag,
  Leaf,
  Sparkles,
  Shirt,
  MapPin,
  Search,
  BookOpen,
  Compass,
  ShieldCheck,
  Lightbulb,
} from 'lucide-vue-next'

// Animated illustrations — entrance choreography embedded; we toggle the
// `.animated` class on each SVG root via ScrollTrigger so the entrance
// re-plays every time the section enters the viewport.
import artHero from '../assets/illustrations/choosing-clothes-animate.svg?raw'
import artBridge from '../assets/illustrations/choosing-clothes-animate2.svg?raw'
import artThrift from '../assets/illustrations/thrift-shopping-animate.svg?raw'
import artWindowShop from '../assets/illustrations/find-ecoshop-animate.svg?raw'
import artKnowledge from '../assets/illustrations/learn-knowledge-animate.svg?raw'

// Shared floor icons — one fixed set used across all sections.
import floorClothing from '../assets/illustrations/floor-clothing.svg'
import floorHandbag from '../assets/illustrations/floor-handbag.svg'
import floorLeaf from '../assets/illustrations/floor-leaf.svg'
import floorLightBulb from '../assets/illustrations/floor-light-bulb.svg'
import floorRecycle from '../assets/illustrations/floor-recycle.svg'
import floorShoes from '../assets/illustrations/floor-shoes.svg'
import floorTag from '../assets/illustrations/floor-tag.svg'

// Order chosen so adjacent items have visual variety (silhouette, color).
const floorIcons = [
  floorClothing,
  floorTag,
  floorLeaf,
  floorHandbag,
  floorRecycle,
  floorShoes,
  floorLightBulb,
]

// River wave paths — drawn 2× viewport wide (2880) so the CSS
// translateX(-50%) loop wraps seamlessly.
function buildFrontRiverPath() {
  const ts = []
  for (let x = 240; x <= 2880; x += 120) ts.push(`T ${x} 32`)
  return `M 0 32 Q 60 22 120 32 ${ts.join(' ')} L 2880 80 L 0 80 Z`
}
function buildBackRiverPath() {
  const ts = []
  for (let x = 360; x <= 2880; x += 180) ts.push(`T ${x} 26`)
  return `M 0 26 Q 90 18 180 26 ${ts.join(' ')} L 2880 80 L 0 80 Z`
}
const riverFrontPathD = buildFrontRiverPath()
const riverBackPathD = buildBackRiverPath()

const pageRef = ref(null)
// All ScrollTriggers + tweens created by buildScrollChoreography below are
// owned by a gsap.context() (see onMounted / onBeforeUnmount). On unmount,
// ctx.revert() kills every trigger and tween at once — no manual array.
let choreographyCtx = null

// Side progress rail — one entry per scroll-section.
const railSections = [
  { key: 'hero',  label: '01 — The Promise' },
  { key: 'sol-2', label: '02 — Your Wardrobe' },
  { key: 'sol-3', label: '03 — Act' },
  { key: 'sol-4', label: '04 — Evaluate' },
  { key: 'sol-5', label: '05 — Discover' },
]

const activeSectionKey = ref('hero')
const activeSectionLabel = computed(
  () => railSections.find((s) => s.key === activeSectionKey.value)?.label || '',
)

function jumpToSection(key) {
  const target = document.querySelector(`[data-section="${key}"]`)
  if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

const solutions = [
  {
    id: 2,
    problem: 'Most of your impact lives in clothes you already own.',
    title: 'See what\'s really in your wardrobe.',
    description:
      'Snap your clothes — we sort, tag, and store them in your browser. No login, no cloud. Once you can see what you already own, the next step gets a lot clearer.',
    cta: 'Start with my wardrobe',
    link: '/wardrobe',
    art: artBridge,
    labelTag: 'STEP 1 · KNOW',
    sprinkleA: Shirt,
    sprinkleB: Sparkles,
  },
  {
    id: 3,
    problem: "Don't shop blind — most 'sustainable' marketing isn't.",
    title: 'Learn what actually matters.',
    description:
      'WearImpact breaks down the real issues — materials, supply chains, waste — in plain language. Five minutes here saves a hundred bad purchases later.',
    cta: 'Learn what actually matters',
    link: '/knowledge',
    art: artKnowledge,
    labelTag: 'STEP 2 · LEARN',
    sprinkleA: BookOpen,
    sprinkleB: Lightbulb,
  },
  {
    id: 4,
    problem: 'A brand says "sustainable." But is it really?',
    title: 'See how transparent your brands are.',
    description:
      'Search any clothing brand and see its real score — across policy, environment, and supply chain — based on the Fashion Transparency Index. No greenwashing survives a side-by-side.',
    cta: 'Evaluate a brand',
    link: '/brand-search',
    art: artWindowShop,
    labelTag: 'STEP 3 · EVALUATE',
    sprinkleA: Search,
    sprinkleB: ShieldCheck,
  },
  {
    id: 5,
    problem: "Whether you're donating or buying second-hand, do it locally.",
    title: 'Find shops near you — donate or buy second-hand.',
    description:
      'WearImpact maps every op-shop, donation point and textile recycling centre within your chosen radius — with directions and opening hours. End the journey where the action is.',
    cta: 'Find shops near you',
    link: '/eco-shop',
    art: artThrift,
    labelTag: 'STEP 4 · ACT',
    sprinkleA: MapPin,
    sprinkleB: Compass,
  },
]

// Per-section ambient palette. As the user scrolls into each .story, GSAP
// scrub-tweens these CSS variables on the .home root, letting the fixed
// background blobs cross-fade between moods. Indexed by data-section.
// Two diagonal stops per section — drives the full-screen `.canvas-tint`
// gradient. Colours are intentionally low-saturation so the tint reads as
// "the light changed" rather than "the page got dyed".
const SECTION_PALETTES = {
  hero:    { '--bg-tint-a': '#d4f3b5', '--bg-tint-b': '#fff5e1', '--bg-tint-opacity': '0.06' },
  'sol-2': { '--bg-tint-a': '#e0dcff', '--bg-tint-b': '#f0eaff', '--bg-tint-opacity': '0.05' },
  'sol-3': { '--bg-tint-a': '#d4f3b5', '--bg-tint-b': '#cfe6ff', '--bg-tint-opacity': '0.07' },
  'sol-4': { '--bg-tint-a': '#fde0c4', '--bg-tint-b': '#ffe9c8', '--bg-tint-opacity': '0.06' },
  'sol-5': { '--bg-tint-a': '#cdffad', '--bg-tint-b': '#bfd9b3', '--bg-tint-opacity': '0.09' },
}

// Scroll-progress reveal: every section's lines + art rise from below as the
// section enters. `scrub` ties the animation to scroll position so reverse
// scroll un-reveals — the page feels like it tracks the wheel exactly.
function buildScrollChoreography() {
  const page = pageRef.value
  if (!page) return

  const prefersReduced = isReduced()

  // Background ambient: wheel-driven topography parallax + per-section
  // palette scrub. Both short-circuit under reduce-motion.
  if (!prefersReduced) {
    const grid = page.querySelector('.canvas-grid')
    if (grid) {
      gsap.to(grid, {
        backgroundPosition: '0 -240px',
        ease: 'none',
        scrollTrigger: { trigger: page, start: 'top top', end: 'bottom bottom', scrub: true },
      })
    }

    // Palette swap on section enter/leave-back. CSS variables are switched
    // instantly, but the blob `background` rules carry a 600ms transition,
    // so visually the colour cross-fades across about half a second.
    // GSAP can't smoothly tween hex colours stored in CSS vars, so we drive
    // the swap with ScrollTrigger callbacks rather than a scrub tween.
    const applyPalette = (key) => {
      const palette = SECTION_PALETTES[key]
      if (!palette) return
      Object.entries(palette).forEach(([k, v]) => page.style.setProperty(k, v))
    }
    page.querySelectorAll('.story[data-section]').forEach((section) => {
      const key = section.dataset.section
      if (!SECTION_PALETTES[key]) return
      ScrollTrigger.create({
        trigger: section,
        start: 'top 55%',
        end: 'bottom 45%',
        onEnter:     () => applyPalette(key),
        onEnterBack: () => applyPalette(key),
      })
    })
  }

  page.querySelectorAll('.story').forEach((section) => {
    const art = section.querySelector('[data-art]')
    const isHero = section.dataset.section === 'hero'

    // Track active section for the side progress rail + global floor swap
    const sectionKey = section.dataset.section
    if (sectionKey) {
      ScrollTrigger.create({
        trigger: section,
        start: 'top 50%',
        end: 'bottom 50%',
        onEnter:     () => (activeSectionKey.value = sectionKey),
        onEnterBack: () => (activeSectionKey.value = sectionKey),
      })
    }

    if (prefersReduced) {
      const everything = section.querySelectorAll('[data-line], [data-art], .story-text, .story-art')
      gsap.set(everything, { opacity: 1, x: 0, y: 0 })
      return
    }

    // Per-section box entrance: .story-text + .story-art slide in from
    // their visual sides on wide screens, fade-up on narrow stacks. The
    // cascade inside .story-text plays a beat later so users see the box
    // land first, then the lines light up.
    //
    // Note: .story-grid--reverse only widens the right column — it does
    // NOT swap DOM order, so visually .story-text is always left and
    // .story-art is always right across every section.
    const textBox = section.querySelector('.story-text')
    const artBox = section.querySelector('.story-art')
    const leftBox = textBox
    const rightBox = artBox
    const isNarrow = window.matchMedia('(max-width: 1024px)').matches

    // The side-slide finishes ~SLIDE_DUR + delay seconds after the trigger
    // fires; we hand that timestamp to the inner-svg `.animated` gate below
    // so the illustration's own entrance only starts after the box landed.
    const SLIDE_DUR = 1.0
    let slideSettleAt = 0    // ms timestamp when the slide finishes

    if (leftBox && rightBox) {
      if (isNarrow) {
        gsap.set([leftBox, rightBox], { y: 60, opacity: 0 })
        const enter = () => {
          gsap.to(leftBox,  { y: 0, opacity: 1, duration: 0.7, ease: 'power3.out' })
          gsap.to(rightBox, { y: 0, opacity: 1, duration: 0.7, ease: 'power3.out', delay: 0.08 })
          slideSettleAt = performance.now() + 780
        }
        const reset = () => gsap.set([leftBox, rightBox], { y: 60, opacity: 0 })
        ScrollTrigger.create({
          trigger: section,
          start: 'top 82%',
          onEnter: enter, onEnterBack: enter, onLeaveBack: reset,
        })
      } else {
        // Wide-screen "open the curtain": each box starts fully off-screen
        // (xPercent: ±120 puts the wrapper one viewport-width past its
        // anchor) and slides in. .home now owns the horizontal clip so the
        // off-screen position never leaks a scrollbar. Hero uses a softer
        // ±60 because it's already in view on page load and a full curtain
        // open from off-screen reads as jarring on first paint.
        const lead = isHero ? -60 : -120
        const trail = isHero ? 60 : 120
        gsap.set(leftBox,  { xPercent: lead, opacity: 0 })
        gsap.set(rightBox, { xPercent: trail, opacity: 0 })
        const enter = () => {
          gsap.to(leftBox,  { xPercent: 0, opacity: 1, duration: SLIDE_DUR, ease: 'power3.out' })
          gsap.to(rightBox, { xPercent: 0, opacity: 1, duration: SLIDE_DUR, ease: 'power3.out', delay: 0.08 })
          slideSettleAt = performance.now() + SLIDE_DUR * 1000 + 80
        }
        const reset = () => {
          gsap.set(leftBox,  { xPercent: lead, opacity: 0 })
          gsap.set(rightBox, { xPercent: trail, opacity: 0 })
        }
        ScrollTrigger.create({
          trigger: section,
          start: 'top 78%',
          onEnter: enter, onEnterBack: enter, onLeaveBack: reset,
        })
      }
    }

    // Per-section enter contract:
    //   .eyebrow / .sol-problem → char stagger (looks like a tag waking up).
    //   h2 / .bridge-em-text    → word-mask rise.
    //   .hero-sub / .sol-desc / paragraphs → fade-up + blur(8px → 0).
    //   CTA / .scroll-hint → simple fade-up.
    // Each one gets its own ScrollTrigger so the cadence within a section
    // reads as a sequence (tag → headline → body → cta) rather than a single
    // group fade. Replay on enter-back so scrolling backwards re-charges it.
    section.querySelectorAll('[data-line]').forEach((el) => {
      // The hero headline is owned by <AnimatedHeading>, do not double-wrap.
      if (el.classList.contains('hero-headline')) return

      // The box-slide trigger above already owns the wrapper's opacity, so
      // line-cascade pre-sets keep their motion (y / yPercent / blur) but
      // skip opacity:0 — otherwise the wrapper slides in carrying invisible
      // content and the side-entrance reads as empty.
      let initial, animated
      if (el.classList.contains('eyebrow') || el.classList.contains('sol-problem')) {
        const { chars } = splitElement(el, { type: 'chars, words' })
        if (!chars.length) return
        gsap.set(chars, { y: 12 })
        initial = chars
        animated = { y: 0, duration: 0.55, stagger: 0.022, ease: 'power3.out' }
      } else if (el.tagName === 'H1' || el.tagName === 'H2' || el.classList.contains('bridge-em-text')) {
        const { words } = splitElement(el, { type: 'words', mask: 'words' })
        if (!words.length) return
        gsap.set(words, { yPercent: 110 })
        initial = words
        animated = { yPercent: 0, duration: 1, stagger: 0.07, ease: 'power3.out' }
      } else if (el.classList.contains('hero-sub') || el.classList.contains('sol-desc') || el.tagName === 'P') {
        gsap.set(el, { y: 60, filter: 'blur(8px)' })
        initial = [el]
        animated = { y: 0, filter: 'blur(0px)', duration: 0.9, ease: 'power3.out' }
      } else {
        gsap.set(el, { y: 18 })
        initial = [el]
        animated = { y: 0, duration: 0.6, ease: 'power3.out' }
      }

      ScrollTrigger.create({
        trigger: el,
        // top 88% (not 75%): on short viewports a hero paragraph can sit
        // at ~83 % of viewport height even when it's clearly visible, so
        // a 75 % trigger leaves it stuck in its blur(8px) pre-state until
        // the user scrolls further. 88 % fires as soon as the line peeks
        // from below; the box-slide trigger (top 78 %) still runs first
        // because lines have higher absolute Y than the section top.
        start: 'top 88%',
        once: false,
        onEnter:     () => gsap.to(initial, animated),
        onEnterBack: () => gsap.to(initial, animated),
        onLeaveBack: () => {
          // Reset to initial state so the animation re-plays on re-entry.
          if (animated.yPercent !== undefined) gsap.set(initial, { yPercent: 110 })
          else if (animated.filter) gsap.set(initial, { y: 60, filter: 'blur(8px)' })
          else if (initial[0]?.classList?.contains('split-char') || initial.length > 1) gsap.set(initial, { y: 12 })
          else gsap.set(initial, { y: 18 })
        },
      })
    })

    if (art) {
      // Hero keeps the y + scale scrub because it's on-screen at page load
      // — there's no curtain entrance to compete with. Solution sections
      // get the full curtain side-slide above, so we drop the scrub here
      // to keep the motion language clean (one big move per box, not
      // three layered tweens).
      if (isHero) {
        gsap.set(art, { y: 100, scale: 0.96 })
        const artTl = gsap.timeline({
          scrollTrigger: {
            trigger: section,
            start: 'top 82%',
            end: 'top 20%',
            scrub: 0.8,
          },
        })
        artTl.to(art, {
          y: 0,
          scale: 1,
          duration: 1,
          ease: 'power3.out',
        })
      }

      // Animated SVGs ship with their entrance gated by `.animated` on the
      // svg root. We strip that class at build time (sed) and re-apply it
      // here so the entrance plays every time the section enters viewport
      // (and reverses out on leave-back, ready to replay on re-enter).
      // Critically: the gate fires on `top 35%` instead of `top 70%` so
      // the box has finished its curtain slide before the inner SVG starts
      // performing — otherwise the illustration's micro-animations play
      // while the whole box is still flying across the screen.
      const innerSvg = art.querySelector('svg[id^="freepik_stories"]')
      if (innerSvg) {
        const startSvg = isHero ? 'top 70%' : 'top 35%'
        ScrollTrigger.create({
          trigger: section,
          start: startSvg,
          end: 'bottom 30%',
          onEnter: () => innerSvg.classList.add('animated'),
          onEnterBack: () => innerSvg.classList.add('animated'),
          onLeave: () => innerSvg.classList.remove('animated'),
          onLeaveBack: () => innerSvg.classList.remove('animated'),
        })
      }
    }
  })

  // Footer-arrival fade — pushes both the floor rail AND the full-screen
  // background canvas (tint + topography) out of view as the dark footer
  // enters. Without this, the footer's dark surface bleeds through the
  // tint sheet as a green halo in its top-right corner.
  const railEl = page.querySelector('.floor-rail')
  const canvasEl = page.querySelector('.home-canvas')
  const footerEl = document.querySelector('footer')

  if (footerEl && !prefersReduced) {
    const updateFooterFade = () => {
      const vh = window.innerHeight
      const footerTop = footerEl.getBoundingClientRect().top
      // Start fading the moment the footer's top enters the viewport, and
      // be fully gone within ~10% of viewport so no green tint can bleed
      // through the dark footer once it's visible at all.
      const fadeStart = vh * 1.0
      const fadeEnd   = vh * 0.88
      let opacity
      if (footerTop >= fadeStart)      opacity = 1
      else if (footerTop <= fadeEnd)   opacity = 0
      else                             opacity = (footerTop - fadeEnd) / (fadeStart - fadeEnd)
      if (railEl) gsap.set(railEl, { opacity, y: 150 * (1 - opacity) })
      if (canvasEl) gsap.set(canvasEl, { opacity })
    }

    ScrollTrigger.create({
      start: 0,
      end: 'max',
      onUpdate: updateFooterFade,
      onRefresh: updateFooterFade,
    })
    updateFooterFade()
  }

}

onMounted(async () => {
  await nextTick()
  // Wrap the entire choreography in a gsap.context() scoped to the page
  // root. Every tween and ScrollTrigger created inside buildScrollChoreography
  // is tracked here and reverted in one call on unmount — no manual
  // triggers[] array, no risk of orphan ScrollTriggers when the user
  // navigates away from this view.
  choreographyCtx = gsap.context(() => buildScrollChoreography(), pageRef.value)
  // Global font/load/idle refresh is owned by armScrollTriggers() in
  // motion/scrollManager.js; no need for a separate load listener here.
})

onBeforeUnmount(() => {
  choreographyCtx?.revert()
  choreographyCtx = null
})
</script>

<style scoped>
/* ──────────────────────────────────────────────────────────────────
   Page shell + fixed background canvas
─────────────────────────────────────────────────────────────────── */
.home {
  width: 100%;
  position: relative;
  background: var(--color-warm-cream);
  /* Section-level overflow:hidden was lifted up here so the side-entrance
     boxes can start fully off-screen (xPercent: ±120) without each section
     clipping them at its own edge. The page itself still hides any
     horizontal overflow so the body never gets a horizontal scrollbar. */
  overflow-x: hidden;

  /* Per-section ambient tint. ScrollTrigger swaps these on entry so the
     whole canvas-tint sheet cross-fades between moods. Defaults = hero. */
  --bg-tint-a: #d4f3b5;
  --bg-tint-b: #fff5e1;
  --bg-tint-opacity: 0.06;
}

.home :deep(.navbar) {
  position: relative;
  z-index: 10;
  margin-bottom: 0;
}

/* Fixed canvas: stays put while content scrolls past. Soft decorative blobs
   + faint mint grid give every section the same backdrop, so there are
   no visible seams between sections. */
.home-canvas {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

/* Full-screen ambient tint sheet — replaces the four-corner blobs. The
   diagonal gradient is intentionally low-contrast so the tint reads as
   light, not as colour blocks. */
.canvas-tint {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: linear-gradient(
    160deg,
    var(--bg-tint-a) 0%,
    transparent 45%,
    transparent 60%,
    var(--bg-tint-b) 100%
  );
  opacity: 0.55;
  transition: background 800ms cubic-bezier(0.22, 1, 0.36, 1);
  will-change: background;
}

/* Hero Patterns "Topography" — full-page seamless contour texture.
   The SVG file has fill #163300 (dark-green); layer opacity controls
   intensity. Tiles 600×600 across the entire fixed canvas, giving every
   section a unified backdrop with no visible seams. */
.canvas-grid {
  position: absolute;
  inset: -240px 0;
  background-image: url('../assets/illustrations/bg-topography.svg');
  background-repeat: repeat;
  background-size: 600px 600px;
  opacity: var(--bg-tint-opacity, 0.06);
  will-change: background-position, opacity;
  transition: opacity 600ms ease;
}

/* canvas-blob-drift keyframe removed alongside the blobs — the new tint
   sheet doesn't need its own motion; the page itself moves under it. */

/* ──────────────────────────────────────────────────────────────────
   Story sections — shared layout
─────────────────────────────────────────────────────────────────── */
.story {
  position: relative;
  z-index: 1;
  min-height: 100vh;
  display: flex;
  align-items: center;
  padding: 60px 48px 160px;       /* extra bottom for global floor rail (130px + breathing room) */
  /* No overflow:hidden here — boxes need to start off-screen for the
     side-entrance. .home owns the page-level horizontal clip instead. */
}

.story-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1.05fr);
  gap: 64px;
  width: 100%;
  max-width: 1440px;
  margin: 0 auto;
  align-items: center;
  position: relative;
  z-index: 2;
}

/* ── Section index — giant background number anchoring each section ── */
.section-index {
  position: absolute;
  top: 28px;
  left: 36px;
  font-size: 240px;
  font-weight: 900;
  line-height: 0.8;
  letter-spacing: -0.04em;
  color: var(--color-primary);
  opacity: 0.08;
  pointer-events: none;
  z-index: 1;
  user-select: none;
}

.section-index--right {
  left: auto;
  right: 36px;
}

/* ── Section label — vertical typographic marker ── */
.section-label {
  position: absolute;
  top: 50%;
  left: 16px;
  transform: translateY(-50%) rotate(-90deg);
  transform-origin: left center;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.24em;
  color: var(--color-primary-text);
  opacity: 0.35;
  white-space: nowrap;
  pointer-events: none;
  z-index: 1;
}

.section-label--right {
  left: auto;
  right: 16px;
  transform: translateY(-50%) rotate(90deg);
  transform-origin: right center;
}

/* ── Sprinkles — small lucide icons sprinkled in the negative space ── */
.sprinkle {
  position: absolute;
  color: var(--color-primary-text);
  opacity: 0.28;
  pointer-events: none;
  z-index: 1;
  display: inline-flex;
}

.sprinkle--tag-1     { top: 18%; right: 8%; transform: rotate(-12deg); animation: sprinkle-bob 6s var(--motion-entrance) infinite; }
.sprinkle--leaf-1    { bottom: 22%; left: 4%; transform: rotate(8deg); animation: sprinkle-bob 7.5s var(--motion-entrance) infinite; animation-delay: -2s; }
.sprinkle--sparkle-1 { top: 64%; right: 14%; animation: sprinkle-twinkle 4s var(--motion-entrance) infinite; }

.sprinkle--shirt-1   { top: 14%; left: 6%; transform: rotate(-6deg); animation: sprinkle-bob 8s var(--motion-entrance) infinite; }
.sprinkle--tag-2     { bottom: 18%; right: 6%; transform: rotate(14deg); animation: sprinkle-bob 6.5s var(--motion-entrance) infinite; animation-delay: -1.4s; }
.sprinkle--check-1   { top: 70%; left: 7%; animation: sprinkle-twinkle 5s var(--motion-entrance) infinite; animation-delay: -2.5s; }

.sprinkle--leaf-2    { top: 20%; left: 10%; transform: rotate(-10deg); animation: sprinkle-bob 7s var(--motion-entrance) infinite; }
.sprinkle--droplet-1 { bottom: 22%; right: 11%; animation: sprinkle-bob 5.5s var(--motion-entrance) infinite; animation-delay: -1.8s; }

.sprinkle--check-2   { top: 22%; right: 9%; animation: sprinkle-twinkle 4.5s var(--motion-entrance) infinite; }
.sprinkle--leaf-3    { bottom: 26%; left: 6%; transform: rotate(12deg); animation: sprinkle-bob 7s var(--motion-entrance) infinite; animation-delay: -2.2s; }
.sprinkle--sparkle-2 { top: 60%; right: 16%; animation: sprinkle-twinkle 5s var(--motion-entrance) infinite; animation-delay: -1.5s; }

.sprinkle--sol-1     { top: 18%; left: 8%; transform: rotate(-8deg); animation: sprinkle-bob 7s var(--motion-entrance) infinite; }
.sprinkle--sol-2     { bottom: 22%; right: 9%; transform: rotate(10deg); animation: sprinkle-bob 6s var(--motion-entrance) infinite; animation-delay: -2s; }

@keyframes sprinkle-bob {
  0%, 100% { transform: translateY(0) rotate(var(--r, 0deg)); }
  50%      { transform: translateY(-8px) rotate(var(--r, 0deg)); }
}

@keyframes sprinkle-twinkle {
  0%, 100% { opacity: 0.18; transform: scale(0.9); }
  50%      { opacity: 0.4;  transform: scale(1.1); }
}

/* ── Story divider — thin lime-dotted seam between sections ── */
.story-divider {
  position: relative;
  z-index: 1;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 24px 0;
}

.story-divider span {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--color-primary);
  opacity: 0.5;
}

.story-divider span:nth-child(2) {
  width: 80px;
  height: 1px;
  border-radius: 0;
  background: linear-gradient(to right, transparent, var(--color-primary-text) 50%, transparent);
  opacity: 0.4;
}

.story-grid--reverse {
  grid-template-columns: minmax(0, 1.05fr) minmax(0, 1fr);
}

.story-text {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.story-art {
  display: flex;
  align-items: center;
  justify-content: center;
}

.story-art :deep(svg) {
  width: 100%;
  height: auto;
  max-width: 580px;
  display: block;
}

/* ── Shared eyebrow ── */
.eyebrow {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--color-primary-text);
  margin-bottom: 24px;
}

/* ──────────────────────────────────────────────────────────────────
   §1 Hero
─────────────────────────────────────────────────────────────────── */
.story--hero {
  padding-top: 40px;
}

.hero-headline {
  font-size: 96px;
  font-weight: 900;
  line-height: 0.86;
  letter-spacing: -0.02em;
  color: var(--color-text);
  margin-bottom: 32px;
}

.hero-line {
  display: block;
}

.hero-sub {
  font-size: 17px;
  font-weight: 500;
  color: var(--color-text-muted);
  line-height: 1.55;
  margin-bottom: 14px;
  max-width: 540px;
}

.hero-sub--solution {
  border-left: 3px solid var(--color-primary);
  padding-left: 16px;
  color: var(--color-text);
  font-weight: 500;
  margin-bottom: 22px;
}
.hero-sub--solution strong {
  color: var(--color-primary-text);
  font-weight: 800;
}

.scroll-hint {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-subtle);
  letter-spacing: 0.04em;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.scroll-hint__arrow {
  display: inline-block;
  font-size: 16px;
  color: var(--color-primary-text);
  animation: scroll-hint-rock 1.8s var(--motion-entrance) infinite;
}

/* Journey entry CTA row — primary action goes straight to /wardrobe so the
   user lands on Step 1 (KNOW). Secondary scrolls into the story for the
   "want context first" reader. */
.hero-cta-row {
  display: inline-flex;
  align-items: center;
  gap: 22px;
  flex-wrap: wrap;
  margin-top: 6px;
}

.hero-cta-primary {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 14px 28px;
  border-radius: var(--radius-pill);
  font-size: 15px;
  font-weight: 700;
  color: var(--color-primary-text);
  background: var(--color-primary);
  border: 1px solid transparent;
  cursor: pointer;
  text-decoration: none;
  transition:
    transform 200ms var(--motion-entrance),
    background 200ms var(--motion-entrance);
}

.hero-cta-primary:hover {
  transform: scale(1.03);
  background: var(--color-primary-dark);
}

.hero-cta-secondary {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 4px;
  background: transparent;
  border: none;
  font-size: 13.5px;
  font-weight: 700;
  letter-spacing: 0.02em;
  color: var(--color-text-subtle);
  cursor: pointer;
  transition: color 200ms var(--motion-entrance);
}

.hero-cta-secondary:hover {
  color: var(--color-primary-text);
}

.hero-cta-secondary__arrow {
  display: inline-block;
  font-size: 14px;
  color: var(--color-primary-text);
  animation: scroll-hint-rock 1.8s var(--motion-entrance) infinite;
}

/* Hero scroll-cue hexagon — anchored to the bottom-centre of the hero
   section, sits just above the floor rail so the river never overlaps it. */
.hero-scroll-down {
  position: absolute;
  bottom: 148px;
  left: 50%;
  transform: translateX(-50%);
  width: 56px;
  height: 64px;
  display: grid;
  place-items: center;
  background: transparent;
  border: none;
  padding: 0;
  cursor: pointer;
  z-index: 6;
  animation: hero-scroll-down-bob 2.4s ease-in-out infinite;
}

.hero-scroll-down__hex {
  position: absolute;
  inset: 0;
  background: var(--color-primary);
  /* Pointy-top hexagon clip; box-shadow cannot follow clip-path so we use
     a drop-shadow filter on the parent instead. */
  clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
  transition: background 240ms ease, transform 240ms ease;
}

.hero-scroll-down:hover .hero-scroll-down__hex {
  background: var(--color-primary-text);
  transform: scale(1.08);
}

.hero-scroll-down__icon {
  position: relative;
  z-index: 1;
  color: var(--color-primary-text);
  transition: color 240ms ease, transform 240ms ease;
}

.hero-scroll-down:hover .hero-scroll-down__icon {
  color: var(--color-primary);
  transform: translateY(2px);
}

.hero-scroll-down:focus-visible {
  outline: none;
}
.hero-scroll-down:focus-visible .hero-scroll-down__hex {
  background: var(--color-primary-text);
  outline: 2px solid var(--color-primary);
  outline-offset: 4px;
}

@keyframes hero-scroll-down-bob {
  0%, 100% { transform: translate(-50%, 0); }
  50%      { transform: translate(-50%, 6px); }
}

@keyframes scroll-hint-rock {
  0%, 100% { transform: rotate(-2deg); }
  50%      { transform: rotate(2deg); }
}

/* Hero illustration — large, no frame. The animated SVG already has its
   own background shapes, so it sits unframed on the cream canvas. */
.story-art--hero :deep(svg) {
  max-width: 620px;
  filter: drop-shadow(0 24px 60px rgba(22, 51, 0, 0.08));
}

/* ──────────────────────────────────────────────────────────────────
   §2 Familiar — wardrobe + questions
─────────────────────────────────────────────────────────────────── */
.story--familiar h2 {
  font-size: 64px;
  font-weight: 900;
  line-height: 0.88;
  letter-spacing: -0.01em;
  color: var(--color-text);
  margin-bottom: 32px;
}

.questions {
  position: relative;
  margin-bottom: 36px;
}

.questions p {
  font-size: 20px;
  font-style: italic;
  font-weight: 500;
  color: var(--color-text-muted);
  line-height: 1.5;
  margin-bottom: 12px;
}

.familiar-stat {
  font-size: 15px;
  font-weight: 500;
  color: var(--color-text-subtle);
  line-height: 1.6;
  margin-top: 24px;
}

.familiar-stat strong {
  color: var(--color-primary-text);
  font-weight: 700;
}

/* Wardrobe scene loops + glow choreography */
.story-art--wardrobe :deep(svg) {
  max-width: 540px;
  filter: drop-shadow(0 24px 60px rgba(22, 51, 0, 0.08));
}

.story-art--wardrobe :deep(.wardrobe-item) {
  transition: filter 250ms var(--motion-entrance);
}

.story--familiar.q1-active :deep(.wardrobe-item-1),
.story--familiar.q2-active :deep(.wardrobe-item-3),
.story--familiar.q3-active :deep(.wardrobe-item-8) {
  filter: drop-shadow(0 0 14px rgba(159, 232, 112, 0.85));
  animation: wardrobe-pulse 1.6s var(--motion-entrance) 1;
}

.story--familiar.stat-active :deep(.wardrobe-item-1),
.story--familiar.stat-active :deep(.wardrobe-item-2),
.story--familiar.stat-active :deep(.wardrobe-item-3),
.story--familiar.stat-active :deep(.wardrobe-item-5),
.story--familiar.stat-active :deep(.wardrobe-item-6),
.story--familiar.stat-active :deep(.wardrobe-item-7),
.story--familiar.stat-active :deep(.wardrobe-item-8),
.story--familiar.stat-active :deep(.wardrobe-item-10),
.story--familiar.stat-active :deep(.wardrobe-item-11),
.story--familiar.stat-active :deep(.wardrobe-item-13),
.story--familiar.stat-active :deep(.wardrobe-item-14) {
  filter: drop-shadow(0 0 8px rgba(159, 232, 112, 0.55));
}

@keyframes wardrobe-pulse {
  0%, 100% { transform: translateY(0) scale(1); }
  40%      { transform: translateY(-2px) scale(1.04); }
}

.story-art--wardrobe :deep(.wardrobe-shadow) {
  animation: wardrobe-shadow-shift 8s var(--motion-entrance) infinite;
  transform-box: fill-box;
}

@keyframes wardrobe-shadow-shift {
  0%, 100% { transform: translateX(0); opacity: 0.18; }
  50%      { transform: translateX(2px); opacity: 0.26; }
}

/* ──────────────────────────────────────────────────────────────────
   §3 Hidden Cost — three motif columns on cream
─────────────────────────────────────────────────────────────────── */
.story--cost {
  flex-direction: column;
  justify-content: center;
}

.cost-content {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
}

.cost-content .eyebrow {
  margin-bottom: 56px;
}

.stat-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 64px;
}

.stat-col {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 18px;
  padding: 32px 24px;
  border: 1px dashed rgba(22, 51, 0, 0.18);
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(4px);
}

.stat-corner {
  position: absolute;
  width: 14px;
  height: 14px;
  border-color: var(--color-primary-text);
  border-style: solid;
  border-width: 0;
}
.stat-corner--tl { top: -1px; left: -1px;  border-top-width: 2px; border-left-width: 2px; }
.stat-corner--tr { top: -1px; right: -1px; border-top-width: 2px; border-right-width: 2px; }
.stat-corner--bl { bottom: -1px; left: -1px;  border-bottom-width: 2px; border-left-width: 2px; }
.stat-corner--br { bottom: -1px; right: -1px; border-bottom-width: 2px; border-right-width: 2px; }

.stat-index {
  position: absolute;
  top: 8px;
  left: 12px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.18em;
  color: var(--color-primary-text);
  opacity: 0.5;
}

.stat-motif {
  width: 200px;
  height: 200px;
  display: block;
}

.stat-motif :deep(svg) {
  width: 100%;
  height: 100%;
}

.stat-motif :deep(.fiber-strand) {
  animation: fiber-flow 5s linear infinite;
}
.stat-motif :deep(.fiber-strand-1) { animation-delay: 0s; }
.stat-motif :deep(.fiber-strand-2) { animation-delay: -1.6s; }
.stat-motif :deep(.fiber-strand-3) { animation-delay: -3.2s; }
.stat-motif :deep(.fiber-cross) {
  animation: fiber-cross-fade 4s var(--motion-entrance) infinite;
}

@keyframes fiber-flow {
  0%   { stroke-dashoffset: 240; }
  100% { stroke-dashoffset: 0; }
}
@keyframes fiber-cross-fade {
  0%, 100% { opacity: 0.3; }
  50%      { opacity: 0.8; }
}

.stat-motif :deep(.co2-cloud) {
  animation: co2-drift 6s var(--motion-entrance) infinite;
  transform-box: fill-box;
}
.stat-motif :deep(.co2-wisp) {
  animation: co2-wisp-fade 4s var(--motion-entrance) infinite;
}
.stat-motif :deep(.co2-wisp-1) { animation-delay: 0s; }
.stat-motif :deep(.co2-wisp-2) { animation-delay: -1.3s; }
.stat-motif :deep(.co2-wisp-3) { animation-delay: -2.6s; }

@keyframes co2-drift {
  0%, 100% { transform: translateY(0); }
  50%      { transform: translateY(-6px); }
}
@keyframes co2-wisp-fade {
  0%, 100% { opacity: 0.2; transform: translateY(0); }
  50%      { opacity: 1;   transform: translateY(-8px); }
}

.stat-motif :deep(.water-drop) {
  animation: water-drop-fall 2.5s linear infinite;
  transform-box: fill-box;
  transform-origin: center;
}
.stat-motif :deep(.water-ripple) {
  animation: water-ripple 2.5s linear infinite;
  transform-box: fill-box;
  transform-origin: 120px 200px;
}
.stat-motif :deep(.water-ripple-2) {
  animation-delay: -0.4s;
}

@keyframes water-drop-fall {
  0%   { transform: translateY(0) scale(1); opacity: 1; }
  70%  { transform: translateY(60px) scale(1, 1.1); opacity: 1; }
  72%  { transform: translateY(72px) scale(1.4, 0.4); opacity: 1; }
  78%  { opacity: 0; }
  100% { transform: translateY(0) scale(1); opacity: 0; }
}
@keyframes water-ripple {
  0%, 70% { transform: scale(0.4); opacity: 0; }
  72%     { transform: scale(0.6); opacity: 1; }
  100%    { transform: scale(1.8); opacity: 0; }
}

.stat-num {
  font-size: 64px;
  font-weight: 900;
  color: var(--color-text);
  line-height: 0.85;
  letter-spacing: -0.02em;
  display: inline-flex;
  align-items: baseline;
  gap: 4px;
  margin: 0;
}

.stat-suffix {
  font-size: 28px;
  font-weight: 700;
  color: var(--color-primary-text);
}

.stat-lbl {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-muted);
  line-height: 1.5;
  max-width: 240px;
}

/* ──────────────────────────────────────────────────────────────────
   §4 Bridge — examining character + emphasised promise
─────────────────────────────────────────────────────────────────── */
.story--bridge h2 {
  font-size: 64px;
  font-weight: 900;
  line-height: 0.88;
  letter-spacing: -0.01em;
  color: var(--color-text);
  margin-bottom: 28px;
}

.bridge-sub {
  font-size: 22px;
  font-weight: 500;
  color: var(--color-text-muted);
  line-height: 1.4;
  margin-bottom: 32px;
}

.bridge-em {
  position: relative;
  display: inline-block;
  font-size: 28px;
  font-weight: 800;
  color: var(--color-text);
  line-height: 1.3;
  margin-bottom: 28px;
}

.bridge-em-text {
  position: relative;
  z-index: 1;
}

.bridge-em-underline {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 4px;
  height: 12px;
  background: var(--color-primary);
  z-index: 0;
  transform-origin: left center;
  transform: scaleX(0);
  transition: transform 700ms var(--motion-stroke-draw) 200ms;
}

.story--bridge [data-reveal].is-revealed .bridge-em-underline,
.bridge-em.is-on .bridge-em-underline {
  transform: scaleX(1);
}

/* When [data-line] reaches full opacity (handled by GSAP), trigger underline. */
.bridge-em[style*="opacity: 1"] .bridge-em-underline {
  transform: scaleX(1);
}

.bridge-hint {
  font-size: 14px;
  color: var(--color-text-subtle);
}

.story-art--bridge :deep(svg) {
  max-width: 600px;
  filter: drop-shadow(0 24px 60px rgba(22, 51, 0, 0.08));
}

/* ──────────────────────────────────────────────────────────────────
   §5–7 Solutions
─────────────────────────────────────────────────────────────────── */
.story--solution h2 {
  font-size: 56px;
  font-weight: 900;
  line-height: 0.9;
  letter-spacing: -0.01em;
  color: var(--color-text);
  margin-bottom: 24px;
}

.sol-problem {
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--color-primary-text);
  margin-bottom: 18px;
}

.sol-desc {
  font-size: 17px;
  color: var(--color-text-muted);
  line-height: 1.55;
  margin-bottom: 32px;
  max-width: 480px;
}

.sol-cta {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 14px 28px;
  background: var(--color-primary);
  color: var(--color-primary-text);
  font-weight: 700;
  font-size: 15px;
  border-radius: var(--radius-pill);
  border: 1px solid transparent;
  text-decoration: none;
  transition: transform 200ms var(--motion-entrance), background 200ms var(--motion-entrance);
  align-self: flex-start;
}

.sol-cta:hover {
  transform: scale(1.03);
  background: var(--color-primary-dark);
}

.story-art--solution :deep(svg) {
  max-width: 560px;
  filter: drop-shadow(0 24px 60px rgba(22, 51, 0, 0.08));
}

/* ──────────────────────────────────────────────────────────────────
   Global floor rail — fixed at viewport bottom, swaps with active section.
   Stays present at all times; on section change items animate out then in.
─────────────────────────────────────────────────────────────────── */
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
  /* Cream veil — top is airy so the lime river surface reads against the
     page; bottom settles back to the cream floor under drifting items. */
  background: linear-gradient(
    to bottom,
    transparent 0%,
    rgba(246, 240, 230, 0.18) 35%,
    rgba(246, 240, 230, 0.78) 78%,
    rgba(246, 240, 230, 0.95) 100%
  );
}

/* Lime "river" — two parallax water layers under a brighter surface edge.
   Each layer SVG is 2× viewport wide and animates translateX -50% to loop
   seamlessly; back layer drifts slower / paler for depth. */
.floor-river {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 80px;
  pointer-events: none;
  overflow: hidden;
}

.river-layer {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 200%;
  display: block;
  will-change: transform;
}

.river-layer--back  { animation: river-drift 22s linear infinite; opacity: 0.85; }
.river-layer--front { animation: river-drift 14s linear infinite; opacity: 1; }

@keyframes river-drift {
  from { transform: translateX(0); }
  to   { transform: translateX(-50%); }
}

.river-edge {
  position: absolute;
  left: 0;
  right: 0;
  top: 28px;
  width: 100%;
  height: 24px;
  pointer-events: none;
}

/* Single flow container — items inside travel left → right via CSS. */
.floor-flow {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 100%;
  pointer-events: none;
}

/* Caption below shows which section the floor belongs to */
.floor-rail__caption {
  position: absolute;
  bottom: 10px;
  right: 28px;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--color-primary-text);
  opacity: 0.4;
  transition: opacity 240ms var(--motion-entrance);
}

/* SVG icons travel left → right.
   Each img is absolutely positioned; left:0 + animation translates
   X from -10vw to 110vw. Negative animation-delay scatters items along
   the path so the rail is always populated. */
.floor-item {
  position: absolute;
  bottom: 38px;          /* sit just above the surface highlight line */
  left: 0;
  width: 56px;
  height: 56px;
  object-fit: contain;
  pointer-events: none;
  animation: floor-travel 36s linear infinite;
  animation-delay: calc(var(--i, 0) * -5.2s);
  will-change: transform, opacity;
}

/* Mild duration + height variety so items don't all march in sync */
.floor-item:nth-child(2) { animation-duration: 40s; bottom: 46px; width: 52px; height: 52px; }
.floor-item:nth-child(3) { animation-duration: 32s; bottom: 40px; }
.floor-item:nth-child(4) { animation-duration: 38s; bottom: 42px; width: 60px; height: 60px; }
.floor-item:nth-child(5) { animation-duration: 42s; bottom: 50px; }
.floor-item:nth-child(6) { animation-duration: 35s; bottom: 44px; width: 50px; height: 50px; }
.floor-item:nth-child(7) { animation-duration: 39s; bottom: 48px; }

@keyframes floor-travel {
  0%   { transform: translateX(-10vw) scale(0.7) rotate(-4deg); opacity: 0; }
  8%   { opacity: 0.85; }
  50%  { transform: translateX(50vw) scale(1) rotate(0deg);     opacity: 0.9; }
  92%  { opacity: 0.85; }
  100% { transform: translateX(110vw) scale(0.7) rotate(4deg);  opacity: 0; }
}

/* ──────────────────────────────────────────────────────────────────
   Side progress rail — fixed right, tracks current section
─────────────────────────────────────────────────────────────────── */
.progress-rail {
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

.rail-dot {
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

.rail-dot:hover {
  color: var(--color-primary-text);
}

.rail-dot__num {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.12em;
  width: 18px;
  text-align: right;
  opacity: 0.6;
  transition: opacity 240ms var(--motion-entrance);
}

.rail-dot__core {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgba(22, 51, 0, 0.25);
  transition: all 280ms var(--motion-entrance);
}

.rail-dot__label {
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

.rail-dot:hover .rail-dot__label,
.rail-dot--active .rail-dot__label {
  opacity: 1;
  transform: translateY(-50%) translateX(0);
}

.rail-dot--active .rail-dot__core {
  background: var(--color-primary);
  width: 14px;
  height: 14px;
  box-shadow: 0 0 0 4px rgba(159, 232, 112, 0.25);
}

.rail-dot--active .rail-dot__num {
  opacity: 1;
  color: var(--color-primary-text);
}

/* ──────────────────────────────────────────────────────────────────
   Reduced motion
─────────────────────────────────────────────────────────────────── */
@media (prefers-reduced-motion: reduce) {
  .canvas-tint {
    transition: none;
  }
  .sprinkle,
  .floor-item,
  .river-layer {
    animation: none;
  }
  /* Distribute items evenly along path when reduced-motion is on */
  .floor-item {
    transform: translateX(calc(8vw + var(--i, 0) * 16vw)) scale(1);
    opacity: 0.85;
  }
  .scroll-hint__arrow {
    animation: none;
  }
}

/* ──────────────────────────────────────────────────────────────────
   Responsive
─────────────────────────────────────────────────────────────────── */
@media (max-width: 1024px) {
  .hero-headline { font-size: 72px; }
  .story--familiar h2,
  .story--bridge h2 { font-size: 48px; }
  .story--solution h2 { font-size: 42px; }
  .stat-num { font-size: 52px; }
  .story-grid { gap: 56px; }
}

/* Short-laptop tier: 13-15" screens where width is fine but vertical
   height is tight (≤820 px). Compress the hero so the scroll-cue
   hexagon and the auxiliary "Still curious?" hint both fit above the
   fold without forcing the user to scroll. */
@media (max-height: 820px) and (min-width: 1025px) {
  .story {
    padding: 36px 48px 110px;
    min-height: auto;
  }
  .hero-headline {
    font-size: 64px;
    margin-bottom: 20px;
  }
  .eyebrow { margin-bottom: 14px; }
  .hero-sub { font-size: 15px; margin-bottom: 10px; }
  .hero-sub--solution { margin-bottom: 14px; padding-left: 12px; }
  .story-art :deep(svg) { max-height: 56vh; }
  .scroll-hint { display: none; }
  .hero-scroll-down {
    bottom: 86px;
    width: 48px;
    height: 56px;
  }
}

@media (max-width: 1024px) {
  .progress-rail {
    display: none;
  }
}

@media (max-width: 768px) {
  .story {
    padding: 56px 20px 110px;
    min-height: auto;
  }
  .floor-rail {
    height: 90px;
  }
  .floor-river { height: 56px; }
  .river-edge { top: 18px; height: 18px; }
  .floor-rail__items {
    padding: 0 16px 12px;
    gap: 6px;
  }
  .floor-item {
    width: 44px;
    height: 44px;
    bottom: 28px;
  }
  .floor-item:nth-child(2) { bottom: 32px; }
  .floor-item:nth-child(3) { bottom: 30px; }
  .floor-item:nth-child(4) { bottom: 30px; }
  .floor-item:nth-child(5) { bottom: 36px; }
  .floor-item:nth-child(6) { bottom: 32px; }
  .floor-item:nth-child(7) { bottom: 34px; }
  .floor-item :deep(svg) { width: 22px; height: 22px; }
  .floor-rail__caption { display: none; }
  .story-grid,
  .story-grid--reverse {
    grid-template-columns: 1fr;
    gap: 40px;
  }
  /* Hide heavy decorations on small screens to keep content focus */
  .section-index,
  .section-label,
  .sprinkle,
  .big-quote--questions {
    display: none;
  }
  .big-quote--open {
    font-size: 80px;
    top: -20px;
    left: -16px;
  }
  .stat-col {
    padding: 24px 18px;
  }
  /* Art always renders below text on mobile */
  .story-art {
    order: 2;
  }
  .story-text {
    order: 1;
  }
  .hero-headline { font-size: 56px; }
  .story--familiar h2,
  .story--bridge h2 { font-size: 40px; }
  .story--solution h2 { font-size: 34px; }
  .stat-row {
    grid-template-columns: 1fr;
    gap: 48px;
  }
  .canvas-tint {
    opacity: 0.45;
  }
}
</style>
