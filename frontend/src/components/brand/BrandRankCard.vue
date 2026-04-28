<template>
  <article class="rank-card" :style="{ '--accent': labelColor, '--accent-bg': labelBg }">
    <div class="rank-card__top">
      <div
        class="rank-card__avatar"
        :style="logoErr ? { background: avatarBg } : {}"
      >
        <img
          v-if="!logoErr"
          :src="logoSrc"
          :alt="brand.company_name"
          class="rank-card__logo"
          @error="logoErr = true"
        />
        <span v-else>{{ brand.company_name.charAt(0).toUpperCase() }}</span>
      </div>
      <div class="rank-card__name-block">
        <p class="rank-card__name">{{ brand.company_name }}</p>
        <span class="rank-card__pill">{{ brand.score_label }}</span>
      </div>
      <button
        type="button"
        class="rank-card__remove"
        :aria-label="`Remove ${brand.company_name} from comparison`"
        @click="$emit('remove', brand.company_id)"
      >
        <X :size="14" :stroke-width="2.5" />
      </button>
    </div>

    <p class="rank-card__rank-line">
      Ranked
      <span class="rank-card__rank-num">#{{ rank }}</span>
      <span class="rank-card__rank-of">of {{ total }}</span>
    </p>

    <!-- Distribution bar with marker -->
    <div class="rank-card__bar" :title="`Top ${percentile}%`">
      <div class="rank-card__bar-track">
        <div class="rank-card__bar-fill" :style="{ width: percentFromTop + '%' }"></div>
      </div>
      <div class="rank-card__bar-marker" :style="{ left: percentFromTop + '%' }">
        <span class="rank-card__bar-tip"></span>
      </div>
      <div class="rank-card__bar-axis">
        <span>Top</span>
        <span>Bottom</span>
      </div>
    </div>

    <div class="rank-card__score-row">
      <span class="rank-card__score">{{ brand.overall_score }}</span>
      <span class="rank-card__score-of">/100</span>
      <button
        type="button"
        class="rank-card__view"
        @click="$emit('view', brand.company_id)"
      >
        View detail
        <ArrowRight :size="14" :stroke-width="2.5" />
      </button>
    </div>
  </article>
</template>

<script setup>
import { computed, ref } from 'vue'
import { ArrowRight, X } from 'lucide-vue-next'

const props = defineProps({
  brand: { type: Object, required: true },
  rank: { type: Number, required: true },
  total: { type: Number, required: true },
})
defineEmits(['remove', 'view'])

const logoErr = ref(false)

// Position on the bar from left (0% = #1) to right (100% = last).
const percentFromTop = computed(() => {
  if (props.total <= 1) return 0
  return ((props.rank - 1) / (props.total - 1)) * 100
})
const percentile = computed(() => Math.round(percentFromTop.value))

const LABEL_COLORS = {
  'Great': '#054d28', 'Good': '#16a34a', "It's a Start": '#ca8a04',
  'Below Average': '#ea580c', 'Avoid': '#d03238',
}
const LABEL_BG = {
  'Great': '#e2f6d5', 'Good': '#ecfccb', "It's a Start": '#fef9c3',
  'Below Average': '#ffedd5', 'Avoid': '#fee2e2',
}
const labelColor = computed(() => LABEL_COLORS[props.brand.score_label] || '#868685')
const labelBg = computed(() => LABEL_BG[props.brand.score_label] || '#e8ebe6')

const logoSrc = computed(() => {
  return `https://img.logo.dev/${guessDomain(props.brand.company_name)}?token=pk_LbFI27UJRDWnSoDCC_4GYA&size=64`
})

const AVATAR_PALETTE = ['#dbeafe', '#e2f6d5', '#fef9c3', '#fce7f3', '#ede9fe', '#ffedd5']
const avatarBg = computed(() => AVATAR_PALETTE[props.brand.company_name.charCodeAt(0) % AVATAR_PALETTE.length])

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
</script>

