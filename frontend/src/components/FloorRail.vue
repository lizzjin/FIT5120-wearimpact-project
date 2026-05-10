<template>
  <div class="floor-rail" aria-hidden="true">
    <!-- Lime "river" — two parallax water layers under a bright surface line. -->
    <div class="floor-river">
      <svg class="river-layer river-layer--back" viewBox="0 0 2880 80" preserveAspectRatio="none">
        <defs>
          <linearGradient :id="gradBackId" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0"    stop-color="#bff0a0" stop-opacity="0.45"/>
            <stop offset="0.55" stop-color="#a8e394" stop-opacity="0.22"/>
            <stop offset="1"    stop-color="#9fe870" stop-opacity="0"/>
          </linearGradient>
        </defs>
        <path
          :d="backPathD"
          :fill="`url(#${gradBackId})`"
        />
      </svg>

      <svg class="river-layer river-layer--front" viewBox="0 0 2880 80" preserveAspectRatio="none">
        <defs>
          <linearGradient :id="gradFrontId" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0"    stop-color="#b6ea90" stop-opacity="0.62"/>
            <stop offset="0.55" stop-color="#9fe870" stop-opacity="0.34"/>
            <stop offset="1"    stop-color="#9fe870" stop-opacity="0"/>
          </linearGradient>
        </defs>
        <path
          :d="frontPathD"
          :fill="`url(#${gradFrontId})`"
        />
      </svg>

      <!-- Surface highlight line — original 1440-wide wave, kept so the
           "draws-itself-in" entrance still reads as a bright lime ribbon
           skimming the top of the water. -->
      <svg class="river-edge" viewBox="0 0 1440 24" preserveAspectRatio="none">
        <path
          ref="wavePathRef"
          d="M 0 12 Q 60 2 120 12 T 240 12 T 360 12 T 480 12 T 600 12 T 720 12 T 840 12 T 960 12 T 1080 12 T 1200 12 T 1320 12 T 1440 12"
          stroke="#9fe870"
          stroke-width="2"
          fill="none"
          stroke-linecap="round"
          opacity="0.85"
        />
      </svg>
    </div>

    <div class="floor-flow">
      <img
        v-for="(src, i) in floorIcons"
        :key="i"
        :src="src"
        class="floor-item"
        :style="{ '--i': i }"
        alt=""
        aria-hidden="true"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { gsap } from 'gsap'
// Shared floor icons — one fixed set used across pages that mount this rail.
import floorClothing from '../assets/illustrations/floor-clothing.svg'
import floorHandbag from '../assets/illustrations/floor-handbag.svg'
import floorLeaf from '../assets/illustrations/floor-leaf.svg'
import floorLightBulb from '../assets/illustrations/floor-light-bulb.svg'
import floorRecycle from '../assets/illustrations/floor-recycle.svg'
import floorShoes from '../assets/illustrations/floor-shoes.svg'
import floorTag from '../assets/illustrations/floor-tag.svg'

// Order chosen so adjacent items have visual variety (silhouette, color).
const floorIcons = [
  floorClothing,
  floorTag,
  floorLeaf,
  floorHandbag,
  floorRecycle,
  floorShoes,
  floorLightBulb,
]

// Each river layer SVG is drawn at 2880 wide (= 2× viewport) and translated
// by -50% in CSS to loop seamlessly. The d strings below carry the wave
// across the full 2880 so the seam at the wrap-around lines up.

// Front wave: period 240 (Q 0→120, then T every +120) — denser, livelier.
function buildFrontPath() {
  const ts = []
  for (let x = 240; x <= 2880; x += 120) ts.push(`T ${x} 32`)
  return `M 0 32 Q 60 22 120 32 ${ts.join(' ')} L 2880 80 L 0 80 Z`
}

// Back wave: period 360 (Q 0→180, then T every +180) — wider, slower.
function buildBackPath() {
  const ts = []
  for (let x = 360; x <= 2880; x += 180) ts.push(`T ${x} 26`)
  return `M 0 26 Q 90 18 180 26 ${ts.join(' ')} L 2880 80 L 0 80 Z`
}

const frontPathD = buildFrontPath()
const backPathD = buildBackPath()

// Unique ids per instance so two rails on one page don't share <linearGradient>.
const uid = Math.random().toString(36).slice(2, 9)
const gradFrontId = `river-front-${uid}`
const gradBackId = `river-back-${uid}`

