<template>
  <section class="kh-intro">
    <span class="kh-intro__index" aria-hidden="true">KH</span>
    <span class="kh-intro__label" aria-hidden="true">KNOWLEDGE HUB — UNDERSTAND THE THEME</span>

    <div class="kh-intro__inner">
      <!-- Left: text + CTA -->
      <div class="kh-intro__text">
        <p ref="eyebrowRef" class="kh-intro__eyebrow">
          STEP 01 · UNDERSTAND THE THEME
        </p>
        <AnimatedHeading
          as="h1"
          class="kh-intro__title"
          :stagger="0.07"
          :delay="0.1"
        >
          What is<br />
          <span class="kh-intro__title-accent">sustainable fashion?</span>
        </AnimatedHeading>
        <p ref="subtitleRef" class="kh-intro__subtitle">
          It's a way of designing, producing, and wearing clothing that minimises
          environmental and social harm. Where fast fashion races to put the
          cheapest garment on a hanger, sustainable fashion treats clothes as
          long-lived goods — chosen for durability, made from kinder materials,
          and recirculated rather than discarded.
        </p>

        <ul ref="bulletsRef" class="kh-intro__bullets">
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

        <div ref="actionsRef" class="kh-intro__actions">
          <button
            type="button"
            class="kh-cta kh-cta--primary is-burst-host"
            @click="$emit('next')"
          >
            <CtaBurst />
            <CtaFlip>
              <BookOpen :size="16" :stroke-width="2" />
              Start the journey
              <ArrowRight :size="16" :stroke-width="2" />
            </CtaFlip>
          </button>
        </div>
      </div>

      <!-- Right: hero illustration animation (Lottie) -->
      <div ref="artRef" class="kh-intro__art" aria-hidden="true">
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
import { ref } from 'vue'
import { Vue3Lottie } from 'vue3-lottie'
import {
  ArrowRight, BookOpen, Hourglass, Leaf, Recycle,
} from 'lucide-vue-next'
import AnimatedHeading from '../AnimatedHeading.vue'
import CtaBurst from '../CtaBurst.vue'
import CtaFlip from '../CtaFlip.vue'
import { useReveal } from '../../motion/useReveal'
import { useStagger } from '../../motion/useStagger'
import heroAnim from '../../assets/lottie/knowledge-hero.json'

defineEmits(['next'])

const eyebrowRef = ref(null)
const subtitleRef = ref(null)
const bulletsRef = ref(null)
const actionsRef = ref(null)
const artRef = ref(null)

useReveal(eyebrowRef, { mode: 'char', stagger: 0.022, duration: 0.5 })
useReveal(subtitleRef, { mode: 'fade-blur', y: 60, delay: 0.25 })
useStagger(bulletsRef, { selector: 'li', stagger: 0.08, y: 24, delay: 0.4 })
useReveal(actionsRef, { mode: 'fade-up', y: 18, delay: 0.55 })
useReveal(artRef, { mode: 'fade-up', y: 24, duration: 1, delay: 0.2 })
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

/* Short-laptop tier — compress so the "Start the journey" CTA fits above
   the fold on ≤820 px high screens (13-15" Windows laptops, MacBook Air). */
@media (max-height: 820px) and (min-width: 901px) {
  .kh-intro { padding: 56px 32px 32px; }
  .kh-intro__index, .kh-intro__label { top: 56px; }
  .kh-intro__inner { margin-top: 24px; gap: 36px; }
  .kh-intro__title { font-size: clamp(32px, 3.6vw, 44px); margin-bottom: 14px; }
  .kh-intro__eyebrow { margin-bottom: 12px; }
  .kh-intro__subtitle { font-size: 15px; margin-bottom: 16px; }
  .kh-intro__bullets { margin-bottom: 20px; gap: 8px; }
  .kh-intro__bullets li { font-size: 13.5px; }
  .kh-intro__art { height: 420px; }
}
</style>
