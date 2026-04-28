<template>
  <div class="es-filter">
    <div class="es-filter__inner">
      <!-- Type chips -->
      <div class="es-filter__group">
        <span class="es-filter__group-label">Type</span>
        <div class="es-filter__chips" role="group" aria-label="Filter by location type">
          <button
            v-for="opt in TYPE_OPTIONS"
            :key="opt.value"
            type="button"
            class="es-chip"
            :class="{ 'es-chip--active': activeFilter === opt.value }"
            :aria-pressed="activeFilter === opt.value"
            @click="$emit('update:active-filter', opt.value)"
          >
            <span
              v-if="opt.color"
              class="es-chip__dot"
              :style="{ background: opt.color }"
            ></span>
            <component v-if="opt.icon" :is="opt.icon" :size="14" :stroke-width="2.2" />
            {{ opt.label }}
          </button>
        </div>
      </div>

      <!-- Radius slider -->
      <div class="es-filter__group es-filter__group--radius">
        <span class="es-filter__group-label">
          Radius
          <strong>{{ radiusKm }} km</strong>
        </span>
        <div class="es-radius">
          <button
            type="button"
            class="es-radius__btn"
            :disabled="radiusKm <= MIN_RADIUS"
            aria-label="Decrease radius"
            @click="step(-1)"
          >
            <Minus :size="14" :stroke-width="2.5" />
          </button>
          <input
            type="range"
            class="es-radius__slider"
            :min="MIN_RADIUS"
            :max="MAX_RADIUS"
            :step="1"
            :value="radiusKm"
            @input="onSlide"
            @change="onCommit"
            aria-label="Search radius in kilometres"
          />
          <button
            type="button"
            class="es-radius__btn"
            :disabled="radiusKm >= MAX_RADIUS"
            aria-label="Increase radius"
            @click="step(1)"
          >
            <Plus :size="14" :stroke-width="2.5" />
          </button>
        </div>
        <span class="es-radius__axis">
          <span>{{ MIN_RADIUS }} km</span>
          <span>{{ MAX_RADIUS }} km</span>
        </span>
      </div>

      <!-- Result count -->
      <div class="es-filter__count">
        <span v-if="isLoading" class="es-filter__count-loading">Searching…</span>
        <template v-else>
          Showing <strong>{{ count }}</strong>
          {{ count === 1 ? 'location' : 'locations' }}
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ShoppingBag, HandHeart, Recycle, Minus, Plus, Layers } from 'lucide-vue-next'

const props = defineProps({
  activeFilter: { type: String, default: 'all' },
  radiusKm: { type: Number, default: 5 },
  count: { type: Number, default: 0 },
  isLoading: { type: Boolean, default: false },
})
const emit = defineEmits(['update:active-filter', 'update:radius-km', 'commit-radius'])

const MIN_RADIUS = 1
const MAX_RADIUS = 20

// Cream-friendly accent palette: lime / dark-green / honey-tan.
const TYPE_OPTIONS = [
  { value: 'all',                label: 'All',         icon: Layers,       color: null },
  { value: 'second_hand_shop',   label: 'Second-hand', icon: ShoppingBag,  color: '#9fe870' },
  { value: 'donation_point',     label: 'Donation',    icon: HandHeart,    color: '#163300' },
  { value: 'recycling',          label: 'Recycling',   icon: Recycle,      color: '#c9a458' },
]

function step(delta) {
  const next = Math.min(MAX_RADIUS, Math.max(MIN_RADIUS, props.radiusKm + delta))
  if (next === props.radiusKm) return
  emit('update:radius-km', next)
  emit('commit-radius', next)
}

function onSlide(e) {
  emit('update:radius-km', Number(e.target.value))
}

function onCommit(e) {
  emit('commit-radius', Number(e.target.value))
}
</script>

<style scoped>
.es-filter {
  position: sticky;
  top: 76px;     /* clears the navbar */
  z-index: 5;
  background: rgba(246, 240, 230, 0.85);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-top: 1px solid var(--color-kh-glass-border);
  border-bottom: 1px solid var(--color-kh-glass-border);
}

.es-filter__inner {
  max-width: 1320px;
  margin: 0 auto;
  padding: 18px 48px;
  display: grid;
  grid-template-columns: minmax(0, 1.4fr) minmax(0, 1fr) auto;
  gap: 32px;
  align-items: center;
}

.es-filter__group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.es-filter__group-label {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--color-text-faint);
}

.es-filter__group-label strong {
  color: var(--color-primary-text);
  font-weight: 900;
  margin-left: 4px;
  letter-spacing: -0.01em;
  font-variant-numeric: tabular-nums;
}

/* ── Chips ─────────────────────────────────────────────────────── */
.es-filter__chips {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.es-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 14px;
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid var(--color-kh-glass-border);
  border-radius: var(--radius-pill);
  font-family: inherit;
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-muted);
  cursor: pointer;
  transition:
    background 180ms var(--motion-entrance),
    color 180ms var(--motion-entrance),
    border-color 180ms var(--motion-entrance);
}

.es-chip:hover:not(.es-chip--active) {
  background: rgba(159, 232, 112, 0.16);
  border-color: rgba(22, 51, 0, 0.18);
  color: var(--color-primary-text);
}

.es-chip--active {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: var(--color-primary-text);
  font-weight: 700;
}

.es-chip__dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  border: 1.5px solid rgba(22, 51, 0, 0.2);
}

/* ── Radius slider ─────────────────────────────────────────────── */
.es-radius {
  display: flex;
  align-items: center;
  gap: 10px;
}

.es-radius__btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  border: 1px solid var(--color-kh-glass-border);
  background: rgba(255, 255, 255, 0.85);
  color: var(--color-primary-text);
  border-radius: 50%;
  cursor: pointer;
  transition: background 160ms var(--motion-entrance);
}

.es-radius__btn:hover:not(:disabled) {
  background: rgba(159, 232, 112, 0.22);
}

.es-radius__btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.es-radius__slider {
  flex: 1;
  -webkit-appearance: none;
  appearance: none;
  height: 4px;
  background: rgba(22, 51, 0, 0.14);
  border-radius: 999px;
  outline: none;
  cursor: pointer;
}

.es-radius__slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: var(--color-primary);
  border: 2px solid var(--color-primary-text);
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(22, 51, 0, 0.2);
}

.es-radius__slider::-moz-range-thumb {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: var(--color-primary);
  border: 2px solid var(--color-primary-text);
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(22, 51, 0, 0.2);
}

.es-radius__axis {
  display: flex;
  justify-content: space-between;
  font-size: 10px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--color-text-faint);
  font-weight: 700;
  margin-top: 2px;
}

/* ── Count ─────────────────────────────────────────────────────── */
.es-filter__count {
  font-size: 13px;
  color: var(--color-text-muted);
  white-space: nowrap;
  font-variant-numeric: tabular-nums;
}

.es-filter__count strong {
  color: var(--color-primary-text);
  font-weight: 800;
  font-size: 16px;
  margin-right: 2px;
}

.es-filter__count-loading {
  color: var(--color-text-faint);
}

/* ── Responsive ───────────────────────────────────────────────── */
@media (max-width: 1024px) {
  .es-filter__inner {
    grid-template-columns: 1fr;
    gap: 18px;
    padding: 16px 20px;
  }
}
</style>