// Stroke-draw the lime surface line once on mount, so the rail "draws itself in"
// instead of just appearing.
const wavePathRef = ref(null)
onMounted(() => {
  const path = wavePathRef.value
  if (!path) return
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
  const length = path.getTotalLength?.() || 1500
  gsap.set(path, { strokeDasharray: length, strokeDashoffset: length })
  gsap.to(path, { strokeDashoffset: 0, duration: 0.9, ease: 'power3.out', delay: 0.2 })
})
</script>

<style scoped>
.floor-rail {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  height: 130px;
  pointer-events: none;
  z-index: 5;
  display: flex;
  align-items: center;
  justify-content: center;
  /* Cream gradient veil — top half kept airy so the river surface reads
     against the page, bottom half settles back to the cream floor. */
  background: linear-gradient(
    to bottom,
    transparent 0%,
    rgba(246, 240, 230, 0.18) 35%,
    rgba(246, 240, 230, 0.78) 78%,
    rgba(246, 240, 230, 0.95) 100%
  );
}

/* ── River container + parallax layers ─────────────────────────────── */
.floor-river {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 80px;
  pointer-events: none;
  overflow: hidden;
}

.river-layer {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 200%;
  display: block;
  will-change: transform;
}

.river-layer--back  { animation: river-drift 22s linear infinite; opacity: 0.85; }
.river-layer--front { animation: river-drift 14s linear infinite; opacity: 1; }

@keyframes river-drift {
  from { transform: translateX(0); }
  to   { transform: translateX(-50%); }
}

/* Surface highlight — sits at the top edge of the river. */
.river-edge {
  position: absolute;
  left: 0;
  right: 0;
  top: 28px;     /* matches front-wave crest band (32 in viewBox) */
  width: 100%;
  height: 24px;
  pointer-events: none;
}

/* ── Drifting items ────────────────────────────────────────────────── */
.floor-flow {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 100%;
  pointer-events: none;
}

.floor-item {
  position: absolute;
  bottom: 38px;          /* sit just above the surface highlight line */
  left: 0;
  width: 56px;
  height: 56px;
  object-fit: contain;
  pointer-events: none;
  animation: floor-travel 36s linear infinite;
  animation-delay: calc(var(--i, 0) * -5.2s);
  will-change: transform, opacity;
}

.floor-item:nth-child(2) { animation-duration: 40s; bottom: 46px; width: 52px; height: 52px; }
.floor-item:nth-child(3) { animation-duration: 32s; bottom: 40px; }
.floor-item:nth-child(4) { animation-duration: 38s; bottom: 42px; width: 60px; height: 60px; }
.floor-item:nth-child(5) { animation-duration: 42s; bottom: 50px; }
.floor-item:nth-child(6) { animation-duration: 35s; bottom: 44px; width: 50px; height: 50px; }
.floor-item:nth-child(7) { animation-duration: 39s; bottom: 48px; }

@keyframes floor-travel {
  0%   { transform: translateX(-10vw) scale(0.7) rotate(-4deg); opacity: 0; }
  8%   { opacity: 0.85; }
  50%  { transform: translateX(50vw) scale(1) rotate(0deg);     opacity: 0.9; }
  92%  { opacity: 0.85; }
  100% { transform: translateX(110vw) scale(0.7) rotate(4deg);  opacity: 0; }
}

@media (prefers-reduced-motion: reduce) {
  .river-layer { animation: none; }
  .floor-item {
    animation: none;
    transform: translateX(calc(8vw + var(--i, 0) * 16vw)) scale(1);
    opacity: 0.85;
  }
}

@media (max-width: 768px) {
  .floor-rail { height: 90px; }
  .floor-river { height: 56px; }
  .river-edge { top: 18px; height: 18px; }
  .floor-item { width: 44px; height: 44px; bottom: 28px; }
  .floor-item:nth-child(2) { bottom: 32px; }
  .floor-item:nth-child(3) { bottom: 30px; }
  .floor-item:nth-child(4) { bottom: 30px; }
  .floor-item:nth-child(5) { bottom: 36px; }
  .floor-item:nth-child(6) { bottom: 32px; }
  .floor-item:nth-child(7) { bottom: 34px; }
}
</style>
