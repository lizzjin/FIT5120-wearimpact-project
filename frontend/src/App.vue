<template>
  <div class="app-container">
    <PasswordGate v-if="!unlocked" @unlocked="onUnlocked" />
    <router-view v-else v-slot="{ Component }">
      <Transition name="page" mode="out-in" @after-enter="onAfterEnter">
        <component :is="Component" />
      </Transition>
    </router-view>
  </div>
</template>

<script setup>
import { ref, onBeforeUnmount, nextTick } from 'vue'
import {
  armScrollTriggers,
  onRouteSettled,
  startLenis,
  stopLenis,
  scrollToTopImmediate,
} from './motion'
import PasswordGate from './components/PasswordGate.vue'
import { isUnlocked } from './services/siteGate'

const unlocked = ref(isUnlocked())

// Start Lenis after the first route mounts. Phase 3 of the motion refactor
// kept Lenis (instead of the planned ScrollSmoother) because ScrollSmoother
// transforms its #smooth-content wrapper, which would break the four
// `position: sticky` elements in the codebase — most visibly the navbar.
if (unlocked.value) {
  nextTick(() => {
    startLenis()
    armScrollTriggers()
  })
}

onBeforeUnmount(() => {
  stopLenis()
})

function onUnlocked() {
  unlocked.value = true
  nextTick(() => {
    startLenis()
    armScrollTriggers()
  })
}

function onAfterEnter() {
  scrollToTopImmediate()
  onRouteSettled()
}
</script>

<style>
/* Page transition — must NOT use transform or filter on the root, because
   any transformed/filtered ancestor breaks `position: sticky` on the Navbar
   inside each route. Stick to opacity-only so the sticky bar stays sticky
   and remains clickable throughout the transition. */
.page-enter-active,
.page-leave-active {
  transition: opacity 280ms cubic-bezier(0.22, 1, 0.36, 1);
}
.page-enter-from,
.page-leave-to {
  opacity: 0;
}
</style>
