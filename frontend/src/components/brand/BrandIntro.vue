<template>
  <section class="brand-intro">
    <span class="brand-intro__index" aria-hidden="true">BS</span>
    <span class="brand-intro__label" aria-hidden="true">BRAND SEARCH — TRANSPARENCY INDEX</span>

    <!-- ── Hero ─────────────────────────────────────────────────────── -->
    <div class="brand-intro__hero">
      <div class="brand-intro__hero-text">
        <p
          class="brand-intro__eyebrow"
          v-motion
          :initial="{ opacity: 0, y: 12 }"
          :enter="{ opacity: 1, y: 0, transition: { duration: 500 } }"
        >
          BRAND TRANSPARENCY · WHY IT MATTERS
        </p>
        <h1
          class="brand-intro__title"
          v-motion
          :initial="{ opacity: 0, y: 24 }"
          :enter="{ opacity: 1, y: 0, transition: { duration: 700, delay: 100 } }"
        >
          Behind every label,<br />
          a supply chain.
        </h1>
        <p
          class="brand-intro__subtitle"
          v-motion
          :initial="{ opacity: 0, y: 18 }"
          :enter="{ opacity: 1, y: 0, transition: { duration: 600, delay: 250 } }"
        >
          Greenwashing is everywhere. Independent disclosure scores cut through it.
          Here's how 247 brands stack up — and how to read the numbers without falling for the marketing.
        </p>
        <button
          type="button"
          class="brand-intro__hero-cta"
          @click="scrollTo('pillars')"
          v-motion
          :initial="{ opacity: 0, y: 20 }"
          :enter="{ opacity: 1, y: 0, transition: { duration: 600, delay: 450 } }"
        >
          See how it works
          <ArrowDown :size="18" :stroke-width="2" />
        </button>
      </div>
      <div class="brand-intro__hero-art" aria-hidden="true">
        <Vue3Lottie
          :animation-data="heroAnim"
          :height="'100%'"
          :width="'100%'"
          :loop="true"
          :autoplay="true"
        />
      </div>
    </div>

    <!-- ── Three pillars ───────────────────────────────────────────── -->
    <div class="pillars" id="pillars">
      <div class="pillars__head">
        <p class="pillars__eyebrow">SECTION 02 · WHAT THE SCORE COVERS</p>
        <h2 class="pillars__title">What we actually measure.</h2>
        <p class="pillars__sub">
          Three things, weighted by how much harm they cause. Environment matters most —
          that's where most of fashion's damage actually happens.
        </p>
      </div>

      <!-- Stacked weight bar -->
      <div
        class="pillar-bar"
        role="img"
        aria-label="Score weight: governance 14%, tracing 36%, environment 50%"
      >
        <div class="pillar-bar__seg pillar-bar__seg--gov" :style="{ flex: 6 }">
          <span class="pillar-bar__seg-label">Governance</span>
          <span class="pillar-bar__seg-pct">14%</span>
        </div>
        <div class="pillar-bar__seg pillar-bar__seg--trace" :style="{ flex: 15 }">
          <span class="pillar-bar__seg-label">Tracing</span>
          <span class="pillar-bar__seg-pct">36%</span>
        </div>
        <div class="pillar-bar__seg pillar-bar__seg--env" :style="{ flex: 21 }">
          <span class="pillar-bar__seg-label">Environment</span>
          <span class="pillar-bar__seg-pct">50%</span>
        </div>
      </div>

      <div class="pillar-grid">
        <article
          class="pillar-card pillar-card--gov"
          v-motion
          :initial="{ opacity: 0, y: 24 }"
          :visible-once="{ opacity: 1, y: 0, transition: { duration: 500 } }"
        >
          <div class="pillar-card__icon-wrap">
            <Scale :size="28" :stroke-width="1.8" />
          </div>
          <p class="pillar-card__points">6 pts max · 14% weight</p>
          <h3 class="pillar-card__title">Governance &amp; Policies</h3>
          <p class="pillar-card__body">
            Most brands say the right things. We check if they actually wrote it down —
            rules for their factories, a senior person who's officially responsible.
            Without that on paper, talk doesn't turn into action.
          </p>
        </article>

        <article
          class="pillar-card pillar-card--trace"
          v-motion
          :initial="{ opacity: 0, y: 24 }"
          :visible-once="{ opacity: 1, y: 0, transition: { duration: 500, delay: 120 } }"
        >
          <div class="pillar-card__icon-wrap">
            <Workflow :size="28" :stroke-width="1.8" />
          </div>
          <p class="pillar-card__points">15 pts max · 36% weight</p>
          <h3 class="pillar-card__title">Supply Chain Tracing</h3>
          <p class="pillar-card__body">
            Most brands lose track of their own clothes after the final factory. We ask
            how far back they can actually see — to the dye-house, the textile mill,
            even the cotton farm where it all began.
          </p>
        </article>

        <article
          class="pillar-card pillar-card--env"
          v-motion
          :initial="{ opacity: 0, y: 24 }"
          :visible-once="{ opacity: 1, y: 0, transition: { duration: 500, delay: 240 } }"
        >
          <div class="pillar-card__icon-wrap">
            <Leaf :size="28" :stroke-width="1.8" />
          </div>
          <p class="pillar-card__points">21 pts max · 50% weight</p>
          <h3 class="pillar-card__title">Environmental Impact</h3>
          <p class="pillar-card__body">
            Better fabrics, real targets to cut emissions, fewer plastic-based materials.
            This is where most of the damage gets done — or undone. Half the score lives
            here for a reason.
          </p>
        </article>
      </div>
    </div>

    <!-- ── Score scale ─────────────────────────────────────────────── -->
    <div class="scale" id="scale">
      <div class="scale__head">
        <p class="scale__eyebrow">SECTION 03 · THE LABELS</p>
        <h2 class="scale__title">Five tiers, plain English.</h2>
        <p class="scale__sub">
          Companies don't get an A–F grade. They get a tier that reflects how transparent
          and credible their reporting is — not how green their marketing looks.
        </p>
      </div>

      <div class="scale-grid">
        <article
          v-for="(t, i) in scaleTiers"
          :key="t.label"
          class="scale-card"
          :data-tone="t.tone"
          v-motion
          :initial="{ opacity: 0, y: 16 }"
          :visible-once="{ opacity: 1, y: 0, transition: { duration: 400, delay: i * 90 } }"
        >
          <span class="scale-card__chip">{{ t.label }}</span>
          <span class="scale-card__range">{{ t.range }}</span>
          <p class="scale-card__desc">{{ t.desc }}</p>
        </article>
      </div>
    </div>

    <!-- ── What this means for you ─────────────────────────────────── -->
    <div class="tips">
      <div class="tips__head">
        <p class="tips__eyebrow">SECTION 04 · HOW TO USE IT</p>
        <h2 class="tips__title">A "Great" rating isn't a license to buy.</h2>
        <p class="tips__sub">
          The score helps you avoid the worst — not justify the next purchase.
          Three rules to keep it honest:
        </p>
      </div>

      <div class="tips-grid">
        <article
          v-for="(t, i) in tips"
          :key="t.title"
          class="tip-card"
          v-motion
          :initial="{ opacity: 0, y: 18 }"
          :visible-once="{ opacity: 1, y: 0, transition: { duration: 450, delay: i * 110 } }"
        >
          <div class="tip-card__icon-wrap">
            <component :is="t.icon" :size="24" :stroke-width="1.8" />
          </div>
          <h3 class="tip-card__title">{{ t.title }}</h3>
          <p class="tip-card__body">{{ t.body }}</p>
        </article>
      </div>
    </div>

    <!-- ── Final CTA + source ───────────────────────────────────────── -->
    <div class="brand-intro__footer">
      <p class="brand-intro__source">
        Data: <strong>Fashion Transparency Index 2024</strong> (Australian market) ·
        scores reflect publicly disclosed corporate policies.
      </p>
      <button type="button" class="brand-intro__cta" @click="$emit('start')">
        Start exploring brands
        <ArrowRight :size="18" :stroke-width="2" />
      </button>
    </div>
  </section>
