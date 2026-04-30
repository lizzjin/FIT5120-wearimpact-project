<template>
  <div class="floor-rail" aria-hidden="true">
    <!-- Wavy lime ground line — shared baseline. -->
    <svg class="floor-rail__wave" viewBox="0 0 1440 24" preserveAspectRatio="none">
      <path
        d="M 0 12 Q 60 2 120 12 T 240 12 T 360 12 T 480 12 T 600 12 T 720 12 T 840 12 T 960 12 T 1080 12 T 1200 12 T 1320 12 T 1440 12"
        stroke="#9fe870"
        stroke-width="2"
        fill="none"
        stroke-linecap="round"
        opacity="0.7"
      />
    </svg>
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
  /* Cream gradient veil so items pop above page content */
  background: linear-gradient(
    to bottom,
    transparent 0%,
    rgba(246, 240, 230, 0.35) 30%,
    rgba(246, 240, 230, 0.85) 70%,
    rgba(246, 240, 230, 0.95) 100%
  );
}

.floor-rail__wave {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 38px;
  width: 100%;
  height: 24px;
  pointer-events: none;
}

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
  bottom: 18px;
  left: 0;
  width: 56px;
  height: 56px;
  object-fit: contain;
  pointer-events: none;
  animation: floor-travel 36s linear infinite;
  animation-delay: calc(var(--i, 0) * -5.2s);
  will-change: transform, opacity;
}

.floor-item:nth-child(2) { animation-duration: 40s; bottom: 26px; width: 52px; height: 52px; }
.floor-item:nth-child(3) { animation-duration: 32s; }
.floor-item:nth-child(4) { animation-duration: 38s; bottom: 22px; width: 60px; height: 60px; }
.floor-item:nth-child(5) { animation-duration: 42s; bottom: 30px; }
.floor-item:nth-child(6) { animation-duration: 35s; bottom: 24px; width: 50px; height: 50px; }
.floor-item:nth-child(7) { animation-duration: 39s; bottom: 28px; }

@keyframes floor-travel {
  0%   { transform: translateX(-10vw) scale(0.7) rotate(-4deg); opacity: 0; }
  8%   { opacity: 0.85; }
  50%  { transform: translateX(50vw) scale(1) rotate(0deg);     opacity: 0.9; }
  92%  { opacity: 0.85; }
  100% { transform: translateX(110vw) scale(0.7) rotate(4deg);  opacity: 0; }
}

@media (prefers-reduced-motion: reduce) {
  .floor-item {
    animation: none;
    transform: translateX(calc(8vw + var(--i, 0) * 16vw)) scale(1);
    opacity: 0.85;
  }
}

@media (max-width: 768px) {
  .floor-rail { height: 90px; }
  .floor-item { width: 44px; height: 44px; }
}
</style>
