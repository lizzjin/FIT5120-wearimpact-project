<template>
  <section class="wd-tile" :class="`wd-tile--${theme}`">
    <!-- Tile header — soft chip + label + count. -->
    <header class="wd-tile__head">
      <span class="wd-tile__icon">
        <component :is="meta.icon" :size="15" :stroke-width="2" />
      </span>
      <h3 class="wd-tile__title">{{ meta.label }}</h3>
      <span class="wd-tile__count">{{ items.length }}</span>
    </header>

    <!-- Body — empty state or item strip. The strip scrolls horizontally
         only (overflow-y: hidden), so Lenis (which only smooths vertical
         scrollY) doesn't need to be excluded — and adding data-lenis-prevent
         here actually broke vertical page scroll: wheel events over the
         strip would bypass Lenis and natively jump body scrollY, leaving
         Lenis's internal target out of sync and yanking the page back. -->
    <div v-if="items.length === 0" class="wd-tile__empty">
      <span class="wd-tile__empty-dot" />
      <span>Nothing yet — drop a photo to fill this drawer.</span>
    </div>

    <div v-else class="wd-tile__strip" role="list">
      <button
        v-for="g in items"
        :key="g.id"
        type="button"
        role="listitem"
        class="wd-tile__card"
        :class="{ 'wd-tile__card--active': activeId === g.id }"
        @click="$emit('select', g.id)"
      >
        <span class="wd-tile__card-media">
          <img v-if="g.image_base64" :src="g.image_base64" :alt="g.filename" />
        </span>
        <span class="wd-tile__card-label">{{ formatSub(g.sub_category) }}</span>
      </button>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { Shirt, ShoppingBag, Footprints, Sparkles } from 'lucide-vue-next'

const props = defineProps({
  category: { type: String, required: true },
  // `sage | dusty | oat | fog` — drives the colour-block treatment.
  theme: { type: String, default: 'sage' },
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
const meta = computed(() => META[props.category] || { label: props.category, icon: Shirt })

function formatSub(v) {
  if (!v) return 'Unsorted'
  return String(v).replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())
}
</script>

<style scoped>
.wd-tile {
  position: relative;
  border-radius: var(--radius-soft);
  border: 1.5px solid var(--color-soft-line-strong);
  box-shadow: var(--shadow-soft);
  padding: 22px 24px 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-height: 220px;
}

/* Theme colours — each tile gets a muted morandi background. The inner
   item-card paper colour stays cream across themes so garment thumbs
   stay legible. */
.wd-tile--sage  { background: var(--color-soft-sage-mist); }
.wd-tile--dusty { background: var(--color-soft-dusty-wash); }
.wd-tile--oat   { background: var(--color-soft-oat); }
.wd-tile--fog   { background: var(--color-soft-fog); }

/* ── Header ───────────────────────────────────────────────── */
.wd-tile__head {
  display: flex;
  align-items: center;
  gap: 10px;
}
.wd-tile__icon {
  width: 30px; height: 30px;
  border-radius: 50%;
  background: var(--color-soft-cream);
  color: var(--color-soft-sage-deep);
  display: grid; place-items: center;
  flex-shrink: 0;
}
.wd-tile__title {
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: var(--color-soft-ink);
}
.wd-tile__count {
  margin-left: auto;
  display: inline-grid;
  place-items: center;
  min-width: 26px;
  height: 26px;
  padding: 0 10px;
  border-radius: var(--radius-soft-pill);
  background: var(--color-soft-cream);
  color: var(--color-soft-ink-soft);
  font-family: var(--font-display);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: -0.01em;
}

/* ── Empty state ──────────────────────────────────────────── */
.wd-tile__empty {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 16px 18px;
  border: 1px dashed rgba(58, 56, 51, 0.18);
  border-radius: 16px;
  background: var(--color-soft-cream);
  color: var(--color-soft-ink-soft);
  font-size: 12.5px;
  font-weight: 500;
}
.wd-tile__empty-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  background: var(--color-soft-sage);
  flex-shrink: 0;
}

/* ── Item strip (horizontal scroll) ───────────────────────── */
.wd-tile__strip {
  display: flex;
  gap: 12px;
  overflow-x: auto;
  overflow-y: hidden;
  padding: 4px 2px 10px;
  scroll-snap-type: x mandatory;
  scrollbar-width: thin;
  scrollbar-color: rgba(58, 56, 51, 0.2) transparent;
}
.wd-tile__strip::-webkit-scrollbar { height: 6px; }
.wd-tile__strip::-webkit-scrollbar-track {
  background: transparent;
}
.wd-tile__strip::-webkit-scrollbar-thumb {
  background: rgba(58, 56, 51, 0.2);
  border-radius: 999px;
}

/* ── Item card ────────────────────────────────────────────── */
.wd-tile__card {
  flex: 0 0 118px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 8px 8px 10px;
  background: var(--color-soft-cream);
  border: 1px solid var(--color-soft-line-strong);
  border-radius: 14px;
  cursor: pointer;
  scroll-snap-align: start;
  text-align: center;
  color: var(--color-soft-ink);
  box-shadow: var(--shadow-soft-sm);
  transition: transform 220ms cubic-bezier(0.22, 1, 0.36, 1),
              box-shadow 220ms ease;
}
.wd-tile__card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-soft);
}
.wd-tile__card--active {
  background: var(--color-soft-sage);
  color: var(--color-soft-ink);
  box-shadow: var(--shadow-soft);
}

.wd-tile__card-media {
  display: grid;
  place-items: center;
  aspect-ratio: 1;
  border-radius: 10px;
  background: var(--color-soft-milk);
  overflow: hidden;
}
.wd-tile__card-media img {
  width: 100%; height: 100%;
  object-fit: contain;
  padding: 6px;
}

.wd-tile__card-label {
  font-size: 11.5px;
  font-weight: 600;
  letter-spacing: -0.01em;
  color: var(--color-soft-ink-soft);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.wd-tile__card--active .wd-tile__card-label { color: var(--color-soft-ink); }

@media (max-width: 700px) {
  .wd-tile { padding: 18px; min-height: 200px; }
  .wd-tile__card { flex: 0 0 100px; }
}
</style>
