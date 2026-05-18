<template>
  <section class="wd-main" ref="rootRef">
    <!-- Editorial masthead: project title left, status meta right.
         Soft-tactile aesthetic — no harsh strokes, just a hair-line
         underline and a warm chip indicator. -->
    <header class="wd-main__masthead">
      <div class="wd-main__masthead-text">
        <p class="wd-main__issue">VOL. 01 · DIGITAL WARDROBE</p>
        <h2 class="wd-main__masthead-title">
          Your <span class="wd-main__masthead-accent">closet</span>, made visible.
        </h2>
      </div>
      <div class="wd-main__masthead-meta">
        <span v-if="recent > 0" class="wd-main__recent">
          <Sparkles :size="13" :stroke-width="2" />
          {{ recent }} added this week
        </span>
        <button
          v-if="total > 0"
          type="button"
          class="wd-main__clear"
          @click="emit('clear')"
        >
          <Trash2 :size="13" :stroke-width="2" />
          Clear all
        </button>
      </div>
    </header>

    <!-- Bento grid: left rail = cover/detail + try-on + advisor;
         right rail = 4 category tiles + upload. Two flex columns
         that grow independently keep the magazine-like rhythm. -->
    <div ref="bentoRef" class="wd-main__bento">
      <!-- ── Left rail ─────────────────────────────────────────── -->
      <div class="wd-main__rail wd-main__rail--left">
        <article class="wd-main__cover wd-soft-paper wd-soft-paper--cream">
          <p class="wd-main__cover-eyebrow">
            <span class="wd-main__cover-eyebrow-dot" />
            LIVE COUNT
          </p>
          <SoftNumeral :value="total" color="sage" class="wd-main__cover-numeral" />
          <p class="wd-main__cover-caption">
            item<span v-if="total !== 1">s</span> in your <em>closet</em>
          </p>
          <div class="wd-main__cover-meta">
            <span class="wd-main__cover-chip">
              <Sparkles :size="13" :stroke-width="2" />
              Local storage · zero cloud
            </span>
          </div>
        </article>

        <TryOnPreview
          ref="tryOnRef"
          class="wd-main__tryon"
          @mannequin-change="onMannequinChange"
        />
      </div>

      <!-- ── Right rail ────────────────────────────────────────── -->
      <div class="wd-main__rail wd-main__rail--right">
        <CategoryTile
          category="upper_body"
          theme="sage"
          :items="grouped.upper_body || []"
          :active-id="selectedId"
          class="wd-main__tile wd-main__tile--hero"
          @select="onSelect"
        />

        <div class="wd-main__twins">
          <CategoryTile
            category="one_pieces"
            theme="dusty"
            :items="grouped.one_pieces || []"
            :active-id="selectedId"
            class="wd-main__tile"
            @select="onSelect"
          />
          <CategoryTile
            category="lower_body"
            theme="oat"
            :items="grouped.lower_body || []"
            :active-id="selectedId"
            class="wd-main__tile"
            @select="onSelect"
          />
        </div>

        <CategoryTile
          category="footwear"
          theme="fog"
          :items="grouped.footwear || []"
          :active-id="selectedId"
          class="wd-main__tile"
          @select="onSelect"
        />

        <UploadCompact class="wd-main__upload" @saved="emit('saved')" />
      </div>
    </div>

    <WardrobeAiIntro v-if="total > 0" @open-advisor="emit('open-advisor')" />

    <WardrobeNextDecision v-if="total > 0" />

    <GarmentDetailModal
      :open="!!selectedGarment"
      :garment="selectedGarment"
      @close="selectedId = null"
      @delete="onDelete"
      @refresh="emit('saved')"
      @try-on="onTryOn"
    />
  </section>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { Sparkles, Trash2 } from 'lucide-vue-next'
