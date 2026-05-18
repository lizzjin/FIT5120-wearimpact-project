<template>
  <nav class="step-indicator" :aria-label="ariaLabel">
    <ol class="step-indicator__list">
      <li
        v-for="(step, i) in steps"
        :key="step.key || i"
        class="step-indicator__item"
        :class="{
          'is-active': i === activeIdx,
          'is-done': i < activeIdx,
        }"
      >
        <span class="step-indicator__dot" aria-hidden="true">
          <Check v-if="i < activeIdx" :size="12" :stroke-width="3" />
          <span v-else class="step-indicator__num">{{ i + 1 }}</span>
        </span>
        <span class="step-indicator__label">{{ step.label }}</span>
        <span
          v-if="i < steps.length - 1"
          class="step-indicator__bar"
          aria-hidden="true"
        />
      </li>
    </ol>
    <p v-if="currentTitle" class="step-indicator__current">
      <span class="step-indicator__eyebrow">Step {{ activeIdx + 1 }} of {{ steps.length }}</span>
      <span class="step-indicator__title">{{ currentTitle }}</span>
    </p>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { Check } from 'lucide-vue-next'

const props = defineProps({
  steps: {
    type: Array,
    required: true,
    validator: (arr) => Array.isArray(arr) && arr.every((s) => s && typeof s.label === 'string'),
  },
  activeKey: { type: [String, Number], default: null },
  activeIndex: { type: Number, default: 0 },
  ariaLabel: { type: String, default: 'Progress' },
})

const activeIdx = computed(() => {
  if (props.activeKey != null) {
    const idx = props.steps.findIndex((s) => s.key === props.activeKey)
    if (idx >= 0) return idx
  }
  return Math.max(0, Math.min(props.activeIndex, props.steps.length - 1))
})

const currentTitle = computed(() => props.steps[activeIdx.value]?.title || '')
</script>

<style scoped>
.step-indicator {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.step-indicator__list {
  display: flex;
  flex-wrap: nowrap;
  list-style: none;
  padding: 0;
  margin: 0;
  gap: 0;
  overflow-x: auto;
  scrollbar-width: none;
}
.step-indicator__list::-webkit-scrollbar { display: none; }

.step-indicator__item {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
  position: relative;
}

.step-indicator__dot {
  width: 26px;
  height: 26px;
  border-radius: 999px;
  background: var(--color-soft-milk, var(--color-surface-alt, #e8ebe6));
  color: var(--color-soft-ink-soft, var(--color-text-muted, #454745));
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  transition:
    background 220ms ease,
    color 220ms ease,
    transform 220ms ease;
  flex-shrink: 0;
}

.step-indicator__num {
  line-height: 1;
}

.step-indicator__label {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-soft-ink-soft, var(--color-text-muted, #454745));
  white-space: nowrap;
  transition: color 220ms ease;
  font-family: var(--font-display, inherit);
}

.step-indicator__bar {
  display: inline-block;
  width: 28px;
  height: 2px;
  background: var(--color-soft-line, var(--color-border-light, rgba(14, 15, 12, 0.08)));
  margin: 0 6px;
  border-radius: 2px;
}

.is-active .step-indicator__dot {
  background: var(--color-primary, #9fe870);
  color: var(--color-primary-text, #163300);
  transform: scale(1.08);
  box-shadow: 0 0 0 4px rgba(159, 232, 112, 0.22);
}
.is-active .step-indicator__label {
  color: var(--color-soft-ink, var(--color-text));
  font-weight: 700;
}

.is-done .step-indicator__dot {
  background: var(--color-soft-sage-deep, var(--color-primary-text, #163300));
  color: var(--color-primary, #9fe870);
}
.is-done .step-indicator__label {
  color: var(--color-soft-ink-soft, var(--color-text-muted));
}

.step-indicator__current {
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.step-indicator__eyebrow {
  font-family: var(--font-display, inherit);
  font-size: 11px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--color-soft-ink-soft, var(--color-text-faint, #aeaeae));
  font-weight: 700;
}
.step-indicator__title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-soft-ink, var(--color-text));
}

@media (max-width: 640px) {
  .step-indicator__label { display: none; }
  .step-indicator__bar { width: 18px; margin: 0 4px; }
}

@media (prefers-reduced-motion: reduce) {
  .is-active .step-indicator__dot { transform: none; }
}
</style>
