<template>
  <div class="es-detail" :style="{ '--type-color': typeMeta.color }">
    <!-- Loading skeleton while detail arrives -->
    <div v-if="isLoading" class="es-detail__loading">
      <span class="es-detail__skel" style="width: 80%"></span>
      <span class="es-detail__skel" style="width: 60%"></span>
      <span class="es-detail__skel" style="width: 70%"></span>
    </div>

    <template v-else>
      <!-- Address / hours / phone / website -->
      <div v-if="detail" class="es-detail__rows">
        <div v-if="detail.address" class="es-detail__row">
          <MapPin :size="14" :stroke-width="2" />
          <span>{{ detail.address }}</span>
        </div>
        <div v-if="openingHours.length > 0" class="es-detail__row es-detail__row--multiline">
          <Clock :size="14" :stroke-width="2" />
          <ul class="es-detail__hours">
            <li v-for="(line, i) in openingHours" :key="i">{{ line }}</li>
          </ul>
        </div>
        <div v-if="detail.phone" class="es-detail__row">
          <Phone :size="14" :stroke-width="2" />
          <a class="es-detail__link" :href="`tel:${detail.phone}`">{{ detail.phone }}</a>
        </div>
        <div v-if="detail.website" class="es-detail__row">
          <Globe :size="14" :stroke-width="2" />
          <a
            class="es-detail__link"
            :href="detail.website"
            target="_blank"
            rel="noopener noreferrer"
          >{{ shortUrl(detail.website) }}</a>
        </div>
      </div>

      <p v-if="detailError" class="es-detail__error">{{ detailError }}</p>

      <!-- Directions controls -->
      <div class="es-detail__directions">
        <p class="es-detail__directions-label">Directions from your location</p>
        <div class="es-detail__modes" role="tablist">
          <button
            v-for="m in TRAVEL_MODES"
            :key="m.value"
            type="button"
            class="es-mode"
            :class="{ 'es-mode--active': travelMode === m.value }"
            :aria-pressed="travelMode === m.value"
            @click="$emit('update:travel-mode', m.value)"
          >
            <component :is="m.icon" :size="14" :stroke-width="2.2" />
            {{ m.label }}
          </button>
        </div>

        <div class="es-detail__actions">
          <button
            type="button"
            class="es-detail__btn es-detail__btn--primary"
            :disabled="isRouteLoading"
            @click="$emit('get-directions')"
          >
            <Navigation2 :size="14" :stroke-width="2.4" />
            {{ isRouteLoading ? 'Drawing route…' : (hasRoute ? 'Update route' : 'Show route') }}
          </button>
          <button
            v-if="hasRoute"
            type="button"
            class="es-detail__btn es-detail__btn--ghost"
            @click="$emit('clear-route')"
          >
            <X :size="14" :stroke-width="2.4" />
            Clear route
          </button>
        </div>

        <div v-if="hasRoute" class="es-detail__route-info">
          <span class="es-detail__route-pill">
            <Route :size="13" :stroke-width="2.2" />
            {{ routeInfo.distance }}
          </span>
          <span class="es-detail__route-pill">
            <Clock :size="13" :stroke-width="2.2" />
            {{ routeInfo.duration }}
          </span>
        </div>

        <p v-if="routeError" class="es-detail__error">{{ routeError }}</p>
      </div>
    </template>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { BusFront, CarFront, Clock, Footprints, Globe, HandHeart, MapPin, Navigation2, Phone, Recycle, Route, ShoppingBag, X } from 'lucide-vue-next'

const props = defineProps({
  place: { type: Object, default: null },
  detail: { type: Object, default: null },
  isLoading: { type: Boolean, default: false },
  detailError: { type: String, default: '' },
  travelMode: { type: String, default: 'DRIVING' },
  isRouteLoading: { type: Boolean, default: false },
  routeInfo: { type: Object, default: null },     // { distance, duration } | null
  routeError: { type: String, default: '' },
})

defineEmits(['update:travel-mode', 'get-directions', 'clear-route'])

const TYPE_META = {
  second_hand_shop: { color: '#9fe870', icon: ShoppingBag },
  donation_point:   { color: '#163300', icon: HandHeart },
  recycling:        { color: '#c9a458', icon: Recycle },
}

const TRAVEL_MODES = [
  { value: 'DRIVING',  label: 'Drive',   icon: CarFront },
  { value: 'WALKING',  label: 'Walk',    icon: Footprints },
  { value: 'TRANSIT',  label: 'Transit', icon: BusFront },
]