</template>

<script setup>
import { ArrowDown, ArrowRight, Filter, HeartHandshake, Hourglass, Leaf, Scale, Workflow } from 'lucide-vue-next'
import { Vue3Lottie } from 'vue3-lottie'
import heroAnim from '../../assets/lottie/brand-hero.json'

defineEmits(['start'])

// Tonal scale: from full lime ("top") fading to dim cream ("bottom").
// Single colour family keeps the explainer aligned with the cream + lime
// system instead of pulling a five-colour traffic-light palette in.
const scaleTiers = [
  { label: 'Great',          range: '76–100', tone: 'top',    desc: 'Strong leadership on transparency and tangible action across all three pillars.' },
  { label: 'Good',           range: '51–75',  tone: 'high',   desc: 'Decent overall performance with credible policies and some gaps still to close.' },
  { label: "It's a Start",   range: '26–50',  tone: 'mid',    desc: 'Some initiatives in place, but significant disclosure or follow-through gaps.' },
  { label: 'Below Average',  range: '11–25',  tone: 'low',    desc: 'Limited transparency. Marketing claims often outpace verifiable evidence.' },
  { label: 'Avoid',          range: '0–10',   tone: 'bottom', desc: 'Very little public evidence of sustainable or ethical supply-chain practice.' },
]

