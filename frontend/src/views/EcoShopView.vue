<template>
  <div class="eco-page">
    <QuizBackground />

    <Navbar />

    <main class="eco-page__main">
      <EcoShopHero
        :is-locating="isLocating"
        :is-fallback="isFallback"
        @use-location="useMyLocation"
      />

      <EcoShopFilterBar
        :active-filter="activeFilter"
        :radius-km="radiusKm"
        :count="filteredPlaces.length"
        :is-loading="isLoading"
        @update:active-filter="(v) => (activeFilter = v)"
        @update:radius-km="(v) => (radiusKm = v)"
        @commit-radius="onRadiusCommit"
      />

      <!-- Mobile tab toggle (≤ 1024px) -->
      <div class="eco-page__tabs" role="tablist">
        <button
          type="button"
          class="eco-tab"
          :class="{ 'eco-tab--active': mobileTab === 'map' }"
          @click="mobileTab = 'map'"
        >
          <MapIcon :size="14" :stroke-width="2" /> Map
        </button>
        <button
          type="button"
          class="eco-tab"
          :class="{ 'eco-tab--active': mobileTab === 'list' }"
          @click="mobileTab = 'list'"
        >
          <List :size="14" :stroke-width="2" /> List ({{ filteredPlaces.length }})
        </button>
      </div>

      <section class="eco-page__split">
        <div class="eco-page__map" :data-active="mobileTab === 'map'">
          <EcoShopMap
            :user-lat="userLat"
            :user-lng="userLng"
            :places="filteredPlaces"
            :radius-km="radiusKm"
            :active-place-id="activePlaceId"
            :hovered-place-id="hoveredPlaceId"
            :route-request="routeRequest"
            @select-place="onSelectPlace"
            @route-info="onRouteInfo"
            @route-error="onRouteError"
          />
        </div>

        <div class="eco-page__list" :data-active="mobileTab === 'list'">
          <EcoShopList
            :places="filteredPlaces"
            :active-place-id="activePlaceId"
            :is-loading="isLoading"
            :active-detail="activeDetail"
            :is-detail-loading="isDetailLoading"
            :detail-error="detailError"
            :travel-mode="travelMode"
            :is-route-loading="isRouteLoading"
            :route-info="routeInfo"
            :route-error="routeError"
            @select="onSelectPlace"
            @hover="(id) => (hoveredPlaceId = id)"
            @update:travel-mode="(v) => (travelMode = v)"
            @get-directions="getDirections"
            @clear-route="clearRoute"
          />
        </div>
      </section>

      <p v-if="errorMessage" class="eco-page__status eco-page__status--error">
        {{ errorMessage }}
      </p>
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { List, Map as MapIcon } from 'lucide-vue-next'
import Navbar from '../components/Navbar.vue'
import QuizBackground from '../components/knowledge/QuizBackground.vue'
import EcoShopHero from '../components/ecoshop/EcoShopHero.vue'
import EcoShopFilterBar from '../components/ecoshop/EcoShopFilterBar.vue'
import EcoShopMap from '../components/ecoshop/EcoShopMap.vue'
import EcoShopList from '../components/ecoshop/EcoShopList.vue'
import { fetchNearbyPlaces, fetchPlaceDetails, getUserCoordinates } from '../services/locationService'

// ── State ────────────────────────────────────────────────────────────────
const userLat = ref(null)
const userLng = ref(null)
const isFallback = ref(false)
const isLocating = ref(false)

const radiusKm = ref(5)
const allPlaces = ref([])
const isLoading = ref(true)
const errorMessage = ref('')

const activeFilter = ref('all')

// Selection + inline detail panel.
const activePlaceId = ref(null)
const hoveredPlaceId = ref(null)
const activeDetail = ref(null)
const isDetailLoading = ref(false)
const detailError = ref('')
const detailCache = new Map()

// Travel mode + route drawing — owned here so the map and list both
// stay in sync without tight coupling.
const travelMode = ref('DRIVING')
const routeRequest = ref(null)        // { profile, start, end } | null
const routeInfo = ref(null)           // { distance, duration } | null
const isRouteLoading = ref(false)
const routeError = ref('')

const mobileTab = ref('map')

// ── Derived ──────────────────────────────────────────────────────────────
const filteredPlaces = computed(() => {
  if (activeFilter.value === 'all') return allPlaces.value
  return allPlaces.value.filter((p) => p.type === activeFilter.value)
})

const activePlace = computed(() =>
  allPlaces.value.find((p) => p.place_id === activePlaceId.value) || null,
)

// ── Geolocation + initial load ──────────────────────────────────────────
async function useMyLocation() {
  isLocating.value = true
  try {
    const coords = await getUserCoordinates()
    userLat.value = coords.lat
    userLng.value = coords.lng
    isFallback.value = coords.isFallback
    await loadPlaces()
  } finally {
    isLocating.value = false
  }
}

async function loadPlaces() {
  if (userLat.value == null || userLng.value == null) return
  isLoading.value = true
  errorMessage.value = ''
  // Re-loading the place set invalidates any active selection / route.
  activePlaceId.value = null
  clearRoute()
  try {
    const data = await fetchNearbyPlaces({
      lat: userLat.value,
      lng: userLng.value,
      radiusKm: radiusKm.value,
    })
    allPlaces.value = data.results || []
  } catch (err) {
    errorMessage.value = err.message || 'Failed to load eco-shops. Please try again.'
    allPlaces.value = []
  } finally {
    isLoading.value = false
  }
}

function onRadiusCommit(km) {
  radiusKm.value = km
  loadPlaces()
}

