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
          <ChevronDown :size="11" :stroke-width="2" />
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
          <!-- Show the full mannequin photo as the "before" reference so
               the user can compare it against the try-on result. Tapping
               anywhere on it opens the mannequin picker — discoverable
               without an extra button. -->
          <button
            type="button"
            class="wd-tryon__idle-photo"
            :aria-label="`Current mannequin: ${mannequinLabel}. Click to choose another.`"
            @click="pickerOpen = true"
          >
            <img :src="mannequinImageUrl" :alt="mannequinLabel" />
          </button>
          <div class="wd-tryon__idle-caption">
            <p class="wd-tryon__hint">Pick a piece</p>
            <p class="wd-tryon__hint-sub">Then tap "Try on mannequin"</p>
          </div>
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
  background: var(--color-soft-milk);
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  /* Tall enough that a 3:4 mannequin photo reads as a hero shot. */
  min-height: 540px;
}

.wd-tryon__head {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

.wd-tryon__mannequin {
  position: relative;
  width: 48px; height: 60px;
  border-radius: 12px;
  overflow: hidden;
  background: var(--color-soft-cream);
  border: none;
  padding: 0;
  cursor: pointer;
  flex-shrink: 0;
  box-shadow: var(--shadow-soft-sm);
  transition: transform 200ms ease, box-shadow 200ms ease;
}
.wd-tryon__mannequin:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-soft);
}
.wd-tryon__mannequin img {
  width: 100%; height: 100%; object-fit: cover;
}
.wd-tryon__mannequin-badge {
  position: absolute;
  bottom: 3px; right: 3px;
  width: 16px; height: 16px;
  border-radius: 999px;
  background: var(--color-soft-sage);
  color: var(--color-soft-ink);
  display: grid; place-items: center;
  border: 2px solid var(--color-soft-cream);
}

.wd-tryon__head-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}
.wd-tryon__eyebrow {
  font-family: var(--font-display);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--color-soft-ink-soft);
}
.wd-tryon__change {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: transparent;
  border: none;
  padding: 0;
  font-size: 13px;
  font-weight: 700;
  color: var(--color-soft-sage-deep);
  cursor: pointer;
  letter-spacing: -0.01em;
}
.wd-tryon__change:hover { text-decoration: underline; text-underline-offset: 3px; }

.wd-tryon__stage {
  flex: 1;
  min-height: 0;
  border-radius: 18px;
  background: var(--color-soft-cream);
  border: 1px solid var(--color-soft-line-strong);
  display: grid;
  place-items: center;
  overflow: hidden;
  position: relative;
  box-shadow: var(--shadow-soft-sm);
}

.wd-tryon__state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  text-align: center;
  padding: 18px;
  color: var(--color-soft-ink-soft);
  width: 100%; height: 100%;
  position: relative;
}

.wd-tryon__state--idle {
  /* Mannequin photo spans the stage; caption sits as a soft cream chip
     pinned to the bottom-left without obscuring the torso. */
  padding: 0;
  display: block;
  position: relative;
}

.wd-tryon__idle-photo {
  display: block;
  width: 100%;
  height: 100%;
  padding: 0;
  margin: 0;
  border: none;
  background: transparent;
  cursor: pointer;
}
.wd-tryon__idle-photo img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 10px 14px;
  box-sizing: border-box;
}

.wd-tryon__idle-caption {
  position: absolute;
  left: 14px;
  bottom: 14px;
  display: inline-flex;
  flex-direction: column;
  gap: 2px;
  padding: 9px 14px;
  border-radius: 14px;
  background: var(--color-soft-cream);
  color: var(--color-soft-ink);
  text-align: left;
  box-shadow: var(--shadow-soft-sm);
  pointer-events: none;
}

.wd-tryon__state--result {
  padding: 0;
}
.wd-tryon__state--result img {
  width: 100%; height: 100%;
  object-fit: contain;
  background: var(--color-soft-cream);
}

.wd-tryon__hint {
  font-family: var(--font-display);
  font-size: 13px;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: var(--color-soft-ink);
  margin: 0;
}
.wd-tryon__hint-sub {
  font-size: 11.5px;
  font-weight: 500;
  color: var(--color-soft-ink-soft);
  margin: 0;
}

.wd-tryon__error-icon {
  color: var(--color-soft-dusty);
}

.wd-tryon__retry {
  margin-top: 6px;
  padding: 7px 16px;
  border-radius: var(--radius-soft-pill);
  border: none;
  background: var(--color-primary);
  color: var(--color-primary-text);
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: background 200ms ease;
}
.wd-tryon__retry:hover { background: var(--color-primary-dark); }

.wd-tryon__action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px 16px;
  border-radius: var(--radius-soft-pill);
  font-size: 12.5px;
  font-weight: 600;
  cursor: pointer;
  border: 1px solid var(--color-soft-line);
  background: transparent;
  color: var(--color-soft-ink-soft);
  transition: background 200ms ease, color 200ms ease, border-color 200ms ease;
}
.wd-tryon__action--ghost:hover {
  background: var(--color-soft-sage-mist);
  color: var(--color-soft-sage-deep);
  border-color: transparent;
}

.wd-spin { animation: wd-spin 0.9s linear infinite; }
@keyframes wd-spin { to { transform: rotate(360deg); } }

.wd-tryon-fade-enter-active,
.wd-tryon-fade-leave-active {
  transition: opacity 240ms cubic-bezier(0.22, 1, 0.36, 1);
}
.wd-tryon-fade-enter-from,
.wd-tryon-fade-leave-to { opacity: 0; }

.wd-tryon-modal {
  position: fixed;
  inset: 0;
  background: rgba(58, 56, 51, 0.35);
  display: grid;
  place-items: center;
  z-index: 60;
  padding: 24px;
}
.wd-tryon-modal__inner {
  width: min(440px, 100%);
  max-height: min(80vh, 640px);
}
.wd-tryon-modal-enter-active,
.wd-tryon-modal-leave-active {
  transition: opacity 240ms cubic-bezier(0.22, 1, 0.36, 1);
}
.wd-tryon-modal-enter-from,
.wd-tryon-modal-leave-to { opacity: 0; }
</style>
