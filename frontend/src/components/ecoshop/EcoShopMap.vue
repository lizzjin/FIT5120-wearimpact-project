<template>
  <!-- data-lenis-prevent: Mapbox's built-in scroll-to-zoom handler needs the
       raw wheel event to control map zoom. Without this, Lenis intercepts
       every wheel tick over the map and scrolls the page instead, so zoom
       never fires and the user feels like the map "won't let them zoom".
       Mapbox itself preventDefaults the wheel internally, so dropping out
       of Lenis here doesn't fall through to native page scroll either. -->
  <div class="es-map" ref="mapWrapRef" data-lenis-prevent>
    <div ref="mapContainer" class="es-map__canvas"></div>

    <div v-if="errorMessage" class="es-map__error">
      <AlertCircle :size="20" :stroke-width="1.8" />
      <span>{{ errorMessage }}</span>
    </div>

    <button
      v-if="!errorMessage"
      type="button"
      class="es-map__recenter"
      title="Recentre on me"
      @click="recenterOnUser"
    >
      <Navigation2 :size="14" :stroke-width="2.4" />
    </button>
  </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'
import { useReveal } from '../../motion/useReveal'

const mapWrapRef = ref(null)
useReveal(mapWrapRef, { mode: 'fade-up', y: 28, duration: 0.9, delay: 0.15 })
import { AlertCircle, Navigation2 } from 'lucide-vue-next'

const props = defineProps({
  userLat: { type: Number, default: null },
  userLng: { type: Number, default: null },
  places: { type: Array, default: () => [] },
  radiusKm: { type: Number, default: 5 },
  activePlaceId: { type: String, default: null },
  hoveredPlaceId: { type: String, default: null },
  // Route request: { profile: 'driving'|'walking'|'cycling', start:[lng,lat], end:[lng,lat] } | null.
  // Setting to null clears the route.
  routeRequest: { type: Object, default: null },
})
const emit = defineEmits(['select-place', 'route-info', 'route-error'])

const mapContainer = ref(null)
const errorMessage = ref('')

const TYPE_COLOURS = {
  second_hand_shop: '#9fe870',
  donation_point:   '#163300',
  recycling:        '#c9a458',
}

const TYPE_LABEL = {
  second_hand_shop: 'Second-hand',
  donation_point:   'Donation',
  recycling:        'Recycling',
}

let mapInstance = null
let userMarker = null
let hoverPopup = null
const placeMarkers = new Map()

const RADIUS_SOURCE_ID = 'es-radius-circle'
const RADIUS_FILL_LAYER = 'es-radius-fill'
const RADIUS_LINE_LAYER = 'es-radius-line'

const ROUTE_SOURCE_ID = 'es-route-source'
const ROUTE_GLOW_LAYER = 'es-route-glow'
const ROUTE_MAIN_LAYER = 'es-route-main'
const ROUTE_DASH_LAYER = 'es-route-dash'

const mapboxToken = import.meta.env.VITE_MAPBOX_ACCESS_TOKEN || ''
const mapboxStyleUrl =
  import.meta.env.VITE_MAPBOX_STYLE_URL || 'mapbox://styles/mapbox/streets-v12'

// ── Animated dash sequences per travel mode ─────────────────────────────
const DASH_SEQUENCES = {
  driving: [[0, 4, 3], [0.4, 4, 2.6], [0.8, 4, 2.2], [1.2, 4, 1.8], [1.6, 4, 1.4], [2, 4, 1], [2.4, 4, 0.6], [2.8, 4, 0.2]],
  walking: [[0, 2.2, 2.2], [0.3, 2.2, 1.9], [0.6, 2.2, 1.6], [0.9, 2.2, 1.3], [1.2, 2.2, 1], [1.5, 2.2, 0.7]],
  cycling: [[0, 5, 3], [0.5, 5, 2.5], [1, 5, 2], [1.5, 5, 1.5], [2, 5, 1]],
}

