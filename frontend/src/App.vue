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
import { armScrollTriggers, onRouteSettled } from './motion'
import { startLenis, stopLenis, getLenis } from './motion/lenis'
import PasswordGate from './components/PasswordGate.vue'
import { isUnlocked } from './services/siteGate'

const unlocked = ref(isUnlocked())

// If we're already unlocked at boot (sessionStorage hit), start Lenis right
// away. Otherwise it'll be started after the gate is cleared. Either way,
// stopLenis on app teardown remains the cleanup path. Lenis is replaced by
// ScrollSmoother in Phase 3 of the motion refactor; Phase 1 only routes the
// ScrollTrigger refresh calls through the new scrollManager entry points.
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
  const lenis = getLenis()
  if (lenis) lenis.scrollTo(0, { immediate: true })
  else window.scrollTo(0, 0)
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
