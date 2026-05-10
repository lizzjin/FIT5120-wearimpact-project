<template>
  <section class="wd-intro">
    <span class="wd-intro__index" aria-hidden="true">WD</span>
    <span class="wd-intro__label" aria-hidden="true">DIGITAL WARDROBE — KNOW WHAT YOU OWN</span>

    <div class="wd-intro__inner">
      <!-- Left: text + CTAs -->
      <div class="wd-intro__text">
        <p ref="eyebrowRef" class="wd-intro__eyebrow">
          STEP 03 · CATALOGUE WHAT YOU ALREADY HAVE
        </p>
        <AnimatedHeading
          as="h1"
          class="wd-intro__title"
          :stagger="0.07"
          :delay="0.1"
        >
          Your closet,<br />
          <span class="wd-intro__title-accent">made visible.</span>
        </AnimatedHeading>
        <p ref="subtitleRef" class="wd-intro__subtitle">
          Snap the clothes you already own. We lift them off the background, sort each piece
          into upper-body, lower-body or footwear, and keep the whole wardrobe right here in
          your browser — no account, no upload to the cloud.
        </p>

        <ul ref="bulletsRef" class="wd-intro__bullets">
          <li><Sparkles :size="14" :stroke-width="2" /> AI background removal + auto-categorisation</li>
          <li><Lock :size="14" :stroke-width="2" /> Stored only on this device — clearing browser data clears it</li>
          <li><Hanger :size="14" :stroke-width="2" /> Browse what you own, by category, in one place</li>
        </ul>

        <div ref="actionsRef" class="wd-intro__actions">
          <button type="button" class="wd-cta wd-cta--ghost" @click="$emit('first-time')">
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
      </div>

      <!-- Right: Lottie hero -->
      <div
        class="wd-intro__art"
        v-motion
        :initial="{ opacity: 0, scale: 0.94 }"
        :enter="{ opacity: 1, scale: 1, transition: { duration: 800, delay: 200 } }"
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
import AnimatedHeading from '../AnimatedHeading.vue'
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
useReveal(eyebrowRef, { mode: 'char', stagger: 0.022, duration: 0.5 })
useReveal(subtitleRef, { mode: 'fade-blur', y: 60, delay: 0.25 })
useStagger(bulletsRef, { selector: 'li', stagger: 0.08, y: 24, delay: 0.4 })
useReveal(actionsRef, { mode: 'fade-up', y: 18, delay: 0.55 })

const emptyHint = ref(false)
const shake = ref(false)

function onEnter() {
  if (props.total === 0) {
    emptyHint.value = true
    shake.value = true
    setTimeout(() => (shake.value = false), 600)
    return
  }
  emit('enter')
}

// Use Shirt as a hanger-stand-in; Lucide doesn't ship a hanger glyph.
const Hanger = Shirt
</script>

<style scoped>
.wd-intro {
  position: relative;
  max-width: 1200px;
  margin: 0 auto;
  padding: 96px 32px 64px;
}

.wd-intro__index {
  position: absolute;
  top: 96px; left: 32px;
  font-family: 'Georgia', serif;
  font-size: 13px; font-weight: 600;
  letter-spacing: 1.5px;
  color: var(--color-text-faint);
}
.wd-intro__label {
  position: absolute;
  top: 96px; right: 32px;
  font-size: 11px; letter-spacing: 2px;
  color: var(--color-text-faint);
}

.wd-intro__inner {
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 56px;
  align-items: center;
  margin-top: 48px;
}

.wd-intro__eyebrow {
  font-size: 12px; font-weight: 700; letter-spacing: 2px;
  color: var(--color-primary-text);
  margin-bottom: 18px;
}

.wd-intro__title {
  font-size: clamp(40px, 5vw, 64px);
  font-weight: 800; letter-spacing: -1.5px;
  line-height: 1.04; color: var(--color-text);
  margin-bottom: 22px;
}
.wd-intro__title-accent {
  color: var(--color-primary);
}

.wd-intro__subtitle {
  font-size: 17px; line-height: 1.6;
  color: var(--color-text-muted);
  max-width: 560px; margin-bottom: 22px;
}

.wd-intro__bullets {
  list-style: none; padding: 0; margin: 0 0 28px;
  display: flex; flex-direction: column; gap: 10px;
}
.wd-intro__bullets li {
  display: inline-flex; align-items: center; gap: 10px;
  font-size: 14px; color: var(--color-text-muted);
}
.wd-intro__bullets li :first-child {
  color: var(--color-primary-text);
  background: var(--color-primary-light);
  padding: 6px; border-radius: 999px;
}

.wd-intro__actions {
  display: flex; flex-wrap: wrap; gap: 10px;
}

.wd-cta {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 13px 24px;
  border-radius: var(--radius-btn);
  font-size: 15px; font-weight: 700;
  border: 1px solid transparent;
  cursor: pointer;
  transition: transform var(--transition-base), background var(--transition-base), color var(--transition-base);
}
.wd-cta--primary {
  background: var(--color-primary);
  color: var(--color-primary-text);
}
.wd-cta--primary:hover { transform: scale(1.03); background: var(--color-primary-dark); }

.wd-cta--ghost {
  background: var(--color-surface);
  color: var(--color-text);
  border-color: var(--color-border-strong);
}
.wd-cta--ghost:hover {
  background: var(--color-surface-alt);
  transform: scale(1.02);
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
  background: rgba(255, 192, 145, 0.18);
  color: var(--color-text);
  border: 1px solid rgba(255, 192, 145, 0.6);
  padding: 10px 14px;
  border-radius: var(--radius-pill);
  font-size: 13px;
}
.wd-link {
  background: none; border: none; padding: 0;
  color: var(--color-primary-text);
  font-weight: 700; cursor: pointer;
  text-decoration: underline; text-underline-offset: 2px;
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
</style>