// Per-mode colour palette — kept in the cream + lime + dark-green +
// honey-tan family so the route always reads as "ours", but each mode
// has a unique main + dash combo so the user can tell them apart at a
// glance even if the dash rhythm is missed.
const ROUTE_PALETTE = {
  driving: { main: '#163300', dash: '#9fe870', glow: '#9fe870' },  // dark line + lime flecks
  walking: { main: '#9fe870', dash: '#163300', glow: '#cdffad' },  // inverted — lime line + dark dashes
  cycling: { main: '#c9a458', dash: '#163300', glow: '#e8d3a0' },  // warm tan — used for TRANSIT mode
}

let routeAnimFrame = null
let lastDashTimestamp = 0
let dashIndex = 0
let activeDashSequence = DASH_SEQUENCES.driving
let activeRouteProfile = 'driving'

// ── Map init ─────────────────────────────────────────────────────────────
function initMap() {
  if (!mapContainer.value) return
  if (!mapboxToken) {
    errorMessage.value = `The map can't load right now — the list on the right still works while we look into it.`
    return
  }
  if (props.userLat == null || props.userLng == null) return

  mapboxgl.accessToken = mapboxToken
  mapInstance = new mapboxgl.Map({
    container: mapContainer.value,
    style: mapboxStyleUrl,
    center: [props.userLng, props.userLat],
    zoom: 13.5,
    attributionControl: false,
  })

  mapInstance.addControl(new mapboxgl.NavigationControl({ showCompass: false }), 'top-right')
  mapInstance.addControl(new mapboxgl.AttributionControl({ compact: true }), 'bottom-right')

  mapInstance.on('load', () => {
    drawUserMarker()
    drawRadiusCircle()
    ensureRouteLayers()
    drawPlaceMarkers()
    if (props.routeRequest) drawRoute(props.routeRequest)
  })
}

// ── User pin ────────────────────────────────────────────────────────────
function drawUserMarker() {
  if (!mapInstance || props.userLat == null) return
  if (userMarker) {
    userMarker.setLngLat([props.userLng, props.userLat])
    return
  }
  const el = document.createElement('div')
  el.className = 'es-user-pin'
  el.innerHTML = `<span class="es-user-pin__dot"></span><span class="es-user-pin__pulse"></span>`
  userMarker = new mapboxgl.Marker({ element: el, anchor: 'center' })
    .setLngLat([props.userLng, props.userLat])
    .addTo(mapInstance)
}

// ── Radius circle ───────────────────────────────────────────────────────
function buildCircleGeoJson(lat, lng, radiusKm, points = 64) {
  const coords = []
  const distanceX = radiusKm / (111.320 * Math.cos((lat * Math.PI) / 180))
  const distanceY = radiusKm / 110.574
  for (let i = 0; i < points; i += 1) {
    const theta = (i / points) * (2 * Math.PI)
    coords.push([lng + distanceX * Math.cos(theta), lat + distanceY * Math.sin(theta)])
  }
  coords.push(coords[0])
  return { type: 'Feature', geometry: { type: 'Polygon', coordinates: [coords] }, properties: {} }
}

function drawRadiusCircle() {
  if (!mapInstance || !mapInstance.isStyleLoaded()) return
  const data = buildCircleGeoJson(props.userLat, props.userLng, props.radiusKm)
  if (mapInstance.getSource(RADIUS_SOURCE_ID)) {
    mapInstance.getSource(RADIUS_SOURCE_ID).setData(data)
    return
  }
  mapInstance.addSource(RADIUS_SOURCE_ID, { type: 'geojson', data })
  mapInstance.addLayer({
    id: RADIUS_FILL_LAYER,
    type: 'fill',
    source: RADIUS_SOURCE_ID,
    paint: { 'fill-color': '#9fe870', 'fill-opacity': 0.10 },
  })
  mapInstance.addLayer({
    id: RADIUS_LINE_LAYER,
    type: 'line',
    source: RADIUS_SOURCE_ID,
    paint: {
      'line-color': '#163300',
      'line-width': 1.5,
      'line-opacity': 0.45,
      'line-dasharray': [2, 3],
    },
  })
}