import GarmentDetailModal from './GarmentDetailModal.vue'
import CategoryTile from './CategoryTile.vue'
import TryOnPreview from './TryOnPreview.vue'
import UploadCompact from './UploadCompact.vue'
import WardrobeAiIntro from './WardrobeAiIntro.vue'
import WardrobeNextDecision from './WardrobeNextDecision.vue'
import SoftNumeral from './SoftNumeral.vue'
import { tryOnSingle, tryOnCacheKey } from '../../services/tryOnApi.js'
import { mannequinStore } from '../../stores/mannequinStore.js'
import { putTryOnCache, getTryOnCache } from '../../services/wardrobeDb.js'
import { useToast } from '../../motion'
import { useReveal } from '../../motion/useReveal'
import { wardrobeBucketFor } from '../../services/wardrobeDb.js'

const props = defineProps({
  garments: { type: Array, default: () => [] },
  total: { type: Number, default: 0 },
  recent: { type: Number, default: 0 }
})
const emit = defineEmits(['saved', 'delete', 'clear', 'open-advisor', 'try-on'])

const rootRef = ref(null)
const bentoRef = ref(null)
const selectedId = ref(null)
const tryOnRef = ref(null)
const toast = useToast()

const grouped = computed(() => {
  const out = { upper_body: [], one_pieces: [], lower_body: [], footwear: [] }
  for (const g of props.garments) {
    const bucket = wardrobeBucketFor(g)
    if (out[bucket]) out[bucket].push(g)
  }
  return out
})

const selectedGarment = computed(
  () => props.garments.find((g) => g.id === selectedId.value) || null
)

watch(
  () => props.garments,
  (val) => {
    if (selectedId.value != null && !val.some((g) => g.id === selectedId.value)) {
      selectedId.value = null
    }
  }
)

// Bento entrance — soft fade-up on the whole grid. `useReveal` is wired
// to the router's settle lifecycle so tiles end up visible even if mount
// is interrupted.
useReveal(bentoRef, { mode: 'fade-up', y: 24, duration: 0.7, delay: 0.15 })

function onSelect(id) {
  selectedId.value = id
}

function onDelete(id) {
  selectedId.value = null
  emit('delete', id)
}

async function onTryOn(garment) {
  // Close the detail modal immediately so the user sees the TryOnPreview
  // loading state in the left rail. The async try-on flow below continues
  // in the background; the `garment` reference is already captured here so
  // resetting selectedId doesn't lose the target.
  selectedId.value = null
  if (!garment || !tryOnRef.value) return
  if (garment.main_category === 'footwear') {
    toast.push('Footwear try-on is not supported by FASHN VTON yet.', { type: 'warning' })
    return
  }

  const cacheKey = tryOnCacheKey(garment.id, mannequinStore.selected)
  if (cacheKey) {
    const cached = await getTryOnCache(cacheKey).catch(() => null)
    if (cached?.result_image) {
      tryOnRef.value.showResult(cached.result_image)
      emit('try-on', garment)
      return
    }
  }

  tryOnRef.value.startLoading()
  emit('try-on', garment)
  try {
    const payload = await tryOnSingle({
      mannequin: mannequinStore.selected,
      garment
    })
    tryOnRef.value.showResult(payload.result_image)
    if (cacheKey) {
      await putTryOnCache({
        garment_key: cacheKey,
        garment_id: garment.id,
        mannequin: { ...mannequinStore.selected },
        result_image: payload.result_image,
        generated_at: Date.now()
      }).catch(() => {})
    }
  } catch (err) {
    const msg = err?.message || 'Try-on failed. Please retry.'
    tryOnRef.value.showError(msg)
    toast.push(msg, { type: 'error' })
  }
}

function onMannequinChange() {
  tryOnRef.value?.reset?.()
}
</script>

<style scoped>
.wd-main {
  max-width: 1320px;
  margin: 0 auto;
  padding: 32px 32px 64px;
}

/* ── Masthead ─────────────────────────────────────────────── */
.wd-main__masthead {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 24px;
  padding-bottom: 22px;
  margin-bottom: 30px;
  border-bottom: 1px solid var(--color-soft-line);
  flex-wrap: wrap;
}

