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
        <div class="wd-detail__sub-row">
          <span class="wd-detail__sub-tag">{{ formatSub(garment.sub_category) }}</span>
          <button
            v-if="!recategorizeOpen"
            type="button"
            class="wd-detail__recategorize"
            @click="recategorizeOpen = true"
          >
            <Pencil :size="11" :stroke-width="2" />
            Change
          </button>
        </div>
        <div v-if="recategorizeOpen" class="wd-detail__recategorize-panel">
          <select v-model="pendingSub" class="wd-detail__recategorize-select">
            <optgroup
              v-for="(subs, main) in availableTaxonomy"
              :key="main"
              :label="RECATEGORIZE_GROUP_LABEL[main]"
            >
              <option v-for="sub in subs" :key="sub" :value="sub">
                {{ formatSub(sub) }}
              </option>
            </optgroup>
          </select>
          <div class="wd-detail__recategorize-actions">
            <button
              type="button"
              class="wd-detail__recategorize-cancel"
              @click="cancelRecategorize"
            >
              Cancel
            </button>
            <button
              type="button"
              class="wd-detail__recategorize-save"
              :disabled="!recategorizeDirty"
              @click="saveRecategorize"
            >
              Save
            </button>
          </div>
          <p class="wd-detail__recategorize-hint">
            Saving clears any cached try-on result for this item.
          </p>
        </div>
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
          Footwear try-on coming soon
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
  Hand, X, Droplets, Tag, Calendar, Trash2, RefreshCw, Shirt, Pencil
} from 'lucide-vue-next'
import MaterialPills from './MaterialPills.vue'
import WashLabelUploader from './WashLabelUploader.vue'
import {
  updateGarmentMaterials,
  updateGarmentCategory
} from '../../services/wardrobeDb.js'
import { useToast } from '../../motion'

const props = defineProps({
  garment: { type: Object, default: null }
})
const emit = defineEmits(['close', 'delete', 'refresh', 'try-on'])

const toast = useToast()
const reuploadOpen = ref(false)
const recategorizeOpen = ref(false)
const pendingSub = ref(null)

// Collapse the re-upload form whenever the user switches to a different
// garment — keeps the UI clean and avoids stale state across selections.
watch(() => props.garment?.id, () => {
  reuploadOpen.value = false
  recategorizeOpen.value = false
  pendingSub.value = props.garment?.sub_category || null
})

watch(recategorizeOpen, (open) => {
  if (open) pendingSub.value = props.garment?.sub_category || null
})

const MAIN_LABEL = {
  upper_body: 'Tops',
  lower_body: 'Bottoms',
  footwear: 'Shoes'
}

// Hardcoded copy of classifier CATEGORY_TAXONOMY (FIT5120-Classification-Mod
// /app.py). Kept in sync manually — if you add a subcategory in app.py,
// add it here too.
const SUBCATEGORY_TAXONOMY = {
  upper_body: [
    't_shirt', 'tank_top_vest', 'shirt_blouse', 'polo_shirt',
    'hoodie_sweatshirt', 'sweater_pullover', 'cardigan',
    'suit_jacket', 'jacket', 'trench_coat', 'overcoat',
    'down_jacket', 'dress'
  ],
  lower_body: [
    'jeans', 'dress_pants', 'sweatpants_joggers', 'leggings',
    'casual_shorts', 'sports_shorts',
    'mini_skirt', 'maxi_skirt', 'pleated_skirt'
  ],
  footwear: [
    'sneakers', 'skate_shoes', 'running_shoes',
    'oxfords', 'loafers', 'derby_shoes',
    'ankle_boots', 'high_boots', 'martin_boots',
    'sandals', 'slippers', 'flip_flops'
  ]
}

const SUBCATEGORY_TO_MAIN = Object.fromEntries(
  Object.entries(SUBCATEGORY_TAXONOMY).flatMap(
    ([main, subs]) => subs.map((sub) => [sub, main])
  )
)

const RECATEGORIZE_GROUP_LABEL = {
  upper_body: 'Tops & one-pieces',
  lower_body: 'Bottoms',
  footwear: 'Shoes'
}

// Footwear stays footwear — reclassifying a sneaker as a dress would be
// nonsensical and would break try-on (FASHN refuses footwear). Upper and
// lower body are interchangeable so users can fix dress↔skirt confusion,
// which is the whole point of this control.
const availableTaxonomy = computed(() => {
  if (!props.garment) return {}
  if (props.garment.main_category === 'footwear') {
    return { footwear: SUBCATEGORY_TAXONOMY.footwear }
  }
  return {
    upper_body: SUBCATEGORY_TAXONOMY.upper_body,
    lower_body: SUBCATEGORY_TAXONOMY.lower_body
  }
})