const tips = [
  {
    icon: Hourglass,
    title: 'Wear longer beats brand swap',
    body: 'A "Good" piece worn for 3 years almost always beats a "Great" piece worn for 1. The score helps you choose well — care extends the win.',
  },
  {
    icon: Filter,
    title: 'Use it to rule out, not to crown',
    body: '"Avoid" tier exists for a reason. Use the scoreboard to filter out the clear bottom — then weigh other factors like fit, need, and longevity.',
  },
  {
    icon: HeartHandshake,
    title: 'Combine with your own care',
    body: 'A high score is a starting point, not a finish line. Wash cold, line dry, mend, and rotate — that\'s where the real footprint reduction happens.',
  },
]

function scrollTo(id) {
  const el = document.getElementById(id)
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
}
</script>

<style scoped>
.brand-intro {
  position: relative;
  padding: 120px 48px 100px;
  max-width: 1320px;
  margin: 0 auto;
}

.brand-intro__index {
  position: absolute;
  top: 96px;
  left: 36px;
  font-size: 200px;
  font-weight: 900;
  line-height: 0.8;
  letter-spacing: -0.04em;
  color: var(--color-primary);
  opacity: 0.08;
  pointer-events: none;
  z-index: 1;
  user-select: none;
}

.brand-intro__label {
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

/* ── Hero ───────────────────────────────────────────────────────── */
.brand-intro__hero {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1.05fr);
  gap: 64px;
  align-items: center;
  position: relative;
  z-index: 2;
  min-height: 70vh;
}

.brand-intro__hero-text {
  display: flex;
  flex-direction: column;
  gap: 24px;
  align-items: flex-start;
}

.brand-intro__eyebrow {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--color-primary-text);
  margin: 0;
}

.brand-intro__title {
  font-size: clamp(2.6rem, 5.5vw, 4.6rem);
  line-height: 0.95;
  font-weight: 900;
  letter-spacing: -0.02em;
  color: var(--color-text);
  margin: 0;
  text-wrap: balance;
}

.brand-intro__subtitle {
  font-size: clamp(1rem, 1.5vw, 1.18rem);
  color: var(--color-text-muted);
  max-width: 540px;
  margin: 0;
  line-height: 1.55;
}

.brand-intro__hero-cta {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 14px 28px;
  border-radius: var(--radius-pill);
  font-size: 15px;
  font-weight: 700;
  color: var(--color-primary-text);
  background: var(--color-primary);
  border: none;
  cursor: pointer;
  transition:
    transform 200ms var(--motion-entrance),
    box-shadow 200ms var(--motion-entrance);
  margin-top: 8px;
}

.brand-intro__hero-cta:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(22, 51, 0, 0.18);
}

.brand-intro__hero-art {
  display: flex;
  align-items: center;
  justify-content: center;
  max-width: 580px;
  width: 100%;
  margin: 0 auto;
}

/* ── Section heads (shared eyebrow style) ─────────────────────── */
.pillars__head, .scale__head, .tips__head {
  text-align: center;
  max-width: 720px;
  margin: 0 auto 36px;
}

.pillars__eyebrow, .scale__eyebrow, .tips__eyebrow {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--color-primary-text);
  margin: 0 0 12px;
}

.pillars__title, .scale__title, .tips__title {
  font-size: clamp(2rem, 3.6vw, 2.8rem);
  font-weight: 900;
  letter-spacing: -0.02em;
  line-height: 1.05;
  color: var(--color-text);
  margin: 0 0 14px;
  text-wrap: balance;
}

.pillars__sub, .scale__sub, .tips__sub {
  font-size: 15px;
  color: var(--color-text-muted);
  line-height: 1.6;
  margin: 0;
}

/* ── Pillars ──────────────────────────────────────────────────── */
.pillars {
  margin-top: 96px;
  position: relative;
  z-index: 2;
}

.pillar-bar {
  display: flex;
  width: 100%;
  height: 56px;
  border-radius: 14px;
  overflow: hidden;
  border: 1px solid var(--color-kh-glass-border);
  margin-bottom: 28px;
}

