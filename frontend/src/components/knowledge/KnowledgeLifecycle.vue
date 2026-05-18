<template>
  <section class="kh-life">
    <header class="kh-life__head">
      <button type="button" class="kh-life__back" @click="$emit('back')">
        <ArrowLeft :size="16" :stroke-width="2" /> Back
      </button>
      <div class="kh-life__heading">
        <p class="kh-life__eyebrow" ref="eyebrowRef">STEP 02 · LIFECYCLE OF A GARMENT</p>
        <AnimatedHeading
          as="h2"
          class="kh-life__title"
          text="From cotton field to landfill — every stage leaves a footprint."
          mode="word"
          :stagger="0.06"
        />
      </div>
    </header>

    <!-- Top half: text on the left, video on the right -->
    <div class="kh-life__split">
      <div ref="copyRef" class="kh-life__copy">
        <h3 class="kh-life__copy-title">A garment lives many lives</h3>
        <p>
          Before a piece of clothing reaches your wardrobe, it has already
          travelled through farms, factories, dye houses, container ships and
          warehouses across several continents. Each step burns energy,
          consumes water, and emits greenhouse gases.
        </p>
        <p>
          The video on the right walks through that journey end-to-end. The
          timeline beneath shows where each stage sits in the global apparel
          industry's footprint — based on
          <em>Quantis 2018: Measuring Fashion</em>, the most-cited
          sector-wide LCA study to date.
        </p>
        <p class="kh-life__copy-callout">
          <Sparkles :size="14" :stroke-width="2" />
          <span>
            <strong>Dyeing &amp; finishing</strong> alone accounts for 36% of
            apparel's climate impact — more than any other production stage.
          </span>
        </p>
      </div>

      <div ref="videoRef" class="kh-life__video">
        <div class="kh-life__video-frame">
          <iframe
            src="https://www.youtube.com/embed/BiSYoeqb_VY?rel=0"
            title="Lifecycle of a garment"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            allowfullscreen
            loading="lazy"
          ></iframe>
        </div>
      </div>
    </div>

    <!-- Timeline -->
    <section class="kh-life__timeline-wrap">
      <header class="kh-life__timeline-head">
        <p class="kh-life__timeline-eyebrow">THE 7-STAGE FOOTPRINT</p>
        <h3 class="kh-life__timeline-title">
          Where a garment's emissions actually come from
        </h3>
      </header>

      <ol class="kh-timeline" role="list" ref="timelineRef">
        <li
          v-for="(stage, i) in stages"
          :key="stage.key"
          class="kh-stage"
          :class="{ 'kh-stage--peak': stage.peak }"
        >
          <div class="kh-stage__node" aria-hidden="true">
            <component :is="stage.icon" :size="18" :stroke-width="2" />
            <span class="kh-stage__num">{{ String(i + 1).padStart(2, '0') }}</span>
          </div>
          <div class="kh-stage__body">
            <p class="kh-stage__name">{{ stage.name }}</p>
            <p class="kh-stage__co2">
              <strong>{{ stage.co2 }}%</strong>
              <span>CO₂</span>
            </p>
            <p class="kh-stage__hint">{{ stage.hint }}</p>
          </div>
        </li>
      </ol>

      <p class="kh-life__timeline-source">
        Figures: Quantis 2018, <em>Measuring Fashion</em>, Table 2 (global
        apparel industry, 2016 baseline).
      </p>
    </section>

    <footer class="kh-life__nav">
      <button type="button" class="kh-cta kh-cta--ghost" @click="$emit('back')">
        <ArrowLeft :size="16" :stroke-width="2" />
        Back
      </button>
      <button type="button" class="kh-cta kh-cta--primary is-burst-host" @click="$emit('next')">
        <CtaBurst />
        <CtaFlip>
          Next: material truths
          <ArrowRight :size="16" :stroke-width="2" />
        </CtaFlip>
      </button>
    </footer>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { gsap } from 'gsap'