const typeMeta = computed(() => TYPE_META[props.place?.type] || { color: '#163300', icon: MapPin })

const openingHours = computed(() => {
  const raw = props.detail?.opening_hours
  if (!raw) return []
  if (Array.isArray(raw)) return raw
  if (typeof raw === 'string') return raw.split('\n').filter(Boolean)
  return []
})

const hasRoute = computed(() => !!props.routeInfo)

function shortUrl(url) {
  try {
    const u = new URL(url)
    return u.hostname.replace(/^www\./, '') + (u.pathname !== '/' ? u.pathname : '')
  } catch {
    return url
  }
}
</script>

<style scoped>
.es-detail {
  --type-color: var(--color-primary);
  background: rgba(159, 232, 112, 0.10);
  border: 1px solid rgba(22, 51, 0, 0.14);
  border-top: none;
  border-radius: 0 0 14px 14px;
  margin-top: -8px;
  padding: 16px 16px 18px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  animation: es-detail-in 280ms cubic-bezier(0.22, 1, 0.36, 1);
}

@keyframes es-detail-in {
  from { opacity: 0; transform: translateY(-6px); max-height: 0; }
  to   { opacity: 1; transform: translateY(0); max-height: 600px; }
}

.es-detail__loading {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.es-detail__skel {
  height: 12px;
  border-radius: 6px;
  background: linear-gradient(90deg, #ede5d4 25%, #e3d9c2 50%, #ede5d4 75%);
  background-size: 200% 100%;
  animation: es-shimmer 1.4s infinite;
}

@keyframes es-shimmer {
  0%   { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* ── Info rows ─────────────────────────────────────────────────── */
.es-detail__rows {
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 13px;
  color: var(--color-text-muted);
  line-height: 1.5;
}

.es-detail__row {
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.es-detail__row svg {
  color: var(--color-primary-text);
  flex-shrink: 0;
  margin-top: 2px;
}

.es-detail__row--multiline {
  align-items: flex-start;
}

.es-detail__hours {
  list-style: none;
  margin: 0;
  padding: 0;
  font-size: 12px;
  color: var(--color-text-muted);
  line-height: 1.6;
}

.es-detail__link {
  color: var(--color-primary-text);
  font-weight: 600;
  text-decoration: none;
  border-bottom: 1px solid rgba(22, 51, 0, 0.18);
}

.es-detail__link:hover {
  border-color: var(--color-primary);
}

/* ── Directions ─────────────────────────────────────────────────── */
.es-detail__directions {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding-top: 10px;
  border-top: 1px dashed rgba(22, 51, 0, 0.14);
}

.es-detail__directions-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--color-text-faint);
  margin: 0;
}

.es-detail__modes {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.es-mode {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 6px 12px;
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid var(--color-kh-glass-border);
  border-radius: var(--radius-pill);
  font-family: inherit;
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-muted);
  cursor: pointer;
  transition: background 160ms var(--motion-entrance), color 160ms var(--motion-entrance);
}

.es-mode:hover:not(.es-mode--active) {
  background: rgba(159, 232, 112, 0.18);
  color: var(--color-primary-text);
}

.es-mode--active {
  background: var(--color-primary-text);
  color: var(--color-warm-cream);
  border-color: var(--color-primary-text);
}

.es-detail__actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.es-detail__btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: var(--radius-pill);
  font-family: inherit;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  transition: transform 160ms var(--motion-entrance), box-shadow 160ms var(--motion-entrance);
  border: 1px solid transparent;
}

.es-detail__btn--primary {
  background: var(--color-primary);
  color: var(--color-primary-text);
  border-color: var(--color-primary);
}

.es-detail__btn--primary:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(22, 51, 0, 0.18);
}

.es-detail__btn--primary:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.es-detail__btn--ghost {
  background: transparent;
  color: var(--color-text-muted);
  border-color: var(--color-kh-glass-border);
}

.es-detail__btn--ghost:hover {
  background: rgba(22, 51, 0, 0.05);
  color: var(--color-primary-text);
}

.es-detail__route-info {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.es-detail__route-pill {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 5px 11px;
  background: var(--color-warm-cream);
  border: 1px solid var(--color-kh-glass-border);
  border-radius: var(--radius-pill);
  font-size: 12px;
  font-weight: 700;
  color: var(--color-primary-text);
}

.es-detail__error {
  font-size: 12px;
  color: #b53236;
  background: rgba(208, 50, 56, 0.08);
  padding: 8px 12px;
  border-radius: 8px;
  margin: 0;
}
</style>
