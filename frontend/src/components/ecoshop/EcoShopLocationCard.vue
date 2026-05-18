<template>
  <button
    type="button"
    class="es-card"
    :class="{ 'es-card--active': isActive }"
    :style="{ '--type-color': typeMeta.color }"
    ref="cardRef"
    @click="$emit('select', place)"
    @mouseenter="$emit('hover', place.place_id)"
    @mouseleave="$emit('hover', null)"
  >
    <span class="es-card__icon-wrap">
      <component :is="typeMeta.icon" :size="18" :stroke-width="2" />
    </span>

    <span class="es-card__body">
      <span class="es-card__head">
        <span class="es-card__name">{{ place.name }}</span>
        <span class="es-card__type">{{ typeMeta.label }}</span>
      </span>
      <span class="es-card__meta">
        <span class="es-card__distance">
          <Navigation2 :size="12" :stroke-width="2.4" />
          {{ place.distance_km }} km
        </span>
        <span v-if="place.address" class="es-card__address">
          {{ place.address }}
        </span>
      </span>
      <span v-if="place.summary" class="es-card__summary">{{ place.summary }}</span>
    </span>

    <ChevronRight :size="16" :stroke-width="2" class="es-card__chev" />
  </button>
</template>

<script setup>
import { computed, ref } from 'vue'
import { ShoppingBag, HandHeart, Recycle, MapPin, Navigation2, ChevronRight } from 'lucide-vue-next'
import { useHover, useFocusRing } from '../../motion'

const props = defineProps({
  place: { type: Object, required: true },
  isActive: { type: Boolean, default: false },
})
defineEmits(['select', 'hover'])

const cardRef = ref(null)
useHover(cardRef, { mode: 'card' })
useFocusRing(cardRef, { color: 'var(--color-primary)' })

const TYPE_META = {
  second_hand_shop: { label: 'Second-hand', icon: ShoppingBag, color: '#9fe870' },
  donation_point:   { label: 'Donation',    icon: HandHeart,   color: '#163300' },
  recycling:        { label: 'Recycling',   icon: Recycle,     color: '#c9a458' },
}

const typeMeta = computed(() =>
  TYPE_META[props.place.type] || { label: 'Eco-shop', icon: MapPin, color: '#163300' },
)
</script>

<style scoped>
.es-card {
  --type-color: var(--color-primary);
  display: flex;
  align-items: flex-start;
  gap: 12px;
  width: 100%;
  padding: 14px 14px 14px 12px;
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid var(--color-kh-glass-border);
  border-radius: 14px;
  text-align: left;
  cursor: pointer;
  font-family: inherit;
  transition:
    transform 200ms var(--motion-entrance),
    box-shadow 200ms var(--motion-entrance),
    border-color 200ms var(--motion-entrance),
    background 200ms var(--motion-entrance);
}

.es-card:hover {
  transform: translateY(-2px);
  border-color: var(--type-color);
  box-shadow: 0 10px 24px rgba(22, 51, 0, 0.08);
}

.es-card--active {
  border-color: var(--type-color);
  background: rgba(159, 232, 112, 0.12);
  box-shadow: 0 0 0 1px var(--type-color), 0 12px 28px rgba(22, 51, 0, 0.10);
}

.es-card__icon-wrap {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: var(--type-color);
  color: var(--color-primary-text);
  flex-shrink: 0;
  margin-top: 2px;
}

/* Donation pin (dark-green) needs cream icon for contrast. */
.es-card[style*="#163300"] .es-card__icon-wrap {
  color: var(--color-warm-cream);
}

.es-card__body {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
  flex: 1;
}

.es-card__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.es-card__name {
  font-size: 14px;
  font-weight: 800;
  color: var(--color-text);
  letter-spacing: -0.01em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
  min-width: 0;
}

.es-card__type {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--color-text-faint);
  flex-shrink: 0;
}

.es-card__meta {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 12px;
  color: var(--color-text-muted);
}

.es-card__distance {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-weight: 700;
  color: var(--color-primary-text);
  flex-shrink: 0;
}

.es-card__address {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  min-width: 0;
}

.es-card__summary {
  font-size: 12px;
  color: var(--color-text-faint);
  line-height: 1.4;
  margin-top: 2px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.es-card__chev {
  color: var(--color-text-faint);
  margin-top: 12px;
  flex-shrink: 0;
  transition: transform 160ms var(--motion-entrance), color 160ms var(--motion-entrance);
}

.es-card:hover .es-card__chev {
  transform: translateX(3px);
  color: var(--color-primary-text);
}
</style>
