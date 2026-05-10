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
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { startLenis, stopLenis, getLenis } from './motion/lenis'
import PasswordGate from './components/PasswordGate.vue'
import { isUnlocked } from './services/siteGate'

const unlocked = ref(isUnlocked())

// If we're already unlocked at boot (sessionStorage hit), start Lenis right
// away. Otherwise it'll be started after the gate is cleared. Either way,
// stopLenis on app teardown remains the cleanup path.
if (unlocked.value) {
  // Defer to next tick so the router-view has actually mounted.
  nextTick(() => {
    startLenis()
    window.addEventListener('load', () => ScrollTrigger.refresh())
  })
}

onBeforeUnmount(() => {
  stopLenis()
})

function onUnlocked() {
  unlocked.value = true
  // Wait for router-view to mount the first route, then arm motion plumbing.
  nextTick(() => {
    startLenis()
    ScrollTrigger.refresh()
  })
}

// After every route change, scroll to top via Lenis (so it stays in sync) and
// re-measure ScrollTrigger so animations on the new page line up with viewport.
function onAfterEnter() {
  const lenis = getLenis()
  if (lenis) lenis.scrollTo(0, { immediate: true })
  else window.scrollTo(0, 0)
  ScrollTrigger.refresh()
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