.wd-main__masthead-text { flex: 1; min-width: 280px; }
.wd-main__issue {
  font-family: var(--font-display);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.24em;
  color: var(--color-soft-ink-soft);
  margin-bottom: 12px;
  text-transform: uppercase;
}
.wd-main__masthead-title {
  font-family: var(--font-display);
  font-size: clamp(30px, 4.4vw, 52px);
  line-height: 1.04;
  letter-spacing: -0.02em;
  font-weight: 700;
  color: var(--color-soft-ink);
}
.wd-main__masthead-accent {
  color: var(--color-soft-sage);
  font-style: italic;
  font-weight: 800;
}

.wd-main__masthead-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}
.wd-main__recent {
  display: inline-flex; align-items: center; gap: 6px;
  font-size: 12px;
  font-weight: 600;
  background: var(--color-soft-sage-mist);
  color: var(--color-soft-sage-deep);
  padding: 7px 14px;
  border-radius: var(--radius-soft-pill);
}

.wd-main__clear {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 7px 14px;
  border-radius: var(--radius-soft-pill);
  background: transparent;
  border: 1px solid var(--color-soft-line);
  color: var(--color-soft-ink-soft);
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: background 200ms ease, color 200ms ease, border-color 200ms ease;
}
.wd-main__clear:hover {
  background: var(--color-soft-dusty-wash);
  color: var(--color-soft-ink);
  border-color: transparent;
}

/* ── Bento grid ───────────────────────────────────────────── */
.wd-main__bento {
  display: grid;
  grid-template-columns: minmax(0, 5fr) minmax(0, 7fr);
  gap: 22px;
  align-items: start;
}

.wd-main__rail {
  display: flex;
  flex-direction: column;
  gap: 22px;
  min-width: 0;
}

/* ── Cover tile ───────────────────────────────────────────── */
.wd-main__cover {
  position: relative;
  border-radius: var(--radius-soft-lg);
  /* `.wd-soft-paper--cream` paints the cream base + fibre noise. */
  padding: 32px 32px 30px;
  border: 1.5px solid var(--color-soft-line-strong);
  box-shadow: var(--shadow-soft);
  overflow: hidden;
  min-height: 380px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.wd-main__cover-eyebrow {
  display: inline-flex; align-items: center; gap: 8px;
  font-family: var(--font-display);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.22em;
  color: var(--color-soft-ink-soft);
  text-transform: uppercase;
}
.wd-main__cover-eyebrow-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  background: var(--color-soft-sage);
}

.wd-main__cover-numeral {
  align-self: flex-start;
  margin: -4px 0 -4px -6px;
}

.wd-main__cover-caption {
  font-family: var(--font-display);
  font-size: clamp(22px, 2.4vw, 30px);
  line-height: 1.25;
  font-weight: 600;
  color: var(--color-soft-ink);
  letter-spacing: -0.01em;
  max-width: 320px;
}
.wd-main__cover-caption em {
  color: var(--color-soft-sage);
  font-style: italic;
  font-weight: 800;
}

.wd-main__cover-meta {
  margin-top: auto;
}
.wd-main__cover-chip {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 7px 14px;
  border-radius: var(--radius-soft-pill);
  background: var(--color-soft-milk);
  color: var(--color-soft-ink-soft);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.08em;
}

/* ── Try-On tile ──────────────────────────────────────────── */
.wd-main__tryon {
  border-radius: var(--radius-soft);
  background: var(--color-soft-milk);
  border: 1.5px solid var(--color-soft-line-strong);
  box-shadow: var(--shadow-soft);
  overflow: hidden;
}

/* ── Right rail ───────────────────────────────────────────── */
.wd-main__twins {
  display: grid;
  grid-template-columns: 1.1fr 1fr;
  gap: 22px;
  min-width: 0;
}
.wd-main__twins > * { min-width: 0; }

/* ── Responsive ───────────────────────────────────────────── */
@media (max-width: 1100px) {
  .wd-main__bento { grid-template-columns: 1fr; }
  .wd-main__twins { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 700px) {
  .wd-main { padding: 20px 16px 48px; }
  .wd-main__twins { grid-template-columns: 1fr; }
  .wd-main__cover { padding: 24px 22px 24px; min-height: 320px; }
  .wd-main__cover-numeral :deep(.wd-numeral) { font-size: clamp(96px, 30vw, 160px); }
}
</style>
