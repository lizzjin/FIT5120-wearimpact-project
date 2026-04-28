<template>
  <div class="leaderboard">
    <div class="leaderboard__head">
      <div class="leaderboard__head-text">
        <h2 class="leaderboard__title">Full leaderboard</h2>
        <p class="leaderboard__sub">{{ total }} brands · sorted by overall score</p>
      </div>
      <div class="leaderboard__filter">
        <span class="leaderboard__filter-label">Show</span>
        <select v-model="filter" class="leaderboard__filter-select">
          <option value="all">All tiers</option>
          <option value="great">Great only</option>
          <option value="goodplus">Good &amp; Great</option>
          <option value="poor">Below Average &amp; Avoid</option>
        </select>
      </div>
    </div>

    <div v-if="isLoading" class="leaderboard__loading">
      <div v-for="n in 8" :key="n" class="leaderboard__row leaderboard__row--skeleton">
        <span class="sk sk-rank"></span>
        <span class="sk sk-avatar"></span>
        <span class="sk sk-name"></span>
        <span class="sk sk-pill"></span>
        <span class="sk sk-score"></span>
      </div>
    </div>

    <ul v-else class="leaderboard__list">
      <li
        v-for="row in pagedRows"
        :key="row.company_id"
        class="leaderboard__row"
        :class="{ 'leaderboard__row--highlight': highlightIds.includes(row.company_id) }"
      >
        <button type="button" class="leaderboard__btn" @click="$emit('open', row.company_id)">
          <span class="leaderboard__rank">#{{ row.rank }}</span>
          <span class="leaderboard__avatar" :style="logoErr[row.company_id] ? { background: avatarBg(row.company_name) } : {}">
            <img
              v-if="!logoErr[row.company_id]"
              :src="logoFor(row.company_name)"
              alt=""
              class="leaderboard__logo"
              @error="logoErr[row.company_id] = true"
            />
            <span v-else>{{ row.company_name.charAt(0).toUpperCase() }}</span>
          </span>
          <span class="leaderboard__name">{{ row.company_name }}</span>
          <span
            class="leaderboard__pill"
            :style="{ background: labelBg(row.score_label), color: labelColor(row.score_label) }"
          >{{ row.score_label }}</span>
          <span class="leaderboard__score">
            <span class="leaderboard__score-num">{{ row.overall_score }}</span>
            <span class="leaderboard__score-of">/100</span>
          </span>
          <ChevronRight :size="16" :stroke-width="2" class="leaderboard__chev" />
        </button>
      </li>
    </ul>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="leaderboard__pager">
      <button
        type="button"
        class="leaderboard__pager-btn"
        :disabled="page === 1"
        @click="goPage(page - 1)"
      >
        <ChevronLeft :size="14" /> Prev
      </button>
      <span class="leaderboard__pager-info">{{ page }} / {{ totalPages }}</span>
      <button
        type="button"
        class="leaderboard__pager-btn"
        :disabled="page === totalPages"
        @click="goPage(page + 1)"
      >
        Next <ChevronRight :size="14" />
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive, ref, watch } from 'vue'
import { ChevronLeft, ChevronRight } from 'lucide-vue-next'

const props = defineProps({
  rows: { type: Array, default: () => [] },        // already sorted with rank field
  highlightIds: { type: Array, default: () => [] },
  isLoading: { type: Boolean, default: false },
  pageSize: { type: Number, default: 14 },
})
defineEmits(['open'])

const page = ref(1)
const filter = ref('all')

const filteredRows = computed(() => {
  if (filter.value === 'all') return props.rows
  if (filter.value === 'great')   return props.rows.filter((r) => r.score_label === 'Great')
  if (filter.value === 'goodplus') return props.rows.filter((r) => ['Great', 'Good'].includes(r.score_label))
  if (filter.value === 'poor')   return props.rows.filter((r) => ['Below Average', 'Avoid'].includes(r.score_label))
  return props.rows
})

const total = computed(() => filteredRows.value.length)
const totalPages = computed(() => Math.max(1, Math.ceil(total.value / props.pageSize)))

const pagedRows = computed(() => {
  const start = (page.value - 1) * props.pageSize
  return filteredRows.value.slice(start, start + props.pageSize)
})

watch(filter, () => { page.value = 1 })
watch(() => props.rows, () => { page.value = 1 })

function goPage(p) {
  if (p < 1 || p > totalPages.value) return
  page.value = p
}

const logoErr = reactive({})

