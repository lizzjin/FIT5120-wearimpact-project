<template>
  <aside class="wd-detail" :class="{ 'wd-detail--empty': !garment }">
    <!-- Inner scroll container: the outer card clips with border-radius +
         overflow:hidden so the scrollbar can never poke out of the rounded
         corner. The actual scrolling happens here. -->
    <div class="wd-detail__scroll" data-lenis-prevent>
    <div v-if="!garment" class="wd-detail__placeholder">
      <div class="wd-detail__placeholder-icon">
        <Hand :size="22" :stroke-width="1.6" />
      </div>
      <p class="wd-detail__placeholder-title">Pick a piece</p>
      <p class="wd-detail__placeholder-hint">
        Tap any item on the right to inspect its photo, washing label and subcategory.
      </p>
    </div>

    <template v-else>
      <header class="wd-detail__head">
        <span class="wd-detail__main-tag">{{ formatMain(garment.main_category) }}</span>
        <button
          type="button"
          class="wd-detail__close"
          aria-label="Close detail"
          @click="$emit('close')"
        >
          <X :size="14" :stroke-width="2.4" />
        </button>
      </header>

      <div class="wd-detail__media">
        <img v-if="garment.image_base64" :src="garment.image_base64" :alt="garment.filename" />
      </div>

      <!-- Washing label section — real OCR-derived materials when the user
           has scanned a label, otherwise a prompt to scan one. -->
      <section class="wd-detail__section">
        <h4 class="wd-detail__section-title">
          <Droplets :size="13" :stroke-width="2" />
          Washing label
        </h4>

        <div v-if="hasMaterials" class="wd-detail__materials">
          <MaterialPills :materials="garment.materials" />
          <button
            type="button"
            class="wd-detail__relabel"
            @click="reuploadOpen = !reuploadOpen"
          >
            <RefreshCw :size="11" :stroke-width="2" />
            {{ reuploadOpen ? 'Cancel re-scan' : 'Re-upload label' }}
          </button>
          <WashLabelUploader
            v-if="reuploadOpen"
            reupload
            @recognized="onLabelRecognized"
            @error="onLabelError"
          />
        </div>
        <div v-else>
          <WashLabelUploader
            @recognized="onLabelRecognized"
            @error="onLabelError"
          />
          <p class="wd-detail__care-hint">
            Photograph the composition line of the label (e.g. "60% Cotton 40% Polyester").
          </p>
        </div>
      </section>

      <section class="wd-detail__section">
        <h4 class="wd-detail__section-title">
          <Tag :size="13" :stroke-width="2" />
          Subcategory
        </h4>
        <span class="wd-detail__sub-tag">{{ formatSub(garment.sub_category) }}</span>
      </section>

      <section class="wd-detail__section">
        <h4 class="wd-detail__section-title">
          <Calendar :size="13" :stroke-width="2" />
          Added
        </h4>
        <p class="wd-detail__meta">{{ formatDate(garment.uploaded_at) }}</p>
      </section>

      <div class="wd-detail__actions">
        <button
          v-if="canTryOn"
          type="button"
          class="wd-detail__tryon"
          @click="$emit('try-on', garment)"
        >
          <Shirt :size="14" :stroke-width="2" />
          Try on mannequin
        </button>
        <button
          v-else
          type="button"
          class="wd-detail__tryon wd-detail__tryon--disabled"
          disabled
          title="FASHN VTON does not support footwear try-on yet."
        >
          <Shirt :size="14" :stroke-width="2" />
          Footwear try-on unavailable
        </button>

        <button type="button" class="wd-detail__delete" @click="$emit('delete', garment.id)">
          <Trash2 :size="14" :stroke-width="2" />
          Remove from wardrobe
        </button>
      </div>
    </template>
    </div>
  </aside>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import {
  Hand, X, Droplets, Tag, Calendar, Trash2, RefreshCw, Shirt
} from 'lucide-vue-next'
import MaterialPills from './MaterialPills.vue'
import WashLabelUploader from './WashLabelUploader.vue'
import { updateGarmentMaterials } from '../../services/wardrobeDb.js'
import { useToast } from '../../motion'