// ── Place markers ───────────────────────────────────────────────────────
function buildPinElement(type, isActive) {
  const colour = TYPE_COLOURS[type] || '#163300'
  const cream = '#f6f0e6'
  const iconColour = type === 'donation_point' ? cream : '#163300'
  const el = document.createElement('div')
  el.className = `es-pin${isActive ? ' es-pin--active' : ''}`
  el.style.setProperty('--pin-colour', colour)
  // Inner wrapper hosts hover/active transforms — keeping the root free
  // of any `transition: transform` so Mapbox's per-frame translate3d
  // (used to reposition markers on zoom) is never animated.
  el.innerHTML = `
    <div class="es-pin__inner">
      <svg viewBox="0 0 32 40" width="32" height="40" aria-hidden="true">
        <path d="M16 2 C 8 2 3 8 3 16 C 3 24 16 38 16 38 C 16 38 29 24 29 16 C 29 8 24 2 16 2 Z"
          fill="${colour}" stroke="#163300" stroke-width="1.6" />
        <circle cx="16" cy="16" r="6.5" fill="${cream}" stroke="${colour}" stroke-width="0.5" />
      </svg>
      <span class="es-pin__icon" style="color: ${iconColour}">${getIconSvg(type)}</span>
    </div>
  `
  return el
}

function getIconSvg(type) {
  const ICONS = {
    second_hand_shop: '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>',
    donation_point:   '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M11 14h2a2 2 0 1 0 0-4h-3c-.6 0-1.1.2-1.4.6L3 16"/><path d="m7 20 1.6-1.4c.3-.4.8-.6 1.4-.6h4c1.1 0 2.1-.4 2.8-1.2l4.6-4.4a2 2 0 0 0-2.75-2.91l-4.2 3.9"/><path d="m2 15 6 6"/><path d="M19.5 8.5c.7-.7 1.5-1.6 1.5-2.7A2.7 2.7 0 0 0 16 4a2.7 2.7 0 0 0-5 1.8c0 1.2.8 2 1.5 2.8L16 12Z"/></svg>',
    recycling:        '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M7 19H4.815a1.83 1.83 0 0 1-1.57-.881 1.785 1.785 0 0 1-.004-1.784L7.196 9.5"/><path d="M11 19h8.203a1.83 1.83 0 0 0 1.556-.89 1.784 1.784 0 0 0 0-1.775l-1.226-2.12"/><path d="m14 16-3 3 3 3"/><path d="M8.293 13.596 7.196 9.5 3.1 10.598"/><path d="m9.344 5.811 1.093-1.892A1.83 1.83 0 0 1 11.985 3a1.784 1.784 0 0 1 1.546.888l3.943 6.843"/><path d="m13.378 9.633 4.096 1.098 1.097-4.096"/></svg>',
  }
  return ICONS[type] || ''
}

function drawPlaceMarkers() {
  if (!mapInstance) return

  const nextIds = new Set(props.places.map((p) => p.place_id))
  for (const [id, entry] of placeMarkers) {
    if (!nextIds.has(id)) {
      entry.marker.remove()
      placeMarkers.delete(id)
    }
  }

  props.places.forEach((place) => {
    if (placeMarkers.has(place.place_id)) {
      const entry = placeMarkers.get(place.place_id)
      entry.marker.setLngLat([place.lng, place.lat])
      return
    }
    const el = buildPinElement(place.type, place.place_id === props.activePlaceId)
    el.addEventListener('click', (e) => {
      e.stopPropagation()
      emit('select-place', place)
    })
    // Hover tooltip — show place name + distance + type label on pointerenter
    // so users get the location's identity without having to click. Closes
    // on pointerleave; we also defer to mouseleave for a touch of tolerance
    // when the cursor exits via a sub-pixel gap.
    el.addEventListener('mouseenter', () => showHoverPopup(place))
    el.addEventListener('mouseleave', () => hideHoverPopup())
    const marker = new mapboxgl.Marker({ element: el, anchor: 'bottom' })
      .setLngLat([place.lng, place.lat])
      .addTo(mapInstance)
    placeMarkers.set(place.place_id, { marker, element: el, type: place.type })
  })
}