<style scoped>
.rank-card {
  --accent: var(--color-text);
  --accent-bg: rgba(255, 255, 255, 0.85);
  position: relative;
  background: rgba(255, 255, 255, 0.92);
  border: 1px solid var(--color-kh-glass-border);
  border-top: 4px solid var(--accent);
  border-radius: 18px;
  padding: 22px 22px 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  box-shadow: 0 12px 30px rgba(22, 51, 0, 0.06);
}

.rank-card__top {
  display: flex;
  align-items: center;
  gap: 12px;
}

.rank-card__avatar {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: white;
  border: 1px solid var(--color-kh-glass-border);
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 800;
  color: var(--color-text);
  overflow: hidden;
}

.rank-card__logo {
  width: 100%; height: 100%;
  object-fit: contain;
  padding: 5px;
}

.rank-card__name-block {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
  min-width: 0;
}

.rank-card__name {
  font-size: 16px;
  font-weight: 800;
  color: var(--color-text);
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.rank-card__pill {
  display: inline-block;
  align-self: flex-start;
  padding: 3px 10px;
  background: var(--accent-bg);
  color: var(--accent);
  border-radius: var(--radius-pill);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.04em;
}

.rank-card__remove {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: transparent;
  border: 1px solid var(--color-kh-glass-border);
  color: var(--color-text-faint);
  cursor: pointer;
  flex-shrink: 0;
  transition: background 160ms var(--motion-entrance), color 160ms var(--motion-entrance);
}

.rank-card__remove:hover {
  background: rgba(208, 50, 56, 0.12);
  color: #d03238;
  border-color: rgba(208, 50, 56, 0.4);
}

.rank-card__rank-line {
  font-size: 13px;
  color: var(--color-text-muted);
  margin: 0;
  display: flex;
  align-items: baseline;
  gap: 6px;
}

.rank-card__rank-num {
  font-size: 32px;
  font-weight: 900;
  color: var(--accent);
  letter-spacing: -0.02em;
}

.rank-card__rank-of {
  font-size: 13px;
  color: var(--color-text-faint);
}

/* Distribution bar */
.rank-card__bar {
  position: relative;
  padding-top: 4px;
}

.rank-card__bar-track {
  height: 6px;
  background: linear-gradient(to right, #054d28, #16a34a 25%, #ca8a04 50%, #ea580c 75%, #d03238);
  border-radius: 999px;
  overflow: hidden;
  opacity: 0.85;
}

.rank-card__bar-fill {
  height: 100%;
  background: rgba(22, 51, 0, 0.12);
}

.rank-card__bar-marker {
  position: absolute;
  top: 0;
  width: 14px;
  height: 14px;
  background: var(--color-warm-cream);
  border: 3px solid var(--accent);
  border-radius: 50%;
  transform: translate(-50%, -2px);
  box-shadow: 0 2px 8px rgba(22, 51, 0, 0.2);
}

.rank-card__bar-tip {
  display: none;
}

.rank-card__bar-axis {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
  font-size: 10px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--color-text-faint);
  font-weight: 700;
}

.rank-card__score-row {
  display: flex;
  align-items: baseline;
  gap: 4px;
  padding-top: 6px;
  border-top: 1px solid rgba(22, 51, 0, 0.08);
}

.rank-card__score {
  font-size: 28px;
  font-weight: 900;
  color: var(--accent);
  letter-spacing: -0.02em;
}

.rank-card__score-of {
  font-size: 13px;
  color: var(--color-text-faint);
  flex: 1;
}

.rank-card__view {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  background: transparent;
  border: 1px solid var(--accent);
  color: var(--accent);
  border-radius: var(--radius-pill);
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  font-family: inherit;
  transition: background 180ms var(--motion-entrance);
}

.rank-card__view:hover {
  background: var(--accent-bg);
}
</style>