const props = defineProps({
  garment: { type: Object, default: null }
})
const emit = defineEmits(['close', 'delete', 'refresh', 'try-on'])

const toast = useToast()
const reuploadOpen = ref(false)

// Collapse the re-upload form whenever the user switches to a different
// garment — keeps the UI clean and avoids stale state across selections.
watch(() => props.garment?.id, () => {
  reuploadOpen.value = false
})

const MAIN_LABEL = {
  upper_body: 'Tops',
  lower_body: 'Bottoms',
  footwear: 'Shoes'
}

const hasMaterials = computed(
  () => Array.isArray(props.garment?.materials) && props.garment.materials.length > 0
)

const canTryOn = computed(() => props.garment?.main_category !== 'footwear')

function formatMain(v) { return MAIN_LABEL[v] || v || 'Unknown' }
function formatSub(v) {
  if (!v) return 'Unsorted'
  return String(v).replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())
}
function formatDate(ts) {
  if (!ts) return '—'
  return new Date(ts).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' })
}

async function onLabelRecognized(payload) {
  const id = props.garment?.id
  if (!id) return
  try {
    await updateGarmentMaterials(id, {
      materials: payload.materials,
      raw_label_text: payload.raw_label_text,
      label_image_base64: payload.label_image_base64,
      label_uploaded_at: payload.label_uploaded_at
    })
    reuploadOpen.value = false
    toast.push(
      `Recognised ${payload.materials.length} material${payload.materials.length === 1 ? '' : 's'}.`,
      { type: 'success' }
    )
    emit('refresh')
  } catch (err) {
    toast.push(err?.message || 'Could not save materials.', { type: 'error' })
  }
}

function onLabelError(message) {
  if (typeof message === 'string' && message !== 'no_materials') {
    toast.push(message, { type: 'warning' })
  }
}
</script>

<style scoped>
.wd-detail {
  background: var(--color-surface);
  border-radius: var(--radius-card-lg);
  box-shadow: var(--shadow-card);
  /* Clip the rounded corners so the inner scrollbar can never poke past them. */
  overflow: hidden;
  display: flex;
  flex-direction: column;
  /* Stretch to fill the left column above the AI advisor card so the panel
     and the rest of the page top-edge / bottom-edge align cleanly. */
  flex: 1;
  min-height: 0;
}

.wd-detail__scroll {
  flex: 1;
  min-height: 0;
  padding: 22px;
  display: flex;
  flex-direction: column;
  gap: 18px;
  overflow-y: auto;
  /* Thin scrollbar that lives entirely inside the rounded outer clip. */
  scrollbar-width: thin;
  scrollbar-color: var(--color-border-strong) transparent;
}
.wd-detail__scroll::-webkit-scrollbar {
  width: 6px;
}
.wd-detail__scroll::-webkit-scrollbar-track {
  background: transparent;
}
.wd-detail__scroll::-webkit-scrollbar-thumb {
  background: var(--color-border-strong);
  border-radius: 999px;
}
.wd-detail__scroll::-webkit-scrollbar-thumb:hover {
  background: var(--color-text-faint);
}
.wd-detail__scroll::-webkit-scrollbar-button {
  display: none;
  height: 0;
  width: 0;
}

.wd-detail--empty .wd-detail__scroll {
  align-items: center;
  justify-content: center;
  text-align: center;
}

.wd-detail__placeholder-icon {
  width: 56px; height: 56px;
  border-radius: 999px;
  background: var(--color-primary-light);
  color: var(--color-primary-text);
  display: grid; place-items: center;
  border: 1px solid var(--color-border-light);
  margin: 0 auto 14px;
}

.wd-detail__placeholder-title {
  font-size: 18px; font-weight: 800;
  color: var(--color-text);
  margin-bottom: 6px;
}
.wd-detail__placeholder-hint {
  font-size: 13px; color: var(--color-text-subtle);
  max-width: 240px; line-height: 1.5;
  margin: 0 auto;
}

