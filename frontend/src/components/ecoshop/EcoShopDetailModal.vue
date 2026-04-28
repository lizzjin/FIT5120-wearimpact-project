<template>
  <DialogRoot :open="open" @update:open="(v) => $emit('update:open', v)">
    <DialogPortal>
      <DialogOverlay class="es-modal-backdrop" />
      <DialogContent class="es-modal" aria-describedby="es-detail-desc">
        <DialogTitle class="sr-only">Eco-shop detail</DialogTitle>
        <DialogDescription id="es-detail-desc" class="sr-only">
          Address, hours and contact information for the selected location.
        </DialogDescription>

        <DialogClose class="es-modal__close" aria-label="Close">
          <X :size="18" :stroke-width="2" />
        </DialogClose>

        <div class="es-modal__scroll">
          <!-- Header -->
          <div
            v-if="place"
            class="es-modal__header"
            :style="{ '--type-color': typeMeta.color }"
          >
            <span class="es-modal__icon">
              <component :is="typeMeta.icon" :size="22" :stroke-width="2" />
            </span>
            <div class="es-modal__title-block">
              <span class="es-modal__type">{{ typeMeta.label }}</span>
              <h2 class="es-modal__name">{{ place.name }}</h2>
              <p class="es-modal__distance">
                <Navigation2 :size="14" :stroke-width="2.4" />
                {{ place.distance_km }} km from you
              </p>
            </div>
          </div>

          <!-- Loading skeleton -->
          <div v-if="isLoading" class="es-modal__skeleton">
            <div class="es-modal__skeleton-line" style="width: 70%"></div>
            <div class="es-modal__skeleton-line" style="width: 90%"></div>
            <div class="es-modal__skeleton-line" style="width: 60%"></div>
            <div class="es-modal__skeleton-line" style="width: 80%"></div>
          </div>

          <!-- Detail content -->
          <div v-else-if="detail" class="es-modal__body">
            <div v-if="detail.address" class="es-modal__row">
              <MapPin :size="18" :stroke-width="2" class="es-modal__row-icon" />
              <div>
                <p class="es-modal__row-label">Address</p>
                <p class="es-modal__row-value">{{ detail.address }}</p>
              </div>
            </div>

            <div v-if="openingHours.length > 0" class="es-modal__row">
              <Clock :size="18" :stroke-width="2" class="es-modal__row-icon" />
              <div>
                <p class="es-modal__row-label">Opening hours</p>
                <ul class="es-modal__hours">
                  <li v-for="(line, i) in openingHours" :key="i">{{ line }}</li>
                </ul>
              </div>
            </div>

            <div v-if="detail.phone" class="es-modal__row">
              <Phone :size="18" :stroke-width="2" class="es-modal__row-icon" />
              <div>
                <p class="es-modal__row-label">Phone</p>
                <a class="es-modal__row-link" :href="`tel:${detail.phone}`">{{ detail.phone }}</a>
              </div>
            </div>

            <div v-if="detail.website" class="es-modal__row">
              <Globe :size="18" :stroke-width="2" class="es-modal__row-icon" />
              <div>
                <p class="es-modal__row-label">Website</p>
                <a
                  class="es-modal__row-link"
                  :href="detail.website"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {{ shortUrl(detail.website) }}
                </a>
              </div>
            </div>

            <a
              v-if="place"
              class="es-modal__directions"
              :href="directionsUrl"
              target="_blank"
              rel="noopener noreferrer"
            >
              Open in Google Maps
              <ArrowUpRight :size="16" :stroke-width="2.4" />
            </a>
          </div>

          <!-- Error state -->
          <div v-else-if="error" class="es-modal__error">
            <AlertCircle :size="20" :stroke-width="1.8" />
            <p>{{ error }}</p>
          </div>
        </div>
      </DialogContent>
    </DialogPortal>
  </DialogRoot>
</template>

<script setup>
import { computed, watch } from 'vue'
import { DialogClose, DialogContent, DialogDescription, DialogOverlay, DialogPortal, DialogRoot, DialogTitle } from 'radix-vue'
import { AlertCircle, ArrowUpRight, Clock, Globe, HandHeart, MapPin, Navigation2, Phone, Recycle, ShoppingBag, X } from 'lucide-vue-next'

const props = defineProps({
  open: { type: Boolean, default: false },
  place: { type: Object, default: null },          // summary from list
  detail: { type: Object, default: null },         // full backend payload
  isLoading: { type: Boolean, default: false },
  error: { type: String, default: '' },
})
defineEmits(['update:open'])

const TYPE_META = {
  second_hand_shop: { label: 'Second-hand shop', icon: ShoppingBag, color: '#9fe870' },
  donation_point:   { label: 'Donation point',   icon: HandHeart,   color: '#163300' },
  recycling:        { label: 'Recycling point',  icon: Recycle,     color: '#c9a458' },
}

const typeMeta = computed(() =>
  TYPE_META[props.place?.type] || { label: 'Eco-shop', icon: MapPin, color: '#163300' },
)

const openingHours = computed(() => {
  const raw = props.detail?.opening_hours
  if (!raw) return []
  if (Array.isArray(raw)) return raw
  if (typeof raw === 'string') return raw.split('\n').filter(Boolean)
  return []
})