.pillar-bar__seg {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 0 16px;
  position: relative;
}

.pillar-bar__seg-label {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  opacity: 0.85;
}

.pillar-bar__seg-pct {
  font-size: 16px;
  font-weight: 900;
  letter-spacing: -0.01em;
}

.pillar-bar__seg--gov   { background: rgba(255, 192, 145, 0.55); color: #5a3215; }
.pillar-bar__seg--trace { background: rgba(159, 232, 112, 0.55); color: var(--color-primary-text); }
.pillar-bar__seg--env   { background: var(--color-primary-text);  color: var(--color-warm-cream); }

.pillar-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 20px;
}

.pillar-card {
  position: relative;
  padding: 32px 26px 28px;
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid var(--color-kh-glass-border);
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  box-shadow: 0 10px 28px rgba(22, 51, 0, 0.05);
  transition:
    transform 280ms var(--motion-entrance),
    box-shadow 280ms var(--motion-entrance),
    border-color 280ms var(--motion-entrance);
  cursor: default;
}

.pillar-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 42px rgba(22, 51, 0, 0.10);
  border-color: rgba(22, 51, 0, 0.22);
}

/* Icon wrap pops on card hover — small interaction reward */
.pillar-card__icon-wrap {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  border-radius: 16px;
  margin-bottom: 6px;
  transition:
    transform 320ms cubic-bezier(0.34, 1.56, 0.64, 1),
    box-shadow 280ms var(--motion-entrance);
}

.pillar-card:hover .pillar-card__icon-wrap {
  transform: rotate(-6deg) scale(1.08);
}

.pillar-card--gov   .pillar-card__icon-wrap { background: rgba(255, 192, 145, 0.22); color: #b45309; }
.pillar-card--trace .pillar-card__icon-wrap { background: rgba(159, 232, 112, 0.22); color: var(--color-primary-text); }
.pillar-card--env   .pillar-card__icon-wrap { background: rgba(22, 51, 0, 0.08);     color: var(--color-primary-text); }

.pillar-card:hover.pillar-card--gov   .pillar-card__icon-wrap { box-shadow: 0 6px 18px rgba(255, 192, 145, 0.45); }
.pillar-card:hover.pillar-card--trace .pillar-card__icon-wrap { box-shadow: 0 6px 18px rgba(159, 232, 112, 0.45); }
.pillar-card:hover.pillar-card--env   .pillar-card__icon-wrap { box-shadow: 0 6px 18px rgba(22, 51, 0, 0.18); }

.pillar-card__points {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--color-text-faint);
  margin: 0;
}

.pillar-card__title {
  font-size: 20px;
  font-weight: 800;
  letter-spacing: -0.01em;
  color: var(--color-text);
  margin: 0;
}

.pillar-card__body {
  font-size: 14px;
  line-height: 1.55;
  color: var(--color-text-muted);
  margin: 0;
}

/* ── Score scale ─────────────────────────────────────────────── */
.scale {
  margin-top: 96px;
  position: relative;
  z-index: 2;
}

.scale-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 14px;
}

/* Tonal scale: only lime + cream + dark-green tones. The card's
   visual energy fades top → bottom, so "better" reads at a glance
   without pulling in red/orange/yellow. */
.scale-card {
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid var(--color-kh-glass-border);
  border-radius: 16px;
  padding: 22px 18px 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  transition: transform 220ms var(--motion-entrance), box-shadow 220ms var(--motion-entrance);
}

.scale-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 14px 30px rgba(22, 51, 0, 0.07);
}

.scale-card__chip {
  display: inline-flex;
  align-self: flex-start;
  padding: 5px 12px;
  border-radius: var(--radius-pill);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.04em;
}

.scale-card__range {
  font-size: 24px;
  font-weight: 900;
  letter-spacing: -0.01em;
}

.scale-card__desc {
  font-size: 13px;
  line-height: 1.5;
  margin: 0;
}

/* Top tier — full lime energy. */
.scale-card[data-tone="top"] {
  background: rgba(159, 232, 112, 0.22);
  border-color: rgba(22, 51, 0, 0.18);
}
.scale-card[data-tone="top"] .scale-card__chip {
  background: var(--color-primary);
  color: var(--color-primary-text);
}
.scale-card[data-tone="top"] .scale-card__range,
.scale-card[data-tone="top"] .scale-card__desc { color: var(--color-primary-text); }