// ── Card / marker selection ─────────────────────────────────────────────
async function onSelectPlace(place) {
  // Clicking the active card again collapses the detail panel.
  if (activePlaceId.value === place.place_id) {
    clearSelection()
    return
  }

  activePlaceId.value = place.place_id
  detailError.value = ''
  // Switching place drops any previously drawn route.
  clearRoute()

  if (detailCache.has(place.place_id)) {
    activeDetail.value = detailCache.get(place.place_id)
    isDetailLoading.value = false
    return
  }

  activeDetail.value = null
  isDetailLoading.value = true
  try {
    const detail = await fetchPlaceDetails(place.place_id)
    const enriched = { ...detail, lat: place.lat, lng: place.lng }
    detailCache.set(place.place_id, enriched)
    activeDetail.value = enriched
  } catch (err) {
    detailError.value = err.message || 'Could not load details. Please try again.'
  } finally {
    isDetailLoading.value = false
  }
}

function clearSelection() {
  activePlaceId.value = null
  activeDetail.value = null
  detailError.value = ''
  clearRoute()
}

// ── Directions ──────────────────────────────────────────────────────────
function travelModeToProfile(mode) {
  // Mapbox Directions exposes driving / walking / cycling. Transit isn't
  // supported by the public Directions endpoint, so fall back to driving
  // and let the UI keep the "Transit" label as user intent.
  if (mode === 'WALKING') return 'walking'
  if (mode === 'TRANSIT') return 'driving'
  return 'driving'
}

function getDirections() {
  const place = activePlace.value
  if (!place || userLat.value == null) return
  routeError.value = ''
  isRouteLoading.value = true
  routeRequest.value = {
    profile: travelModeToProfile(travelMode.value),
    start: [userLng.value, userLat.value],
    end: [place.lng, place.lat],
    // Bump revision so re-clicking the same mode still triggers a redraw.
    rev: Date.now(),
  }
}

function clearRoute() {
  routeRequest.value = null
  routeInfo.value = null
  routeError.value = ''
  isRouteLoading.value = false
}

function onRouteInfo(info) {
  routeInfo.value = info
  isRouteLoading.value = false
}

function onRouteError(msg) {
  routeError.value = msg
  isRouteLoading.value = false
  routeInfo.value = null
}

// Re-run directions when the travel mode changes while a route is shown.
watch(travelMode, () => {
  if (routeInfo.value || routeRequest.value) getDirections()
})

// Filter change shouldn't keep selection if the active place is hidden.
watch([activeFilter, allPlaces], () => {
  if (
    activePlaceId.value &&
    !filteredPlaces.value.some((p) => p.place_id === activePlaceId.value)
  ) {
    clearSelection()
  }
})

// ── Lifecycle ───────────────────────────────────────────────────────────
onMounted(async () => {
  const coords = await getUserCoordinates()
  userLat.value = coords.lat
  userLng.value = coords.lng
  isFallback.value = coords.isFallback
  await loadPlaces()
})
</script>

<style scoped>
.eco-page {
  position: relative;
  min-height: 100vh;
  color: var(--color-text);
  font-family: 'Inter', system-ui, -apple-system, Arial, sans-serif;
  overflow-x: hidden;
  background: transparent;
}

.eco-page__main {
  position: relative;
  z-index: 1;
  padding-bottom: 60px;
}

/* ── Mobile tab toggle ───────────────────────────────────────────── */
.eco-page__tabs {
  display: none;
  gap: 8px;
  padding: 16px 20px 0;
  max-width: 1320px;
  margin: 0 auto;
}

.eco-tab {
  flex: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px 14px;
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid var(--color-kh-glass-border);
  border-radius: var(--radius-pill);
  color: var(--color-text-muted);
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  font-family: inherit;
  transition: background 160ms var(--motion-entrance), color 160ms var(--motion-entrance);
}

.eco-tab--active {
  background: var(--color-primary);
  color: var(--color-primary-text);
  border-color: var(--color-primary);
}

/* ── Split section — full-bleed map surface ───────────────────────── */
/* Edge-to-edge so the map is the dominant surface, not a thumbnail.
   Height fills the rest of the viewport once the user scrolls past the
   hero and the filter bar sticks to the navbar. */
.eco-page__split {
  position: relative;
  max-width: none;
  margin: 24px 0 0;
  padding: 0 16px;
  display: grid;
  grid-template-columns: minmax(0, 1.85fr) minmax(380px, 1fr);
  gap: 16px;
  /* Filter bar (~118px) + sticky navbar (~76px) ≈ 194 → leave 10px breath. */
  height: calc(100vh - 204px);
  min-height: 640px;
}

.eco-page__map,
.eco-page__list {
  height: 100%;
  min-height: 540px;
}

.eco-page__status {
  max-width: 1320px;
  margin: 16px auto 0;
  padding: 12px 24px;
  font-size: 13px;
  text-align: center;
}

.eco-page__status--error {
  color: #b53236;
}

/* ── Responsive ───────────────────────────────────────────────────── */
@media (max-width: 1024px) {
  .eco-page__tabs { display: flex; }

  .eco-page__split {
    grid-template-columns: 1fr;
    padding: 0 20px;
    height: auto;
    min-height: 0;
    max-height: none;
    margin-top: 12px;
  }

  .eco-page__map,
  .eco-page__list {
    display: none;
    height: 75vh;
    min-height: 480px;
  }

  .eco-page__map[data-active="true"],
  .eco-page__list[data-active="true"] {
    display: block;
  }
}
</style>
