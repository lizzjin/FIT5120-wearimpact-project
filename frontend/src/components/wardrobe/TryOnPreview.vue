<template>
  <div class="wd-tryon">
    <header class="wd-tryon__head">
      <button
        type="button"
        class="wd-tryon__mannequin"
        @click="pickerOpen = true"
        :aria-label="`Selected mannequin: ${mannequinLabel}. Click to choose another.`"
      >
        <img :src="mannequinImageUrl" :alt="mannequinLabel" />
        <span class="wd-tryon__mannequin-badge">
          <UserRound :size="11" :stroke-width="2" />
        </span>
      </button>
      <div class="wd-tryon__head-text">
        <p class="wd-tryon__eyebrow">Try-on preview</p>
        <button
          type="button"
          class="wd-tryon__change"
          @click="pickerOpen = true"
        >
          {{ mannequinLabel }}
          <ChevronDown :size="11" :stroke-width="2.4" />
        </button>
      </div>
    </header>

    <div class="wd-tryon__stage">
      <Transition name="wd-tryon-fade" mode="out-in">
        <div v-if="state === 'loading'" key="loading" class="wd-tryon__state">
          <Loader2 :size="22" :stroke-width="2" class="wd-spin" />
          <p class="wd-tryon__hint">Rendering on the mannequin…</p>
          <p class="wd-tryon__hint-sub">Usually 8–15 seconds.</p>
        </div>
        <div v-else-if="state === 'error'" key="error" class="wd-tryon__state">
          <CircleAlert :size="22" :stroke-width="2" class="wd-tryon__error-icon" />
          <p class="wd-tryon__hint">{{ errorMessage }}</p>
          <button type="button" class="wd-tryon__retry" @click="reset">
            Reset
          </button>
        </div>
        <div v-else-if="state === 'result' && resultImage" key="result" class="wd-tryon__state wd-tryon__state--result">
          <img :src="resultImage" alt="Mannequin wearing the selected garment" />
        </div>
        <div v-else key="idle" class="wd-tryon__state wd-tryon__state--idle">
          <Shirt :size="22" :stroke-width="1.6" />
          <p class="wd-tryon__hint">Pick an item and tap "Try on mannequin".</p>
        </div>
      </Transition>
    </div>

    <button
      v-if="state === 'result'"
      type="button"
      class="wd-tryon__action wd-tryon__action--ghost"
      @click="reset"
    >
      Try another piece
    </button>

    <Teleport to="body">
      <Transition name="wd-tryon-modal">
        <div
          v-if="pickerOpen"
          class="wd-tryon-modal"
          role="dialog"
          aria-modal="true"
          @click.self="pickerOpen = false"
        >
          <MannequinPicker
            class="wd-tryon-modal__inner"
            @close="pickerOpen = false"
            @change="onMannequinChange"
          />
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import {
  Shirt, Loader2, CircleAlert, ChevronDown, UserRound
} from 'lucide-vue-next'
import MannequinPicker from './MannequinPicker.vue'
import { mannequinStore, getMannequinImageUrl } from '../../stores/mannequinStore.js'

const emit = defineEmits(['mannequin-change'])

const state = ref('idle')  // idle | loading | result | error
const resultImage = ref('')
const errorMessage = ref('')
const pickerOpen = ref(false)

const mannequinLabel = computed(() => {
  const sel = mannequinStore.selected
  if (!sel?.category || !sel?.filename) return 'Female · model-03'
  const id = sel.filename.replace(/\.png$/i, '')
  return `${sel.category} · ${id}`
})

const mannequinImageUrl = computed(() => getMannequinImageUrl(mannequinStore.selected))

function onMannequinChange(selection) {
  emit('mannequin-change', selection)
}

function startLoading() {
  state.value = 'loading'
  errorMessage.value = ''
  resultImage.value = ''
}

function showResult(image) {
  if (!image) {
    showError('Try-on returned no image.')
    return
  }
  resultImage.value = image
  state.value = 'result'
}

function showError(message) {
  errorMessage.value = message || 'Try-on failed. Please retry.'
  state.value = 'error'
}

function reset() {
  state.value = 'idle'
  resultImage.value = ''
  errorMessage.value = ''
}