import { ScrollTrigger, useGsapContext, isReduced } from '../../motion'
import AnimatedHeading from '../AnimatedHeading.vue'
import CtaBurst from '../CtaBurst.vue'
import CtaFlip from '../CtaFlip.vue'
import { useReveal } from '../../motion/useReveal'
import {
  ArrowLeft,
  ArrowRight,
  Sparkles,
  Sprout,        // fibre production
  Cog,           // yarn preparation (spinning machinery)
  Layers,        // fabric preparation
  Droplets,      // dyeing & finishing — water/dye theme
  Scissors,      // assembly (cut & sew)
  Truck,         // distribution
  Trash2,        // end of life
} from 'lucide-vue-next'

defineEmits(['back', 'next'])

// Eyebrow gets a per-character fade so the section title block reads as one
// composed reveal: tag → headline → timeline.
const eyebrowRef = ref(null)
const copyRef = ref(null)
const videoRef = ref(null)
useReveal(eyebrowRef, { mode: 'char', stagger: 0.022, duration: 0.5, replay: true })
useReveal(copyRef, { mode: 'fade-blur', y: 60, delay: 0.25, replay: true })
useReveal(videoRef, { mode: 'fade-up', y: 32, duration: 1, delay: 0.2, replay: true })

// Lifecycle scrollytelling: as the timeline enters viewport, each stage
// pops in turn — a lightweight, mobile-safe stand-in for a full pin.
//
// useGsapContext owns lifecycle: the tween + ScrollTrigger created inside
// the callback are scoped to timelineRef and reverted on unmount, so the
// previous manual `lifecycleTriggers[]` + `forEach kill` pattern (which
// missed the ScrollTrigger instance hanging off each trigger) is gone.
//
// The back.out(1.6) overshoot has been replaced with power3.out per the
// motion plan: the rest of the site uses restrained-elegant easing and a
// bounce overshoot was the one place that read as "decorative" rather
// than "informational" — kept everything else, just the easing changed.
const timelineRef = ref(null)

useGsapContext(timelineRef, () => {
  if (isReduced()) return
  const wrap = timelineRef.value
  const stages = wrap.querySelectorAll('.kh-stage')
  if (!stages.length) return

  gsap.set(stages, { opacity: 0, y: 24, scale: 0.96 })

  const play = () =>
    gsap.to(stages, {
      opacity: 1,
      y: 0,
      scale: 1,
      duration: 0.65,
      ease: 'power3.out',
      stagger: 0.07,
    })
  const reset = () => gsap.set(stages, { opacity: 0, y: 24, scale: 0.96 })

  ScrollTrigger.create({
    trigger: wrap,
    start: 'top 78%',
    onEnter: play,
    onEnterBack: play,
    onLeaveBack: reset,
  })
})

// CO2 share figures from Quantis 2018 Table 2 (global apparel, 2016).
// "peak" flags the dominant stage so the UI can highlight it.
const stages = [
  {
    key: 'fiber',
    icon: Sprout,
    name: 'Fibre production',
    co2: 15,
    hint: 'Cotton fields, oil-derived polyester, sheep, viscose pulp.',
  },
  {
    key: 'yarn',
    icon: Cog,
    name: 'Yarn preparation',
    co2: 28,
    hint: 'Spinning fibre into thread — heavy electricity use.',
  },
  {
    key: 'fabric',
    icon: Layers,
    name: 'Fabric preparation',
    co2: 12,
    hint: 'Knitting or weaving thread into cloth.',
  },
  {
    key: 'dyeing',
    icon: Droplets,
    name: 'Dyeing & finishing',
    co2: 36,
    peak: true,
    hint: 'Bleach, dye, softener, water-treatment — the largest single share.',
  },
  {
    key: 'assembly',
    icon: Scissors,
    name: 'Assembly',
    co2: 7,
    hint: 'Cutting and sewing cloth into wearable garments.',
  },
  {
    key: 'distribution',
    icon: Truck,
    name: 'Distribution',
    co2: 1,
    hint: 'Container shipping + retail logistics. Air freight balloons this.',
  },
  {
    key: 'eol',
    icon: Trash2,
    name: 'End of life',
    co2: 1,
    hint: 'Incineration or landfill — 87% of UK clothing ends up here.',
  },
]
</script>

<style scoped>
.kh-life {
  max-width: 1280px;
  margin: 0 auto;
  padding: 32px 32px 72px;
}

