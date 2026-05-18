<template>
  <div class="wd-compact" :class="{ 'is-busy': isBusy }">
    <header class="wd-compact__head">
      <div class="wd-compact__icon">
        <UploadCloud :size="16" :stroke-width="2" />
      </div>
      <div>
        <p class="wd-compact__title">Add more clothes</p>
        <p class="wd-compact__hint">JPG · PNG · WEBP — up to 8 photos</p>
      </div>
    </header>

    <label
      class="wd-compact__drop"
      :class="{ 'is-dragging': isDragging }"
      @dragover.prevent="isDragging = true"
      @dragleave.prevent="isDragging = false"
      @drop.prevent="onDrop"
    >
      <input
        ref="fileInput"
        type="file"
        accept="image/png,image/jpeg,image/webp"
        multiple
        class="wd-compact__input"
        @change="onPick"
      />
      <span v-if="files.length === 0" class="wd-compact__drop-empty">
        Drop photos here — or <span class="wd-compact__drop-link">browse</span>
      </span>
      <span v-else class="wd-compact__drop-empty">
        {{ files.length }} ready to go
      </span>
    </label>

    <ul v-if="files.length" class="wd-compact__thumbs">
      <li v-for="(f, i) in files" :key="i" class="wd-compact__thumb">
        <img :src="previews[i]" :alt="f.name" />
        <button
          type="button"
          class="wd-compact__remove"
          aria-label="Remove file"
          @click="removeFile(i)"
        >
          <X :size="10" :stroke-width="2.6" />
        </button>
      </li>
    </ul>

    <!-- Status row collapses to nothing once setSummary / setError
         timers fire, so the panel doesn't keep a permanent "Added 3."
         flag after the toast has already done its job. Transition
         fades the row out instead of yanking it. -->
    <Transition name="wd-status" mode="out-in">
      <div
        v-if="statusBar"
        :key="statusBar.type"
        class="wd-compact__status"
        :class="`wd-compact__status--${statusBar.type}`"
      >
        <component
          :is="statusBar.icon"
          :size="13"
          :stroke-width="2"
          :class="statusBar.iconClass"
        />
        {{ statusBar.text }}
      </div>
    </Transition>

    <button
      type="button"
      class="wd-compact__cta"
      :disabled="files.length === 0 || isBusy"
      ref="ctaRef"
      @click="classify"
    >
      <Sparkles :size="14" :stroke-width="2" />
      {{ isBusy ? 'Classifying…' : 'Classify & save' }}
    </button>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, ref, watch } from 'vue'
import {
  UploadCloud, X, CircleAlert, Loader2, CheckCircle2, Sparkles
} from 'lucide-vue-next'
import { extractItems, pollPreview } from '../../services/wardrobeApi.js'
import { addGarment, updateGarmentImage } from '../../services/wardrobeDb.js'
import { useRipple, useToast } from '../../motion'
import { humanize } from '../../utils/friendlyError.js'

const emit = defineEmits(['saved'])

const ctaRef = ref(null)
const toast = useToast()
// Click ripple on the Classify & save button — a tactile beat that
// confirms the press before the ~1 min model spin-up. Dark green tint
// to read against the lime CTA background.
useRipple(ctaRef, { color: 'rgba(22, 51, 0, 0.18)' })

const fileInput = ref(null)
const files = ref([])
const previews = ref([])
const isDragging = ref(false)
const isBusy = ref(false)
const statusMessage = ref('')
const errorMessage = ref('')
const lastSummary = ref('')

const ACCEPTED = ['image/png', 'image/jpeg', 'image/webp']
const MAX_FILES = 8
const MAX_TOTAL_MB = 10

// In-panel status banners auto-dismiss so the panel does not stay
// permanently flagged after a single upload. Success / warning info is
// already mirrored in a global toast (see classify() below), so the
// in-panel copy is a short visual receipt rather than a sticky badge.
const SUMMARY_TIMEOUT_MS = 4000
const ERROR_TIMEOUT_MS = 6000
let summaryTimer = null
let errorTimer = null

function setSummary(text) {
  lastSummary.value = text
  if (summaryTimer) clearTimeout(summaryTimer)
  if (text) {
    summaryTimer = setTimeout(() => { lastSummary.value = ''; summaryTimer = null }, SUMMARY_TIMEOUT_MS)
  }
}