.wd-detail__head {
  display: flex; align-items: center; justify-content: space-between;
  flex-shrink: 0;
}
.wd-detail__main-tag {
  display: inline-block;
  background: var(--color-primary);
  color: var(--color-primary-text);
  padding: 5px 12px;
  border-radius: var(--radius-pill);
  font-size: 12px; font-weight: 700; letter-spacing: 0.3px;
}
.wd-detail__close {
  width: 28px; height: 28px;
  border-radius: 999px;
  border: 1px solid var(--color-border);
  background: var(--color-surface);
  color: var(--color-text-muted);
  display: grid; place-items: center;
  cursor: pointer;
  transition: color var(--transition-base), background var(--transition-base);
}
.wd-detail__close:hover { color: var(--color-text); background: var(--color-surface-alt); }

.wd-detail__media {
  aspect-ratio: 1;
  border-radius: var(--radius-card);
  background: linear-gradient(135deg, var(--color-primary-lighter), var(--color-surface-alt));
  display: grid; place-items: center;
  overflow: hidden;
  /* Padding lives on the parent so the inner img has a clean 100%/100%
     box to fit into — no border-box gotchas, no overflow-clipping. */
  padding: 18px;
  box-sizing: border-box;
  /* In a fixed-height flex column the media would otherwise be the first
     thing to shrink — pin it so the photo always shows at full square. */
  flex-shrink: 0;
}
.wd-detail__media img {
  max-width: 100%;
  max-height: 100%;
  width: auto;
  height: auto;
  object-fit: contain;
}

.wd-detail__section {
  display: flex; flex-direction: column; gap: 8px;
  flex-shrink: 0;
}

.wd-detail__section-title {
  display: inline-flex; align-items: center; gap: 6px;
  font-size: 11px; font-weight: 700; letter-spacing: 1.5px;
  text-transform: uppercase;
  color: var(--color-text-subtle);
}

.wd-detail__materials {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.wd-detail__relabel {
  align-self: flex-start;
  display: inline-flex; align-items: center; gap: 4px;
  background: transparent;
  border: none;
  color: var(--color-text-muted);
  font-size: 11px; font-weight: 600;
  letter-spacing: 0.4px;
  cursor: pointer;
  padding: 0;
  text-decoration: underline;
  text-underline-offset: 3px;
}
.wd-detail__relabel:hover { color: var(--color-primary-text); }

.wd-detail__care-hint {
  font-size: 11px; color: var(--color-text-faint);
  line-height: 1.5;
}

.wd-detail__sub-tag {
  align-self: flex-start;
  background: var(--color-surface-alt);
  color: var(--color-text);
  padding: 5px 12px;
  border-radius: var(--radius-pill);
  font-size: 13px; font-weight: 700;
  border: 1px solid var(--color-border-light);
}

.wd-detail__meta {
  font-size: 13px; color: var(--color-text-muted);
}

.wd-detail__actions {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex-shrink: 0;
}

.wd-detail__tryon {
  display: inline-flex; align-items: center; justify-content: center; gap: 6px;
  padding: 10px 14px;
  border-radius: var(--radius-btn);
  background: var(--color-primary);
  color: var(--color-primary-text);
  border: none;
  font-size: 13px; font-weight: 800;
  cursor: pointer;
  box-shadow: var(--shadow-card);
  transition: transform var(--transition-base), background var(--transition-base);
}
.wd-detail__tryon:hover:not(:disabled) {
  transform: translateY(-1px);
  background: var(--color-primary-dark);
}
.wd-detail__tryon--disabled {
  background: var(--color-surface-alt);
  color: var(--color-text-faint);
  cursor: not-allowed;
  box-shadow: none;
  border: 1px solid var(--color-border-light);
}

.wd-detail__delete {
  display: inline-flex; align-items: center; justify-content: center; gap: 6px;
  padding: 10px 14px;
  border-radius: var(--radius-pill);
  background: transparent;
  border: 1px solid var(--color-border-strong);
  color: var(--color-text-muted);
  font-size: 13px; font-weight: 600;
  cursor: pointer;
  transition: color var(--transition-base), border-color var(--transition-base), background var(--transition-base);
}
.wd-detail__delete:hover {
  color: var(--color-danger);
  border-color: var(--color-danger);
  background: rgba(208, 50, 56, 0.06);
}
</style>
