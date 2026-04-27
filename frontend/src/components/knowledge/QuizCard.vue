<template>
  <article ref="cardRef" class="quiz-card">
    <header class="quiz-card__header">
      <span class="quiz-card__counter">
        Question {{ String(index + 1).padStart(2, '0') }}
        <span class="quiz-card__counter-of">/ {{ String(total).padStart(2, '0') }}</span>
      </span>
    </header>

    <h2 class="quiz-card__question">{{ question.question }}</h2>

    <div class="quiz-card__options">
      <QuizOption
        v-for="(opt, i) in question.options"
        :key="`${question.id}-${i}`"
        :option="opt"
        :index="i"
        :state="optionState(i)"
        @pick="onPick"
      />
    </div>

    <Transition name="quiz-explanation">
      <div v-if="revealed" class="quiz-card__explanation">
        <div class="quiz-card__explanation-row">
          <span
            class="quiz-card__verdict"
            :class="lastAnswer?.isCorrect ? 'quiz-card__verdict--good' : 'quiz-card__verdict--bad'"
          >
            {{ lastAnswer?.isCorrect ? 'Correct' : 'Not quite' }}
          </span>
          <span class="quiz-card__answer-text">
            Answer:
            <strong>{{ question.options[question.correctIndex] }}</strong>
          </span>
        </div>
        <p class="quiz-card__explanation-text">{{ question.explanation }}</p>
        <p class="quiz-card__explanation-source">— {{ question.source }}</p>
        <button type="button" class="quiz-card__next" @click="onNext">
          {{ isLast ? 'See your summary' : 'Next question' }}
          <ArrowRight :size="16" :stroke-width="2" />
        </button>
      </div>
    </Transition>
  </article>
</template>

<script setup>
import { computed, ref } from 'vue'
import { ArrowRight } from 'lucide-vue-next'
import QuizOption from './QuizOption.vue'

const props = defineProps({
  question: { type: Object, required: true },
  index: { type: Number, required: true },
  total: { type: Number, required: true },
  revealed: { type: Boolean, default: false },
  lastAnswer: { type: Object, default: null }, // { picked, isCorrect } | null
})

const emit = defineEmits(['pick', 'next'])

const cardRef = ref(null)
defineExpose({ cardRef })

const isLast = computed(() => props.index + 1 >= props.total)

function optionState(i) {
  if (!props.revealed) return 'default'
  if (i === props.question.correctIndex) return 'correct'
  if (props.lastAnswer && i === props.lastAnswer.picked) return 'wrong'
  return 'inert'
}

function onPick(i) {
  emit('pick', i)
}

function onNext() {
  emit('next')
}
</script>

<style scoped>
.quiz-card {
  position: relative;
  width: 100%;
  max-width: 720px;
  margin: 0 auto;
  padding: 36px 36px 32px;
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid var(--color-kh-glass-border);
  border-radius: 24px;
  box-shadow: 0 12px 32px rgba(22, 51, 0, 0.06);
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.quiz-card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.quiz-card__counter {
  font-size: 12px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--color-kh-accent);
  font-weight: 600;
}

.quiz-card__counter-of {
  color: var(--color-kh-text-faint);
  margin-left: 4px;
}

.quiz-card__question {
  font-size: clamp(1.5rem, 2.6vw, 2rem);
  line-height: 1.25;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: var(--color-kh-text);
  margin: 0;
  text-wrap: balance;
}

.quiz-card__options {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.quiz-card__explanation {
  margin-top: 4px;
  padding: 20px 22px;
  background: var(--color-kh-glass-strong);
  border: 1px solid var(--color-kh-glass-border);
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.quiz-card__explanation-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.quiz-card__verdict {
  display: inline-flex;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.quiz-card__verdict--good {
  color: var(--color-kh-correct);
  background: rgba(159, 232, 112, 0.16);
  border: 1px solid rgba(159, 232, 112, 0.45);
}

.quiz-card__verdict--bad {
  color: var(--color-kh-wrong);
  background: rgba(255, 192, 145, 0.16);
  border: 1px solid rgba(255, 192, 145, 0.45);
}

.quiz-card__answer-text {
  font-size: 14px;
  color: var(--color-kh-text-muted);
}

.quiz-card__answer-text strong {
  color: var(--color-kh-text);
  font-weight: 600;
}

.quiz-card__explanation-text {
  font-size: 15px;
  line-height: 1.55;
  color: var(--color-kh-text-muted);
  margin: 0;
}

.quiz-card__explanation-source {
  font-size: 12px;
  color: var(--color-kh-text-faint);
  margin: 0;
  font-style: italic;
}

.quiz-card__next {
  align-self: flex-start;
  margin-top: 6px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  font-size: 14px;
  font-weight: 600;
  color: var(--color-kh-text);
  background: var(--color-kh-glass-strong);
  border: 1px solid var(--color-kh-accent);
  border-radius: 999px;
  cursor: pointer;
  transition: transform 180ms var(--motion-entrance),
    box-shadow 180ms var(--motion-entrance),
    background 180ms var(--motion-entrance);
}

.quiz-card__next:hover {
  transform: translateY(-1px);
  background: rgba(159, 232, 112, 0.12);
  box-shadow: 0 0 24px var(--color-kh-glow-blue);
}

.quiz-card__next:focus-visible {
  outline: 2px solid var(--color-kh-accent);
  outline-offset: 3px;
}

/* Slide-down explanation strip — max-height + opacity for smoothness. */
.quiz-explanation-enter-active,
.quiz-explanation-leave-active {
  transition: max-height 360ms var(--motion-entrance),
    opacity 280ms var(--motion-entrance),
    margin-top 360ms var(--motion-entrance),
    padding 360ms var(--motion-entrance);
  overflow: hidden;
}

.quiz-explanation-enter-from,
.quiz-explanation-leave-to {
  max-height: 0;
  opacity: 0;
  padding-top: 0;
  padding-bottom: 0;
  margin-top: 0;
}

.quiz-explanation-enter-to,
.quiz-explanation-leave-from {
  max-height: 320px;
  opacity: 1;
}

@media (max-width: 640px) {
  .quiz-card {
    padding: 24px 20px 20px;
    border-radius: 20px;
  }
}
</style>
