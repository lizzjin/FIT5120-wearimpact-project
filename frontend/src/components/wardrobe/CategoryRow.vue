<template>
  <section class="wd-row">
    <header class="wd-row__head">
      <div class="wd-row__title-wrap">
        <span class="wd-row__icon">
          <component :is="iconComponent" :size="16" :stroke-width="2" />
        </span>
        <h3 class="wd-row__title">{{ label }}</h3>
        <span class="wd-row__count">{{ items.length }}</span>
      </div>
    </header>

    <div v-if="items.length === 0" class="wd-row__empty">
      Nothing here yet — upload a photo to fill this drawer.
    </div>

    <div v-else class="wd-row__strip" role="list">
      <button
        v-for="g in items"
        :key="g.id"
        type="button"
        role="listitem"
        class="wd-mini"
        :class="{ 'wd-mini--active': activeId === g.id }"
        @click="$emit('select', g.id)"
      >
        <div class="wd-mini__media">
          <img v-if="g.image_base64" :src="g.image_base64" :alt="g.filename" />
        </div>
        <span class="wd-mini__sub">{{ formatSub(g.sub_category) }}</span>
      </button>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { Shirt, ShoppingBag, Footprints, Layers, Sparkles } from 'lucide-vue-next'

const props = defineProps({
  category: { type: String, required: true },
  items: { type: Array, default: () => [] },
  activeId: { type: [Number, String, null], default: null }
})
defineEmits(['select'])

const META = {
  upper_body: { label: 'Tops',       icon: Shirt },
  one_pieces: { label: 'One-Pieces', icon: Sparkles },
  lower_body: { label: 'Bottoms',    icon: ShoppingBag },
  footwear:   { label: 'Shoes',      icon: Footprints }
}
const meta = computed(() => META[props.category] || { label: props.category, icon: Layers })
const label = computed(() => meta.value.label)
const iconComponent = computed(() => meta.value.icon)

function formatSub(v) {
  if (!v) return '—'
  return String(v).replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())
}
</script>

<style scoped>
.wd-row {
  background: var(--color-surface);
  border-radius: var(--radius-card);
  padding: 16px 18px;
  box-shadow: var(--shadow-card);
  /* Lock the row to a single fixed height so the empty state and a
     full strip occupy exactly the same vertical space — that's what
     keeps the left detail panel and right rail aligned with this column.
     Sized to hold a 110×110 thumbnail + caption without clipping. */
  height: 220px;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.wd-row__head {
  margin-bottom: 12px;
}

.wd-row__title-wrap {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: var(--color-primary-light);
  border: 1px solid var(--color-border-light);
  padding: 6px 12px 6px 10px;
  border-radius: var(--radius-pill);
}

.wd-row__icon {
  width: 22px; height: 22px;
  border-radius: 999px;
  background: var(--color-primary);
  color: var(--color-primary-text);
  display: grid; place-items: center;
}

.wd-row__title {
  font-size: 14px; font-weight: 800;
  color: var(--color-primary-text);
  letter-spacing: -0.2px;
}

.wd-row__count {
  font-size: 11px; font-weight: 700;
  background: var(--color-primary-text);
  color: var(--color-primary);
  padding: 2px 8px;
  border-radius: var(--radius-pill);
}

.wd-row__empty {
  flex: 1;
  background: var(--color-surface-alt);
  border: 1px dashed var(--color-border-strong);
  border-radius: var(--radius-card-sm);
  padding: 18px;
  display: grid;
  place-items: center;
  text-align: center;
  color: var(--color-text-subtle);
  font-size: 13px;
}

.wd-row__strip {
  flex: 1;
  display: flex;
  gap: 12px;
  overflow-x: auto;
  overflow-y: hidden;
  padding: 4px 2px 8px;
  scroll-snap-type: x mandatory;
  scrollbar-width: thin;
  min-width: 0;
}
.wd-row__strip::-webkit-scrollbar { height: 6px; }
.wd-row__strip::-webkit-scrollbar-thumb {
  background: var(--color-border-strong);
  border-radius: 999px;
}

.wd-mini {
  flex: 0 0 110px;
  background: var(--color-surface);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-card-sm);
  padding: 8px 8px 10px;
  cursor: pointer;
  scroll-snap-align: start;
  text-align: center;
  display: flex; flex-direction: column; gap: 6px;
  transition: transform var(--transition-base), border-color var(--transition-base), box-shadow var(--transition-base);
}
.wd-mini:hover {
  transform: translateY(-3px);
  border-color: var(--color-primary);
  box-shadow: var(--shadow-card-hover);
}
.wd-mini--active {
  border-color: var(--color-primary-text);
  box-shadow: 0 0 0 2px var(--color-primary);
}

.wd-mini__media {
  aspect-ratio: 1;
  border-radius: var(--radius-card-sm);
  background: linear-gradient(135deg, var(--color-primary-lighter), var(--color-surface-alt));
  overflow: hidden;
  display: grid; place-items: center;
}
.wd-mini__media img {
  width: 100%; height: 100%; object-fit: contain; padding: 8px;
}

.wd-mini__sub {
  font-size: 11px;
  font-weight: 600;
  color: var(--color-text-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
}
</style>
