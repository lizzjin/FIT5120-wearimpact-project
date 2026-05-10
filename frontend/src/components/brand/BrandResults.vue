<template>
  <section class="results">
    <button type="button" class="results__back" @click="$emit('back')">
      <ArrowLeft :size="14" :stroke-width="2.5" />
      Back to search
    </button>

    <div class="results__head">
      <p ref="eyebrowRef" class="results__eyebrow">STEP 03 · YOUR RESULTS</p>
      <AnimatedHeading
        as="h1"
        class="results__title"
        :stagger="0.06"
        :delay="0.1"
      >
        Your <span class="results__title-num">{{ selected.length }}</span>
        {{ selected.length === 1 ? 'pick' : 'picks' }}
        vs. <span class="results__title-num">{{ total > 0 ? total : '…' }}</span> companies.
      </AnimatedHeading>
      <p ref="subRef" class="results__sub">
        Each card shows where your pick lands in the full ranking. Click any row below to dig in.
      </p>
    </div>

    <!-- ── Selected rank cards ──────────────────────────────────── -->
    <div v-if="selected.length === 0" class="results__empty">
      <p>You removed all picks. Go back and pick at least one brand.</p>
      <button type="button" class="results__empty-btn" @click="$emit('back')">
        <ArrowLeft :size="14" :stroke-width="2.5" />
        Back to search
      </button>
    </div>
    <div v-else-if="ranked.length === 0" class="results__loading-cards" :data-count="selected.length">
      <div v-for="brand in selected" :key="brand.company_id" class="results__loading-card">
        <span class="results__loading-name">{{ brand.company_name }}</span>
        <span class="results__loading-hint">Computing rank…</span>
      </div>
    </div>
    <div v-else class="results__rank-grid" :data-count="selected.length">
      <BrandRankCard
        v-for="brand in selected"
        :key="brand.company_id"
        :brand="brand"
        :rank="rankFor(brand.company_id)"
        :total="total"
        @remove="(id) => $emit('remove-brand', id)"
        @view="(id) => $emit('open', id)"
      />
    </div>

    <!-- ── Full leaderboard ─────────────────────────────────────── -->
    <BrandLeaderboard
      v-if="ranked.length > 0"
      :rows="ranked"
      :highlight-ids="selectedIds"
      :is-loading="false"
      @open="(id) => $emit('open', id)"
    />
    <BrandLeaderboard
      v-else
      :rows="[]"
      :highlight-ids="[]"
      :is-loading="true"
      @open="() => {}"
    />
  </section>
</template>

<script setup>
import { computed, ref } from 'vue'
import { ArrowLeft } from 'lucide-vue-next'
import BrandRankCard from './BrandRankCard.vue'
import BrandLeaderboard from './BrandLeaderboard.vue'
import AnimatedHeading from '../AnimatedHeading.vue'
import { useReveal } from '../../motion/useReveal'

const eyebrowRef = ref(null)
const subRef = ref(null)
useReveal(eyebrowRef, { mode: 'char', stagger: 0.022, duration: 0.5 })
useReveal(subRef, { mode: 'fade-blur', y: 40, delay: 0.25 })

const props = defineProps({
  selected: { type: Array, default: () => [] },     // user picks
  ranked: { type: Array, default: () => [] },       // all 247 rows with rank field
  isLoading: { type: Boolean, default: false },
})
defineEmits(['back', 'remove-brand', 'open'])

const total = computed(() => props.ranked.length)
const selectedIds = computed(() => props.selected.map((s) => s.company_id))

const rankMap = computed(() => {
  const m = new Map()
  for (const r of props.ranked) m.set(r.company_id, r.rank)
  return m
})

function rankFor(id) {
  return rankMap.value.get(id) ?? 0
}
</script>

<style scoped>
.results {
  position: relative;
  padding: 80px 48px 100px;
  max-width: 1200px;
  margin: 0 auto;
}

.results__back {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: transparent;
  border: 1px solid var(--color-kh-glass-border);
  border-radius: var(--radius-pill);
  cursor: pointer;
  font-family: inherit;
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-muted);
  transition: background 180ms var(--motion-entrance), color 180ms var(--motion-entrance);
  margin-bottom: 28px;
}

.results__back:hover {
  background: rgba(159, 232, 112, 0.18);
  color: var(--color-primary-text);
}

.results__head {
  margin-bottom: 36px;
}

.results__eyebrow {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--color-primary-text);
  margin: 0 0 12px;
}

.results__title {
  font-size: clamp(2rem, 4vw, 3.2rem);
  font-weight: 900;
  line-height: 1.05;
  letter-spacing: -0.02em;
  color: var(--color-text);
  margin: 0 0 12px;
  text-wrap: balance;
}

.results__title-num {
  color: var(--color-primary-text);
  font-variant-numeric: tabular-nums;
}

.results__sub {
  font-size: 15px;
  color: var(--color-text-muted);
  line-height: 1.55;
  margin: 0;
  max-width: 580px;
}

.results__rank-grid {
  display: grid;
  gap: 18px;
  margin-bottom: 56px;
}

.results__rank-grid[data-count="1"] { grid-template-columns: minmax(0, 480px); }
.results__rank-grid[data-count="2"] { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.results__rank-grid[data-count="3"] { grid-template-columns: repeat(3, minmax(0, 1fr)); }

.results__empty {
  background: rgba(255, 255, 255, 0.7);
  border: 1px dashed var(--color-kh-glass-border);
  border-radius: 18px;
  padding: 36px;
  text-align: center;
  margin-bottom: 56px;
  color: var(--color-text-muted);
}

.results__empty p {
  margin: 0 0 14px;
  font-size: 14px;
}

.results__empty-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 18px;
  background: var(--color-primary);
  color: var(--color-primary-text);
  border: none;
  border-radius: var(--radius-pill);
  font-family: inherit;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
}

.results__loading-cards {
  display: grid;
  gap: 18px;
  margin-bottom: 56px;
}
.results__loading-cards[data-count="1"] { grid-template-columns: minmax(0, 480px); }
.results__loading-cards[data-count="2"] { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.results__loading-cards[data-count="3"] { grid-template-columns: repeat(3, minmax(0, 1fr)); }

.results__loading-card {
  background: rgba(255, 255, 255, 0.7);
  border: 1px dashed var(--color-kh-glass-border);
  border-radius: 18px;
  padding: 28px 22px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  text-align: center;
}

.results__loading-name {
  font-size: 16px;
  font-weight: 800;
  color: var(--color-text);
}

.results__loading-hint {
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--color-text-faint);
  font-weight: 700;
}

@media (max-width: 1024px) {
  .results__rank-grid[data-count="2"],
  .results__rank-grid[data-count="3"] {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .results { padding: 56px 20px 80px; }
}
</style>
