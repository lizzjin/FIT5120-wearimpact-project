<template>
  <div class="app-container">
    <PasswordGate v-if="!unlocked" @unlocked="onUnlocked" />
    <router-view v-else v-slot="{ Component }">
      <Transition
        name="page"
        mode="out-in"
        @before-enter="onBeforeEnter"
        @after-enter="onAfterEnter"
      >
        <component :is="Component" />
      </Transition>
    </router-view>
    <ToastHost />
    <ConfirmHost />
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
import ToastHost from './components/ToastHost.vue'
import ConfirmHost from './components/ConfirmHost.vue'
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

// Snap scroll to top the instant the new route's DOM is inserted but before
// it fades in. Doing this in @after-enter (post fade-in) is too late — the
// user can briefly see the new page rendered at the previous scroll Y
// (e.g. clicking a deep "next step" card from the bottom of /knowledge made
// /brand-search appear scrolled, then jump back up). Keeping the call here
// too acts as a safety net if @before-enter is ever skipped.
function onBeforeEnter() {
  scrollToTopImmediate()
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
