<template>
  <section class="wd-ai" ref="rootRef">
    <span class="wd-ai__index" aria-hidden="true">02</span>
    <span class="wd-ai__label" aria-hidden="true">STEP 02 — WHAT THE AI CAN DO</span>

    <div class="wd-ai__inner">
      <!-- Left: copy + 4 capability cards + CTA -->
      <div class="wd-ai__text">
        <p ref="eyebrowRef" class="wd-ai__eyebrow">
          STEP 02 · WHAT THE AI CAN DO
        </p>
        <h2 ref="titleRef" class="wd-ai__title">
          Your wardrobe,<br />
          <span class="wd-ai__title-accent">audited by AI.</span>
        </h2>
        <p ref="subRef" class="wd-ai__sub">
          The AI takes stock of what's hanging in your closet, looks up what
          each piece actually costs the planet, and walks you through the four
          questions worth asking before you do anything else.
        </p>

        <ul ref="cardsRef" class="wd-ai__cards">
          <li class="wd-ai__card">
            <span class="wd-ai__card-icon" aria-hidden="true">
              <Leaf :size="18" :stroke-width="2" />
            </span>
            <h3 class="wd-ai__card-title">Impact snapshot</h3>
            <p class="wd-ai__card-body">
              How much CO<sub>2</sub> and water your wardrobe really costs —
              and how that stacks up against the average shopper.
            </p>
          </li>
          <li class="wd-ai__card">
            <span class="wd-ai__card-icon" aria-hidden="true">
              <Zap :size="18" :stroke-width="2" />
            </span>
            <h3 class="wd-ai__card-title">Reduce footprint</h3>
            <p class="wd-ai__card-body">
              The three changes with the biggest payoff, ranked by how many
              kilos of CO<sub>2</sub> each one saves.
            </p>
          </li>
          <li class="wd-ai__card">
            <span class="wd-ai__card-icon" aria-hidden="true">
              <ShoppingBag :size="18" :stroke-width="2" />
            </span>
            <h3 class="wd-ai__card-title">Rethink purchases</h3>
            <p class="wd-ai__card-body">
              An honest check on what you really need next — with second-hand
              and recycled options to look at first.
            </p>
          </li>
          <li class="wd-ai__card">
            <span class="wd-ai__card-icon" aria-hidden="true">
              <Repeat :size="18" :stroke-width="2" />
            </span>
            <h3 class="wd-ai__card-title">Make clothes last</h3>
            <p class="wd-ai__card-body">
              Washing, care and repair habits that double how long each piece
              lasts — and keep it out of landfill.
            </p>
          </li>
        </ul>

        <div ref="ctaRef" class="wd-ai__actions">
          <button
            type="button"
            class="wd-ai__cta is-burst-host"
            @click="$emit('open-advisor')"
          >
            <CtaBurst />
            <CtaFlip>
              <Sparkles :size="16" :stroke-width="2" />
              Ask the AI advisor
              <ArrowRight :size="16" :stroke-width="2" />
            </CtaFlip>
          </button>
          <p class="wd-ai__cta-hint">
            <Lock :size="12" :stroke-width="2" />
            Your photos stay on your device — only the type of each piece is
            sent to the AI.
          </p>
        </div>
      </div>

      <!-- Right: Lottie / illustration slot -->
      <div ref="artRef" class="wd-ai__art" aria-hidden="true">
        <Vue3Lottie
          :animation-data="heroAnim"
          :loop="true"
          :autoplay="true"
          class="wd-ai__lottie"
        />
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { Vue3Lottie } from 'vue3-lottie'
import {
  ArrowRight, Leaf, Lock, Repeat, ShoppingBag, Sparkles, Zap,
} from 'lucide-vue-next'
import CtaBurst from '../CtaBurst.vue'
import CtaFlip from '../CtaFlip.vue'
import { useReveal } from '../../motion/useReveal'
import { useStagger } from '../../motion/useStagger'
import heroAnim from '../../assets/lottie/wardrobe-ai.json'

defineEmits(['open-advisor'])

const rootRef = ref(null)
const eyebrowRef = ref(null)
const titleRef = ref(null)
const subRef = ref(null)
const cardsRef = ref(null)
const ctaRef = ref(null)
const artRef = ref(null)

useReveal(eyebrowRef, { mode: 'fade-up', y: 12, duration: 0.5 })
useReveal(titleRef, { mode: 'fade-up', y: 30, duration: 0.7, delay: 0.1 })
useReveal(subRef, { mode: 'fade-up', y: 18, duration: 0.6, delay: 0.25 })
useStagger(cardsRef, { selector: '.wd-ai__card', stagger: 0.08, y: 24, delay: 0.35 })
useReveal(ctaRef, { mode: 'fade-up', y: 18, delay: 0.6 })
useReveal(artRef, { mode: 'fade-up', y: 24, duration: 1, delay: 0.2 })
</script>

