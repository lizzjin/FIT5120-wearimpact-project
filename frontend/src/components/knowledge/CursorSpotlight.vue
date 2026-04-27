<template>
  <div v-if="enabled" ref="spotRef" class="kh-spotlight" aria-hidden="true"></div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'

// Soft radial glow that follows the cursor with lerp easing.
// Mounted only on devices with a fine pointer; touch screens skip the
// component entirely so no listeners are attached.

const enabled = ref(false)
const spotRef = ref(null)

let target = { x: 0, y: 0 }
let pos = { x: 0, y: 0 }
let rafId = null
let initialized = false

function updatePosition() {
  // Lerp toward target — factor 0.12 gives a noticeable trail without lag.
  pos.x += (target.x - pos.x) * 0.12
  pos.y += (target.y - pos.y) * 0.12
  if (spotRef.value) {
    spotRef.value.style.transform = `translate3d(${pos.x}px, ${pos.y}px, 0) translate(-50%, -50%)`
  }
  rafId = requestAnimationFrame(updatePosition)
}

function onMouseMove(event) {
  target.x = event.clientX
  target.y = event.clientY
  if (!initialized) {
    pos.x = target.x
    pos.y = target.y
    initialized = true
  }
}

onMounted(() => {
  if (!window.matchMedia || !window.matchMedia('(pointer: fine)').matches) {
    return
  }
  enabled.value = true
  // Defer adding listener until the spotlight element exists.
  requestAnimationFrame(() => {
    window.addEventListener('mousemove', onMouseMove, { passive: true })
    rafId = requestAnimationFrame(updatePosition)
  })
})

onBeforeUnmount(() => {
  window.removeEventListener('mousemove', onMouseMove)
  if (rafId != null) cancelAnimationFrame(rafId)
})
</script>

<style scoped>
.kh-spotlight {
  position: fixed;
  top: 0;
  left: 0;
  width: 800px;
  height: 800px;
  pointer-events: none;
  z-index: 0;
  background: radial-gradient(
    circle,
    rgba(159, 232, 112, 0.09) 0%,
    rgba(159, 232, 112, 0.04) 30%,
    transparent 70%
  );
  mix-blend-mode: screen;
  will-change: transform;
}

@media (prefers-reduced-motion: reduce) {
  .kh-spotlight {
    /* Reduce opacity rather than disabling — positional tracking still works. */
    opacity: 0.6;
  }
}
</style>