// ── Hover popup ─────────────────────────────────────────────────────────
function escapeHtml(s) {
  return String(s ?? '').replace(/[&<>"']/g, (c) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
  }[c]))
}

function renderPopupHtml(place) {
  const typeKey = place.type
  const typeLabel = TYPE_LABEL[typeKey] || 'Place'
  const dist = place.distance_km != null ? `${place.distance_km} km away` : ''
  const name = escapeHtml(place.name)
  return `
    <div class="es-pin-popup__inner">
      <span class="es-pin-popup__type es-pin-popup__type--${typeKey}">${typeLabel}</span>
      <span class="es-pin-popup__name">${name}</span>
      ${dist ? `<span class="es-pin-popup__dist">${dist}</span>` : ''}
    </div>
  `
}

function showHoverPopup(place) {
  if (!mapInstance) return
  if (!hoverPopup) {
    hoverPopup = new mapboxgl.Popup({
      closeButton: false,
      closeOnClick: false,
      closeOnMove: false,
      // Sit above the pin tip; pin element is 28px tall with anchor=bottom.
      offset: 30,
      className: 'es-pin-popup',
      anchor: 'bottom',
      maxWidth: '240px',
    })
  }
  hoverPopup
    .setLngLat([place.lng, place.lat])
    .setHTML(renderPopupHtml(place))
    .addTo(mapInstance)
}

function hideHoverPopup() {
  if (hoverPopup) hoverPopup.remove()
}

function setActiveMarker(id) {
  for (const [pid, entry] of placeMarkers) {
    entry.element.classList.toggle('es-pin--active', pid === id)
  }
}

function setHoveredMarker(id) {
  for (const [pid, entry] of placeMarkers) {
    entry.element.classList.toggle('es-pin--hover', pid === id && pid !== props.activePlaceId)
  }
}

function recenterOnUser() {
  if (mapInstance && props.userLat != null) {
    mapInstance.flyTo({ center: [props.userLng, props.userLat], zoom: 13.5, duration: 600 })
  }
}

// ── Route layers / drawing / dash animation ─────────────────────────────
function ensureRouteLayers() {
  if (!mapInstance) return
  if (mapInstance.getSource(ROUTE_SOURCE_ID)) return

  const palette = ROUTE_PALETTE[activeRouteProfile] || ROUTE_PALETTE.driving

  mapInstance.addSource(ROUTE_SOURCE_ID, {
    type: 'geojson',
    data: { type: 'FeatureCollection', features: [] },
  })

  // Outer glow — soft halo behind the line for legibility on busy maps.
  mapInstance.addLayer({
    id: ROUTE_GLOW_LAYER,
    type: 'line',
    source: ROUTE_SOURCE_ID,
    layout: { 'line-join': 'round', 'line-cap': 'round' },
    paint: {
      'line-color': palette.glow,
      'line-width': 12,
      'line-opacity': 0.25,
      'line-blur': 2,
    },
  })

  // Solid base line — high contrast on light cream map.
  mapInstance.addLayer({
    id: ROUTE_MAIN_LAYER,
    type: 'line',
    source: ROUTE_SOURCE_ID,
    layout: { 'line-join': 'round', 'line-cap': 'round' },
    paint: {
      'line-color': palette.main,
      'line-width': 5,
      'line-opacity': 0.92,
    },
  })

  // Animated dash on top — flowing pattern signals direction of travel.
  mapInstance.addLayer({
    id: ROUTE_DASH_LAYER,
    type: 'line',
    source: ROUTE_SOURCE_ID,
    layout: { 'line-join': 'round', 'line-cap': 'round' },
    paint: {
      'line-color': palette.dash,
      'line-width': 3,
      'line-opacity': 0.95,
      'line-dasharray': activeDashSequence[0],
    },
  })
}

function buildRouteFeature(coords) {
  return {
    type: 'FeatureCollection',
    features: [{ type: 'Feature', geometry: { type: 'LineString', coordinates: coords }, properties: {} }],
  }
}

