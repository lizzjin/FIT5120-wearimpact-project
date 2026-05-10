<template>
  <section class="wd-main">
    <header class="wd-main__head">
      <button type="button" class="wd-main__back" @click="emit('back')">
        <ArrowLeft :size="16" :stroke-width="2" />
        Back
      </button>
      <div class="wd-main__heading">
        <p ref="eyebrowRef" class="wd-main__eyebrow">MY WARDROBE</p>
        <AnimatedHeading
          as="h2"
          class="wd-main__title"
          :text="`${total} item${total === 1 ? '' : 's'} in your closet`"
          :stagger="0.07"
          :delay="0.1"
        />
      </div>
      <div class="wd-main__stats">
        <span class="wd-main__stat">
          <Sparkles :size="13" :stroke-width="2" />
          {{ recent }} added this week
        </span>
        <button
          v-if="total > 0"
          type="button"
          class="wd-main__clear"
          @click="emit('clear')"
        >
          <Trash2 :size="13" :stroke-width="2" /> Clear all
        </button>
      </div>
    </header>


    <div ref="gridRef" class="wd-main__grid">
      <!-- Left column: detail panel on top, AI advisor pinned to the
           bottom edge so it lines up with the upload card on the right. -->
      <div class="wd-main__left">
        <GarmentDetailPanel
          :garment="selectedGarment"
          @close="selectedId = null"
          @delete="onDelete"
        />
        <button
          v-if="total > 0"
          type="button"
          class="wd-main__advisor-card"
          @click="emit('open-advisor')"
        >
          <span class="wd-main__advisor-icon">
            <Sparkles :size="20" :stroke-width="2" />
          </span>
          <span class="wd-main__advisor-text">
            <span class="wd-main__advisor-title">Ask the AI advisor</span>
            <span class="wd-main__advisor-sub">Outfit ideas from your closet</span>
          </span>
          <ArrowRight :size="16" :stroke-width="2" class="wd-main__advisor-arrow" />
        </button>
      </div>

      <!-- Middle + right: wardrobe canvas -->
      <div class="wd-main__canvas">
        <div class="wd-main__rows">
          <CategoryRow
            v-for="cat in MAIN_CATEGORIES"
            :key="cat"
            :category="cat"
            :items="grouped[cat] || []"
            :active-id="selectedId"
            @select="(id) => (selectedId = id)"
          />
        </div>

        <aside class="wd-main__rail">
          <MannequinSlot />
          <UploadCompact @saved="emit('saved')" />
        </aside>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { ArrowLeft, ArrowRight, Sparkles, Trash2 } from 'lucide-vue-next'
import GarmentDetailPanel from './GarmentDetailPanel.vue'
import CategoryRow from './CategoryRow.vue'
import MannequinSlot from './MannequinSlot.vue'
import UploadCompact from './UploadCompact.vue'
import AnimatedHeading from '../AnimatedHeading.vue'
import { MAIN_CATEGORIES } from '../../services/wardrobeDb.js'
import { useReveal } from '../../motion/useReveal'

const eyebrowRef = ref(null)
const gridRef = ref(null)
useReveal(eyebrowRef, { mode: 'char', stagger: 0.022, duration: 0.5 })
// Soft fade-up on the grid container — earlier we staggered each direct
// child, but grid children include interactive cards/buttons; staggering
// them mid-mount caused timing edge-cases when the section state was
// switched after the user already had items. A single fade keeps the
// "wardrobe opens" feel without touching individual item interactivity.
useReveal(gridRef, { mode: 'fade-up', y: 24, duration: 0.7, delay: 0.2 })

const props = defineProps({
  garments: { type: Array, default: () => [] },
  total: { type: Number, default: 0 },
  recent: { type: Number, default: 0 }
})
const emit = defineEmits(['back', 'saved', 'delete', 'clear', 'open-advisor'])

const selectedId = ref(null)

const grouped = computed(() => {
  const out = {}
  for (const cat of MAIN_CATEGORIES) out[cat] = []
  for (const g of props.garments) {
    if (out[g.main_category]) out[g.main_category].push(g)
    else (out[g.main_category] = [g])
  }
  return out
})

const selectedGarment = computed(
  () => props.garments.find((g) => g.id === selectedId.value) || null
)

// Clear the panel if the selected garment disappears (deletion or refresh).
watch(
  () => props.garments,
  (val) => {
    if (selectedId.value != null && !val.some((g) => g.id === selectedId.value)) {
      selectedId.value = null
    }
  }
)

function onDelete(id) {
  selectedId.value = null
  emit('delete', id)
}
</script>

