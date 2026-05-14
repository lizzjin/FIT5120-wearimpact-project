<template>
  <section class="wd-onboard">
    <button type="button" class="wd-onboard__back" @click="$emit('back')">
      <ArrowLeft :size="16" :stroke-width="2" />
      Back
    </button>

    <header class="wd-onboard__head">
      <p ref="eyebrowRef" class="wd-onboard__eyebrow">FIRST TIME USING THIS</p>
      <h2 class="wd-onboard__title" ref="titleRef">
        <span class="wd-onboard__title-line">Three steps to a</span>
        <span class="wd-onboard__title-line"><em class="wd-onboard__title-accent">smarter</em> closet.</span>
      </h2>
      <p ref="subRef" class="wd-onboard__sub">
        Snap, sort, browse. Each piece you upload is processed locally and stays on your
        device. Here's what happens at each step.
      </p>
    </header>

    <div ref="stepsRef" class="wd-steps">
      <article
        v-for="(step, i) in steps"
        :key="step.title"
        class="wd-step"
        :class="`wd-step--${stepThemes[i]}`"
      >
        <span class="wd-step__num">{{ String(i + 1).padStart(2, '0') }}</span>
        <div class="wd-step__media">
          <div class="wd-anim-placeholder">
            <component :is="step.icon" :size="28" :stroke-width="2.4" />
            <p class="wd-anim-placeholder__title">{{ step.placeholder }}</p>
          </div>
        </div>
        <h3 class="wd-step__title">{{ step.title }}</h3>
        <p class="wd-step__body">{{ step.body }}</p>
      </article>
    </div>

    <div class="wd-onboard__cta-row">
      <button type="button" class="wd-cta wd-cta--primary is-burst-host" @click="$emit('enter')">
        <CtaBurst />
        <CtaFlip>
          I'm ready — take me to my wardrobe
          <ArrowRight :size="16" :stroke-width="2" />
        </CtaFlip>
      </button>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { ArrowLeft, ArrowRight, Camera, Brain, LayoutGrid } from 'lucide-vue-next'
import CtaBurst from '../CtaBurst.vue'
import CtaFlip from '../CtaFlip.vue'
import { useReveal } from '../../motion/useReveal'
import { useStagger } from '../../motion/useStagger'

defineEmits(['back', 'enter'])

const eyebrowRef = ref(null)
const subRef = ref(null)
const stepsRef = ref(null)
const titleRef = ref(null)
useReveal(eyebrowRef, { mode: 'char', stagger: 0.022, duration: 0.5 })
useReveal(subRef, { mode: 'fade-blur', y: 40, delay: 0.4 })
useStagger(titleRef, { selector: '.wd-onboard__title-line', stagger: 0.1, y: 36, delay: 0.1, duration: 0.6 })
useStagger(stepsRef, { selector: '.wd-step', stagger: 0.12, y: 32, delay: 0.55 })

// Theme per step — soft morandi palette echoing the wardrobe tiles.
const stepThemes = ['sage', 'dusty', 'oat']

const steps = [
  {
    title: 'Snap or upload your clothes',
    body: 'Take a clean photo against any background — or pick existing photos from your device. Up to 8 at a time.',
    icon: Camera,
    placeholder: 'Upload demo animation'
  },
  {
    title: 'AI sorts each piece',
    body: 'We remove the background, identify whether it is upper-body, lower-body or footwear, and tag the subcategory.',
    icon: Brain,
    placeholder: 'Classification animation'
  },
  {
    title: 'Browse your wardrobe',
    body: 'Everything lands in three drawers — upper-body, lower-body, footwear. Click any item to see details and washing notes.',
    icon: LayoutGrid,
    placeholder: 'Wardrobe walkthrough'
  }
]
</script>

<style scoped>
.wd-onboard {
  position: relative;
  max-width: 1280px;
  margin: 0 auto;
  padding: 64px 32px 48px;
}

.wd-onboard__back {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 8px 16px;
  border-radius: var(--radius-soft-pill);
  background: var(--color-soft-cream);
  border: none;
  color: var(--color-soft-ink-soft);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: var(--shadow-soft-sm);
  transition: background 220ms ease, color 220ms ease, transform 220ms ease;
}
.wd-onboard__back:hover {
  background: var(--color-soft-milk);
  color: var(--color-soft-ink);
  transform: translateY(-1px);
}

.wd-onboard__head {
  margin-top: 30px;
  margin-bottom: 40px;
  max-width: 880px;
}
.wd-onboard__eyebrow {
  display: inline-block;
  font-family: var(--font-display);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.22em;
  background: var(--color-soft-sage-mist);
  color: var(--color-soft-sage-deep);
  padding: 6px 14px;
  border-radius: var(--radius-soft-pill);
  margin-bottom: 18px;
  text-transform: uppercase;
}
.wd-onboard__title {
  font-family: var(--font-display);
  font-size: clamp(32px, 4.8vw, 56px);
  line-height: 1.05;
  letter-spacing: -0.02em;
  font-weight: 700;
  color: var(--color-soft-ink);
  margin-bottom: 18px;
}
.wd-onboard__title-line { display: block; }
.wd-onboard__title-accent {
  color: var(--color-soft-sage);
  font-style: italic;
  font-weight: 800;
}
.wd-onboard__sub {
  font-size: 16px; line-height: 1.6;
  color: var(--color-soft-ink-soft);
}

.wd-steps {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 22px;
}

.wd-step {
  position: relative;
  background: var(--color-soft-cream);
  border-radius: var(--radius-soft);
  border: 1.5px solid var(--color-soft-line-strong);
  padding: 28px 26px 26px;
  box-shadow: var(--shadow-soft);
  transition: transform 240ms cubic-bezier(0.22, 1, 0.36, 1),
              box-shadow 240ms ease;
}
.wd-step:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-soft-lg);
}
.wd-step--sage  { background: var(--color-soft-sage-mist); }
.wd-step--dusty { background: var(--color-soft-dusty-wash); }
.wd-step--oat   { background: var(--color-soft-oat); }

.wd-step__num {
  position: absolute;
  top: 18px; right: 22px;
  font-family: var(--font-display);
  font-style: italic;
  font-weight: 800;
  font-size: 28px;
  line-height: 1;
  color: var(--color-soft-ink);
  opacity: 0.35;
}

.wd-step__media {
  height: 156px;
  margin-bottom: 18px;
}

.wd-anim-placeholder {
  width: 100%; height: 100%;
  border-radius: 16px;
  background: var(--color-soft-cream);
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  gap: 10px;
  color: var(--color-soft-sage-deep);
  box-shadow: var(--shadow-soft-sm);
}
.wd-anim-placeholder__title {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.04em;
  color: var(--color-soft-ink-soft);
  text-align: center;
}

.wd-step__title {
  font-family: var(--font-display);
  font-size: 19px;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: var(--color-soft-ink);
  margin-bottom: 10px;
}
.wd-step__body {
  font-size: 14px;
  line-height: 1.55;
  color: var(--color-soft-ink);
  opacity: 0.78;
}

.wd-onboard__cta-row {
  margin-top: 40px;
  display: flex; justify-content: center;
}

.wd-cta {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 13px 26px;
  border-radius: var(--radius-soft-pill);
  border: none;
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 700;
  letter-spacing: -0.01em;
  cursor: pointer;
  transition: background 220ms ease, color 220ms ease, transform 220ms ease, box-shadow 220ms ease;
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

@media (max-width: 900px) {
  .wd-onboard { padding: 40px 20px; }
  .wd-steps { grid-template-columns: 1fr; }
}
</style>