<style scoped>
.wd-ai {
  position: relative;
  max-width: 1200px;
  margin: 88px auto 0;
  padding: 0 32px;
}

.wd-ai__index {
  position: absolute;
  top: -4px; left: 32px;
  font-family: 'Georgia', serif;
  font-size: 13px; font-weight: 600;
  letter-spacing: 1.5px;
  color: var(--color-soft-ink-soft);
  opacity: 0.6;
}
.wd-ai__label {
  position: absolute;
  top: -4px; right: 32px;
  font-family: var(--font-display);
  font-size: 11px; letter-spacing: 0.22em;
  color: var(--color-soft-ink-soft);
  opacity: 0.6;
  text-transform: uppercase;
}

.wd-ai__inner {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 64px;
  align-items: center;
  margin-top: 36px;
}

/* ── Left column ──────────────────────────────────────────── */
.wd-ai__eyebrow {
  display: inline-block;
  font-family: var(--font-display);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.22em;
  background: var(--color-soft-sage-mist);
  color: var(--color-soft-sage-deep);
  padding: 6px 14px;
  border-radius: var(--radius-soft-pill);
  margin: 0 0 18px;
  text-transform: uppercase;
}

.wd-ai__title {
  font-family: var(--font-display);
  font-size: clamp(34px, 4vw, 52px);
  line-height: 1.05;
  letter-spacing: -0.02em;
  font-weight: 700;
  color: var(--color-soft-ink);
  margin: 0 0 18px;
}
.wd-ai__title-accent {
  color: var(--color-primary);
  font-style: italic;
  font-weight: 800;
}

.wd-ai__sub {
  font-size: 16px;
  line-height: 1.6;
  color: var(--color-soft-ink-soft);
  margin: 0 0 28px;
  max-width: 540px;
  font-weight: 500;
}

.wd-ai__cards {
  list-style: none;
  padding: 0;
  margin: 0 0 32px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.wd-ai__card {
  position: relative;
  padding: 18px 18px 16px;
  border-radius: var(--radius-soft);
  background: var(--color-soft-cream);
  border: 1px solid var(--color-soft-line);
  box-shadow: var(--shadow-soft-sm);
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.wd-ai__card-icon {
  width: 34px; height: 34px;
  border-radius: 10px;
  background: var(--color-primary-light);
  color: var(--color-primary-text);
  display: grid; place-items: center;
}

.wd-ai__card-title {
  font-family: var(--font-display);
  font-size: 14.5px;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: var(--color-soft-ink);
  margin: 0;
}

.wd-ai__card-body {
  font-size: 13px;
  line-height: 1.5;
  color: var(--color-soft-ink-soft);
  margin: 0;
  font-weight: 500;
}
.wd-ai__card-body sub {
  font-size: 0.7em;
  vertical-align: baseline;
}

/* ── CTA row ──────────────────────────────────────────────── */
.wd-ai__actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: flex-start;
}

.wd-ai__cta {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 14px 26px;
  border-radius: var(--radius-btn);
  font-family: var(--font-display);
  font-size: 15px;
  font-weight: 700;
  letter-spacing: -0.01em;
  background: var(--color-primary);
  color: var(--color-primary-text);
  border: 1px solid transparent;
  cursor: pointer;
  box-shadow: var(--shadow-soft-sm);
  transition: transform var(--transition-base), background var(--transition-base), box-shadow 220ms ease;
}
.wd-ai__cta:hover {
  transform: scale(1.03);
  background: var(--color-primary-dark);
  box-shadow: var(--shadow-soft);
}

.wd-ai__cta-hint {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--color-soft-ink-soft);
  margin: 0;
  font-weight: 500;
}

/* ── Right column ─────────────────────────────────────────── */
.wd-ai__art {
  height: 520px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.wd-ai__lottie {
  width: 100%;
  height: 100%;
  max-width: 560px;
}

/* ── Responsive ───────────────────────────────────────────── */
@media (max-width: 1024px) {
  .wd-ai__inner { grid-template-columns: 1fr; gap: 36px; }
  .wd-ai__art { height: 360px; order: -1; }
}

@media (max-width: 640px) {
  .wd-ai { margin-top: 64px; padding: 0 20px; }
  .wd-ai__cards { grid-template-columns: 1fr; gap: 10px; }
  .wd-ai__index, .wd-ai__label { display: none; }
}
</style>
