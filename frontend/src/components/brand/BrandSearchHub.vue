<template>
  <section class="search-hub">
    <span class="search-hub__index" aria-hidden="true">02</span>

    <div class="search-hub__head">
      <p ref="eyebrowRef" class="search-hub__eyebrow">
        STEP 02 · PICK YOUR BRANDS
      </p>
      <AnimatedHeading
        as="h1"
        class="search-hub__title"
        :stagger="0.07"
        :delay="0.1"
      >
        Pick up to 3 brands<br />to compare.
      </AnimatedHeading>
      <p ref="subRef" class="search-hub__sub">
        Type any clothing brand or click a suggestion below. Use the X on a chip to remove.
      </p>
    </div>

    <!-- ── Tag input row ─────────────────────────────────────────── -->
    <div ref="inputRowRef" class="search-hub__input-row">
      <BrandTagInput v-model="selected" :max="3" />
      <button
        type="button"
        class="search-hub__compare-cta is-burst-host"
        :disabled="selected.length === 0"
        @click="$emit('compare', selected)"
      >
        <CtaBurst />
        <CtaFlip>
          {{ selected.length === 0 ? 'Add a brand' : `Compare ${selected.length}` }}
          <ArrowRight :size="18" :stroke-width="2.5" />
        </CtaFlip>
      </button>
    </div>

    <!-- ── Carousel ──────────────────────────────────────────────── -->
    <div ref="carouselWrapRef" class="search-hub__carousel-wrap">
      <BrandCarousel
        :items="suggestions"
        :selected-ids="selectedIds"
        :pool="companies.length"
        :is-loading="isLoading && suggestions.length === 0"
        @pick="onPick"
        @refresh="reroll"
      />
    </div>

    <!-- ── Back to intro ─────────────────────────────────────────── -->
    <button type="button" class="search-hub__back" @click="$emit('back')">
      <ArrowLeft :size="14" :stroke-width="2.5" />
      Back to overview
    </button>
  </section>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { ArrowLeft, ArrowRight } from 'lucide-vue-next'
import BrandTagInput from './BrandTagInput.vue'
import BrandCarousel from './BrandCarousel.vue'
import AnimatedHeading from '../AnimatedHeading.vue'
import CtaBurst from '../CtaBurst.vue'
import CtaFlip from '../CtaFlip.vue'
import { useReveal } from '../../motion/useReveal'

const eyebrowRef = ref(null)
const subRef = ref(null)
const inputRowRef = ref(null)
const carouselWrapRef = ref(null)
useReveal(eyebrowRef, { mode: 'char', stagger: 0.022, duration: 0.5 })
useReveal(subRef, { mode: 'fade-blur', y: 40, delay: 0.25 })
useReveal(inputRowRef, { mode: 'fade-up', y: 24, delay: 0.4 })
useReveal(carouselWrapRef, { mode: 'fade-up', y: 28, delay: 0.55 })

const props = defineProps({
  modelValue: { type: Array, default: () => [] },
  // Companies are owned by the parent (BrandSearchView) so the carousel
  // and the leaderboard share the same dataset and we don't refetch.
  companies: { type: Array, default: () => [] },
  isLoading: { type: Boolean, default: false },
})
const emit = defineEmits(['update:modelValue', 'compare', 'back'])

const selected = ref([...props.modelValue])
watch(selected, (val) => emit('update:modelValue', val), { deep: true })
watch(() => props.modelValue, (val) => {
  if (val.length !== selected.value.length) selected.value = [...val]
})

const selectedIds = computed(() => selected.value.map((s) => s.company_id))

// 8 random brands per visit. Re-sampled whenever the user enters this
// view (BrandSearchView re-mounts the hub via the v-if/v-else state
// machine), and whenever Shuffle is pressed.
const SUGGESTION_COUNT = 8
const suggestions = ref([])

function reroll() {
  suggestions.value = sampleN(props.companies, SUGGESTION_COUNT)
}

// Sample as soon as the parent's companies list arrives.
watch(
  () => props.companies,
  (list) => {
    if (list.length > 0 && suggestions.value.length === 0) reroll()
  },
  { immediate: true },
)

function sampleN(arr, n) {
  const copy = [...arr]
  for (let i = copy.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[copy[i], copy[j]] = [copy[j], copy[i]]
  }
  return copy.slice(0, n)
}

function onPick(item) {
  if (selected.value.length >= 3) return
  if (selected.value.some((s) => s.company_id === item.company_id)) return
  selected.value = [
    ...selected.value,
    {
      company_id: item.company_id,
      company_name: item.company_name,
      overall_score: item.overall_score,
      score_label: item.score_label,
      logo: `https://img.logo.dev/${guessDomain(item.company_name)}?token=pk_LbFI27UJRDWnSoDCC_4GYA&size=40`,
    },
  ]
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

// Re-sample on every mount — entering Page 2 always shows fresh picks.
onMounted(() => {
  if (props.companies.length > 0) reroll()
})
</script>

<style scoped>
.search-hub {
  position: relative;
  padding: 120px 48px 80px;
  max-width: 1200px;
  margin: 0 auto;
}

.search-hub__index {
  position: absolute;
  top: 96px;
  left: 36px;
  font-size: 200px;
  font-weight: 900;
  line-height: 0.8;
  letter-spacing: -0.04em;
  color: var(--color-primary);
  opacity: 0.08;
  pointer-events: none;
  z-index: 1;
  user-select: none;
}

.search-hub__head {
  position: relative;
  z-index: 2;
  margin-bottom: 36px;
}

.search-hub__eyebrow {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--color-primary-text);
  margin: 0 0 12px;
}

.search-hub__title {
  font-size: clamp(2.4rem, 5vw, 4rem);
  font-weight: 900;
  line-height: 0.96;
  letter-spacing: -0.02em;
  color: var(--color-text);
  margin: 0 0 14px;
  text-wrap: balance;
}

.search-hub__sub {
  font-size: 16px;
  color: var(--color-text-muted);
  line-height: 1.55;
  margin: 0;
  max-width: 580px;
}

.search-hub__input-row {
  position: relative;
  z-index: 3;
  display: flex;
  gap: 14px;
  align-items: stretch;
  margin-bottom: 56px;
}

.search-hub__input-row > :first-child {
  flex: 1;
}

.search-hub__compare-cta {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 0 28px;
  font-size: 15px;
  font-weight: 800;
  color: var(--color-primary-text);
  background: var(--color-primary);
  border: none;
  border-radius: var(--radius-pill);
  cursor: pointer;
  white-space: nowrap;
  flex-shrink: 0;
  transition: transform 200ms var(--motion-entrance), box-shadow 200ms var(--motion-entrance), opacity 200ms var(--motion-entrance);
}

.search-hub__compare-cta:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 28px rgba(22, 51, 0, 0.22);
}

.search-hub__compare-cta:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  background: rgba(22, 51, 0, 0.12);
  color: var(--color-text-faint);
}

.search-hub__carousel-wrap {
  position: relative;
  z-index: 2;
}

.search-hub__back {
  margin-top: 56px;
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
}

.search-hub__back:hover {
  background: rgba(159, 232, 112, 0.18);
  color: var(--color-primary-text);
}

@media (max-width: 768px) {
  .search-hub { padding: 80px 20px 60px; }
  .search-hub__index { display: none; }
  .search-hub__input-row { flex-direction: column; }
  .search-hub__compare-cta { padding: 14px 24px; justify-content: center; }
}
</style>