const recategorizeDirty = computed(
  () => pendingSub.value && pendingSub.value !== props.garment?.sub_category
)

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

async function saveRecategorize() {
  const id = props.garment?.id
  const newSub = pendingSub.value
  if (!id || !newSub || newSub === props.garment.sub_category) {
    recategorizeOpen.value = false
    return
  }
  const newMain = SUBCATEGORY_TO_MAIN[newSub]
  if (!newMain) {
    toast.push('Unknown subcategory.', { type: 'error' })
    return
  }
  try {
    await updateGarmentCategory(id, newMain, newSub)
    recategorizeOpen.value = false
    toast.push('Category updated.', { type: 'success' })
    emit('refresh')
  } catch (err) {
    toast.push(err?.message || 'Could not update category.', { type: 'error' })
  }
}

function cancelRecategorize() {
  recategorizeOpen.value = false
  pendingSub.value = props.garment?.sub_category || null
}
</script>

<style scoped>
.wd-detail {
  background: transparent;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
}

.wd-detail__scroll {
  flex: 1;
  min-height: 0;
  padding: 26px 28px 24px;
  display: flex;
  flex-direction: column;
  gap: 22px;
  overflow-y: auto;
  /* Stop wheel events from chaining up to <html> when this container reaches
     its scroll boundary (or has no scrollable content at all — short
     garments). Without this, the modal-detail panel was a Lenis-prevented
     scroll container that silently passed wheel events to the html element
     (which still has overflow-y:scroll for the rest of the site), and the
     blurred page behind the modal kept scrolling. */
  overscroll-behavior: contain;
  scrollbar-width: thin;
  scrollbar-color: rgba(58, 56, 51, 0.18) transparent;
}
.wd-detail__scroll::-webkit-scrollbar { width: 6px; }
.wd-detail__scroll::-webkit-scrollbar-thumb {
  background: rgba(58, 56, 51, 0.18);
  border-radius: 999px;
}

.wd-detail--empty .wd-detail__scroll {
  align-items: center;
  justify-content: center;
  text-align: center;
}

.wd-detail__placeholder-icon {
  width: 60px; height: 60px;
  border-radius: 50%;
  background: var(--color-soft-sage-mist);
  color: var(--color-soft-sage-deep);
  display: grid; place-items: center;
  box-shadow: var(--shadow-soft-sm);
  margin: 0 auto 16px;
}

.wd-detail__placeholder-title {
  font-family: var(--font-display);
  font-size: 18px;
  font-weight: 700;
  color: var(--color-soft-ink);
  margin-bottom: 6px;
  letter-spacing: -0.01em;
}
.wd-detail__placeholder-hint {
  font-size: 13px;
  color: var(--color-soft-ink-soft);
  max-width: 240px;
  line-height: 1.55;
  margin: 0 auto;
}

.wd-detail__head {
  display: flex; align-items: center; justify-content: space-between;
  flex-shrink: 0;
}
.wd-detail__main-tag {
  display: inline-block;
  background: var(--color-soft-sage-mist);
  color: var(--color-soft-sage-deep);
  padding: 6px 14px;
  border-radius: var(--radius-soft-pill);
  font-family: var(--font-display);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}
.wd-detail__close {
  width: 32px; height: 32px;
  border-radius: 50%;
  background: var(--color-soft-milk);
  color: var(--color-soft-ink-soft);
  border: none;
  display: grid; place-items: center;
  cursor: pointer;
  transition: background 200ms ease, color 200ms ease;
}
.wd-detail__close:hover {
  background: var(--color-soft-dusty-wash);
  color: var(--color-soft-ink);
}

.wd-detail__media {
  aspect-ratio: 1;
  border-radius: 20px;
  background: var(--color-soft-milk);
  display: grid; place-items: center;
  overflow: hidden;
  padding: 18px;
  box-sizing: border-box;
  flex-shrink: 0;
  box-shadow: var(--shadow-soft-sm);
}
.wd-detail__media img {
  max-width: 100%; max-height: 100%;
  width: auto; height: auto;
  object-fit: contain;
}

.wd-detail__section {
  display: flex; flex-direction: column; gap: 10px;
  flex-shrink: 0;
}

.wd-detail__section-title {
  display: inline-flex; align-items: center; gap: 6px;
  font-family: var(--font-display);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.2em;
  color: var(--color-soft-ink-soft);
  text-transform: uppercase;
}

