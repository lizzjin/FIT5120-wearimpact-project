<template>
  <section class="wd-intro">
    <span class="wd-intro__index" aria-hidden="true">VOL. 01</span>
    <span class="wd-intro__label" aria-hidden="true">DIGITAL WARDROBE — KNOW WHAT YOU OWN</span>

    <div class="wd-intro__inner">
      <!-- Left: text + CTAs -->
      <div class="wd-intro__text">
        <p ref="eyebrowRef" class="wd-intro__eyebrow">
          STEP 03 · CATALOGUE WHAT YOU ALREADY HAVE
        </p>
        <h1 class="wd-intro__title" ref="titleRef">
          <span class="wd-intro__title-line">Your closet,</span>
          <span class="wd-intro__title-line">made <em class="wd-intro__title-accent">visible.</em></span>
        </h1>
        <p ref="subtitleRef" class="wd-intro__subtitle">
          Snap the clothes you already own. We lift them off the background, sort each piece
          into upper-body, lower-body or footwear, and keep the whole wardrobe right here in
          your browser — no account, no upload to the cloud.
        </p>

        <ul ref="bulletsRef" class="wd-intro__bullets">
          <li><Sparkles :size="14" :stroke-width="2" /> AI background removal + auto-categorisation</li>
          <li><Lock :size="14" :stroke-width="2" /> Stored only on this device — clear cache, clear closet</li>
          <li><Hanger :size="14" :stroke-width="2" /> Browse what you own, by category, in one place</li>
        </ul>

        <div ref="actionsRef" class="wd-intro__actions">
          <button
            type="button"
            class="wd-cta wd-cta--ghost"
            :class="{ 'wd-cta--shake': firstTimeShake }"
            @click="onFirstTime"
          >
            <BookOpen :size="16" :stroke-width="2" />
            First time using this
          </button>
          <button
            type="button"
            class="wd-cta wd-cta--primary is-burst-host"
            :class="{ 'wd-cta--shake': shake }"
            @click="onEnter"
          >
            <CtaBurst />
            <CtaFlip>
              <Hanger :size="16" :stroke-width="2" />
              Enter my wardrobe
              <ArrowRight :size="16" :stroke-width="2" />
            </CtaFlip>
          </button>
        </div>

        <Transition name="wd-empty-fade">
          <p v-if="emptyHint" class="wd-intro__empty-hint">
            <CircleAlert :size="14" :stroke-width="2" />
            Your wardrobe is empty — start with
            <button type="button" class="wd-link" @click="$emit('first-time')">
              First time using this
            </button>
            to see how it works.
          </p>
        </Transition>

        <Transition name="wd-empty-fade">
          <p v-if="alreadyHasHint" class="wd-intro__empty-hint">
            <CircleAlert :size="14" :stroke-width="2" />
            You already have {{ total }} item{{ total === 1 ? '' : 's' }} in your closet — head straight to
            <button type="button" class="wd-link" @click="$emit('enter')">
              Enter my wardrobe
            </button>.
          </p>
        </Transition>
      </div>

      <!-- Right: Lottie hero -->
      <div
        class="wd-intro__art"
        ref="artRef"
        aria-hidden="true"
      >
        <Vue3Lottie
          :animation-data="heroAnim"
          :loop="true"
          :autoplay="true"
          class="wd-intro__lottie"
        />
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import {
  Sparkles, Lock, BookOpen, ArrowRight, CircleAlert, Shirt
} from 'lucide-vue-next'
import { Vue3Lottie } from 'vue3-lottie'
import heroAnim from '../../assets/lottie/wardrobe-hero.json'
import CtaBurst from '../CtaBurst.vue'
import CtaFlip from '../CtaFlip.vue'
import { useReveal } from '../../motion/useReveal'
import { useStagger } from '../../motion/useStagger'

const props = defineProps({
  total: { type: Number, default: 0 }
})
const emit = defineEmits(['first-time', 'enter'])

const eyebrowRef = ref(null)
const subtitleRef = ref(null)
const bulletsRef = ref(null)
const actionsRef = ref(null)
const artRef = ref(null)
const titleRef = ref(null)
useReveal(eyebrowRef, { mode: 'char', stagger: 0.022, duration: 0.5 })
useReveal(subtitleRef, { mode: 'fade-blur', y: 60, delay: 0.45 })
useStagger(titleRef, { selector: '.wd-intro__title-line', stagger: 0.12, y: 60, duration: 0.7, delay: 0.1 })
useStagger(bulletsRef, { selector: 'li', stagger: 0.08, y: 24, delay: 0.55 })
useReveal(actionsRef, { mode: 'fade-up', y: 18, delay: 0.7 })
useReveal(artRef, { mode: 'scale-fade', duration: 0.8, delay: 0.25 })

const emptyHint = ref(false)
const alreadyHasHint = ref(false)
const shake = ref(false)
const firstTimeShake = ref(false)

function onEnter() {
  if (props.total === 0) {
    emptyHint.value = true
    alreadyHasHint.value = false
    shake.value = true
    setTimeout(() => (shake.value = false), 600)
    return
  }
  emit('enter')
}

function onFirstTime() {
  // Users with an existing wardrobe shouldn't re-run the onboarding —
  // it's designed for empty-closet first runs and would feel redundant.
  if (props.total > 0) {
    alreadyHasHint.value = true
    emptyHint.value = false
    firstTimeShake.value = true
    setTimeout(() => (firstTimeShake.value = false), 600)
    return
  }
  emit('first-time')
}

// Use Shirt as a hanger-stand-in; Lucide doesn't ship a hanger glyph.
const Hanger = Shirt
</script>

<style scoped>
.wd-intro {
  position: relative;
  max-width: 1280px;
  margin: 0 auto;
  padding: 88px 32px 64px;
}

