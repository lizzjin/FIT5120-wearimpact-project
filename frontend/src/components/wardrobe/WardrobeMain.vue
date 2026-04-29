<template>
  <section class="wd-main">
    <header class="wd-main__head">
      <button type="button" class="wd-main__back" @click="emit('back')">
        <ArrowLeft :size="16" :stroke-width="2" />
        Back
      </button>
      <div class="wd-main__heading">
        <p class="wd-main__eyebrow">MY WARDROBE</p>
        <h2 class="wd-main__title">{{ total }} item{{ total === 1 ? '' : 's' }} in your closet</h2>
      </div>
      <div class="wd-main__stats">
        <span class="wd-main__stat">
          <Sparkles :size="13" :stroke-width="2" />
          {{ recent }} added this week
        </span>
        <button
          v-if="total > 0"
          type="button"
          class="wd-main__advisor"
          @click="emit('open-advisor')"
        >
          <Sparkles :size="13" :stroke-width="2" /> AI advisor
        </button>
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


    <div class="wd-main__grid">
      <!-- Left: detail panel -->
      <GarmentDetailPanel
        :garment="selectedGarment"
        @close="selectedId = null"
        @delete="onDelete"
      />

      <!-- Right: wardrobe canvas -->
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
import { ArrowLeft, Sparkles, Trash2 } from 'lucide-vue-next'
import GarmentDetailPanel from './GarmentDetailPanel.vue'
import CategoryRow from './CategoryRow.vue'
import MannequinSlot from './MannequinSlot.vue'
import UploadCompact from './UploadCompact.vue'
import { MAIN_CATEGORIES } from '../../services/wardrobeDb.js'

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

.wd-main__advisor {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 6px 12px;
  border-radius: var(--radius-pill);
  background: var(--color-primary);
  border: 1px solid var(--color-primary);
  color: var(--color-primary-text);
  font-size: 12px; font-weight: 700;
  cursor: pointer;
  transition: transform var(--transition-base), background var(--transition-base);
}
.wd-main__advisor:hover {
  transform: scale(1.04);
  background: var(--color-primary-dark);
}


.wd-main__grid {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 24px;
  align-items: start;
}

.wd-main__canvas {
  display: grid;
  grid-template-columns: 1fr 240px;
  gap: 18px;
}

.wd-main__rows {
  display: flex; flex-direction: column;
  gap: 14px;
}

.wd-main__rail {
  display: flex; flex-direction: column;
  gap: 14px;
}

@media (max-width: 1100px) {
  .wd-main__grid { grid-template-columns: 1fr; }
  .wd-main__canvas { grid-template-columns: 1fr; }
}
@media (max-width: 700px) {
  .wd-main { padding: 20px 16px 48px; }
}
</style>
