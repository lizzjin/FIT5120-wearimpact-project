<template>
  <section id="quiz-summary" class="quiz-summary">
    <div
      ref="cardRef"
      class="quiz-summary__card"
      v-motion
      :initial="{ opacity: 0, y: 24 }"
      :visible-once="{ opacity: 1, y: 0, transition: { duration: 700 } }"
    >
      <p class="quiz-summary__eyebrow">Your knowledge snapshot</p>

      <h2 class="quiz-summary__score">
        <span class="quiz-summary__score-num">
          <OdometerNumber :value="correctCount" :duration="1100" />
        </span>
        <span class="quiz-summary__score-of">/ {{ total }}</span>
      </h2>

      <p class="quiz-summary__verdict">{{ verdict }}</p>

      <div class="quiz-summary__stats">
        <div v-for="stat in highlights" :key="stat.label" class="quiz-summary__stat">
          <span class="quiz-summary__stat-value">{{ stat.value }}</span>
          <span class="quiz-summary__stat-label">{{ stat.label }}</span>
        </div>
      </div>

      <p class="quiz-summary__takeaway">
        Buy less. Wear longer. Choose better.
        <br class="quiz-summary__takeaway-break" />
        The single most effective fashion action is the one already in your closet.
      </p>

      <button type="button" class="quiz-summary__cta" @click="scrollToTeaser">
        See how AI can guide your wardrobe
        <ArrowDown :size="16" :stroke-width="2" />
      </button>

      <div class="quiz-summary__art" v-html="summaryArtSvg" aria-hidden="true" />
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { ArrowDown } from 'lucide-vue-next'
import OdometerNumber from '../OdometerNumber.vue'
import summaryArtSvg from '../../assets/illustrations/knowledge-summary-animate.svg?raw'

const props = defineProps({
  answers: { type: Array, required: true },
})

const total = computed(() => props.answers.length)
const correctCount = computed(() => props.answers.filter((a) => a?.isCorrect).length)
const cardRef = ref(null)

const verdict = computed(() => {
  const c = correctCount.value
  if (c === total.value) return 'Top of the class — you really know your fibre footprint.'
  if (c >= 3) return 'Solid instincts. A few stats may still surprise you below.'
  return 'No grade — just facts. Now you know.'
})

const highlights = computed(() => [
  { value: '~30%', label: 'Carbon cut from extending wear by 9 months' },
  { value: '~35%', label: 'Ocean microplastics from synthetic laundry' },
  { value: '200y+', label: 'Polyester persistence in landfill' },
])

function scrollToTeaser() {
  const el = document.getElementById('wardrobe-teaser')
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

onMounted(() => {
  // Replay the Storyset entrance whenever the summary scrolls into view.
  const sectionEl = document.getElementById('quiz-summary')
  const innerSvg = sectionEl?.querySelector('.quiz-summary__art svg[id^="freepik_stories"]')
  if (!innerSvg || !('IntersectionObserver' in window)) return
  const obs = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) innerSvg.classList.add('animated')
        else innerSvg.classList.remove('animated')
      }
    },
    { threshold: 0.2 },
  )
  obs.observe(sectionEl)
})
</script>

<style scoped>
.quiz-summary {
  padding: 80px 20px 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.quiz-summary__card {
  width: 100%;
  max-width: 720px;
  padding: 44px 36px;
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid var(--color-kh-glass-border);
  border-radius: 24px;
  box-shadow: 0 12px 32px rgba(22, 51, 0, 0.06);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 18px;
}

.quiz-summary__eyebrow {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--color-kh-accent);
  margin: 0;
}

.quiz-summary__score {
  margin: 0;
  font-size: clamp(3rem, 8vw, 5rem);
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--color-kh-text);
  font-variant-numeric: tabular-nums;
  display: flex;
  align-items: baseline;
  gap: 8px;
}

.quiz-summary__score-num {
  /* Solid lime text instead of clipped gradient — odometer's inner spans
     don't inherit text-fill-color: transparent reliably on cream bg. */
  color: var(--color-primary-text);
  font-weight: 900;
}

.quiz-summary__score-of {
  font-size: 0.5em;
  color: var(--color-kh-text-faint);
  font-weight: 500;
}

.quiz-summary__verdict {
  font-size: 16px;
  color: var(--color-kh-text-muted);
  margin: 0;
  max-width: 480px;
  line-height: 1.5;
}

.quiz-summary__stats {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  width: 100%;
  margin-top: 8px;
}

.quiz-summary__stat {
  padding: 18px 12px;
  background: var(--color-kh-glass-strong);
  border: 1px solid var(--color-kh-glass-border);
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.quiz-summary__stat-value {
  font-size: clamp(1.4rem, 2.6vw, 1.8rem);
  font-weight: 700;
  color: var(--color-kh-text);
  letter-spacing: -0.01em;
  font-variant-numeric: tabular-nums;
}

.quiz-summary__stat-label {
  font-size: 12px;
  color: var(--color-kh-text-faint);
  line-height: 1.35;
}

.quiz-summary__takeaway {
  font-size: 16px;
  line-height: 1.6;
  color: var(--color-kh-text);
  margin: 8px 0 0;
  max-width: 520px;
}

.quiz-summary__cta {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 12px 24px;
  margin-top: 8px;
  font-size: 14px;
  font-weight: 600;
  color: var(--color-kh-text);
  background: var(--color-kh-glass-strong);
  border: 1px solid var(--color-kh-accent);
  border-radius: 999px;
  cursor: pointer;
  transition: transform 200ms var(--motion-entrance),
    box-shadow 200ms var(--motion-entrance),
    background 200ms var(--motion-entrance);
}

.quiz-summary__cta:hover {
  transform: translateY(-1px);
  background: rgba(159, 232, 112, 0.12);
  box-shadow: 0 0 28px var(--color-kh-glow-blue);
}

.quiz-summary__cta:focus-visible {
  outline: 2px solid var(--color-kh-accent);
  outline-offset: 3px;
}

.quiz-summary__art {
  width: 100%;
  display: flex;
  justify-content: center;
  margin-top: 16px;
}

.quiz-summary__art :deep(svg) {
  width: 100%;
  max-width: 380px;
  height: auto;
}

@media (max-width: 640px) {
  .quiz-summary__card {
    padding: 32px 22px;
  }
  .quiz-summary__stats {
    grid-template-columns: 1fr;
  }
  .quiz-summary__takeaway-break {
    display: none;
  }
}
</style>