/* High tier — softer lime. */
.scale-card[data-tone="high"] {
  background: rgba(159, 232, 112, 0.10);
}
.scale-card[data-tone="high"] .scale-card__chip {
  background: rgba(159, 232, 112, 0.55);
  color: var(--color-primary-text);
}
.scale-card[data-tone="high"] .scale-card__range { color: var(--color-primary-text); }
.scale-card[data-tone="high"] .scale-card__desc { color: var(--color-text-muted); }

/* Mid tier — neutral cream pivot. */
.scale-card[data-tone="mid"] {
  background: rgba(255, 255, 255, 0.85);
}
.scale-card[data-tone="mid"] .scale-card__chip {
  background: rgba(22, 51, 0, 0.07);
  color: var(--color-text-muted);
}
.scale-card[data-tone="mid"] .scale-card__range { color: var(--color-text-muted); }
.scale-card[data-tone="mid"] .scale-card__desc { color: var(--color-text-muted); }

/* Low tier — fading. */
.scale-card[data-tone="low"] {
  background: rgba(255, 255, 255, 0.55);
}
.scale-card[data-tone="low"] .scale-card__chip {
  background: rgba(22, 51, 0, 0.09);
  color: var(--color-text-faint);
}
.scale-card[data-tone="low"] .scale-card__range { color: var(--color-text-faint); }
.scale-card[data-tone="low"] .scale-card__desc { color: var(--color-text-faint); }

/* Bottom tier — almost out. */
.scale-card[data-tone="bottom"] {
  background: rgba(22, 51, 0, 0.04);
  border-color: rgba(22, 51, 0, 0.16);
}
.scale-card[data-tone="bottom"] .scale-card__chip {
  background: rgba(22, 51, 0, 0.14);
  color: var(--color-text-faint);
}
.scale-card[data-tone="bottom"] .scale-card__range { color: var(--color-text-faint); }
.scale-card[data-tone="bottom"] .scale-card__desc { color: var(--color-text-faint); }

/* ── Tips ─────────────────────────────────────────────────────── */
.tips {
  margin-top: 96px;
  position: relative;
  z-index: 2;
}

.tips-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 20px;
}

.tip-card {
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid var(--color-kh-glass-border);
  border-radius: 18px;
  padding: 26px 24px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  transition: transform 260ms var(--motion-entrance), background 260ms var(--motion-entrance);
}

.tip-card:hover {
  transform: translateY(-3px);
  background: rgba(255, 255, 255, 0.85);
}

.tip-card__icon-wrap {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: var(--color-primary);
  color: var(--color-primary-text);
  margin-bottom: 4px;
  transition: transform 320ms cubic-bezier(0.34, 1.56, 0.64, 1);
}

.tip-card:hover .tip-card__icon-wrap {
  transform: rotate(-8deg) scale(1.06);
}

.tip-card__title {
  font-size: 17px;
  font-weight: 800;
  color: var(--color-text);
  margin: 0;
  letter-spacing: -0.01em;
}

.tip-card__body {
  font-size: 14px;
  line-height: 1.55;
  color: var(--color-text-muted);
  margin: 0;
}

/* ── Footer / final CTA ───────────────────────────────────────── */
.brand-intro__footer {
  margin-top: 96px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 18px;
  text-align: center;
  position: relative;
  z-index: 2;
}

.brand-intro__source {
  font-size: 13px;
  color: var(--color-text-faint);
  margin: 0;
}

.brand-intro__source strong {
  color: var(--color-text-muted);
  font-weight: 700;
}

.brand-intro__cta {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 18px 34px;
  border-radius: var(--radius-pill);
  font-size: 16px;
  font-weight: 700;
  color: var(--color-primary-text);
  background: var(--color-primary);
  border: none;
  cursor: pointer;
  transition: transform 200ms var(--motion-entrance), box-shadow 200ms var(--motion-entrance);
}

.brand-intro__cta:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(22, 51, 0, 0.22);
}

/* ── Responsive ────────────────────────────────────────────────── */
@media (max-width: 1024px) {
  .brand-intro__hero { grid-template-columns: 1fr; gap: 40px; min-height: auto; }
  .brand-intro__title { font-size: clamp(2.2rem, 7vw, 3.4rem); }
  .pillar-grid, .tips-grid { grid-template-columns: 1fr; }
  .scale-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 768px) {
  .brand-intro { padding: 80px 20px 60px; }
  .brand-intro__index, .brand-intro__label { display: none; }
  .pillar-bar { height: auto; flex-direction: column; }
  .pillar-bar__seg { padding: 12px 16px; flex-direction: row; justify-content: space-between; }
  .scale-grid { grid-template-columns: 1fr; }
}
</style>