function setError(text) {
  errorMessage.value = text
  if (errorTimer) clearTimeout(errorTimer)
  if (text) {
    errorTimer = setTimeout(() => { errorMessage.value = ''; errorTimer = null }, ERROR_TIMEOUT_MS)
  }
}

onBeforeUnmount(() => {
  if (summaryTimer) clearTimeout(summaryTimer)
  if (errorTimer) clearTimeout(errorTimer)
})

// Status row is a single slot: errors win, then in-flight progress,
// then success summary. Returning null tells the <Transition> to fade
// the row out entirely.
const statusBar = computed(() => {
  if (errorMessage.value) return { type: 'err',  icon: CircleAlert,  text: errorMessage.value }
  if (isBusy.value)       return { type: 'info', icon: Loader2,      text: statusMessage.value, iconClass: 'wd-spin' }
  if (lastSummary.value)  return { type: 'ok',   icon: CheckCircle2, text: lastSummary.value }
  return null
})

function onPick(e) {
  ingest(e.target.files)
  if (fileInput.value) fileInput.value.value = ''
}
function onDrop(e) {
  isDragging.value = false
  ingest(e.dataTransfer?.files)
}

function ingest(fileList) {
  setError('')
  if (!fileList) return
  const next = [...files.value]
  for (const f of Array.from(fileList)) {
    if (!ACCEPTED.includes(f.type)) {
      setError(humanize(`Unsupported file: ${f.name}`, { context: 'upload' }))
      continue
    }
    if (next.length >= MAX_FILES) {
      setError(humanize(`Max ${MAX_FILES} photos at a time.`, { context: 'upload' }))
      break
    }
    next.push(f)
  }
  const totalMb = next.reduce((s, f) => s + f.size, 0) / (1024 * 1024)
  if (totalMb > MAX_TOTAL_MB) {
    setError(humanize(`Total size > ${MAX_TOTAL_MB} MB.`, { context: 'upload' }))
    return
  }
  files.value = next
}

function removeFile(i) {
  const next = [...files.value]; next.splice(i, 1); files.value = next
}

watch(files, (val) => {
  for (const url of previews.value) URL.revokeObjectURL(url)
  previews.value = val.map((f) => URL.createObjectURL(f))
})

async function classify() {
  if (files.value.length === 0 || isBusy.value) return
  setError('')
  setSummary('')
  isBusy.value = true
  statusMessage.value = 'Classifying — first run may take ~1 min…'

  try {
    const data = await extractItems(files.value, { mode: 'high' })
    statusMessage.value = 'Saving…'

    let savedCount = 0
    const pollJobs = []

    for (const r of data.results || []) {
      if (!r.ok) continue
      const id = await addGarment({
        filename: r.filename,
        main_category: r.category,
        sub_category: r.subcategory,
        confidence: r.subcategory_confidence,
        image_base64: r.preview_image,
        uploaded_at: Date.now()
      })
      savedCount++

      if (r.preview_token && r.preview_ready === false) {
        pollJobs.push(
          pollPreview(r.preview_token).then((hi) => {
            if (hi) return updateGarmentImage(id, hi)
          })
        )
      }
    }

    const failed = (data.results || []).filter((r) => !r.ok).length
    setSummary(`Added ${savedCount}${failed ? ` · ${failed} failed` : ''}.`)
    if (savedCount > 0) {
      toast.push(`Added ${savedCount} item${savedCount === 1 ? '' : 's'} to your wardrobe.`, { type: 'success' })
    }
    if (failed > 0) {
      toast.push(`${failed} photo${failed === 1 ? '' : 's'} could not be classified.`, { type: 'warning' })
    }
    files.value = []
    emit('saved')
    Promise.all(pollJobs).then(() => emit('saved'))
  } catch (err) {
    const msg = humanize(err, { context: 'upload' })
    setError(msg)
    toast.push(msg, {
      type: 'error',
      timeout: 6000,
    })
  } finally {
    isBusy.value = false
    statusMessage.value = ''
  }
}
</script>

<style scoped>
.wd-compact {
  background: var(--color-soft-cream);
  border-radius: var(--radius-soft);
  border: 1.5px solid var(--color-soft-line-strong);
  padding: 20px;
  box-shadow: var(--shadow-soft);
  display: flex; flex-direction: column; gap: 14px;
}
.wd-compact.is-busy { opacity: 0.94; }