.wd-detail__materials {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.wd-detail__relabel {
  align-self: flex-start;
  display: inline-flex; align-items: center; gap: 5px;
  background: transparent;
  border: none;
  color: var(--color-soft-sage-deep);
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  padding: 0;
  text-decoration: underline;
  text-underline-offset: 3px;
}
.wd-detail__relabel:hover { color: var(--color-soft-ink); }

.wd-detail__care-hint {
  font-size: 11.5px;
  color: var(--color-soft-ink-soft);
  line-height: 1.55;
}

.wd-detail__sub-row {
  display: flex; align-items: center; gap: 10px;
  flex-wrap: wrap;
}

.wd-detail__sub-tag {
  background: var(--color-soft-dusty-wash);
  color: var(--color-soft-ink);
  padding: 6px 14px;
  border-radius: var(--radius-soft-pill);
  font-size: 13px;
  font-weight: 600;
  letter-spacing: -0.01em;
}

.wd-detail__recategorize {
  display: inline-flex; align-items: center; gap: 5px;
  background: transparent;
  border: none;
  color: var(--color-soft-sage-deep);
  font-size: 11.5px;
  font-weight: 600;
  cursor: pointer;
  padding: 0;
  text-decoration: underline;
  text-underline-offset: 3px;
}
.wd-detail__recategorize:hover { color: var(--color-soft-ink); }

.wd-detail__recategorize-panel {
  display: flex; flex-direction: column; gap: 10px;
  padding: 14px;
  background: var(--color-soft-milk);
  border-radius: 16px;
  box-shadow: var(--shadow-soft-sm);
}

.wd-detail__recategorize-select {
  width: 100%;
  padding: 9px 12px;
  font-size: 13px;
  font-weight: 600;
  color: var(--color-soft-ink);
  background: var(--color-soft-cream);
  border: 1px solid var(--color-soft-line);
  border-radius: 10px;
  cursor: pointer;
}
.wd-detail__recategorize-select:focus {
  outline: none;
  border-color: var(--color-soft-sage);
  box-shadow: 0 0 0 3px var(--color-soft-sage-mist);
}

.wd-detail__recategorize-actions {
  display: flex; gap: 8px;
  justify-content: flex-end;
}

.wd-detail__recategorize-cancel,
.wd-detail__recategorize-save {
  padding: 8px 16px;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: -0.01em;
  border-radius: var(--radius-soft-pill);
  cursor: pointer;
  border: none;
  transition: background 200ms ease, color 200ms ease, transform 200ms ease;
}

.wd-detail__recategorize-cancel {
  background: transparent;
  color: var(--color-soft-ink-soft);
}
.wd-detail__recategorize-cancel:hover {
  background: var(--color-soft-milk);
  color: var(--color-soft-ink);
}

.wd-detail__recategorize-save {
  background: var(--color-primary);
  color: var(--color-primary-text);
}
.wd-detail__recategorize-save:hover:not(:disabled) {
  background: var(--color-primary-dark);
}
.wd-detail__recategorize-save:disabled {
  background: var(--color-soft-milk);
  color: var(--color-soft-ink-soft);
  opacity: 0.6;
  cursor: not-allowed;
}

.wd-detail__recategorize-hint {
  font-size: 11px;
  color: var(--color-soft-ink-soft);
  line-height: 1.45;
}

.wd-detail__meta {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-soft-ink-soft);
}

.wd-detail__actions {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
  flex-shrink: 0;
}

.wd-detail__tryon {
  display: inline-flex; align-items: center; justify-content: center; gap: 8px;
  padding: 12px 18px;
  border-radius: var(--radius-soft-pill);
  border: none;
  background: var(--color-primary);
  color: var(--color-primary-text);
  font-family: var(--font-display);
  font-size: 13px;
  font-weight: 700;
  letter-spacing: -0.01em;
  cursor: pointer;
  box-shadow: var(--shadow-soft-sm);
  transition: background 220ms ease, transform 220ms ease, box-shadow 220ms ease;
}
.wd-detail__tryon:hover:not(:disabled) {
  background: var(--color-primary-dark);
  transform: scale(1.03);
  box-shadow: var(--shadow-soft);
}
.wd-detail__tryon--disabled {
  background: var(--color-soft-milk);
  color: var(--color-soft-ink-soft);
  opacity: 0.6;
  cursor: not-allowed;
  box-shadow: none;
}

.wd-detail__delete {
  display: inline-flex; align-items: center; justify-content: center; gap: 8px;
  padding: 11px 18px;
  border-radius: var(--radius-soft-pill);
  border: 1px solid var(--color-soft-line);
  background: transparent;
  color: var(--color-soft-ink-soft);
  font-size: 12.5px;
  font-weight: 600;
  cursor: pointer;
  transition: background 200ms ease, color 200ms ease, border-color 200ms ease;
}
.wd-detail__delete:hover {
  background: var(--color-soft-dusty-wash);
  color: var(--color-soft-ink);
  border-color: transparent;
}
</style>
