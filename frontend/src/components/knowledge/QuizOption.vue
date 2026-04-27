<template>
  <button
    ref="btnRef"
    type="button"
    class="quiz-option"
    :class="[`quiz-option--${state}`]"
    :disabled="state === 'inert'"
    :aria-pressed="state === 'correct' || state === 'wrong'"
    @click="handleClick"
  >
    <span class="quiz-option__letter">{{ letter }}</span>
    <span class="quiz-option__text">{{ option }}</span>
    <span class="quiz-option__icon" aria-hidden="true">
      <Check v-if="showCorrectIcon" :size="18" :stroke-width="2.5" />
      <X v-else-if="showWrongIcon" :size="18" :stroke-width="2.5" />
    </span>
    <Transition name="kh-burst">
      <span
        v-if="showBurst"
        class="quiz-option__burst"
        :class="`quiz-option__burst--${burstColorState}`"
        aria-hidden="true"
      ></span>
    </Transition>
  </button>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { Check, X } from 'lucide-vue-next'

const props = defineProps({
  option: { type: String, required: true },
  index: { type: Number, required: true },
  // 'default' | 'correct' | 'wrong' | 'inert'
  state: { type: String, default: 'default' },
})

const emit = defineEmits(['pick'])

const btnRef = ref(null)
const letter = computed(() => String.fromCharCode(65 + props.index))
const showCorrectIcon = computed(() => props.state === 'correct')
const showWrongIcon = computed(() => props.state === 'wrong')

function handleClick() {
  if (props.state === 'inert' || props.state === 'correct' || props.state === 'wrong') return
  emit('pick', props.index)
}

// Reveal burst — short expanding ring on transition into correct/wrong.
const showBurst = ref(false)
const burstColorState = ref('correct')

watch(
  () => props.state,
  (next, prev) => {
    if (prev !== 'default') return
    if (next !== 'correct' && next !== 'wrong') return
    if (window.matchMedia?.('(prefers-reduced-motion: reduce)').matches) return
    burstColorState.value = next
    showBurst.value = true
    setTimeout(() => {
      showBurst.value = false
    }, 650)
  },
)
</script>

<style scoped>
.quiz-option {
  position: relative;
  display: grid;
  grid-template-columns: 32px 1fr 24px;
  align-items: center;
  gap: 14px;
  width: 100%;
  padding: 16px 20px;
  font-size: 15px;
  font-weight: 500;
  text-align: left;
  color: var(--color-kh-text);
  background: var(--color-kh-glass);
  border: 1px solid var(--color-kh-glass-border);
  border-radius: 14px;
  cursor: pointer;
  transition:
    transform 160ms var(--motion-entrance),
    border-color 160ms var(--motion-entrance),
    background 160ms var(--motion-entrance),
    box-shadow 200ms var(--motion-entrance);
  overflow: visible;
}

.quiz-option:not(.quiz-option--inert):not(.quiz-option--correct):not(.quiz-option--wrong):hover {
  border-color: var(--color-kh-accent);
  background: rgba(159, 232, 112, 0.18);
  box-shadow: 0 4px 14px rgba(22, 51, 0, 0.08);
  transform: translateY(-1px);
}

.quiz-option:focus-visible {
  outline: 2px solid var(--color-kh-accent);
  outline-offset: 3px;
}

.quiz-option__letter {
  width: 32px;
  height: 32px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.04em;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid var(--color-kh-glass-border);
  color: var(--color-kh-text-muted);
}

.quiz-option__text {
  line-height: 1.45;
}

.quiz-option__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
}

.quiz-option--correct {
  border-color: var(--color-kh-correct);
  background: rgba(205, 255, 173, 0.5);
  box-shadow: var(--shadow-kh-glow-correct);
  cursor: default;
}

.quiz-option--correct .quiz-option__letter {
  background: var(--color-kh-correct);
  border-color: var(--color-primary-text);
  color: var(--color-primary-text);
}

.quiz-option--correct .quiz-option__icon {
  color: var(--color-primary-text);
}

.quiz-option--wrong {
  border-color: var(--color-kh-wrong);
  background: rgba(255, 192, 145, 0.4);
  box-shadow: var(--shadow-kh-glow-wrong);
  cursor: default;
}

.quiz-option--wrong .quiz-option__letter {
  background: var(--color-kh-wrong);
  border-color: var(--color-primary-text);
  color: var(--color-primary-text);
}

.quiz-option--wrong .quiz-option__icon {
  color: var(--color-primary-text);
}

.quiz-option--inert {
  opacity: 0.5;
  pointer-events: none;
  cursor: default;
}

.quiz-option__burst {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  pointer-events: none;
  transform: translate(-50%, -50%) scale(0.4);
  border: 2px solid currentColor;
  opacity: 0.8;
}

.quiz-option__burst--correct {
  color: var(--color-kh-pulse-correct);
  box-shadow: 0 0 22px var(--color-kh-pulse-correct);
}

.quiz-option__burst--wrong {
  color: var(--color-kh-pulse-wrong);
  box-shadow: 0 0 22px var(--color-kh-pulse-wrong);
}

.kh-burst-enter-active {
  animation: kh-option-burst 600ms cubic-bezier(0.22, 1, 0.36, 1) forwards;
}
.kh-burst-leave-active {
  transition: opacity 120ms ease;
}
.kh-burst-leave-to {
  opacity: 0;
}

@keyframes kh-option-burst {
  0% {
    transform: translate(-50%, -50%) scale(0.3);
    opacity: 0.85;
  }
  60% {
    opacity: 0.55;
  }
  100% {
    transform: translate(-50%, -50%) scale(2.6);
    opacity: 0;
  }
}

@media (prefers-reduced-motion: reduce) {
  .quiz-option__burst {
    display: none;
  }
}
</style>
