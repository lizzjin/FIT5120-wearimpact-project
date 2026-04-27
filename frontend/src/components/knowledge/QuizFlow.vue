<template>
  <section id="quiz-flow" class="quiz-flow" ref="sectionRef">
    <div class="quiz-flow__progress" aria-hidden="true">
      <div class="quiz-flow__progress-fill" :style="{ width: `${progressPct}%` }"></div>
    </div>

    <div class="quiz-flow__slot">
      <Transition name="quiz-card" mode="out-in">
        <QuizCard
          :key="currentQuestion.id"
          :question="currentQuestion"
          :index="index"
          :total="total"
          :revealed="revealed"
          :last-answer="lastAnswer"
          @pick="onPick"
          @next="onNext"
        />
      </Transition>
    </div>

  </section>
</template>

<script setup>
import { computed, inject, ref } from 'vue'
import { quizQuestions } from '../../data/quizQuestions.js'
import QuizCard from './QuizCard.vue'

const emit = defineEmits(['complete'])
const bus = inject('quizBus', null)

const total = quizQuestions.length
const index = ref(0)
const answers = ref([])
const revealed = ref(false)
const isComplete = ref(false)

const sectionRef = ref(null)

const currentQuestion = computed(() => quizQuestions[index.value])
const lastAnswer = computed(() => answers.value[index.value] ?? null)
const progressPct = computed(() => ((index.value + 1) / total) * 100)

function onPick(optionIndex) {
  if (revealed.value) return
  const isCorrect = optionIndex === currentQuestion.value.correctIndex
  answers.value[index.value] = { picked: optionIndex, isCorrect }
  revealed.value = true
  bus?.emit(isCorrect ? 'pick:correct' : 'pick:wrong', { index: index.value })
}

function onNext() {
  if (index.value + 1 >= total) {
    isComplete.value = true
    bus?.emit('complete', [...answers.value])
    emit('complete', [...answers.value])
    return
  }
  bus?.emit('advance', { from: index.value })
  // Vue's <Transition mode="out-in"> handles the swap: old card fades+
  // slides out fully before the new one mounts. No manual GSAP timeline,
  // no flicker, no race conditions with Vue re-render.
  revealed.value = false
  index.value += 1
}

</script>

<style scoped>
.quiz-flow {
  position: relative;
  min-height: 100vh;
  padding: 80px 20px 100px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.quiz-flow__progress {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: rgba(22, 51, 0, 0.06);
  overflow: hidden;
}

.quiz-flow__progress-fill {
  height: 100%;
  background: var(--gradient-kh-progress);
  box-shadow: 0 0 12px var(--color-kh-glow-purple);
  transition: width 600ms cubic-bezier(0.22, 1, 0.36, 1);
}

.quiz-flow__slot {
  width: 100%;
  display: flex;
  justify-content: center;
}

/* ── Card swap — Vue Transition mode="out-in" ───────────────────────
   Old card slides + fades out (200ms) then new card slides + fades in
   (350ms). out-in mode guarantees full unmount of old before mount of
   new — no DOM races, no option flash. */
.quiz-card-enter-active {
  transition:
    opacity 350ms cubic-bezier(0.22, 1, 0.36, 1),
    transform 350ms cubic-bezier(0.22, 1, 0.36, 1);
}

.quiz-card-leave-active {
  transition:
    opacity 200ms cubic-bezier(0.65, 0, 0.35, 1),
    transform 200ms cubic-bezier(0.65, 0, 0.35, 1);
}

.quiz-card-enter-from {
  opacity: 0;
  transform: translateX(40px);
}

.quiz-card-leave-to {
  opacity: 0;
  transform: translateX(-40px);
}

</style>
