<template>
  <section class="kh-life">
    <header class="kh-life__head">
      <button type="button" class="kh-life__back" @click="$emit('back')">
        <ArrowLeft :size="16" :stroke-width="2" /> Back
      </button>
      <div class="kh-life__heading">
        <p class="kh-life__eyebrow">STEP 02 · LIFECYCLE OF A GARMENT</p>
        <h2 class="kh-life__title">
          From cotton field to landfill — every stage leaves a footprint.
        </h2>
      </div>
    </header>

    <div
      class="kh-life__copy-wrap"
      v-motion
      :initial="{ opacity: 0, y: 18 }"
      :enter="{ opacity: 1, y: 0, transition: { duration: 600 } }"
    >
      <div class="kh-life__copy">
        <h3 class="kh-life__copy-title">A garment lives many lives</h3>
        <p>
          Before a piece of clothing reaches your wardrobe, it has already
          travelled through farms, factories, dye houses, container ships and
          warehouses across several continents. Each step burns energy,
          consumes water, and emits greenhouse gases.
        </p>
        <p>
          The timeline below shows where each stage sits in the global apparel
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
    </div>

    <!-- Timeline -->
    <section
      class="kh-life__timeline-wrap"
      v-motion
      :initial="{ opacity: 0, y: 24 }"
      :enter="{ opacity: 1, y: 0, transition: { duration: 700, delay: 250 } }"
    >
      <header class="kh-life__timeline-head">
        <p class="kh-life__timeline-eyebrow">THE 7-STAGE FOOTPRINT</p>
        <h3 class="kh-life__timeline-title">
          Where a garment's emissions actually come from
        </h3>
      </header>

      <ol class="kh-timeline" role="list">
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
      <button type="button" class="kh-cta kh-cta--primary" @click="$emit('next')">
        Next: material truths
        <ArrowRight :size="16" :stroke-width="2" />
      </button>
    </footer>
  </section>
</template>

<script setup>
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

/* ── Intro copy (full width above timeline) ─────────────────── */
.kh-life__copy-wrap {
  margin-bottom: 72px;
  max-width: 820px;
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
