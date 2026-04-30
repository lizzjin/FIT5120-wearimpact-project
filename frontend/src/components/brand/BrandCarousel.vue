<template>
  <div class="brand-carousel">
    <div class="brand-carousel__head">
      <p class="brand-carousel__eyebrow">{{ pool > 0 ? `SUGGESTED FROM ${pool} BRANDS` : 'LOADING SUGGESTIONS…' }}</p>
      <button
        type="button"
        class="brand-carousel__refresh"
        :disabled="isLoading"
        @click="$emit('refresh')"
      >
        <RefreshCcw :size="14" :stroke-width="2" />
        Shuffle
      </button>
    </div>

    <div
      v-if="isLoading && items.length === 0"
      class="brand-carousel__loading"
    >
      <span
        v-for="n in 5"
        :key="n"
        class="brand-carousel__loading-card"
      ></span>
    </div>

    <div
      v-else
      class="brand-carousel__viewport"
      @mouseenter="paused = true"
      @mouseleave="paused = false"
    >
      <div
        class="brand-carousel__track"
        :class="{ 'brand-carousel__track--paused': paused }"
      >
        <!-- Loop the list twice for a seamless marquee -->
        <button
          v-for="(item, i) in doubledItems"
          :key="`${item.company_id}-${i}`"
          type="button"
          class="brand-suggestion"
          :class="{ 'brand-suggestion--selected': isSelected(item.company_id) }"
          @click="$emit('pick', item)"
        >
          <!-- Header row: logo + name + category -->
          <span class="brand-suggestion__head">
            <span
              class="brand-suggestion__avatar"
              :style="logoErr[item.company_id] ? { background: avatarBg(item.company_name) } : {}"
            >
              <img
                v-if="!logoErr[item.company_id]"
                :src="logoFor(item.company_name)"
                alt=""
                class="brand-suggestion__logo"
                @error="logoErr[item.company_id] = true"
              />
              <span v-else class="brand-suggestion__letter">
                {{ item.company_name.charAt(0).toUpperCase() }}
              </span>
            </span>
            <span class="brand-suggestion__name-block">
              <span class="brand-suggestion__name">{{ item.company_name }}</span>
              <span class="brand-suggestion__category">
                {{ item.product_category === 'footwear' ? 'Footwear' : 'Apparel' }}
              </span>
            </span>
          </span>

          <!-- Rank line -->
          <span v-if="item.rank && pool > 1" class="brand-suggestion__rank">
            Ranked <strong>{{ item.rank }}</strong> of {{ pool }}
          </span>

          <!-- Mini distribution bar — neutral track, marker shows position -->
          <span v-if="item.rank && pool > 1" class="brand-suggestion__bar-wrap">
            <span class="brand-suggestion__bar">
              <span class="brand-suggestion__bar-track"></span>
              <span
                class="brand-suggestion__bar-marker"
                :style="{ left: ((item.rank - 1) / (pool - 1)) * 100 + '%' }"
              ></span>
            </span>
            <span class="brand-suggestion__bar-axis">
              <span>Top</span>
              <span>Bottom</span>
            </span>
          </span>

          <!-- Score + label -->
          <span class="brand-suggestion__foot">
            <span class="brand-suggestion__score-num">
              {{ item.overall_score }}<span class="brand-suggestion__score-of">/100</span>
            </span>
            <span
              class="brand-suggestion__pill"
              :style="{ background: labelBg(item.score_label), color: labelColor(item.score_label) }"
            >{{ item.score_label }}</span>
          </span>

          <span v-if="isSelected(item.company_id)" class="brand-suggestion__check" aria-hidden="true">
            <Check :size="14" :stroke-width="3" />
          </span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive, ref } from 'vue'
import { Check, RefreshCcw } from 'lucide-vue-next'

const props = defineProps({
  items: { type: Array, default: () => [] },
  selectedIds: { type: Array, default: () => [] },
  isLoading: { type: Boolean, default: false },
  pool: { type: Number, default: 0 },          // total companies in dataset
})
defineEmits(['pick', 'refresh'])

const paused = ref(false)
const logoErr = reactive({})

const doubledItems = computed(() => [...props.items, ...props.items])

function isSelected(id) { return props.selectedIds.includes(id) }

function logoFor(name) {
  return `https://img.logo.dev/${guessDomain(name)}?token=pk_LbFI27UJRDWnSoDCC_4GYA&size=48`
}

function guessDomain(name) {
  const overrides = {
    'H&M': 'hm.com', 'H&M Group': 'hm.com', 'Inditex': 'inditex.com',
    'Levi Strauss & Co': 'levi.com', 'PVH Corp': 'pvh.com', 'VF Corporation': 'vfc.com',
    'Hanesbrands': 'hanes.com', 'Fast Retailing': 'fastretailing.com', 'Kering': 'kering.com',
    'LVMH': 'lvmh.com', 'Adidas': 'adidas.com', 'Nike': 'nike.com', 'Puma': 'puma.com',
    'Patagonia': 'patagonia.com',
  }
  if (overrides[name]) return overrides[name]
  return name.toLowerCase().replace(/[^a-z0-9]/g, '') + '.com'
}

const AVATAR_PALETTE = ['#dbeafe', '#e2f6d5', '#fef9c3', '#fce7f3', '#ede9fe', '#ffedd5']
function avatarBg(name) {
  return AVATAR_PALETTE[name.charCodeAt(0) % AVATAR_PALETTE.length]
}

