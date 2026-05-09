<template>
  <!-- Knowledge background — unified cream canvas matching HomeView.
       Topography pattern + drifting blobs + abstract shapes, all on the
       warm-cream base so /knowledge feels like the same site as /. -->
  <div class="kh-canvas" aria-hidden="true">
    <span class="kh-canvas-blob kh-canvas-blob--tr" />
    <span class="kh-canvas-blob kh-canvas-blob--bl" />
    <span class="kh-canvas-blob kh-canvas-blob--mid" />
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

@media (prefers-reduced-motion: reduce) {
  .kh-canvas-blob {
    animation: none;
  }
}
</style>
