<template>
  <div class="wd-label-up" :class="{ 'is-busy': isBusy }">
    <label
      class="wd-label-up__drop"
      :class="{ 'is-dragging': isDragging }"
      @dragover.prevent="isDragging = true"
      @dragleave.prevent="isDragging = false"
      @drop.prevent="onDrop"
    >
      <input
        ref="fileInput"
        type="file"
        accept="image/png,image/jpeg,image/webp"
        class="wd-label-up__input"
        @change="onPick"
      />
      <span class="wd-label-up__drop-icon">
        <Camera v-if="!isBusy" :size="18" :stroke-width="1.8" />
        <Loader2 v-else :size="18" :stroke-width="2" class="wd-spin" />
      </span>
      <span class="wd-label-up__drop-text">
        <strong>{{ promptTitle }}</strong>
        <span class="wd-label-up__drop-hint">{{ promptHint }}</span>
      </span>
    </label>

    <Transition name="wd-label-fade">
      <p
        v-if="error"
        class="wd-label-up__error"
        role="alert"
      >
        <CircleAlert :size="13" :stroke-width="2" />
        {{ error }}
      </p>
    </Transition>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { Camera, Loader2, CircleAlert } from 'lucide-vue-next'
import { recognizeLabel } from '../../services/wardrobeApi.js'

const props = defineProps({
  reupload: { type: Boolean, default: false }
})
const emit = defineEmits(['recognized', 'error'])

const fileInput = ref(null)
const isBusy = ref(false)
const isDragging = ref(false)
const error = ref('')

const ACCEPTED = ['image/png', 'image/jpeg', 'image/webp']

const promptTitle = computed(() => {
  if (isBusy.value) return 'Reading the label…'
  return props.reupload ? 'Re-upload washing label' : 'Upload washing label'
})
const promptHint = computed(() => {
  if (isBusy.value) return 'OCR usually takes 3–8 seconds.'
  return 'JPG / PNG / WEBP · we extract materials automatically.'
})

function onPick(e) {
  const f = e.target.files?.[0]
  if (f) handleFile(f)
  if (fileInput.value) fileInput.value.value = ''
}

function onDrop(e) {
  isDragging.value = false
  const f = e.dataTransfer?.files?.[0]
  if (f) handleFile(f)
}

async function handleFile(file) {
  error.value = ''
  if (!ACCEPTED.includes(file.type)) {
    error.value = 'Unsupported file type. Use JPG / PNG / WEBP.'
    return
  }
  // Reuse the same 10 MB cap that the model service enforces.
  if (file.size > 10 * 1024 * 1024) {
    error.value = 'Image too large (max 10 MB).'
    return
  }

  isBusy.value = true
  try {
    // Stash a data URL of the original upload so we can show the user the
    // label they captured (even if classification is later re-run).
    const dataUrl = await readAsDataUrl(file)
    const payload = await recognizeLabel(file)
    if (!payload?.materials || payload.materials.length === 0) {
      error.value = 'No materials recognised. Try a closer or sharper photo.'
      emit('error', payload?.notes?.[0] || 'no_materials')
    } else {
      emit('recognized', {
        materials: payload.materials,
        raw_label_text: payload.raw_text || '',
        translated_text: payload.translated_text || '',
        label_image_base64: dataUrl,
        label_uploaded_at: Date.now()
      })
    }
  } catch (err) {
    const msg = err?.message || 'OCR failed. Please retry.'
    error.value = msg
    emit('error', msg)
  } finally {
    isBusy.value = false
  }
}

function readAsDataUrl(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => resolve(reader.result)
    reader.onerror = () => reject(reader.error || new Error('Failed to read file'))
    reader.readAsDataURL(file)
  })
}
</script>

<style scoped>
.wd-label-up {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.wd-label-up.is-busy { opacity: 0.92; }

.wd-label-up__drop {
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
  border: 1.5px dashed var(--color-border-strong);
  border-radius: var(--radius-card-sm);
  background: var(--color-primary-lighter);
  padding: 12px 14px;
  cursor: pointer;
  transition: border-color var(--transition-base), background var(--transition-base);
}
.wd-label-up__drop:hover,
.wd-label-up__drop.is-dragging {
  border-color: var(--color-primary-text);
  background: var(--color-primary-light);
}

.wd-label-up__input {
  position: absolute;
  inset: 0;
  opacity: 0;
  cursor: pointer;
}

.wd-label-up__drop-icon {
  width: 32px;
  height: 32px;
  border-radius: 999px;
  background: var(--color-primary);
  color: var(--color-primary-text);
  display: grid;
  place-items: center;
  flex-shrink: 0;
}

.wd-label-up__drop-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
  font-size: 12px;
  color: var(--color-text);
}
.wd-label-up__drop-text strong {
  font-size: 13px;
  font-weight: 700;
}
.wd-label-up__drop-hint {
  font-size: 11px;
  color: var(--color-text-subtle);
}

.wd-label-up__error {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  color: var(--color-danger);
  background: rgba(208, 50, 56, 0.06);
  padding: 6px 10px;
  border-radius: var(--radius-pill);
}

.wd-spin { animation: wd-spin 0.9s linear infinite; }
@keyframes wd-spin { to { transform: rotate(360deg); } }

.wd-label-fade-enter-active,
.wd-label-fade-leave-active {
  transition: opacity 220ms cubic-bezier(0.22, 1, 0.36, 1),
              transform 220ms cubic-bezier(0.22, 1, 0.36, 1);
}
.wd-label-fade-enter-from { opacity: 0; transform: translateY(-4px); }
.wd-label-fade-leave-to   { opacity: 0; transform: translateY(-4px); }
</style>
