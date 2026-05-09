<template>
  <div class="knowledge-page">
    <!-- Shared cream canvas — same component used by /brand-search and
         /wardrobe so the cream + drifting blobs stay seamless. -->
    <QuizBackground />

    <Navbar />

    <main class="knowledge-page__main">
      <Transition name="kh-view" mode="out-in">
        <KnowledgeIntro
          v-if="view === 'intro'"
          key="intro"
          @next="goLifecycle"
        />
        <KnowledgeLifecycle
          v-else-if="view === 'lifecycle'"
          key="lifecycle"
          @back="goIntro"
          @next="goMaterials"
        />
        <KnowledgeMaterials
          v-else-if="view === 'materials'"
          key="materials"
          @back="goLifecycle"
          @next="goCards"
        />
        <KnowledgeCards
          v-else-if="view === 'cards'"
          key="cards"
          @back="goMaterials"
        />
        <KnowledgeIntro
          v-else
          key="intro-fallback"
          @next="goLifecycle"
        />
      </Transition>
    </main>

    <!-- Shared homepage floor rail — same flowing icons + lime wave. -->
    <FloorRail />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Navbar from '../components/Navbar.vue'
import QuizBackground from '../components/knowledge/QuizBackground.vue'
import FloorRail from '../components/FloorRail.vue'
import KnowledgeIntro from '../components/knowledge/KnowledgeIntro.vue'
import KnowledgeLifecycle from '../components/knowledge/KnowledgeLifecycle.vue'
import KnowledgeMaterials from '../components/knowledge/KnowledgeMaterials.vue'
import KnowledgeCards from '../components/knowledge/KnowledgeCards.vue'

// View state machine: intro → lifecycle → materials → cards.
// Materials and cards are placeholders for now; routing back to intro
// means an unfinished branch never strands the user on a blank page.
const view = ref('intro')

function scrollTop() {
  requestAnimationFrame(() => window.scrollTo({ top: 0, behavior: 'smooth' }))
}

function goIntro() { view.value = 'intro'; scrollTop() }
function goLifecycle() { view.value = 'lifecycle'; scrollTop() }
function goMaterials() { view.value = 'materials'; scrollTop() }
function goCards() { view.value = 'cards'; scrollTop() }
</script>

<style scoped>
.knowledge-page {
  position: relative;
  min-height: 100vh;
  color: var(--color-text);
  font-family: 'Inter', system-ui, -apple-system, Arial, sans-serif;
  overflow-x: hidden;
  background: transparent;
}

.knowledge-page__main {
  position: relative;
  z-index: 1;
  /* Reserve room above the fixed floor rail (130px tall) so page content
     never collides with the flowing icons. */
  padding-bottom: 160px;
}

/* Shared transition — matches the wardrobe state-machine cadence. */
.kh-view-enter-active,
.kh-view-leave-active {
  transition:
    opacity 320ms cubic-bezier(0.22, 1, 0.36, 1),
    transform 320ms cubic-bezier(0.22, 1, 0.36, 1);
}
.kh-view-enter-from { opacity: 0; transform: translateY(20px); }
.kh-view-leave-to   { opacity: 0; transform: translateY(-12px); }
</style>