defineExpose({ startLoading, showResult, showError, reset })
</script>

<style scoped>
.wd-tryon {
  background: var(--color-surface);
  border-radius: var(--radius-card);
  padding: 14px;
  box-shadow: var(--shadow-card);
  display: flex;
  flex-direction: column;
  gap: 12px;
  flex: 1;
  min-height: 0;
}

.wd-tryon__head {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}

.wd-tryon__mannequin {
  position: relative;
  width: 44px; height: 56px;
  border-radius: var(--radius-card-sm);
  overflow: hidden;
  background: var(--color-surface-alt);
  border: 1px solid var(--color-border-light);
  padding: 0;
  cursor: pointer;
  flex-shrink: 0;
}
.wd-tryon__mannequin img {
  width: 100%; height: 100%; object-fit: cover;
}
.wd-tryon__mannequin-badge {
  position: absolute;
  bottom: 3px; right: 3px;
  width: 16px; height: 16px;
  border-radius: 999px;
  background: var(--color-primary);
  color: var(--color-primary-text);
  display: grid; place-items: center;
  border: 2px solid var(--color-surface);
}

.wd-tryon__head-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}
.wd-tryon__eyebrow {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1.2px;
  text-transform: uppercase;
  color: var(--color-text-subtle);
}
.wd-tryon__change {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: transparent;
  border: none;
  padding: 0;
  font-size: 12px;
  font-weight: 700;
  color: var(--color-primary-text);
  cursor: pointer;
}
.wd-tryon__change:hover { text-decoration: underline; text-underline-offset: 3px; }

.wd-tryon__stage {
  flex: 1;
  min-height: 0;
  border-radius: var(--radius-card-sm);
  background: linear-gradient(160deg, var(--color-primary-lighter), var(--color-surface-alt));
  display: grid;
  place-items: center;
  overflow: hidden;
}

.wd-tryon__state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  text-align: center;
  padding: 16px;
  color: var(--color-primary-text);
  width: 100%; height: 100%;
}

.wd-tryon__state--idle {
  color: var(--color-text-faint);
}

.wd-tryon__state--result {
  padding: 0;
}
.wd-tryon__state--result img {
  width: 100%; height: 100%;
  object-fit: contain;
  background: var(--color-surface);
}

.wd-tryon__hint {
  font-size: 12px;
  font-weight: 700;
  margin: 0;
}
.wd-tryon__hint-sub {
  font-size: 11px;
  font-weight: 600;
  opacity: 0.75;
  margin: 0;
}

.wd-tryon__error-icon {
  color: var(--color-danger);
}

.wd-tryon__retry {
  margin-top: 4px;
  padding: 4px 10px;
  border-radius: var(--radius-pill);
  background: var(--color-surface);
  color: var(--color-text);
  border: 1px solid var(--color-border-strong);
  font-size: 11px; font-weight: 600;
  cursor: pointer;
}

.wd-tryon__action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 8px 12px;
  border-radius: var(--radius-pill);
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  border: 1px solid var(--color-border-strong);
  background: transparent;
  color: var(--color-text-muted);
}
.wd-tryon__action--ghost:hover {
  border-color: var(--color-primary-text);
  color: var(--color-primary-text);
}

.wd-spin { animation: wd-spin 0.9s linear infinite; }
@keyframes wd-spin { to { transform: rotate(360deg); } }

.wd-tryon-fade-enter-active,
.wd-tryon-fade-leave-active {
  transition: opacity 220ms cubic-bezier(0.22, 1, 0.36, 1);
}
.wd-tryon-fade-enter-from,
.wd-tryon-fade-leave-to { opacity: 0; }

.wd-tryon-modal {
  position: fixed;
  inset: 0;
  background: rgba(20, 30, 18, 0.45);
  display: grid;
  place-items: center;
  z-index: 60;
  padding: 24px;
}
.wd-tryon-modal__inner {
  width: min(420px, 100%);
  max-height: min(80vh, 640px);
}
.wd-tryon-modal-enter-active,
.wd-tryon-modal-leave-active {
  transition: opacity 220ms cubic-bezier(0.22, 1, 0.36, 1);
}
.wd-tryon-modal-enter-from,
.wd-tryon-modal-leave-to { opacity: 0; }
</style>