function clearRouteOnMap() {
  if (!mapInstance || !mapInstance.getSource(ROUTE_SOURCE_ID)) return
  mapInstance.getSource(ROUTE_SOURCE_ID).setData({ type: 'FeatureCollection', features: [] })
  stopRouteAnimation()
}

function fitRouteBounds(coords) {
  if (!mapInstance || coords.length === 0) return
  const bounds = coords.reduce(
    (b, c) => b.extend(c),
    new mapboxgl.LngLatBounds(coords[0], coords[0]),
  )
  mapInstance.fitBounds(bounds, { padding: 80, duration: 700, maxZoom: 15.4 })
}

function stopRouteAnimation() {
  if (routeAnimFrame) {
    cancelAnimationFrame(routeAnimFrame)
    routeAnimFrame = null
  }
}

function startRouteAnimation() {
  stopRouteAnimation()
  if (!mapInstance) return
  lastDashTimestamp = performance.now()
  dashIndex = 0
  const tick = (now) => {
    if (!mapInstance || !mapInstance.getLayer(ROUTE_DASH_LAYER)) return
    if (now - lastDashTimestamp > 70) {
      dashIndex = (dashIndex + 1) % activeDashSequence.length
      mapInstance.setPaintProperty(ROUTE_DASH_LAYER, 'line-dasharray', activeDashSequence[dashIndex])
      lastDashTimestamp = now
    }
    routeAnimFrame = requestAnimationFrame(tick)
  }
  routeAnimFrame = requestAnimationFrame(tick)
}

function setRouteVisualStyle(profile) {
  if (!mapInstance || !mapInstance.getLayer(ROUTE_DASH_LAYER)) return
  const seq = DASH_SEQUENCES[profile] || DASH_SEQUENCES.driving
  activeDashSequence = seq
  activeRouteProfile = profile

  const palette = ROUTE_PALETTE[profile] || ROUTE_PALETTE.driving

  // Repaint all three layers so the colour scheme matches the mode.
  mapInstance.setPaintProperty(ROUTE_GLOW_LAYER, 'line-color', palette.glow)
  mapInstance.setPaintProperty(ROUTE_MAIN_LAYER, 'line-color', palette.main)
  mapInstance.setPaintProperty(ROUTE_DASH_LAYER, 'line-color', palette.dash)

  // Mode-specific line widths so the route reads differently for walk vs drive.
  const widths = { driving: 5, walking: 3.5, cycling: 4 }
  mapInstance.setPaintProperty(ROUTE_MAIN_LAYER, 'line-width', widths[profile] ?? 5)
}

function formatDistance(meters = 0) {
  if (meters < 1000) return `${Math.round(meters)} m`
  return `${(meters / 1000).toFixed(1)} km`
}

function formatDuration(seconds = 0) {
  const mins = Math.round(seconds / 60)
  if (mins < 60) return `${mins} min`
  const h = Math.floor(mins / 60)
  const m = mins % 60
  return m === 0 ? `${h} h` : `${h} h ${m} min`
}

async function fetchDirections(profile, start, end) {
  const url = `https://api.mapbox.com/directions/v5/mapbox/${profile}/${start[0]},${start[1]};${end[0]},${end[1]}?geometries=geojson&overview=full&steps=false&access_token=${mapboxToken}`
  const res = await fetch(url)
  if (!res.ok) throw new Error(`Directions request failed (HTTP ${res.status})`)
  const data = await res.json()
  return data.routes?.[0] || null
}

async function drawRoute(req) {
  if (!mapInstance) return
  ensureRouteLayers()
  try {
    const profile = req.profile
    const route = await fetchDirections(profile, req.start, req.end)
    if (!route) {
      emit('route-error', 'No route found for this location.')
      return
    }
    const coords = route.geometry?.coordinates || []
    if (coords.length === 0) {
      emit('route-error', 'No route found for this location.')
      return
    }

    setRouteVisualStyle(profile)
    mapInstance.getSource(ROUTE_SOURCE_ID).setData(buildRouteFeature(coords))
    fitRouteBounds(coords)
    startRouteAnimation()

    const leg = route.legs?.[0]
    emit('route-info', {
      distance: formatDistance(leg?.distance ?? route.distance),
      duration: formatDuration(leg?.duration ?? route.duration),
    })
  } catch (err) {
    emit('route-error', err.message || 'Could not generate directions.')
  }
}

