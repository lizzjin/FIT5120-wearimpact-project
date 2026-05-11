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
  fillHover: { type: String, default: 'var(--color-primary-text, #163300)' },
  text: { type: String, default: 'var(--color-primary-text, #163300)' },
  textHover: { type: String, default: 'var(--color-primary, #9fe870)' },
  stroke: { type: String, default: 'transparent' },
  strokeHover: { type: String, default: 'var(--color-primary-text, #163300)' },
  bubbleCount: { type: Number, default: 20 },
  bubbleColor: { type: String, default: '#163300' },
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
  letter-spacing: 0.01em;
  cursor: pointer;
  text-decoration: none;
  border: 1px solid var(--btn-stroke);
  background: transparent;
  color: var(--btn-text);
  transition: color 240ms ease, border-color 240ms ease, transform 240ms ease;
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
  transform: scaleX(1);
  transform-origin: right center;
  transition: transform 360ms cubic-bezier(0.65, 0, 0.35, 1), background 240ms ease;
  z-index: -1;
}

.cta-button.variant-outline .cta-button__background {
  transform: scaleX(0);
  transform-origin: left center;
}

.cta-button:hover {
  color: var(--btn-text-hover);
  border-color: var(--btn-stroke-hover);
  transform: translateY(-1px);
}

.cta-button:hover .cta-button__background {
  background: var(--btn-fill-hover);
  transform: scaleX(1);
  transform-origin: left center;
}

.cta-button:focus-visible {
  outline: 2px solid var(--btn-stroke-hover);
  outline-offset: 3px;
}

</style>
