<template>
  <!-- Knowledge background — unified Wise cream canvas matching HomeView.
       Topography pattern + drifting blobs + abstract shapes, all on the
       warm-cream base so /knowledge feels like the same site as /. -->
  <div class="kh-canvas" aria-hidden="true">
    <span class="kh-canvas-blob kh-canvas-blob--tr" />
    <span class="kh-canvas-blob kh-canvas-blob--bl" />
    <span class="kh-canvas-blob kh-canvas-blob--mid" />
    <svg class="kh-canvas-shape kh-canvas-shape--ring" viewBox="0 0 120 120">
      <circle cx="60" cy="60" r="50" fill="none" stroke="#163300" stroke-width="1" stroke-dasharray="3 6" />
    </svg>
    <svg class="kh-canvas-shape kh-canvas-shape--leaf" viewBox="0 0 80 80">
      <path d="M40 8 C 60 20 60 60 40 72 C 20 60 20 20 40 8 Z" fill="none" stroke="#9fe870" stroke-width="2" />
      <line x1="40" y1="8" x2="40" y2="72" stroke="#9fe870" stroke-width="1.4" />
    </svg>
    <svg class="kh-canvas-shape kh-canvas-shape--squiggle" viewBox="0 0 200 40">
      <path d="M4 20 Q 25 4, 50 20 T 100 20 T 150 20 T 196 20" fill="none" stroke="#163300" stroke-width="1.4" stroke-linecap="round" />
    </svg>
    <span class="kh-canvas-pattern" />
  </div>
</template>

<script setup>
// Static decorative canvas. Unifies /knowledge with /'s aesthetic.
</script>

<style scoped>
.kh-canvas {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
  background: var(--color-warm-cream);
}

.kh-canvas-blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(70px);
  opacity: 0.55;
}

.kh-canvas-blob--tr {
  top: -120px;
  right: -160px;
  width: 520px;
  height: 520px;
  background: radial-gradient(circle, var(--color-primary) 0%, transparent 70%);
  animation: kh-canvas-drift 22s ease-in-out infinite;
}

.kh-canvas-blob--bl {
  bottom: -180px;
  left: -200px;
  width: 620px;
  height: 620px;
  background: radial-gradient(circle, var(--color-mint) 0%, transparent 70%);
  animation: kh-canvas-drift 28s ease-in-out infinite reverse;
}

.kh-canvas-blob--mid {
  top: 38%;
  left: 42%;
  width: 360px;
  height: 360px;
  background: radial-gradient(circle, var(--color-pastel-green) 0%, transparent 70%);
  opacity: 0.28;
  animation: kh-canvas-drift 36s ease-in-out infinite;
  animation-delay: -12s;
}

.kh-canvas-shape {
  position: absolute;
  pointer-events: none;
  opacity: 0.18;
}

.kh-canvas-shape--ring {
  top: 12%;
  left: 8%;
  width: 140px;
  height: 140px;
  animation: kh-canvas-rotate 60s linear infinite;
}

.kh-canvas-shape--leaf {
  bottom: 18%;
  right: 12%;
  width: 90px;
  height: 90px;
  opacity: 0.22;
  animation: kh-canvas-drift-up 24s ease-in-out infinite;
}

.kh-canvas-shape--squiggle {
  top: 62%;
  left: 6%;
  width: 220px;
  opacity: 0.16;
  animation: kh-canvas-squiggle 14s ease-in-out infinite;
}

.kh-canvas-pattern {
  position: absolute;
  inset: 0;
  background-image: url('../../assets/illustrations/bg-topography.svg');
  background-repeat: repeat;
  background-size: 600px 600px;
  opacity: 0.06;
}

@keyframes kh-canvas-drift {
  0%, 100% { transform: translate(0, 0) scale(1); }
  50%      { transform: translate(40px, -30px) scale(1.06); }
}

@keyframes kh-canvas-rotate {
  to { transform: rotate(360deg); }
}

@keyframes kh-canvas-drift-up {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50%      { transform: translateY(-24px) rotate(8deg); }
}

@keyframes kh-canvas-squiggle {
  0%, 100% { transform: translateX(0); }
  50%      { transform: translateX(30px); }
}

@media (prefers-reduced-motion: reduce) {
  .kh-canvas-blob,
  .kh-canvas-shape {
    animation: none;
  }
}
</style>