.wd-intro__index {
  position: absolute;
  top: 96px; left: 32px;
  font-family: 'Georgia', serif;
  font-style: italic;
  font-size: 13px;
  letter-spacing: 0.18em;
  color: var(--color-soft-ink-soft);
}
.wd-intro__label {
  position: absolute;
  top: 100px; right: 32px;
  font-size: 11px;
  letter-spacing: 0.22em;
  color: var(--color-soft-ink-soft);
}

.wd-intro__inner {
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 56px;
  align-items: center;
  margin-top: 48px;
}

.wd-intro__eyebrow {
  display: inline-block;
  font-family: var(--font-display);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.22em;
  color: var(--color-soft-sage-deep);
  background: var(--color-soft-sage-mist);
  padding: 6px 14px;
  border-radius: var(--radius-soft-pill);
  margin-bottom: 22px;
  text-transform: uppercase;
}

.wd-intro__title {
  font-family: var(--font-display);
  font-size: clamp(40px, 6.4vw, 78px);
  line-height: 1.02;
  letter-spacing: -0.025em;
  font-weight: 700;
  color: var(--color-soft-ink);
  margin-bottom: 26px;
  max-width: 720px;
}
.wd-intro__title-line {
  display: block;
}
.wd-intro__title-accent {
  color: var(--color-soft-sage);
  font-style: italic;
  font-weight: 800;
}

.wd-intro__subtitle {
  font-size: 17px; line-height: 1.6;
  color: var(--color-soft-ink-soft);
  max-width: 560px;
  margin-bottom: 22px;
}

.wd-intro__bullets {
  list-style: none; padding: 0; margin: 0 0 28px;
  display: flex; flex-direction: column; gap: 10px;
}
.wd-intro__bullets li {
  display: inline-flex; align-items: center; gap: 10px;
  font-size: 14px;
  font-weight: 500;
  color: var(--color-soft-ink);
}
.wd-intro__bullets li :first-child {
  color: var(--color-soft-sage-deep);
  background: var(--color-soft-sage-mist);
  padding: 6px; border-radius: 999px;
  flex-shrink: 0;
}

.wd-intro__actions {
  display: flex; flex-wrap: wrap; gap: 12px;
}

.wd-cta {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 13px 22px;
  border-radius: var(--radius-soft-pill);
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 700;
  letter-spacing: -0.01em;
  border: none;
  cursor: pointer;
  transition: background 220ms ease, color 220ms ease,
              transform 220ms cubic-bezier(0.22, 1, 0.36, 1),
              box-shadow 220ms ease;
}
.wd-cta--primary {
  background: var(--color-primary);
  color: var(--color-primary-text);
  box-shadow: var(--shadow-soft-sm);
}
.wd-cta--primary:hover {
  background: var(--color-primary-dark);
  transform: scale(1.03);
  box-shadow: var(--shadow-soft);
}

.wd-cta--ghost {
  background: var(--color-soft-cream);
  color: var(--color-soft-ink);
  box-shadow: var(--shadow-soft-sm);
}
.wd-cta--ghost:hover {
  background: var(--color-soft-milk);
  transform: translateY(-2px);
  box-shadow: var(--shadow-soft);
}

.wd-cta--shake {
  animation: wd-shake 480ms cubic-bezier(0.36, 0.07, 0.19, 0.97);
}
@keyframes wd-shake {
  0%, 100% { transform: translateX(0); }
  20%      { transform: translateX(-6px); }
  40%      { transform: translateX(6px); }
  60%      { transform: translateX(-4px); }
  80%      { transform: translateX(4px); }
}

.wd-intro__empty-hint {
  margin-top: 16px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: var(--color-soft-dusty-wash);
  color: var(--color-soft-ink);
  padding: 9px 14px;
  border-radius: var(--radius-soft-pill);
  font-size: 13px;
  font-weight: 600;
}
.wd-link {
  background: none; border: none; padding: 0;
  color: var(--color-soft-sage-deep);
  font-weight: 700;
  cursor: pointer;
  text-decoration: underline;
  text-underline-offset: 3px;
}

/* ── Lottie hero ─────────────────────────────────────────────────────── */
.wd-intro__art {
  height: 540px;
  display: flex; align-items: center; justify-content: center;
}
.wd-intro__lottie {
  width: 100%;
  height: 100%;
  max-width: 640px;
}

.wd-empty-fade-enter-active, .wd-empty-fade-leave-active {
  transition: opacity 220ms ease, transform 220ms ease;
}
.wd-empty-fade-enter-from, .wd-empty-fade-leave-to {
  opacity: 0; transform: translateY(-4px);
}

@media (max-width: 900px) {
  .wd-intro { padding: 64px 20px 40px; }
  .wd-intro__inner { grid-template-columns: 1fr; gap: 32px; }
  .wd-intro__art { height: 320px; }
  .wd-intro__index, .wd-intro__label { top: 64px; }
}

/* Short-laptop tier — compress the wardrobe intro so "Enter my wardrobe"
   fits above the fold on ≤820 px high screens. */
@media (max-height: 820px) and (min-width: 901px) {
  .wd-intro { padding: 56px 32px 28px; }
  .wd-intro__index, .wd-intro__label { top: 56px; }
  .wd-intro__inner { margin-top: 24px; gap: 36px; }
  .wd-intro__title {
    font-size: clamp(32px, 3.6vw, 44px);
    margin-bottom: 14px;
  }
  .wd-intro__eyebrow { margin-bottom: 12px; }
  .wd-intro__subtitle { font-size: 15px; margin-bottom: 16px; }
  .wd-intro__bullets { margin-bottom: 18px; gap: 6px; }
  .wd-intro__bullets li { font-size: 13.5px; }
  .wd-intro__art { height: 380px; }
}
</style>
