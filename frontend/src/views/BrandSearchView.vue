<template>
  <div class="brand-page">
    <!-- Unified Wise canvas — same component used on /knowledge to keep
         the cream + drifting blobs + topography aesthetic seamless. -->
    <QuizBackground />

    <Navbar />

    <main class="brand-page__main">
      <Transition name="brand-view" mode="out-in">
        <BrandIntro
          v-if="view === 'intro'"
          key="intro"
          @start="goSearch"
        />
        <BrandSearchHub
          v-else-if="view === 'search'"
          key="search"
          v-model="selected"
          :companies="ranked"
          :is-loading="isCompaniesLoading"
          @compare="onCompare"
          @back="goIntro"
        />
        <BrandResults
          v-else
          key="results"
          :selected="selected"
          :ranked="ranked"
          :is-loading="isCompaniesLoading"
          @back="goSearch"
          @remove-brand="removeBrand"
          @open="openDetail"
        />
      </Transition>
    </main>

    <BrandDetailModal
      :open="modalOpen"
      :detail="detail"
      :is-loading="isDetailLoading"
      @update:open="(v) => { if (!v) closeDetail() }"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import Navbar from '../components/Navbar.vue'
import QuizBackground from '../components/knowledge/QuizBackground.vue'
import BrandIntro from '../components/brand/BrandIntro.vue'
import BrandSearchHub from '../components/brand/BrandSearchHub.vue'
import BrandResults from '../components/brand/BrandResults.vue'
import BrandDetailModal from '../components/brand/BrandDetailModal.vue'
import { fetchAllCompaniesAll, fetchCompanyDetail } from '../services/brandService'

// View state machine: intro → search → results.
// Page entry defaults to 'intro' so users meet the explainer first.
const view = ref('intro')

// Brand picks across the search/results flow. Each entry contains
// company_id, company_name, overall_score, score_label.
const selected = ref([])

// Full company dataset, fetched once at view mount (paged behind the
// scenes because the API caps page_size at 50). Shared with both
// BrandSearchHub (for carousel sampling) and BrandResults (leaderboard).
const companies = ref([])
const isCompaniesLoading = ref(false)

// Ranked variant (sorted by overall_score desc, rank assigned client-side).
const ranked = computed(() => {
  if (companies.value.length === 0) return []
  const sorted = [...companies.value].sort((a, b) => b.overall_score - a.overall_score)
  return sorted.map((r, i) => ({ ...r, rank: i + 1 }))
})

// Detail modal state — shared by Intro CTA flow, search hub picks,
// and leaderboard rows.
const modalOpen = ref(false)
const detail = ref(null)
const isDetailLoading = ref(false)
const detailCache = new Map()

// ── View transitions ──────────────────────────────────────────────
function goIntro() {
  view.value = 'intro'
  scrollTop()
}

function goSearch() {
  view.value = 'search'
  scrollTop()
}

async function onCompare(picks) {
  selected.value = picks
  view.value = 'results'
  scrollTop()
  await ensureCompaniesLoaded()
}

function scrollTop() {
  requestAnimationFrame(() => window.scrollTo({ top: 0, behavior: 'smooth' }))
}

// ── Companies dataset (paged fetch, cached for the session) ───────
// Backend caps page_size at 50, so fetchAllCompaniesAll() pages through
// in parallel and concatenates the result.
async function ensureCompaniesLoaded() {
  if (companies.value.length > 0 || isCompaniesLoading.value) return
  isCompaniesLoading.value = true
  try {
    companies.value = await fetchAllCompaniesAll()
  } catch (err) {
    // eslint-disable-next-line no-console
    console.error('[BrandSearch] failed to fetch companies', err)
    companies.value = []
  } finally {
    isCompaniesLoading.value = false
  }
}

onMounted(() => {
  // Pre-load on mount so carousel + leaderboard are ready before
  // the user navigates to the search/results view.
  ensureCompaniesLoaded()
})

function removeBrand(id) {
  selected.value = selected.value.filter((s) => s.company_id !== id)
}

// ── Detail modal ─────────────────────────────────────────────────
async function openDetail(companyId) {
  modalOpen.value = true
  if (detailCache.has(companyId)) {
    detail.value = detailCache.get(companyId)
    isDetailLoading.value = false
    return
  }
  detail.value = null
  isDetailLoading.value = true
  try {
    const d = await fetchCompanyDetail(companyId)
    detailCache.set(companyId, d)
    detail.value = d
  } catch {
    detail.value = null
  } finally {
    isDetailLoading.value = false
  }
}

function closeDetail() {
  modalOpen.value = false
  // Keep `detail` so the panel content doesn't blank during close transition.
}
</script>

<style scoped>
.brand-page {
  position: relative;
  min-height: 100vh;
  color: var(--color-text);
  font-family: 'Inter', system-ui, -apple-system, Arial, sans-serif;
  overflow-x: hidden;
  /* QuizBackground paints the cream canvas as a fixed full-screen layer. */
  background: transparent;
}

.brand-page__main {
  position: relative;
  z-index: 1;
}

.brand-view-enter-active,
.brand-view-leave-active {
  transition:
    opacity 320ms cubic-bezier(0.22, 1, 0.36, 1),
    transform 320ms cubic-bezier(0.22, 1, 0.36, 1);
}

.brand-view-enter-from { opacity: 0; transform: translateY(20px); }
.brand-view-leave-to   { opacity: 0; transform: translateY(-12px); }
</style>
