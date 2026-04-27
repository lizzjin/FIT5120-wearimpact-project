<template>
  <section id="quiz-hero" class="quiz-hero">
    <span class="quiz-hero__index" aria-hidden="true">Q&amp;A</span>
    <span class="quiz-hero__label" aria-hidden="true">KNOWLEDGE — TEST YOURSELF</span>

    <div class="quiz-hero__inner">
      <div class="quiz-hero__text">
        <p
          class="quiz-hero__eyebrow"
          v-motion
          :initial="{ opacity: 0, y: 12 }"
          :enter="{ opacity: 1, y: 0, transition: { duration: 500 } }"
        >
          SUSTAINABLE FASHION · KNOWLEDGE HUB
        </p>

        <h1
          class="quiz-hero__title"
          v-motion
          :initial="{ opacity: 0, y: 24 }"
          :enter="{ opacity: 1, y: 0, transition: { duration: 700, delay: 100 } }"
        >
          Decode the hidden impact<br />
          of every garment.
        </h1>

        <p
          class="quiz-hero__subtitle"
          v-motion
          :initial="{ opacity: 0, y: 18 }"
          :enter="{ opacity: 1, y: 0, transition: { duration: 600, delay: 250 } }"
        >
          Five quick questions. Real numbers behind what you wear.
        </p>

        <div ref="statsRef" class="quiz-hero__stats">
          <div class="quiz-hero__stat">
            <span class="quiz-hero__stat-value">
              <OdometerNumber :value="100" :duration="1400" />B
            </span>
            <span class="quiz-hero__stat-label">Garments produced / year</span>
          </div>
          <div class="quiz-hero__stat">
            <span class="quiz-hero__stat-value">
              <OdometerNumber :value="92" :duration="1400" />M
            </span>
            <span class="quiz-hero__stat-label">Tonnes of textile waste / year</span>
          </div>
          <div class="quiz-hero__stat">
            <span class="quiz-hero__stat-value">
              <OdometerNumber :value="2" :duration="1200" />×
            </span>
            <span class="quiz-hero__stat-label">Drop in average wears per garment</span>
          </div>
        </div>

        <button
          type="button"
          class="quiz-hero__cta"
          @click="scrollToQuiz"
          v-motion
          :initial="{ opacity: 0, y: 20 }"
          :enter="{ opacity: 1, y: 0, transition: { duration: 600, delay: 500 } }"
        >
          Start the quiz
          <ArrowDown :size="18" :stroke-width="2" />
        </button>
      </div>

      <div class="quiz-hero__art" v-html="heroArtSvg" aria-hidden="true" />
    </div>

    <button
      type="button"
      class="quiz-hero__scroll-cue"
      aria-label="Scroll to quiz"
      @click="scrollToQuiz"
    >
      <span class="quiz-hero__scroll-dot"></span>
    </button>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { ArrowDown } from 'lucide-vue-next'
import OdometerNumber from '../OdometerNumber.vue'
import heroArtSvg from '../../assets/illustrations/knowledge-hero-animate.svg?raw'

const statsRef = ref(null)

function scrollToQuiz() {
  const el = document.getElementById('quiz-flow')
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

onMounted(() => {
  // Pre-warm the GSAP chunk so the user's first card-swap is instant.
  import('gsap').catch(() => {})

  // Replay the Storyset entrance whenever the hero scrolls into view.
  const heroSection = document.getElementById('quiz-hero')
  const innerSvg = heroSection?.querySelector('.quiz-hero__art svg[id^="freepik_stories"]')
  if (!innerSvg || !('IntersectionObserver' in window)) return

  const obs = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          innerSvg.classList.add('animated')
        } else {
          innerSvg.classList.remove('animated')
        }
      }
    },
    { threshold: 0.2 },
  )
  obs.observe(heroSection)
})
</script>

<style scoped>
.quiz-hero {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 120px 48px 100px;
  overflow: hidden;
}