/* ── Header ─────────────────────────────────────────────────── */
.kh-life__head {
  display: flex;
  align-items: center;
  gap: 18px;
  margin-bottom: 28px;
  flex-wrap: wrap;
}
.kh-life__back {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 8px 14px;
  border-radius: var(--radius-pill);
  background: transparent;
  border: 1px solid var(--color-border-strong);
  color: var(--color-text-muted);
  font-size: 13px; font-weight: 600;
  cursor: pointer;
  transition: color var(--transition-base), background var(--transition-base);
}
.kh-life__back:hover {
  color: var(--color-text);
  background: var(--color-surface-alt);
}
.kh-life__heading { flex: 1; min-width: 240px; }
.kh-life__eyebrow {
  font-size: 11px; font-weight: 700; letter-spacing: 2px;
  color: var(--color-primary-text);
  text-transform: uppercase;
  margin-bottom: 6px;
}
.kh-life__title {
  font-size: clamp(22px, 3vw, 30px);
  font-weight: 800; letter-spacing: -0.6px;
  line-height: 1.18;
  color: var(--color-text);
}

/* ── Top split (text + video) ───────────────────────────────── */
.kh-life__split {
  display: grid;
  grid-template-columns: 1fr 1.15fr;
  gap: 36px;
  align-items: stretch;
  margin-bottom: 72px;
}
.kh-life__copy {
  background: var(--color-surface);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-card-lg);
  padding: 28px 30px;
  box-shadow: var(--shadow-card);
  font-size: 15px; line-height: 1.65;
  color: var(--color-text-muted);
}
.kh-life__copy-title {
  font-size: 20px; font-weight: 800;
  color: var(--color-text);
  letter-spacing: -0.3px;
  margin-bottom: 14px;
}
.kh-life__copy p + p { margin-top: 12px; }
.kh-life__copy-callout {
  display: grid;
  grid-template-columns: 28px 1fr;
  gap: 10px;
  align-items: start;
  margin-top: 18px;
  padding: 12px 14px;
  background: var(--color-primary-lighter);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-card-sm);
  font-size: 13.5px; line-height: 1.55;
  color: var(--color-text);
}
.kh-life__copy-callout > :first-child {
  width: 28px; height: 28px;
  margin-top: 1px;
  border-radius: 999px;
  background: var(--color-primary);
  color: var(--color-primary-text);
  display: grid; place-items: center;
}

/* ── Video ──────────────────────────────────────────────────── */
/* The video container stretches to match the left card's height
   (set by `align-items: stretch` on the grid). The frame inside
   centres its 16:9 iframe vertically, so when the column is taller
   than the frame's natural aspect ratio there's symmetric padding
   above and below — bottoms still line up with the left card. */
.kh-life__video {
  display: flex;
  align-items: center;
  justify-content: center;
}
.kh-life__video-frame {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  border-radius: var(--radius-card-lg);
  overflow: hidden;
  background: var(--color-text);
  box-shadow: var(--shadow-card);
}
.kh-life__video-frame iframe {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  border: 0;
}

/* ── Timeline ───────────────────────────────────────────────── */
.kh-life__timeline-wrap {
  background: var(--color-surface);
  border-radius: var(--radius-card-lg);
  padding: 32px 28px 28px;
  box-shadow: var(--shadow-card);
  border: 1px solid var(--color-border-light);
}
.kh-life__timeline-head { margin-bottom: 22px; }
.kh-life__timeline-eyebrow {
  font-size: 11px; font-weight: 700; letter-spacing: 2px;
  color: var(--color-primary-text);
  text-transform: uppercase;
  margin-bottom: 6px;
}
.kh-life__timeline-title {
  font-size: clamp(18px, 2.4vw, 22px);
  font-weight: 800; letter-spacing: -0.3px;
  color: var(--color-text);
}

