<template>
  <component
    :is="tag"
    v-bind="anchorAttrs"
    :type="tag === 'button' ? type : null"
    class="cta-button is-burst-host"
    :class="[`variant-${variant}`]"
    :style="cssVars"
    ref="rootRef"
  >
    <span class="cta-button__background" aria-hidden="true" />

    <CtaFlip class="cta-button__text"><slot /></CtaFlip>

    <CtaBurst :count="bubbleCount" :color="bubbleColor" />
  </component>
</template>

<script setup>
import { computed, ref } from 'vue'
import CtaBurst from './CtaBurst.vue'
import CtaFlip from './CtaFlip.vue'
import { useRipple } from '../motion'

const rootRef = ref(null)
// Ripple from the click coordinate. The CSS hover state already handles
// the scale/colour/background-slide transitions; useHover would fight
// the `transform: translateY(-1px)` rule on :hover, so it is deliberately
// not applied here. The bubble-burst overlay sits on top of the ripple
// and continues to fire on hover.
useRipple(rootRef, { color: 'rgba(22, 51, 0, 0.18)', duration: 0.6 })

const props = defineProps({
  href: { type: String, default: null },
  to: { type: [String, Object], default: null },
  type: { type: String, default: 'button' },
  variant: { type: String, default: 'solid' },
  fill: { type: String, default: 'var(--color-primary, #9fe870)' },
  // Site-wide standard for hover: lime → pastel lime (--color-primary-dark
  // #cdffad). The old default was dark green, which produced an aggressive
  // colour-takeover that other pages (Knowledge, Brand, EcoShop, Wardrobe)
  // explicitly avoided. Keeping text/stroke unchanged on hover keeps the
  // pill on-brand and matches the rest of the site.
  fillHover: { type: String, default: 'var(--color-primary-dark, #cdffad)' },
  text: { type: String, default: 'var(--color-primary-text, #163300)' },
  textHover: { type: String, default: 'var(--color-primary-text, #163300)' },
  stroke: { type: String, default: 'transparent' },
  strokeHover: { type: String, default: 'transparent' },
  bubbleCount: { type: Number, default: 20 },
  bubbleColor: { type: String, default: 'var(--color-primary, #9fe870)' },
})

const tag = computed(() => {
  if (props.to) return 'router-link'
  if (props.href) return 'a'
  return 'button'
})

const anchorAttrs = computed(() => {
  if (props.to) return { to: props.to }
  if (props.href) {
    const external = /^https?:/.test(props.href)
    return external
      ? { href: props.href, target: '_blank', rel: 'noopener noreferrer' }
      : { href: props.href }
  }
  return {}
})

const cssVars = computed(() => ({
  '--btn-fill': props.fill,
  '--btn-fill-hover': props.fillHover,
  '--btn-text': props.text,
  '--btn-text-hover': props.textHover,
  '--btn-stroke': props.stroke,
  '--btn-stroke-hover': props.strokeHover,
}))

</script>

<style scoped>
.cta-button {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 28px;
  border-radius: 999px;
  font-family: inherit;
  font-weight: 700;
  font-size: 15px;
  cursor: pointer;
  text-decoration: none;
  border: 1px solid var(--btn-stroke);
  background: transparent;
  color: var(--btn-text);
  transition: transform 200ms var(--motion-entrance, cubic-bezier(0.22, 1, 0.36, 1));
  isolation: isolate;
  /* Burst dots fly past the pill edge — must let them out of the box. The
     background layer is a separate element clipped by its own border-radius,
     so the visible pill shape is unaffected. */
  overflow: visible;
}

.cta-button__background {
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: var(--btn-fill);
  transition: background 200ms var(--motion-entrance, cubic-bezier(0.22, 1, 0.36, 1));
  z-index: -1;
}

.cta-button:hover {
  transform: scale(1.03);
}

.cta-button:hover .cta-button__background {
  background: var(--btn-fill-hover);
}

.cta-button:focus-visible {
  outline: 2px solid var(--color-primary-text, #163300);
  outline-offset: 3px;
}

</style>