// ── Watchers ────────────────────────────────────────────────────────────
watch(
  () => [props.userLat, props.userLng],
  ([lat, lng]) => {
    if (!mapInstance && lat != null && lng != null) { initMap(); return }
    if (mapInstance && lat != null && lng != null) {
      drawUserMarker()
      drawRadiusCircle()
      mapInstance.flyTo({ center: [lng, lat], zoom: 13.5, duration: 600 })
    }
  },
)

watch(() => props.places, () => drawPlaceMarkers(), { deep: true })

watch(() => props.radiusKm, () => drawRadiusCircle())

watch(
  () => props.activePlaceId,
  (id) => {
    setActiveMarker(id)
    if (id && mapInstance) {
      const place = props.places.find((p) => p.place_id === id)
      if (place) {
        mapInstance.flyTo({ center: [place.lng, place.lat], zoom: 14.2, duration: 600 })
      }
    }
  },
)

watch(() => props.hoveredPlaceId, (id) => setHoveredMarker(id))

watch(
  () => props.routeRequest,
  (req) => {
    if (!req) {
      clearRouteOnMap()
      return
    }
    drawRoute(req)
  },
  { deep: true },
)

// ── Lifecycle ───────────────────────────────────────────────────────────
onMounted(() => {
  initMap()
})

onBeforeUnmount(() => {
  stopRouteAnimation()
  for (const entry of placeMarkers.values()) entry.marker.remove()
  placeMarkers.clear()
  if (userMarker) userMarker.remove()
  if (hoverPopup) { hoverPopup.remove(); hoverPopup = null }
  if (mapInstance) mapInstance.remove()
  mapInstance = null
})
</script>

<style scoped>
.es-map {
  position: relative;
  width: 100%;
  height: 100%;
  border-radius: 18px;
  overflow: hidden;
  border: 1px solid var(--color-kh-glass-border);
  background: rgba(255, 255, 255, 0.5);
  /* Belt-and-braces with data-lenis-prevent on the wrapper: if a wheel ever
     lands on the wrapper edge instead of the Mapbox canvas, stop it from
     chaining up to <html>. Mapbox already preventDefaults wheel on its
     canvas, so this only matters in the few-px gutter. */
  overscroll-behavior: contain;
}

.es-map__canvas {
  width: 100%;
  height: 100%;
  min-height: 540px;
}

.es-map__error {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  background: rgba(255, 255, 255, 0.92);
  color: var(--color-text-muted);
  font-size: 14px;
  padding: 24px;
  text-align: center;
}

.es-map__recenter {
  position: absolute;
  bottom: 18px;
  right: 18px;
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: var(--color-warm-cream);
  border: 1px solid var(--color-kh-glass-border);
  color: var(--color-primary-text);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 14px rgba(22, 51, 0, 0.14);
  transition: transform 160ms var(--motion-entrance), background 160ms var(--motion-entrance);
}

.es-map__recenter:hover {
  background: rgba(159, 232, 112, 0.32);
  transform: translateY(-1px);
}
</style>

<style>
/* ── Hover popup ─────────────────────────────────────────────────────────
   Mapbox injects popup DOM directly under .mapboxgl-popup at the map
   container root, so scoped CSS can't reach it — these rules live in the
   unscoped block. `.es-pin-popup` is the className we pass to the Popup
   constructor; we use it to target only OUR popup and not anything
   third-party libs might add later. */
.es-pin-popup.mapboxgl-popup {
  /* Pointer-events: none on the wrapper so the tooltip doesn't intercept
     clicks aimed at the pin underneath. Mapbox's content/tip elements
     re-enable pointer events by default, but we don't want either. */
  pointer-events: none;
  z-index: 5;
}