.kh-timeline {
  list-style: none; padding: 0; margin: 0;
  position: relative;
  display: grid;
  /* 7 equal columns; on small screens it becomes a horizontal scroller */
  grid-template-columns: repeat(7, minmax(0, 1fr));
  gap: 14px;
}
/* Connecting line behind the nodes */
.kh-timeline::before {
  content: '';
  position: absolute;
  left: 24px; right: 24px;
  top: 38px;     /* aligns with node centre */
  height: 2px;
  background: linear-gradient(
    to right,
    transparent 0%,
    var(--color-border-strong) 6%,
    var(--color-border-strong) 94%,
    transparent 100%
  );
  z-index: 0;
}

.kh-stage {
  position: relative;
  display: flex; flex-direction: column;
  align-items: center;
  gap: 10px;
  text-align: center;
  z-index: 1;
}
.kh-stage__node {
  position: relative;
  width: 76px; height: 76px;
  border-radius: 999px;
  background: var(--color-surface);
  border: 2px solid var(--color-border-strong);
  color: var(--color-text-muted);
  display: grid; place-items: center;
  transition:
    background var(--transition-base),
    color var(--transition-base),
    border-color var(--transition-base),
    transform var(--transition-base);
}
.kh-stage:hover .kh-stage__node {
  transform: translateY(-3px);
  background: var(--color-primary-lighter);
  border-color: var(--color-primary-text);
  color: var(--color-primary-text);
}
.kh-stage__num {
  position: absolute;
  bottom: -6px; right: -6px;
  background: var(--color-text);
  color: var(--color-warm-cream);
  font-size: 9px; font-weight: 800;
  letter-spacing: 0.6px;
  padding: 2px 6px;
  border-radius: 999px;
}
.kh-stage--peak .kh-stage__node {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: var(--color-primary-text);
}
.kh-stage--peak .kh-stage__num {
  background: var(--color-primary-text);
}

.kh-stage__body { padding: 0 4px; }
.kh-stage__name {
  font-size: 12.5px; font-weight: 800;
  color: var(--color-text);
  letter-spacing: -0.1px;
  margin-bottom: 4px;
}
.kh-stage__co2 {
  display: inline-flex; align-items: baseline; gap: 3px;
  font-size: 11px; font-weight: 700;
  color: var(--color-primary-text);
  margin-bottom: 6px;
}
.kh-stage__co2 strong {
  font-size: 18px; font-weight: 800;
  color: var(--color-text);
  letter-spacing: -0.4px;
}
.kh-stage--peak .kh-stage__co2 strong {
  color: var(--color-primary-text);
}
.kh-stage__hint {
  font-size: 11px; line-height: 1.45;
  color: var(--color-text-muted);
}

.kh-life__timeline-source {
  margin-top: 22px;
  font-size: 11px;
  color: var(--color-text-subtle);
  text-align: right;
  font-style: italic;
}

/* ── Bottom nav ─────────────────────────────────────────────── */
.kh-life__nav {
  display: flex; justify-content: space-between;
  margin-top: 36px;
  flex-wrap: wrap; gap: 12px;
}
.kh-cta {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 13px 22px;
  border-radius: var(--radius-btn);
  font-size: 14px; font-weight: 700;
  border: 1px solid transparent;
  cursor: pointer;
  transition: transform var(--transition-base), background var(--transition-base);
}
.kh-cta--primary {
  background: var(--color-primary);
  color: var(--color-primary-text);
}
.kh-cta--primary:hover { transform: scale(1.03); background: var(--color-primary-dark); }
.kh-cta--ghost {
  background: transparent;
  color: var(--color-text);
  border-color: var(--color-border-strong);
}
.kh-cta--ghost:hover {
  background: var(--color-surface-alt);
  transform: scale(1.02);
}

/* ── Responsive ─────────────────────────────────────────────── */
@media (max-width: 1100px) {
  .kh-life__split { grid-template-columns: 1fr; gap: 24px; }
}
@media (max-width: 900px) {
  .kh-life { padding: 22px 18px 56px; }
  .kh-timeline {
    /* Horizontal scroll on phones — 7 nodes won't fit in <600px */
    grid-template-columns: repeat(7, 140px);
    overflow-x: auto;
    scroll-snap-type: x proximity;
    padding-bottom: 8px;
  }
  .kh-stage { scroll-snap-align: start; }
  .kh-life__copy { padding: 22px; }
}
</style>