const directionsUrl = computed(() => {
  if (!props.place) return ''
  const q = `${props.place.lat},${props.place.lng}`
  return `https://www.google.com/maps/dir/?api=1&destination=${encodeURIComponent(q)}`
})

function shortUrl(url) {
  try {
    const u = new URL(url)
    return u.hostname.replace(/^www\./, '') + (u.pathname !== '/' ? u.pathname : '')
  } catch {
    return url
  }
}

watch(() => props.open, (v) => {
  document.body.style.overflow = v ? 'hidden' : ''
})
</script>

<style scoped>
.sr-only {
  position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px;
  overflow: hidden; clip: rect(0, 0, 0, 0); white-space: nowrap; border-width: 0;
}

.es-modal-backdrop {
  position: fixed; inset: 0;
  background: rgba(22, 51, 0, 0.4);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  z-index: 200;
  animation: fadeIn 200ms ease;
}

.es-modal {
  position: fixed; top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  width: calc(100% - 48px);
  max-width: 520px;
  max-height: 88vh;
  background: var(--color-warm-cream);
  border-radius: 24px;
  overflow: hidden;
  display: flex; flex-direction: column;
  z-index: 201;
  box-shadow: 0 30px 60px rgba(22, 51, 0, 0.28);
  animation: modalScaleIn 280ms cubic-bezier(0.22, 1, 0.36, 1);
}

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes modalScaleIn {
  from { opacity: 0; transform: translate(-50%, -50%) scale(0.95); }
  to   { opacity: 1; transform: translate(-50%, -50%) scale(1); }
}

.es-modal__close {
  position: absolute; top: 16px; right: 16px;
  width: 36px; height: 36px;
  border-radius: 50%;
  border: 1px solid var(--color-kh-glass-border);
  background: var(--color-warm-cream);
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  color: var(--color-text-subtle);
  z-index: 1;
  transition: background 0.15s, color 0.15s;
}

.es-modal__close:hover {
  background: rgba(159, 232, 112, 0.22);
  color: var(--color-primary-text);
}

.es-modal__scroll {
  overflow-y: auto;
  padding: 28px 28px 28px;
  display: flex; flex-direction: column; gap: 24px;
}

/* Header */
.es-modal__header {
  --type-color: var(--color-primary);
  display: flex;
  gap: 14px;
  align-items: flex-start;
  padding: 18px;
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid var(--color-kh-glass-border);
  border-left: 4px solid var(--type-color);
  border-radius: 14px;
}

.es-modal__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: var(--type-color);
  color: var(--color-primary-text);
  flex-shrink: 0;
}

.es-modal__header[style*="#163300"] .es-modal__icon {
  color: var(--color-warm-cream);
}

.es-modal__type {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--color-text-faint);
}

.es-modal__name {
  font-size: 20px;
  font-weight: 900;
  color: var(--color-text);
  letter-spacing: -0.01em;
  margin: 4px 0 6px;
  line-height: 1.2;
}

.es-modal__distance {
  font-size: 12px;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  color: var(--color-primary-text);
  font-weight: 700;
  margin: 0;
}

/* Body */
.es-modal__body {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.es-modal__row {
  display: flex;
  gap: 14px;
  align-items: flex-start;
}

.es-modal__row-icon {
  color: var(--color-primary-text);
  margin-top: 2px;
  flex-shrink: 0;
}

.es-modal__row-label {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--color-text-faint);
  margin: 0 0 4px;
}

.es-modal__row-value {
  font-size: 14px;
  color: var(--color-text);
  line-height: 1.5;
  margin: 0;
}

.es-modal__row-link {
  font-size: 14px;
  color: var(--color-primary-text);
  font-weight: 600;
  text-decoration: none;
  border-bottom: 1px solid rgba(22, 51, 0, 0.2);
  transition: border-color 160ms;
}

.es-modal__row-link:hover {
  border-color: var(--color-primary);
}

.es-modal__hours {
  list-style: none;
  margin: 0;
  padding: 0;
  font-size: 13px;
  color: var(--color-text-muted);
  line-height: 1.65;
}

.es-modal__directions {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  align-self: flex-start;
  padding: 12px 22px;
  background: var(--color-primary);
  color: var(--color-primary-text);
  border-radius: var(--radius-pill);
  font-size: 14px;
  font-weight: 700;
  text-decoration: none;
  transition: transform 200ms var(--motion-entrance), box-shadow 200ms var(--motion-entrance);
  margin-top: 4px;
}

.es-modal__directions:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 24px rgba(22, 51, 0, 0.22);
}

/* Skeleton */
.es-modal__skeleton {
  display: flex; flex-direction: column; gap: 12px;
}

.es-modal__skeleton-line {
  height: 14px;
  border-radius: 7px;
  background: linear-gradient(90deg, #ede5d4 25%, #e3d9c2 50%, #ede5d4 75%);
  background-size: 200% 100%;
  animation: es-shimmer 1.4s infinite;
}

@keyframes es-shimmer {
  0%   { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* Error */
.es-modal__error {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 18px;
  background: rgba(208, 50, 56, 0.06);
  border: 1px solid rgba(208, 50, 56, 0.2);
  border-radius: 12px;
  color: #b53236;
  font-size: 13px;
}

.es-modal__error p { margin: 0; }
</style>
