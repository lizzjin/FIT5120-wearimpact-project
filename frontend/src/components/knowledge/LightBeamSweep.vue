<template>
  <div ref="rootRef" class="kh-beam" aria-hidden="true">
    <div ref="beamRef" class="kh-beam__band"></div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'

const rootRef = ref(null)
const beamRef = ref(null)
let gsapLib = null

function prefersReducedMotion() {
  return window.matchMedia?.('(prefers-reduced-motion: reduce)').matches ?? false
}

async function sweep() {
  if (prefersReducedMotion()) return
  if (!gsapLib) {
    try {
      const mod = await import('gsap')
      gsapLib = mod.gsap ?? mod.default ?? mod
    } catch {
      return
    }
  }
  if (!beamRef.value) return
  gsapLib.killTweensOf(beamRef.value)
  gsapLib.fromTo(
    beamRef.value,
    { xPercent: -120, opacity: 0 },
    {
      xPercent: 120,
      opacity: 1,
      duration: 0.5,
      ease: 'power2.inOut',
      onComplete: () => {
        gsapLib.set(beamRef.value, { opacity: 0, xPercent: -120 })
      },
    },
  )
}

defineExpose({ sweep })

onMounted(async () => {
  try {
    const mod = await import('gsap')
    gsapLib = mod.gsap ?? mod.default ?? mod
  } catch {
    gsapLib = null
  }
})
</script>

<style scoped>
.kh-beam {
  position: fixed;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
  z-index: 2;
}

.kh-beam__band {
  position: absolute;
  top: -20vh;
  left: 0;
  width: 70px;
  height: 140vh;
  transform: rotate(12deg) translateX(-120%);
  background: linear-gradient(
    to right,
    transparent 0%,
    rgba(246, 240, 230, 0.32) 50%,
    transparent 100%
  );
  filter: blur(2px);
  mix-blend-mode: overlay;
  opacity: 0;
  will-change: transform, opacity;
}
</style>
