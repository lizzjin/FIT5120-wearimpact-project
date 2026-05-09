<template>
  <div class="home" ref="pageRef">
    <Navbar />

    <!-- Fixed background canvas — does NOT scroll with content.
         Unified backdrop across all sections so there are no visible seams.
         Two soft lime/mint blobs drift, three abstract shapes orbit slowly,
         and a faint mint grid anchors the depth. Each element has its own
         period so they never pulse together. -->
    <div class="home-canvas" aria-hidden="true">
      <span class="canvas-blob canvas-blob--tr" />
      <span class="canvas-blob canvas-blob--bl" />
      <span class="canvas-blob canvas-blob--mid" />
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
          <h1 class="hero-headline">
            <span class="hero-line" data-line>Wear it longer.</span>
            <span class="hero-line" data-line>Waste it less.</span>
            <span class="hero-line" data-line>Look better doing both.</span>
          </h1>
          <p class="hero-sub" data-line>
            Fashion leaves a footprint long before it reaches your wardrobe.
            WearImpact helps you choose better, buy second-hand, and make
            more of what you already own.
          </p>
          <p class="hero-sub hero-sub--solution" data-line>
            <strong>That's why WearImpact exists:</strong> to make sustainable
            fashion easier to understand, easier to find, and easier to act on.
          </p>
          <span class="scroll-hint" data-line>
            Still curious?
            <span class="scroll-hint__arrow" aria-hidden="true">↓</span>
          </span>
        </div>
        <div class="story-art story-art--hero" data-art v-html="artHero" aria-hidden="true" />
      </div>
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
            <router-link :to="sol.link" class="sol-cta" data-line>
              {{ sol.cta }}
              <ArrowRight :size="17" :stroke-width="2.5" class="cta-arrow" />
            </router-link>
          </div>
          <div class="story-art story-art--solution" data-art v-html="sol.art" aria-hidden="true" />
        </div>
      </section>
      <div v-if="i < solutions.length - 1" class="story-divider" aria-hidden="true"><span /><span /><span /></div>
    </template>

    <!-- Global floor rail — fixed at viewport bottom. Single shared set of
         SVG icons flowing left → right continuously, identical across all
         sections. Footer fade hides the whole rail when reaching footer. -->
    <div class="floor-rail" aria-hidden="true">
      <!-- Wavy lime ground line — shared baseline. -->
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
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import Navbar from '../components/Navbar.vue'
import FooterSection from '../components/FooterSection.vue'
import {
  ArrowRight,
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

gsap.registerPlugin(ScrollTrigger)

const pageRef = ref(null)
const triggers = []

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
      'Snap your clothes — we sort, tag, and store them in your browser. No login, no cloud. Then ask the AI advisor for outfit ideas built only from what you actually own.',
    cta: 'Open My Wardrobe',
    link: '/wardrobe',
    art: artBridge,
    labelTag: 'YOUR CLOSET',
    sprinkleA: Shirt,
    sprinkleB: Sparkles,
  },
  {
    id: 3,
    problem: "You want to shop sustainably — but you don't know where to start.",
    title: 'Find second-hand stores near you.',
    description:
      'WearImpact maps every op-shop, donation point and textile recycling centre within your chosen radius — with directions and opening hours.',
    cta: 'Find Eco-Shops Near Me',
    link: '/eco-shop',
    art: artThrift,
    labelTag: 'ACT',
    sprinkleA: MapPin,
    sprinkleB: Compass,
  },
  {
    id: 4,
    problem: 'A brand says "sustainable." But is it really?',
    title: 'See how transparent your brands are.',
    description:
      'Search any clothing brand and see its real score — across policy, environment, and supply chain — based on the Fashion Transparency Index.',
    cta: 'Search a Brand',
    link: '/brand-search',
    art: artWindowShop,
    labelTag: 'EVALUATE',
    sprinkleA: Search,
    sprinkleB: ShieldCheck,
  },
  {
    id: 5,
    problem: "It's hard to choose better when you don't know what to look for.",
    title: 'Learn what actually matters.',
    description:
      'WearImpact breaks down the real issues — materials, supply chains, waste — in plain language so you can make more informed choices.',
    cta: 'Start Learning',
    link: '/knowledge',
    art: artKnowledge,
    labelTag: 'DISCOVER',
    sprinkleA: BookOpen,
    sprinkleB: Lightbulb,
  },
]

