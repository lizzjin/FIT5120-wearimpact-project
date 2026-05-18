<template>
  <div class="wd-mp" data-lenis-prevent>
    <header class="wd-mp__head">
      <h4 class="wd-mp__title">Pick a mannequin</h4>
      <button type="button" class="wd-mp__close" @click="$emit('close')" aria-label="Close picker">
        <X :size="14" :stroke-width="2" />
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

    <p class="wd-mp__note">
      <Sparkles :size="11" :stroke-width="2" />
      <span>Mannequin photos are AI-generated for preview purposes only.</span>
    </p>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { X, Check, Sparkles } from 'lucide-vue-next'
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
  background: var(--color-soft-cream);
  border-radius: var(--radius-soft-lg);
  padding: 22px;
  box-shadow: var(--shadow-soft-lg);
  display: flex;
  flex-direction: column;
  gap: 14px;
  max-height: 100%;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: rgba(58, 56, 51, 0.18) transparent;
}
.wd-mp::-webkit-scrollbar { width: 6px; }
.wd-mp::-webkit-scrollbar-thumb {
  background: rgba(58, 56, 51, 0.18);
  border-radius: 999px;
}

.wd-mp__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.wd-mp__title {
  font-family: var(--font-display);
  font-size: 15px;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: var(--color-soft-ink);
  margin: 0;
}
.wd-mp__close {
  width: 32px; height: 32px;
  border-radius: 999px;
  border: none;
  background: var(--color-soft-milk);
  color: var(--color-soft-ink-soft);
  display: grid; place-items: center;
  cursor: pointer;
  transition: background 200ms ease, color 200ms ease;
}
.wd-mp__close:hover {
  background: var(--color-soft-dusty-wash);
  color: var(--color-soft-ink);
}

.wd-mp__tabs {
  display: flex;
  gap: 6px;
}
.wd-mp__tab {
  flex: 1;
  padding: 8px 12px;
  border-radius: var(--radius-soft-pill);
  border: none;
  background: var(--color-soft-milk);
  color: var(--color-soft-ink-soft);
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: background 200ms ease, color 200ms ease;
}
.wd-mp__tab:hover { background: var(--color-soft-sage-mist); color: var(--color-soft-sage-deep); }
.wd-mp__tab.is-active {
  background: var(--color-soft-sage);
  color: var(--color-soft-ink);
}

.wd-mp__grid {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.wd-mp__cell { display: contents; }

.wd-mp__thumb {
  position: relative;
  aspect-ratio: 3 / 4;
  border-radius: 14px;
  overflow: hidden;
  border: 2px solid transparent;
  padding: 0;
  background: var(--color-soft-milk);
  cursor: pointer;
  box-shadow: var(--shadow-soft-sm);
  transition: transform 220ms ease, box-shadow 220ms ease, border-color 220ms ease;
}
.wd-mp__thumb:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-soft);
}
.wd-mp__thumb.is-selected {
  border-color: var(--color-soft-sage);
}
.wd-mp__thumb img {
  width: 100%; height: 100%; object-fit: cover;
  display: block;
}
.wd-mp__tick {
  position: absolute;
  top: 6px; right: 6px;
  width: 22px; height: 22px;
  border-radius: 999px;
  background: var(--color-soft-sage);
  color: var(--color-soft-ink);
  display: grid;
  place-items: center;
  box-shadow: var(--shadow-soft-sm);
}

.wd-mp__note {
  display: flex;
  align-items: center;
  gap: 6px;
  margin: 4px 2px 0;
  padding: 8px 10px;
  border-radius: var(--radius-soft-md, 10px);
  background: var(--color-soft-milk);
  color: var(--color-soft-ink-soft);
  font-size: 11px;
  line-height: 1.4;
  letter-spacing: 0.01em;
}
.wd-mp__note svg { flex-shrink: 0; }
</style>