.es-pin-popup .mapboxgl-popup-content {
  background: var(--color-soft-cream, #faf7f2);
  color: var(--color-soft-ink, #0e0f0c);
  border: 1px solid var(--color-soft-line-strong, rgba(14, 15, 12, 0.14));
  border-radius: 14px;
  padding: 10px 14px;
  box-shadow: 0 10px 24px rgba(14, 15, 12, 0.12), 0 2px 6px rgba(14, 15, 12, 0.06);
  font-family: 'Inter', system-ui, sans-serif;
}

/* Tip — the little triangle pointing at the pin. Mapbox draws it via
   bordered pseudo-elements; we match the popup's cream fill so the seam
   between content and tip is invisible. */
.es-pin-popup .mapboxgl-popup-tip {
  border-top-color: var(--color-soft-cream, #faf7f2);
  border-bottom-color: var(--color-soft-cream, #faf7f2);
}

.es-pin-popup__inner {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 140px;
}

.es-pin-popup__type {
  align-self: flex-start;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  padding: 3px 8px;
  border-radius: 999px;
  margin-bottom: 2px;
}
.es-pin-popup__type--second_hand_shop {
  background: rgba(159, 232, 112, 0.32);
  color: #163300;
}
.es-pin-popup__type--donation_point {
  background: rgba(22, 51, 0, 0.10);
  color: #163300;
}
.es-pin-popup__type--recycling {
  background: rgba(201, 164, 88, 0.22);
  color: #6b4e10;
}

.es-pin-popup__name {
  font-size: 13.5px;
  font-weight: 700;
  letter-spacing: -0.01em;
  line-height: 1.3;
  color: var(--color-soft-ink, #0e0f0c);
}

.es-pin-popup__dist {
  font-size: 12px;
  font-weight: 500;
  color: var(--color-soft-ink-soft, #454745);
}

/* Root pin element — Mapbox writes inline transform: translate3d(...) here
   on every zoom frame to keep the pin glued to its lng/lat. NO `transform`
   or `transition: transform` rules may live on this selector or markers
   will visibly drift during wheel-zooms. */
.es-pin {
  width: 32px;
  height: 40px;
  cursor: pointer;
}

.es-pin__inner {
  position: relative;
  width: 100%;
  height: 100%;
  transition: transform 200ms cubic-bezier(0.34, 1.56, 0.64, 1), filter 180ms ease;
  transform-origin: bottom center;
  will-change: transform;
}

.es-pin svg {
  display: block;
  filter: drop-shadow(0 4px 6px rgba(22, 51, 0, 0.25));
}

.es-pin__icon {
  position: absolute;
  top: 9px;
  left: 50%;
  transform: translateX(-50%);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 14px;
  height: 14px;
  pointer-events: none;
}

.es-pin:hover .es-pin__inner,
.es-pin--hover .es-pin__inner {
  transform: scale(1.12) translateY(-2px);
}
.es-pin:hover,
.es-pin--hover { z-index: 2; }

.es-pin--active .es-pin__inner {
  transform: scale(1.22) translateY(-3px);
}
.es-pin--active { z-index: 3; }

.es-pin--active svg {
  filter: drop-shadow(0 6px 14px rgba(22, 51, 0, 0.35));
}

.es-user-pin {
  position: relative;
  width: 18px;
  height: 18px;
  pointer-events: none;
}

.es-user-pin__dot {
  position: absolute;
  inset: 4px;
  border-radius: 50%;
  background: var(--color-primary, #9fe870);
  border: 2px solid #163300;
  z-index: 2;
}

.es-user-pin__pulse {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: rgba(159, 232, 112, 0.55);
  animation: es-user-pulse 2.4s ease-out infinite;
}

@keyframes es-user-pulse {
  0%   { transform: scale(0.6); opacity: 0.85; }
  100% { transform: scale(2.4); opacity: 0; }
}

.mapboxgl-ctrl-top-right .mapboxgl-ctrl {
  margin: 12px 12px 0 0 !important;
  border-radius: 12px !important;
  overflow: hidden;
  box-shadow: 0 4px 14px rgba(22, 51, 0, 0.1) !important;
}
</style>
