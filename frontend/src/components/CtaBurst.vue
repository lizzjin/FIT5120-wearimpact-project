<template>
  <span class="cta-burst" aria-hidden="true">
    <span
      v-for="b in bubbles"
      :key="b.i"
      class="cta-burst__bubble"
      :style="{ '--bx': b.x + 'px', '--by': b.y + 'px', background: color }"
    />
  </span>
</template>

<script setup>
// Drop-in bubble-burst overlay matching the hover effect on
// labs.anyflow.agency. Mount inside any button and add `is-burst-host` to
// the button itself; no other markup changes needed.
//
// Animation captured from labs.anyflow.agency (framer-motion driven):
//   0 → 60 %  (~570 ms, ease-out): translate 0 → target, scale 0 → 1.5,
//                                  opacity 0 → 0.8
//   60 → 100 % (~380 ms, ease-in): translate stays at target, scale 1.5 → 0,
//                                  opacity 0.8 → 0
const props = defineProps({
  count: { type: Number, default: 20 },
  color: { type: String, default: '#163300' },
})

// Even angular distribution + randomised radius mirrors Anyflow's layout
// (i · 360/N spokes, 70–105 px from centre — slightly tighter than the
// reference because our pill buttons are smaller).
const bubbles = Array.from({ length: props.count }, (_, i) => {
  const angle = (i / props.count) * Math.PI * 2
  const dist = 70 + Math.random() * 35
  return {
    i,
    x: Math.cos(angle) * dist,
    y: Math.sin(angle) * dist,
  }
})
</script>

<style>
/* Intentionally unscoped: the activator selector lives on the *parent*
   button (`.is-burst-host:hover .cta-burst__bubble`) and scoped CSS can't
   match outside its own component subtree. The class names are namespaced
   so collisions are not a concern. */
.cta-burst {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.cta-burst__bubble {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 8px;
  height: 8px;
  border-radius: 999px;
  opacity: 0;
  transform: translate(-50%, -50%) scale(0);
  pointer-events: none;
}

@keyframes cta-burst-puff {
  0% {
    opacity: 0;
    transform: translate(-50%, -50%) scale(0);
    animation-timing-function: cubic-bezier(0.22, 1, 0.36, 1);
  }
  60% {
    opacity: 0.8;
    transform: translate(calc(-50% + var(--bx)), calc(-50% + var(--by))) scale(1.5);
    animation-timing-function: cubic-bezier(0.55, 0, 0.78, 0.4);
  }
  100% {
    opacity: 0;
    transform: translate(calc(-50% + var(--bx)), calc(-50% + var(--by))) scale(0);
  }
}

/* Forced overrides: !important ensures any host button — even one with
   scoped `overflow: hidden` — lets the dots fly past its edges. */
.is-burst-host {
  position: relative !important;
  overflow: visible !important;
}

.is-burst-host:hover .cta-burst__bubble,
.is-burst-host:focus-visible .cta-burst__bubble {
  animation: cta-burst-puff 950ms forwards;
}

@media (prefers-reduced-motion: reduce) {
  .is-burst-host:hover .cta-burst__bubble,
  .is-burst-host:focus-visible .cta-burst__bubble {
    animation: none;
  }
}
</style>
