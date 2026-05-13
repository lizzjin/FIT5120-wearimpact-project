<template>
  <div class="wd-mp" data-lenis-prevent>
    <header class="wd-mp__head">
      <h4 class="wd-mp__title">Choose a mannequin</h4>
      <button type="button" class="wd-mp__close" @click="$emit('close')" aria-label="Close picker">
        <X :size="14" :stroke-width="2.4" />
      </button>
    </header>

    <div class="wd-mp__tabs" role="tablist">
      <button
        v-for="cat in categories"
        :key="cat"
        type="button"
        role="tab"
        :aria-selected="cat === activeCategory"
        class="wd-mp__tab"
        :class="{ 'is-active': cat === activeCategory }"
        @click="activeCategory = cat"
      >
        {{ cat }}
      </button>
    </div>

    <ul class="wd-mp__grid">
      <li v-for="f in modelsForCategory" :key="f" class="wd-mp__cell">
        <button
          type="button"
          class="wd-mp__thumb"
          :class="{ 'is-selected': isSelected(f) }"
          @click="pick(f)"
        >
          <img :src="`/person-models/${activeCategory}/${f}`" :alt="`${activeCategory} ${f}`" />
          <span v-if="isSelected(f)" class="wd-mp__tick">
            <Check :size="12" :stroke-width="3" />
          </span>
        </button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { X, Check } from 'lucide-vue-next'
import { mannequinStore, setMannequin } from '../../stores/mannequinStore.js'

const emit = defineEmits(['close', 'change'])

const categories = ['Female', 'Male', 'Non-Binary']
const activeCategory = ref(mannequinStore.selected.category || 'Female')

// Fall back to a hard-coded 6-per-category list when the JSON index
// is unreachable — the public folder is always shipped with all 18
// PNGs so this keeps the UI responsive even if Vite's dev server is
// momentarily slow to serve the static index.
const FALLBACK_FILES = ['model-01.png', 'model-02.png', 'model-03.png', 'model-04.png', 'model-05.png', 'model-06.png']
const allModels = ref({
  Female: FALLBACK_FILES,
  Male: FALLBACK_FILES,
  'Non-Binary': FALLBACK_FILES
})

onMounted(async () => {
  try {
    const res = await fetch('/person-models/index.json', { cache: 'force-cache' })
    if (res.ok) {
      const data = await res.json()
      if (data && typeof data === 'object') {
        allModels.value = { ...allModels.value, ...data }
      }
    }
  } catch {
    // Fallback list still works.
  }
})

const modelsForCategory = computed(() => allModels.value[activeCategory.value] || FALLBACK_FILES)

function isSelected(filename) {
  return (
    mannequinStore.selected.category === activeCategory.value &&
    mannequinStore.selected.filename === filename
  )
}

function pick(filename) {
  setMannequin({ category: activeCategory.value, filename })
  emit('change', { category: activeCategory.value, filename })
  emit('close')
}
</script>

<style scoped>
.wd-mp {
  background: var(--color-surface);
  border-radius: var(--radius-card);
  padding: 16px;
  box-shadow: var(--shadow-card);
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: 100%;
  overflow-y: auto;
}

.wd-mp__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.wd-mp__title {
  font-size: 13px;
  font-weight: 800;
  letter-spacing: 0.4px;
  color: var(--color-text);
  margin: 0;
}
.wd-mp__close {
  width: 26px; height: 26px;
  border-radius: 999px;
  border: 1px solid var(--color-border);
  background: var(--color-surface);
  color: var(--color-text-muted);
  display: grid; place-items: center;
  cursor: pointer;
}
.wd-mp__close:hover {
  color: var(--color-text);
  background: var(--color-surface-alt);
}

.wd-mp__tabs {
  display: flex;
  gap: 6px;
}
.wd-mp__tab {
  flex: 1;
  padding: 6px 10px;
  border-radius: var(--radius-pill);
  border: 1px solid var(--color-border-light);
  background: var(--color-surface);
  color: var(--color-text-muted);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.5px;
  cursor: pointer;
  transition: color var(--transition-base), background var(--transition-base), border-color var(--transition-base);
}
.wd-mp__tab.is-active {
  background: var(--color-primary);
  color: var(--color-primary-text);
  border-color: var(--color-primary);
}

.wd-mp__grid {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.wd-mp__cell { display: contents; }

.wd-mp__thumb {
  position: relative;
  aspect-ratio: 3 / 4;
  border-radius: var(--radius-card-sm);
  overflow: hidden;
  border: 2px solid transparent;
  padding: 0;
  background: var(--color-surface-alt);
  cursor: pointer;
  transition: border-color var(--transition-base), transform var(--transition-base);
}
.wd-mp__thumb:hover {
  transform: translateY(-1px);
  border-color: var(--color-primary-light);
}
.wd-mp__thumb.is-selected {
  border-color: var(--color-primary);
}
.wd-mp__thumb img {
  width: 100%; height: 100%; object-fit: cover;
  display: block;
}
.wd-mp__tick {
  position: absolute;
  top: 4px; right: 4px;
  width: 18px; height: 18px;
  border-radius: 999px;
  background: var(--color-primary);
  color: var(--color-primary-text);
  display: grid;
  place-items: center;
}
</style>