const LABEL_COLORS = {
  'Great': '#054d28', 'Good': '#16a34a', "It's a Start": '#ca8a04',
  'Below Average': '#ea580c', 'Avoid': '#d03238',
}
const LABEL_BG = {
  'Great': '#e2f6d5', 'Good': '#ecfccb', "It's a Start": '#fef9c3',
  'Below Average': '#ffedd5', 'Avoid': '#fee2e2',
}
function labelColor(l) { return LABEL_COLORS[l] || '#868685' }
function labelBg(l) { return LABEL_BG[l] || '#e8ebe6' }
</script>

<style scoped>
.brand-carousel {
  width: 100%;
}

.brand-carousel__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}

.brand-carousel__eyebrow {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--color-primary-text);
  margin: 0;
  opacity: 0.7;
}

.brand-carousel__refresh {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid var(--color-kh-glass-border);
  border-radius: var(--radius-pill);
  font-size: 12px;
  font-weight: 700;
  color: var(--color-primary-text);
  cursor: pointer;
  transition: background 180ms var(--motion-entrance);
}

.brand-carousel__refresh:hover:not(:disabled) {
  background: rgba(159, 232, 112, 0.22);
}

.brand-carousel__refresh:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.brand-carousel__loading {
  display: flex;
  gap: 14px;
  overflow: hidden;
}

.brand-carousel__loading-card {
  flex: 0 0 320px;
  height: 196px;
  border-radius: 18px;
  background: linear-gradient(90deg, #ede5d4 25%, #e3d9c2 50%, #ede5d4 75%);
  background-size: 200% 100%;
  animation: brand-shimmer 1.4s infinite;
}

@keyframes brand-shimmer {
  0%   { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.brand-carousel__viewport {
  position: relative;
  overflow: hidden;
  /* fade edges so cards melt in/out */
  mask-image: linear-gradient(to right, transparent, black 4%, black 96%, transparent);
  -webkit-mask-image: linear-gradient(to right, transparent, black 4%, black 96%, transparent);
}

.brand-carousel__track {
  display: flex;
  gap: 14px;
  width: max-content;
  /* 60s for a calm, "browse" pace — too fast feels like ticker tape. */
  animation: brand-marquee 60s linear infinite;
}

.brand-carousel__track--paused {
  animation-play-state: paused;
}

@keyframes brand-marquee {
  from { transform: translateX(0); }
  to   { transform: translateX(-50%); }
}

/* Suggestion card — bigger, info-rich, monochrome on cream. */
.brand-suggestion {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding: 20px 22px 18px;
  width: 320px;
  flex-shrink: 0;
  background: rgba(255, 255, 255, 0.92);
  border: 1px solid var(--color-kh-glass-border);
  border-radius: 18px;
  cursor: pointer;
  text-align: left;
  font-family: inherit;
  transition:
    transform 240ms var(--motion-entrance),
    box-shadow 240ms var(--motion-entrance),
    border-color 240ms var(--motion-entrance);
}

.brand-suggestion:hover {
  transform: translateY(-4px);
  box-shadow: 0 18px 36px rgba(22, 51, 0, 0.12);
}

.brand-suggestion--selected {
  background: rgba(159, 232, 112, 0.16);
  box-shadow: 0 0 0 1px var(--color-primary), 0 14px 32px rgba(22, 51, 0, 0.10);
}

/* Header row */
.brand-suggestion__head {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-suggestion__avatar {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: white;
  border: 1px solid var(--color-kh-glass-border);
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.brand-suggestion__logo {
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 5px;
}

.brand-suggestion__letter {
  font-size: 18px;
  font-weight: 800;
  color: var(--color-text);
}

.brand-suggestion__name-block {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
  flex: 1;
}

.brand-suggestion__name {
  font-size: 16px;
  font-weight: 800;
  color: var(--color-text);
  letter-spacing: -0.01em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.brand-suggestion__category {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--color-text-faint);
}

/* Rank line */
.brand-suggestion__rank {
  font-size: 12px;
  color: var(--color-text-muted);
  letter-spacing: 0.02em;
  margin-top: -4px;
}

.brand-suggestion__rank strong {
  font-size: 16px;
  font-weight: 900;
  color: var(--color-primary-text);
  letter-spacing: -0.01em;
}

/* Mini distribution bar — neutral cream track, dark-green marker.
   No traffic-light gradient: tier signal lives on the label pill below. */
.brand-suggestion__bar-wrap {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.brand-suggestion__bar {
  position: relative;
  display: block;
  height: 5px;
}

.brand-suggestion__bar-track {
  position: absolute;
  inset: 0;
  background: rgba(22, 51, 0, 0.10);
  border-radius: 999px;
}

.brand-suggestion__bar-marker {
  position: absolute;
  top: 50%;
  width: 12px;
  height: 12px;
  background: var(--color-primary);
  border: 2px solid var(--color-primary-text);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  box-shadow: 0 2px 6px rgba(22, 51, 0, 0.18);
}

.brand-suggestion__bar-axis {
  display: flex;
  justify-content: space-between;
  font-size: 9px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--color-text-faint);
  font-weight: 700;
}

/* Footer row: score + label pill */
.brand-suggestion__foot {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 10px;
  border-top: 1px solid rgba(22, 51, 0, 0.08);
}

.brand-suggestion__score-num {
  font-size: 26px;
  font-weight: 900;
  color: var(--color-primary-text);
  letter-spacing: -0.02em;
  line-height: 1;
}

.brand-suggestion__score-of {
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-faint);
  margin-left: 2px;
}

.brand-suggestion__pill {
  font-size: 11px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: var(--radius-pill);
  letter-spacing: 0.04em;
  white-space: nowrap;
}

.brand-suggestion__check {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: var(--color-primary);
  color: var(--color-primary-text);
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
</style>