<style scoped>
.wd-main {
  max-width: 1280px;
  margin: 0 auto;
  padding: 32px 32px 64px;
}

.wd-main__head {
  display: flex;
  align-items: center;
  gap: 18px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.wd-main__back {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 8px 14px;
  border-radius: var(--radius-pill);
  background: transparent;
  border: 1px solid var(--color-border-strong);
  color: var(--color-text-muted);
  font-size: 13px; font-weight: 600;
  cursor: pointer;
  transition: color var(--transition-base), background var(--transition-base);
}
.wd-main__back:hover { color: var(--color-text); background: var(--color-surface-alt); }

.wd-main__heading {
  flex: 1; min-width: 200px;
}
.wd-main__eyebrow {
  font-size: 11px; font-weight: 700; letter-spacing: 2px;
  color: var(--color-primary-text);
  margin-bottom: 4px;
}
.wd-main__title {
  font-size: 22px; font-weight: 800;
  letter-spacing: -0.4px;
  color: var(--color-text);
}

.wd-main__stats {
  display: flex; align-items: center; gap: 10px;
}
.wd-main__stat {
  display: inline-flex; align-items: center; gap: 6px;
  font-size: 12px; font-weight: 700;
  background: var(--color-primary-light);
  color: var(--color-primary-text);
  padding: 6px 12px;
  border-radius: var(--radius-pill);
  border: 1px solid var(--color-border-light);
}
.wd-main__clear {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 6px 12px;
  border-radius: var(--radius-pill);
  background: transparent;
  border: 1px solid var(--color-border-strong);
  color: var(--color-text-muted);
  font-size: 12px; font-weight: 600;
  cursor: pointer;
}
.wd-main__clear:hover {
  color: var(--color-danger);
  border-color: var(--color-danger);
}

/* Prominent advisor entry — lives at the top of the right rail so it's
   always in the user's eyeline alongside the wardrobe rows. */
.wd-main__advisor-card {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  padding: 14px 14px 14px 12px;
  border-radius: var(--radius-card);
  background: var(--color-primary);
  border: 1px solid var(--color-primary);
  color: var(--color-primary-text);
  cursor: pointer;
  text-align: left;
  box-shadow: var(--shadow-card);
  transition: transform var(--transition-base), background var(--transition-base), box-shadow var(--transition-base);
}
.wd-main__advisor-card:hover {
  transform: translateY(-2px);
  background: var(--color-primary-dark);
  box-shadow: var(--shadow-card-hover);
}
.wd-main__advisor-icon {
  width: 36px; height: 36px;
  border-radius: 999px;
  background: var(--color-primary-text);
  color: var(--color-primary);
  display: grid; place-items: center;
  flex-shrink: 0;
}
.wd-main__advisor-text {
  display: flex; flex-direction: column;
  gap: 2px;
  min-width: 0;
  flex: 1;
}
.wd-main__advisor-title {
  font-size: 13px; font-weight: 800;
  letter-spacing: -0.2px;
}
.wd-main__advisor-sub {
  font-size: 11px;
  font-weight: 600;
  opacity: 0.78;
}
.wd-main__advisor-arrow {
  flex-shrink: 0;
  transition: transform var(--transition-base);
}
.wd-main__advisor-card:hover .wd-main__advisor-arrow {
  transform: translateX(3px);
}


/* Locked layout height: 3 category rows (220px) + 2 × 14px gap.
   Driving every column from this single value keeps the advisor card
   and the upload card flush with the third row's bottom edge, even
   when a tall garment-detail view is open in the left column. */
.wd-main__grid {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 24px;
  align-items: start;
}

.wd-main__left,
.wd-main__canvas {
  height: 688px;
}

.wd-main__canvas {
  display: grid;
  grid-template-columns: 1fr 280px;
  gap: 18px;
  align-items: stretch;
}

.wd-main__rows {
  display: flex; flex-direction: column;
  gap: 14px;
}

.wd-main__left {
  display: flex;
  flex-direction: column;
  gap: 14px;
  min-height: 0;
}

.wd-main__rail {
  display: flex; flex-direction: column;
  gap: 14px;
  min-height: 0;
}

@media (max-width: 1100px) {
  .wd-main__grid { grid-template-columns: 1fr; }
  .wd-main__canvas { grid-template-columns: 1fr; }
  /* Drop the locked height when columns stack — they're no longer
     side-by-side, so there's nothing to align to. */
  .wd-main__left,
  .wd-main__canvas { height: auto; }
}
@media (max-width: 700px) {
  .wd-main { padding: 20px 16px 48px; }
}
</style>
