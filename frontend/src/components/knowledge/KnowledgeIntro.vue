<template>
  <section class="kh-intro">
    <span class="kh-intro__index" aria-hidden="true">KH</span>
    <span class="kh-intro__label" aria-hidden="true">KNOWLEDGE HUB — UNDERSTAND THE THEME</span>

    <div class="kh-intro__inner">
      <!-- Left: text + CTA -->
      <div class="kh-intro__text">
        <p
          class="kh-intro__eyebrow"
          v-motion
          :initial="{ opacity: 0, y: 12 }"
          :enter="{ opacity: 1, y: 0, transition: { duration: 500 } }"
        >
          STEP 01 · UNDERSTAND THE THEME
        </p>
        <h1
          class="kh-intro__title"
          v-motion
          :initial="{ opacity: 0, y: 24 }"
          :enter="{ opacity: 1, y: 0, transition: { duration: 700, delay: 100 } }"
        >
          What is<br />
          <span class="kh-intro__title-accent">sustainable fashion?</span>
        </h1>
        <p
          class="kh-intro__subtitle"
          v-motion
          :initial="{ opacity: 0, y: 18 }"
          :enter="{ opacity: 1, y: 0, transition: { duration: 600, delay: 250 } }"
        >
          It's a way of designing, producing, and wearing clothing that minimises
          environmental and social harm. Where fast fashion races to put the
          cheapest garment on a hanger, sustainable fashion treats clothes as
          long-lived goods — chosen for durability, made from kinder materials,
          and recirculated rather than discarded.
        </p>

        <ul
          class="kh-intro__bullets"
          v-motion
          :initial="{ opacity: 0, y: 18 }"
          :enter="{ opacity: 1, y: 0, transition: { duration: 600, delay: 400 } }"
        >
          <li>
            <Hourglass :size="14" :stroke-width="2" />
            <span>
              <strong>Built to last.</strong>
              Garments worn for years, not for a season's photo.
            </span>
          </li>
          <li>
            <Leaf :size="14" :stroke-width="2" />
            <span>
              <strong>Lower-impact fibres.</strong>
              Organic, recycled, regenerative — alternatives that don't outlive
              the wardrobe.
            </span>
          </li>
          <li>
            <Recycle :size="14" :stroke-width="2" />
            <span>
              <strong>Circular by design.</strong>
              Repaired, resold, recycled — diverted from landfill at every
              chance.
            </span>
          </li>
        </ul>

        <div
          class="kh-intro__actions"
          v-motion
          :initial="{ opacity: 0, y: 20 }"
          :enter="{ opacity: 1, y: 0, transition: { duration: 600, delay: 550 } }"
        >
          <button
            type="button"
            class="kh-cta kh-cta--primary"
            @click="$emit('next')"
          >
            <BookOpen :size="16" :stroke-width="2" />
            Start the journey
            <ArrowRight :size="16" :stroke-width="2" />
          </button>
        </div>
      </div>

      <!-- Right: hero illustration animation (Lottie) -->
      <div
        class="kh-intro__art"
        v-motion
        :initial="{ opacity: 0, scale: 0.94 }"
        :enter="{ opacity: 1, scale: 1, transition: { duration: 800, delay: 200 } }"
        aria-hidden="true"
      >
        <Vue3Lottie
          :animation-data="heroAnim"
          :loop="true"
          :autoplay="true"
          class="kh-intro__lottie"
        />
      </div>
    </div>
  </section>
</template>

<script setup>
import { Vue3Lottie } from 'vue3-lottie'
import {
  ArrowRight, BookOpen, Hourglass, Leaf, Recycle,
} from 'lucide-vue-next'
import heroAnim from '../../assets/lottie/knowledge-hero.json'

defineEmits(['next'])
</script>

<style scoped>
.kh-intro {
  position: relative;
  max-width: 1200px;
  margin: 0 auto;
  padding: 96px 32px 64px;
}

.kh-intro__index {
  position: absolute;
  top: 96px; left: 32px;
  font-family: 'Georgia', serif;
  font-size: 13px; font-weight: 600;
  letter-spacing: 1.5px;
  color: var(--color-text-faint);
}
.kh-intro__label {
  position: absolute;
  top: 96px; right: 32px;
  font-size: 11px; letter-spacing: 2px;
  color: var(--color-text-faint);
}

.kh-intro__inner {
  display: grid;
  grid-template-columns: 1fr 1.15fr;
  gap: 56px;
  align-items: center;
  margin-top: 48px;
}

.kh-intro__eyebrow {
  font-size: 12px; font-weight: 700; letter-spacing: 2px;
  color: var(--color-primary-text);
  margin-bottom: 18px;
}

.kh-intro__title {
  font-size: clamp(40px, 5vw, 64px);
  font-weight: 800; letter-spacing: -1.5px;
  line-height: 1.04; color: var(--color-text);
  margin-bottom: 22px;
}
.kh-intro__title-accent {
  color: var(--color-primary);
}

.kh-intro__subtitle {
  font-size: 17px; line-height: 1.6;
  color: var(--color-text-muted);
  max-width: 580px; margin-bottom: 26px;
}

.kh-intro__bullets {
  list-style: none; padding: 0; margin: 0 0 32px;
  display: flex; flex-direction: column; gap: 14px;
}
.kh-intro__bullets li {
  display: grid;
  grid-template-columns: 28px 1fr;
  align-items: start;
  gap: 12px;
  font-size: 14.5px; line-height: 1.55;
  color: var(--color-text-muted);
}
.kh-intro__bullets li > :first-child {
  margin-top: 4px;
  color: var(--color-primary-text);
  background: var(--color-primary-light);
  padding: 6px;
  border-radius: 999px;
  width: 28px; height: 28px;
  box-sizing: border-box;
  display: grid; place-items: center;
}
.kh-intro__bullets li strong {
  color: var(--color-text);
  font-weight: 700;
}

.kh-intro__actions {
  display: flex; flex-wrap: wrap; gap: 10px;
}

.kh-cta {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 13px 24px;
  border-radius: var(--radius-btn);
  font-size: 15px; font-weight: 700;
  border: 1px solid transparent;
  cursor: pointer;
  transition: transform var(--transition-base), background var(--transition-base);
}
.kh-cta--primary {
  background: var(--color-primary);
  color: var(--color-primary-text);
}
.kh-cta--primary:hover { transform: scale(1.03); background: var(--color-primary-dark); }

/* ── Lottie art ──────────────────────────────────────────────── */
.kh-intro__art {
  height: 600px;
  display: flex; align-items: center; justify-content: center;
}
.kh-intro__lottie {
  width: 100%;
  height: 100%;
  max-width: 720px;
}

@media (max-width: 900px) {
  .kh-intro { padding: 64px 20px 40px; }
  .kh-intro__inner { grid-template-columns: 1fr; gap: 32px; }
  .kh-intro__art { height: 360px; }
  .kh-intro__index, .kh-intro__label { top: 64px; }
}
</style>