.wd-compact__head {
  display: flex; align-items: center; gap: 12px;
}
.wd-compact__icon {
  width: 36px; height: 36px;
  border-radius: 50%;
  background: var(--color-soft-sage-mist);
  color: var(--color-soft-sage-deep);
  display: grid; place-items: center;
  flex-shrink: 0;
}
.wd-compact__title {
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: var(--color-soft-ink);
}
.wd-compact__hint {
  font-size: 11.5px;
  font-weight: 500;
  color: var(--color-soft-ink-soft);
}

.wd-compact__drop {
  position: relative; display: block;
  border: 1.5px dashed rgba(58, 56, 51, 0.22);
  border-radius: 18px;
  background: var(--color-soft-sage-mist);
  padding: 22px 14px;
  text-align: center; cursor: pointer;
  transition: background 220ms ease, border-color 220ms ease;
}
.wd-compact__drop:hover, .wd-compact__drop.is-dragging {
  background: var(--color-soft-sage);
  border-color: var(--color-soft-sage-deep);
}
.wd-compact__input {
  position: absolute; inset: 0; opacity: 0; cursor: pointer;
}
.wd-compact__drop-empty {
  font-size: 13.5px;
  font-weight: 600;
  color: var(--color-soft-ink);
}
.wd-compact__drop-link {
  color: var(--color-soft-sage-deep);
  text-decoration: underline;
  text-underline-offset: 3px;
  font-weight: 700;
}

.wd-compact__thumbs {
  list-style: none; padding: 0; margin: 0;
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px;
}
.wd-compact__thumb {
  position: relative; aspect-ratio: 1;
  border-radius: 12px;
  overflow: hidden;
  background: var(--color-soft-milk);
  box-shadow: var(--shadow-soft-sm);
}
.wd-compact__thumb img {
  width: 100%; height: 100%; object-fit: cover;
}
.wd-compact__remove {
  position: absolute; top: 4px; right: 4px;
  width: 20px; height: 20px;
  border-radius: 50%;
  border: none;
  background: rgba(58, 56, 51, 0.55);
  color: var(--color-soft-cream);
  display: grid; place-items: center; cursor: pointer;
  transition: background 200ms ease;
}
.wd-compact__remove:hover { background: var(--color-soft-ink); }

.wd-compact__status {
  display: inline-flex; align-items: center; gap: 6px;
  font-size: 12px;
  font-weight: 600;
  padding: 6px 12px;
  border-radius: var(--radius-soft-pill);
}
.wd-compact__status--info { background: var(--color-soft-sage-mist); color: var(--color-soft-sage-deep); }
.wd-compact__status--ok   { background: var(--color-soft-sage-mist); color: var(--color-soft-sage-deep); }
.wd-compact__status--err  { background: var(--color-soft-dusty-wash); color: var(--color-soft-ink); }

.wd-status-enter-active,
.wd-status-leave-active {
  transition: opacity 220ms cubic-bezier(0.22, 1, 0.36, 1),
              transform 220ms cubic-bezier(0.22, 1, 0.36, 1);
}
.wd-status-enter-from { opacity: 0; transform: translateY(4px); }
.wd-status-leave-to   { opacity: 0; transform: translateY(-4px); }

.wd-spin { animation: wd-spin 0.9s linear infinite; }
@keyframes wd-spin { to { transform: rotate(360deg); } }

.wd-compact__cta {
  display: inline-flex; align-items: center; justify-content: center; gap: 8px;
  padding: 12px 18px;
  border-radius: var(--radius-soft-pill);
  border: none;
  background: var(--color-primary); color: var(--color-primary-text);
  font-family: var(--font-display);
  font-size: 13.5px;
  font-weight: 700;
  letter-spacing: -0.01em;
  cursor: pointer;
  box-shadow: var(--shadow-soft-sm);
  transition: background 220ms ease, transform 220ms ease, box-shadow 220ms ease;
}
.wd-compact__cta:hover:not(:disabled) {
  background: var(--color-primary-dark);
  transform: scale(1.03);
  box-shadow: var(--shadow-soft);
}
.wd-compact__cta:disabled {
  background: var(--color-soft-milk);
  color: var(--color-soft-ink-soft);
  opacity: 0.6;
  cursor: not-allowed;
  box-shadow: none;
}
</style>
