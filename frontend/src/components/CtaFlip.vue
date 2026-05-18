<template>
  <span class="cta-flip">
    <span class="cta-flip__line cta-flip__line--front"><slot /></span>
    <span class="cta-flip__line cta-flip__line--back" aria-hidden="true"><slot /></span>
  </span>
</template>

<script setup>
// Drop-in text-flip wrapper matching labs.anyflow.agency: on the host
// button's :hover, the front line slides up and out, the cloned back line
// slides up from below into its slot. Activated by the same
// `.is-burst-host` parent class that drives <CtaBurst>, so a button gets
// the full Anyflow effect by adding `is-burst-host` plus mounting both
// <CtaBurst /> and <CtaFlip>{{ label content }}</CtaFlip>.
//
// `gap: inherit` makes the cloned line's icon/text spacing match whatever
// the host button already declares (typically 8–10 px), so the duplicated
// row visually lines up with the original layout.
</script>

<style>
.cta-flip {
  position: relative;
  display: inline-flex;
  overflow: hidden;
  line-height: 1;
  /* Inherit the host button's gap so the wrapper is layout-transparent. */
  gap: inherit;
  z-index: 1;
}

.cta-flip__line {
  display: inline-flex;
  align-items: center;
  gap: inherit;
  transition: transform 360ms cubic-bezier(0.65, 0, 0.35, 1);
}

.cta-flip__line--back {
  position: absolute;
  inset: 0;
  transform: translateY(110%);
}

.is-burst-host:hover .cta-flip__line--front,
.is-burst-host:focus-visible .cta-flip__line--front {
  transform: translateY(-110%);
}
.is-burst-host:hover .cta-flip__line--back,
.is-burst-host:focus-visible .cta-flip__line--back {
  transform: translateY(0);
}

@media (prefers-reduced-motion: reduce) {
  .cta-flip__line {
    transition: none;
  }
  .is-burst-host:hover .cta-flip__line--front,
  .is-burst-host:focus-visible .cta-flip__line--front,
  .is-burst-host:hover .cta-flip__line--back,
  .is-burst-host:focus-visible .cta-flip__line--back {
    transform: none;
  }
}
</style>
