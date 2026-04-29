<template>
  <div class="wardrobe-page">
    <!-- Shared Wise canvas — same component used by /brand-search and
         /knowledge so the cream + drifting blobs stay seamless. -->
    <QuizBackground />

    <Navbar />

    <main class="wardrobe-page__main">
      <Transition name="wd-view" mode="out-in">
        <WardrobeIntro
          v-if="view === 'intro'"
          key="intro"
          :total="total"
          @first-time="goOnboarding"
          @enter="goWardrobe"
        />
        <WardrobeOnboarding
          v-else-if="view === 'onboarding'"
          key="onboarding"
          @back="goIntro"
          @enter="goWardrobe"
        />
        <WardrobeMain
          v-else-if="view === 'wardrobe'"
          key="wardrobe"
          :garments="garments"
          :total="total"
          :recent="recent"
          @back="goIntro"
          @saved="refresh"
          @delete="onDelete"
          @clear="onClearAll"
          @open-advisor="goAdvisor"
        />
        <WardrobeAdvisor
          v-else
          key="advisor"
          :garments="garments"
          @close="goWardrobe"
        />
      </Transition>
    </main>
  </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import Navbar from '../components/Navbar.vue'
import QuizBackground from '../components/knowledge/QuizBackground.vue'
import WardrobeIntro from '../components/wardrobe/WardrobeIntro.vue'
import WardrobeOnboarding from '../components/wardrobe/WardrobeOnboarding.vue'
import WardrobeMain from '../components/wardrobe/WardrobeMain.vue'
import WardrobeAdvisor from '../components/wardrobe/WardrobeAdvisor.vue'

import {
  getAllGarments,
  countTotal,
  countRecent,
  deleteGarment,
  clearWardrobe
} from '../services/wardrobeDb.js'

// View state machine: intro → onboarding → wardrobe.
const view = ref('intro')

const garments = ref([])
const total = ref(0)
const recent = ref(0)

async function refresh() {
  garments.value = await getAllGarments()
  total.value = await countTotal()
  recent.value = await countRecent(7)
}

function scrollTop() {
  requestAnimationFrame(() => window.scrollTo({ top: 0, behavior: 'smooth' }))
}

function goIntro() { view.value = 'intro'; scrollTop() }
function goOnboarding() { view.value = 'onboarding'; scrollTop() }
function goWardrobe() { view.value = 'wardrobe'; scrollTop() }
function goAdvisor() { view.value = 'advisor'; scrollTop() }

async function onDelete(id) {
  await deleteGarment(id)
  await refresh()
}

async function onClearAll() {
  if (!confirm('Delete every item from your wardrobe? This cannot be undone.')) return
  await clearWardrobe()
  await refresh()
}

// Background poll catches async hi-quality preview swaps written by
// UploadCompact after the foreground promise resolved.
let pollHandle = null
onMounted(() => {
  refresh()
  pollHandle = setInterval(refresh, 4000)
})
onBeforeUnmount(() => {
  if (pollHandle) clearInterval(pollHandle)
})
</script>

<style scoped>
.wardrobe-page {
  position: relative;
  min-height: 100vh;
  color: var(--color-text);
  font-family: 'Inter', system-ui, -apple-system, Arial, sans-serif;
  overflow-x: hidden;
  background: transparent;
}

.wardrobe-page__main {
  position: relative;
  z-index: 1;
  padding-bottom: 64px;
}

.wd-view-enter-active,
.wd-view-leave-active {
  transition:
    opacity 320ms cubic-bezier(0.22, 1, 0.36, 1),
    transform 320ms cubic-bezier(0.22, 1, 0.36, 1);
}
.wd-view-enter-from { opacity: 0; transform: translateY(20px); }
.wd-view-leave-to   { opacity: 0; transform: translateY(-12px); }
</style>