/* Decorative giant `Q&A` index, mirroring the .section-index on Home */
.quiz-hero__index {
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

.quiz-hero__label {
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

.quiz-hero__inner {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1.05fr);
  gap: 64px;
  width: 100%;
  max-width: 1320px;
  align-items: center;
  position: relative;
  z-index: 2;
}

.quiz-hero__text {
  display: flex;
  flex-direction: column;
  gap: 24px;
  align-items: flex-start;
}

.quiz-hero__eyebrow {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--color-primary-text);
  margin: 0;
}

.quiz-hero__title {
  font-size: clamp(2.6rem, 5.5vw, 4.6rem);
  line-height: 0.95;
  font-weight: 900;
  letter-spacing: -0.02em;
  color: var(--color-text);
  margin: 0;
  text-wrap: balance;
}

.quiz-hero__subtitle {
  font-size: clamp(1rem, 1.5vw, 1.18rem);
  color: var(--color-text-muted);
  max-width: 540px;
  margin: 0;
  line-height: 1.55;
}

.quiz-hero__stats {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  width: 100%;
  max-width: 540px;
  margin-top: 8px;
}

.quiz-hero__stat {
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid var(--color-kh-glass-border);
  border-radius: 14px;
  padding: 16px 12px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.quiz-hero__stat-value {
  font-size: clamp(1.5rem, 2.6vw, 2rem);
  font-weight: 900;
  color: var(--color-text);
  letter-spacing: -0.01em;
  font-variant-numeric: tabular-nums;
}

.quiz-hero__stat-label {
  font-size: 12px;
  color: var(--color-text-muted);
  line-height: 1.35;
}

.quiz-hero__cta {
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
  transition: transform 200ms var(--motion-entrance), box-shadow 200ms var(--motion-entrance);
  box-shadow: 0 0 0 0 rgba(22, 51, 0, 0);
  margin-top: 8px;
}

.quiz-hero__cta:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(22, 51, 0, 0.18);
}

.quiz-hero__cta:focus-visible {
  outline: 2px solid var(--color-primary-text);
  outline-offset: 4px;
}

.quiz-hero__art {
  display: flex;
  align-items: center;
  justify-content: center;
}

.quiz-hero__art :deep(svg) {
  width: 100%;
  max-width: 580px;
  height: auto;
  filter: drop-shadow(0 24px 60px rgba(22, 51, 0, 0.08));
}

.quiz-hero__scroll-cue {
  position: absolute;
  bottom: 200px;
  left: 50%;
  transform: translateX(-50%);
  width: 26px;
  height: 42px;
  border: 1px solid var(--color-text-subtle);
  border-radius: 14px;
  background: transparent;
  cursor: pointer;
  display: inline-flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: 6px;
  transition: border-color 200ms var(--motion-entrance);
  z-index: 2;
}

.quiz-hero__scroll-cue:hover {
  border-color: var(--color-primary-text);
}

.quiz-hero__scroll-dot {
  width: 3px;
  height: 8px;
  border-radius: 2px;
  background: var(--color-text-muted);
  animation: kh-scroll-bounce 2.2s ease-in-out infinite;
}

@keyframes kh-scroll-bounce {
  0%, 100% { transform: translateY(0); opacity: 1; }
  50%      { transform: translateY(14px); opacity: 0.2; }
}

@media (max-width: 1024px) {
  .quiz-hero__title { font-size: clamp(2.2rem, 7vw, 3.4rem); }
  .quiz-hero__inner { gap: 48px; }
}

@media (max-width: 768px) {
  .quiz-hero {
    padding: 100px 24px 80px;
  }
  .quiz-hero__inner {
    grid-template-columns: 1fr;
    gap: 40px;
  }
  .quiz-hero__index,
  .quiz-hero__label {
    display: none;
  }
  .quiz-hero__stats {
    grid-template-columns: 1fr;
    max-width: 320px;
  }
  .quiz-hero__scroll-cue { display: none; }
}
</style>
