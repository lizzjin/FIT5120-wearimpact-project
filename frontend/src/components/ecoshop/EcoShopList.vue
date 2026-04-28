<template>
  <aside class="es-list">
    <header class="es-list__head">
      <h2 class="es-list__title">Nearby locations</h2>
      <span class="es-list__count">{{ places.length }}</span>
    </header>

    <!-- Skeleton -->
    <div v-if="isLoading" class="es-list__scroll">
      <div v-for="n in 5" :key="`sk-${n}`" class="es-list__skeleton"></div>
    </div>

    <!-- Empty state -->
    <div v-else-if="places.length === 0" class="es-list__empty">
      <MapPinOff :size="32" :stroke-width="1.5" />
      <p class="es-list__empty-title">No matches in this radius.</p>
      <p class="es-list__empty-sub">Try widening the radius or switching the type filter.</p>
    </div>

    <!-- Cards (with inline expansion) -->
    <div v-else class="es-list__scroll" ref="scrollEl">
      <div
        v-for="place in places"
        :key="place.place_id"
        class="es-list__row"
        :ref="(el) => (rowRefs[place.place_id] = el)"
      >
        <EcoShopLocationCard
          :place="place"
          :is-active="place.place_id === activePlaceId"
          @select="(p) => $emit('select', p)"
          @hover="(id) => $emit('hover', id)"
        />
        <Transition name="es-expand">
          <EcoShopLocationDetail
            v-if="place.place_id === activePlaceId"
            :place="place"
            :detail="activeDetail"
            :is-loading="isDetailLoading"
            :detail-error="detailError"
            :travel-mode="travelMode"
            :is-route-loading="isRouteLoading"
            :route-info="routeInfo"
            :route-error="routeError"
            @update:travel-mode="(v) => $emit('update:travel-mode', v)"
            @get-directions="$emit('get-directions')"
            @clear-route="$emit('clear-route')"
          />
        </Transition>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { nextTick, ref, watch } from 'vue'
import { MapPinOff } from 'lucide-vue-next'
import EcoShopLocationCard from './EcoShopLocationCard.vue'
import EcoShopLocationDetail from './EcoShopLocationDetail.vue'

const props = defineProps({
  places: { type: Array, default: () => [] },
  activePlaceId: { type: String, default: null },
  isLoading: { type: Boolean, default: false },
  // Detail panel data — passed straight to the inline detail component.
  activeDetail: { type: Object, default: null },
  isDetailLoading: { type: Boolean, default: false },
  detailError: { type: String, default: '' },
  travelMode: { type: String, default: 'DRIVING' },
  isRouteLoading: { type: Boolean, default: false },
  routeInfo: { type: Object, default: null },
  routeError: { type: String, default: '' },
})

defineEmits([
  'select', 'hover',
  'update:travel-mode', 'get-directions', 'clear-route',
])

const scrollEl = ref(null)
const rowRefs = ref({})

// When a card is selected, scroll its row into view inside the list panel
// so the expanded detail is fully visible without manual scrolling.
watch(
  () => props.activePlaceId,
  async (id) => {
    if (!id) return
    await nextTick()
    const row = rowRefs.value[id]
    if (row && typeof row.scrollIntoView === 'function') {
      row.scrollIntoView({ behavior: 'smooth', block: 'nearest' })
    }
  },
)
</script>

<style scoped>
.es-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
  height: 100%;
  background: rgba(255, 255, 255, 0.55);
  border: 1px solid var(--color-kh-glass-border);
  border-radius: 18px;
  padding: 18px 18px 6px;
  overflow: hidden;
}

.es-list__head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
}

.es-list__title {
  font-size: 18px;
  font-weight: 900;
  letter-spacing: -0.01em;
  color: var(--color-text);
  margin: 0;
}

.es-list__count {
  font-size: 12px;
  font-weight: 800;
  color: var(--color-primary-text);
  background: rgba(159, 232, 112, 0.28);
  padding: 3px 10px;
  border-radius: var(--radius-pill);
}

.es-list__scroll {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding-right: 4px;
  padding-bottom: 12px;
}

.es-list__row {
  display: flex;
  flex-direction: column;
}

.es-list__scroll::-webkit-scrollbar { width: 6px; }
.es-list__scroll::-webkit-scrollbar-track { background: transparent; }
.es-list__scroll::-webkit-scrollbar-thumb {
  background: rgba(22, 51, 0, 0.18);
  border-radius: 999px;
}
.es-list__scroll::-webkit-scrollbar-thumb:hover { background: rgba(22, 51, 0, 0.30); }

.es-list__skeleton {
  height: 78px;
  border-radius: 14px;
  background: linear-gradient(90deg, #ede5d4 25%, #e3d9c2 50%, #ede5d4 75%);
  background-size: 200% 100%;
  animation: es-shimmer 1.4s infinite;
}

@keyframes es-shimmer {
  0%   { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.es-list__empty {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  text-align: center;
  color: var(--color-text-faint);
  padding: 28px 16px;
}

.es-list__empty-title {
  font-size: 14px;
  font-weight: 700;
  color: var(--color-text-muted);
  margin: 4px 0 0;
}

.es-list__empty-sub {
  font-size: 12px;
  margin: 0;
  max-width: 240px;
  line-height: 1.45;
}

/* Inline expand transition */
.es-expand-enter-active,
.es-expand-leave-active {
  transition: max-height 320ms cubic-bezier(0.22, 1, 0.36, 1),
              opacity 240ms cubic-bezier(0.22, 1, 0.36, 1);
  overflow: hidden;
}
.es-expand-enter-from,
.es-expand-leave-to { opacity: 0; max-height: 0; }
.es-expand-enter-to,
.es-expand-leave-from { opacity: 1; max-height: 800px; }
</style>