function logoFor(name) {
  return `https://img.logo.dev/${guessDomain(name)}?token=pk_LbFI27UJRDWnSoDCC_4GYA&size=40`
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

defineExpose({ goPage })
</script>

<style scoped>
.leaderboard {
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid var(--color-kh-glass-border);
  border-radius: 24px;
  padding: 28px 28px 24px;
}

.leaderboard__head {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 14px;
  margin-bottom: 20px;
}

.leaderboard__title {
  font-size: 22px;
  font-weight: 900;
  color: var(--color-text);
  letter-spacing: -0.01em;
  margin: 0 0 4px;
}

.leaderboard__sub {
  font-size: 13px;
  color: var(--color-text-faint);
  margin: 0;
}

.leaderboard__filter {
  display: flex;
  align-items: center;
  gap: 10px;
}

.leaderboard__filter-label {
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  font-weight: 700;
  color: var(--color-text-faint);
}

.leaderboard__filter-select {
  padding: 8px 14px;
  font-size: 13px;
  font-weight: 600;
  font-family: inherit;
  color: var(--color-text);
  background: white;
  border: 1px solid var(--color-kh-glass-border);
  border-radius: var(--radius-pill);
  cursor: pointer;
  outline: none;
}

.leaderboard__filter-select:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(159, 232, 112, 0.22);
}

.leaderboard__list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.leaderboard__row {
  border-radius: 12px;
  transition: background 160ms var(--motion-entrance), box-shadow 160ms var(--motion-entrance);
}

.leaderboard__row:hover {
  background: rgba(159, 232, 112, 0.10);
}

.leaderboard__row--highlight {
  background: rgba(159, 232, 112, 0.18);
  box-shadow: inset 0 0 0 1px var(--color-primary);
}

.leaderboard__btn {
  width: 100%;
  display: grid;
  grid-template-columns: 56px 36px minmax(0, 1fr) auto auto 16px;
  align-items: center;
  gap: 14px;
  padding: 10px 14px;
  background: transparent;
  border: none;
  cursor: pointer;
  font-family: inherit;
  text-align: left;
}

.leaderboard__rank {
  font-size: 14px;
  font-weight: 800;
  color: var(--color-text-faint);
  letter-spacing: 0.04em;
}

.leaderboard__avatar {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: white;
  border: 1px solid var(--color-kh-glass-border);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  font-size: 14px;
  font-weight: 800;
  color: var(--color-text);
}

.leaderboard__logo {
  width: 100%; height: 100%;
  object-fit: contain;
  padding: 4px;
}

.leaderboard__name {
  font-size: 14px;
  font-weight: 700;
  color: var(--color-text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.leaderboard__pill {
  font-size: 11px;
  font-weight: 700;
  padding: 3px 10px;
  border-radius: var(--radius-pill);
  letter-spacing: 0.04em;
  white-space: nowrap;
}

.leaderboard__score {
  display: flex;
  align-items: baseline;
  gap: 2px;
  font-variant-numeric: tabular-nums;
}

.leaderboard__score-num {
  font-size: 18px;
  font-weight: 900;
  color: var(--color-text);
  letter-spacing: -0.01em;
}

.leaderboard__score-of {
  font-size: 11px;
  color: var(--color-text-faint);
}

.leaderboard__chev {
  color: var(--color-text-faint);
  transition: transform 160ms var(--motion-entrance);
}

.leaderboard__btn:hover .leaderboard__chev {
  transform: translateX(3px);
  color: var(--color-primary-text);
}

/* Skeleton */
.sk {
  background: linear-gradient(90deg, #ede5d4 25%, #e3d9c2 50%, #ede5d4 75%);
  background-size: 200% 100%;
  animation: shimmer 1.4s infinite;
  border-radius: 8px;
}
.sk-rank   { width: 32px; height: 14px; }
.sk-avatar { width: 36px; height: 36px; border-radius: 10px; }
.sk-name   { width: 60%; height: 14px; }
.sk-pill   { width: 80px; height: 18px; border-radius: 999px; }
.sk-score  { width: 44px; height: 16px; }
.leaderboard__row--skeleton {
  display: grid;
  grid-template-columns: 56px 36px minmax(0, 1fr) auto auto;
  gap: 14px;
  align-items: center;
  padding: 10px 14px;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* Pager */
.leaderboard__pager {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 24px;
}

.leaderboard__pager-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: white;
  border: 1px solid var(--color-kh-glass-border);
  border-radius: var(--radius-pill);
  font-family: inherit;
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-muted);
  cursor: pointer;
  transition: background 160ms var(--motion-entrance);
}

.leaderboard__pager-btn:hover:not(:disabled) {
  background: rgba(159, 232, 112, 0.18);
  color: var(--color-primary-text);
}

.leaderboard__pager-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.leaderboard__pager-info {
  font-size: 13px;
  font-weight: 700;
  color: var(--color-text-muted);
  font-variant-numeric: tabular-nums;
}

@media (max-width: 768px) {
  .leaderboard { padding: 20px 16px 18px; }
  .leaderboard__btn {
    grid-template-columns: 32px 36px minmax(0, 1fr) auto;
    gap: 10px;
  }
  .leaderboard__pill, .leaderboard__chev { display: none; }
}
</style>