// Scroll-progress reveal: every section's lines + art rise from below as the
// section enters. `scrub` ties the animation to scroll position so reverse
// scroll un-reveals — the page feels like it tracks the wheel exactly.
function buildScrollChoreography() {
  const page = pageRef.value
  if (!page) return

  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches

  page.querySelectorAll('.story').forEach((section) => {
    const lines = section.querySelectorAll('[data-line]')
    const art = section.querySelector('[data-art]')

    // Track active section for the side progress rail + global floor swap
    const sectionKey = section.dataset.section
    if (sectionKey) {
      const railTrig = ScrollTrigger.create({
        trigger: section,
        start: 'top 50%',
        end: 'bottom 50%',
        onEnter:     () => (activeSectionKey.value = sectionKey),
        onEnterBack: () => (activeSectionKey.value = sectionKey),
      })
      triggers.push(railTrig)
    }

    if (prefersReduced) {
      gsap.set([...lines, art].filter(Boolean), { opacity: 1, y: 0 })
      return
    }

    if (lines.length) {
      gsap.set(lines, { opacity: 0, y: 36 })
      const linesTl = gsap.timeline({
        scrollTrigger: {
          trigger: section,
          start: 'top 78%',
          end: 'top 30%',
          scrub: 0.6,
        },
      })
      linesTl.to(lines, {
        opacity: 1,
        y: 0,
        duration: 1,
        stagger: 0.15,
        ease: 'power2.out',
      })
      triggers.push(linesTl.scrollTrigger)
    }

    if (art) {
      gsap.set(art, { opacity: 0, y: 80, scale: 0.94 })
      const artTl = gsap.timeline({
        scrollTrigger: {
          trigger: section,
          start: 'top 82%',
          end: 'top 20%',
          scrub: 0.8,
        },
      })
      artTl.to(art, {
        opacity: 1,
        y: 0,
        scale: 1,
        duration: 1,
        ease: 'power3.out',
      })
      triggers.push(artTl.scrollTrigger)

      // Animated SVGs ship with their entrance gated by `.animated` on the
      // svg root. We strip that class at build time (sed) and re-apply it
      // here so the entrance plays every time the section enters viewport
      // (and reverses out on leave-back, ready to replay on re-enter).
      const innerSvg = art.querySelector('svg[id^="freepik_stories"]')
      if (innerSvg) {
        const replayTrig = ScrollTrigger.create({
          trigger: section,
          start: 'top 70%',
          end: 'bottom 30%',
          onEnter: () => innerSvg.classList.add('animated'),
          onEnterBack: () => innerSvg.classList.add('animated'),
          onLeave: () => innerSvg.classList.remove('animated'),
          onLeaveBack: () => innerSvg.classList.remove('animated'),
        })
        triggers.push(replayTrig)
      }
    }
  })

  // Floor rail — only footer fade is dynamic now.
  // The rail content (single shared SVG flow) loops continuously via CSS;
  // we just need to push the rail out of view when the footer arrives.
  const railEl = page.querySelector('.floor-rail')
  const footerEl = document.querySelector('footer')

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

    const railTrig = ScrollTrigger.create({
      start: 0,
      end: 'max',
      onUpdate: updateRail,
      onRefresh: updateRail,
    })
    triggers.push(railTrig)
    updateRail()
  }

}

onMounted(async () => {
  await nextTick()
  buildScrollChoreography()
  // Refresh once after fonts/images settle so trigger positions are accurate.
  window.addEventListener('load', () => ScrollTrigger.refresh())
})

onBeforeUnmount(() => {
  triggers.forEach((t) => t?.kill?.())
  triggers.length = 0
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

.canvas-blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(70px);
  opacity: 0.55;
}

.canvas-blob--tr {
  top: -120px;
  right: -160px;
  width: 520px;
  height: 520px;
  background: radial-gradient(circle, var(--color-primary) 0%, transparent 70%);
  animation: canvas-blob-drift 22s ease-in-out infinite;
}

.canvas-blob--bl {
  bottom: -180px;
  left: -200px;
  width: 620px;
  height: 620px;
  background: radial-gradient(circle, var(--color-mint) 0%, transparent 70%);
  animation: canvas-blob-drift 28s ease-in-out infinite reverse;
}

.canvas-blob--mid {
  top: 38%;
  left: 42%;
  width: 360px;
  height: 360px;
  background: radial-gradient(circle, var(--color-pastel-green) 0%, transparent 70%);
  opacity: 0.28;
  animation: canvas-blob-drift 36s ease-in-out infinite;
  animation-delay: -12s;
}

/* Hero Patterns "Topography" — full-page seamless contour texture.
   The SVG file has fill #163300 (dark-green); layer opacity controls
   intensity. Tiles 600×600 across the entire fixed canvas, giving every
   section a unified backdrop with no visible seams. */
.canvas-grid {
  position: absolute;
  inset: 0;
  background-image: url('../assets/illustrations/bg-topography.svg');
  background-repeat: repeat;
  background-size: 600px 600px;
  opacity: 0.06;
}

@keyframes canvas-blob-drift {
  0%, 100% { transform: translate(0, 0) scale(1); }
  50%      { transform: translate(40px, -30px) scale(1.06); }
}

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
  overflow: hidden;
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
  text-decoration: none;
  transition: transform 280ms var(--motion-entrance), box-shadow 280ms var(--motion-entrance);
  align-self: flex-start;
  box-shadow: 0 0 0 0 rgba(22, 51, 0, 0);
}

.sol-cta:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(22, 51, 0, 0.18);
}

.sol-cta .cta-arrow {
  transition: transform 280ms var(--motion-entrance);
}

.sol-cta:hover .cta-arrow {
  transform: translateX(3px);
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
  /* Cream gradient veil so items pop above page content */
  background: linear-gradient(
    to bottom,
    transparent 0%,
    rgba(246, 240, 230, 0.35) 30%,
    rgba(246, 240, 230, 0.85) 70%,
    rgba(246, 240, 230, 0.95) 100%
  );
}

/* Wavy lime ground — shared baseline across all sections */
.floor-rail__wave {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 38px;
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

/* Mild duration + height variety so items don't all march in sync */
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
  .canvas-blob--tr,
  .canvas-blob--bl,
  .canvas-blob--mid,
  .sprinkle,
  .floor-item {
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
  .floor-rail__items {
    padding: 0 16px 12px;
    gap: 6px;
  }
  .floor-item {
    width: 44px;
    height: 44px;
  }
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
  .canvas-blob {
    filter: blur(50px);
    opacity: 0.4;
  }
}
</style>
