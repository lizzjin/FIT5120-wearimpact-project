<template>
  <section class="wd-onboard">
    <button type="button" class="wd-onboard__back" @click="$emit('back')">
      <ArrowLeft :size="16" :stroke-width="2" />
      Back
    </button>

    <header class="wd-onboard__head">
      <p ref="eyebrowRef" class="wd-onboard__eyebrow">FIRST TIME USING THIS</p>
      <AnimatedHeading
        as="h2"
        class="wd-onboard__title"
        text="Three steps to a smarter closet."
        :stagger="0.07"
        :delay="0.1"
      />
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
      >
        <span class="wd-step__num">{{ String(i + 1).padStart(2, '0') }}</span>
        <div class="wd-step__media">
          <div class="wd-anim-placeholder">
            <component :is="step.icon" :size="22" :stroke-width="1.6" />
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
import AnimatedHeading from '../AnimatedHeading.vue'
import CtaBurst from '../CtaBurst.vue'
import CtaFlip from '../CtaFlip.vue'
import { useReveal } from '../../motion/useReveal'
import { useStagger } from '../../motion/useStagger'

defineEmits(['back', 'enter'])

const eyebrowRef = ref(null)
const subRef = ref(null)
const stepsRef = ref(null)
useReveal(eyebrowRef, { mode: 'char', stagger: 0.022, duration: 0.5 })
useReveal(subRef, { mode: 'fade-blur', y: 40, delay: 0.25 })
useStagger(stepsRef, { selector: '.wd-step', stagger: 0.12, y: 32, delay: 0.4 })

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
  max-width: 1200px;
  margin: 0 auto;
  padding: 64px 32px 40px;
}

.wd-onboard__back {
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
.wd-onboard__back:hover { color: var(--color-text); background: var(--color-surface-alt); }

.wd-onboard__head {
  margin-top: 24px;
  margin-bottom: 36px;
  max-width: 720px;
}
.wd-onboard__eyebrow {
  font-size: 12px; font-weight: 700; letter-spacing: 2px;
  color: var(--color-primary-text);
  margin-bottom: 10px;
}
.wd-onboard__title {
  font-size: clamp(32px, 4vw, 48px);
  font-weight: 800; letter-spacing: -1px;
  color: var(--color-text);
  margin-bottom: 14px;
}
.wd-onboard__sub {
  font-size: 16px; line-height: 1.6;
  color: var(--color-text-muted);
}

.wd-steps {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.wd-step {
  position: relative;
  background: var(--color-surface);
  border-radius: var(--radius-card);
  padding: 24px;
  box-shadow: var(--shadow-card);
  transition: transform var(--transition-base), box-shadow var(--transition-base);
}
.wd-step:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-card-hover);
}

.wd-step__num {
  position: absolute;
  top: 18px; right: 22px;
  font-family: 'Georgia', serif;
  font-size: 14px; font-weight: 600;
  color: var(--color-text-faint);
  letter-spacing: 1.5px;
}

.wd-step__media {
  height: 160px;
  margin-bottom: 18px;
}

.wd-anim-placeholder {
  width: 100%; height: 100%;
  border-radius: var(--radius-card-sm);
  background:
    repeating-linear-gradient(
      45deg,
      rgba(159, 232, 112, 0.08) 0 12px,
      transparent 12px 24px
    ),
    var(--color-primary-lighter);
  border: 1.5px dashed rgba(22, 51, 0, 0.18);
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  gap: 8px;
  color: var(--color-primary-text);
}
.wd-anim-placeholder__title {
  font-size: 12px; font-weight: 700; letter-spacing: 0.5px;
}

.wd-step__title {
  font-size: 18px; font-weight: 800;
  color: var(--color-text);
  margin-bottom: 8px;
  letter-spacing: -0.3px;
}
.wd-step__body {
  font-size: 14px; line-height: 1.55;
  color: var(--color-text-muted);
}

.wd-onboard__cta-row {
  margin-top: 36px;
  display: flex; justify-content: center;
}

.wd-cta {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 14px 26px;
  border-radius: var(--radius-btn);
  font-size: 15px; font-weight: 700;
  border: 1px solid transparent;
  cursor: pointer;
  transition: transform var(--transition-base), background var(--transition-base);
}
.wd-cta--primary {
  background: var(--color-primary);
  color: var(--color-primary-text);
}
.wd-cta--primary:hover { transform: scale(1.03); background: var(--color-primary-dark); }

@media (max-width: 900px) {
  .wd-onboard { padding: 40px 20px; }
  .wd-steps { grid-template-columns: 1fr; }
}
</style>
