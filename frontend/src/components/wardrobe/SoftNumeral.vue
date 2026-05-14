<template>
  <!-- Large display numeral used as the wardrobe's "cover star". Counts
       up from 0 on mount, then sits at the real value. Soft DM Sans
       italic, no stroke, no skew — feels like a magazine page number. -->
  <span
    ref="rootRef"
    class="wd-numeral"
    :class="[`wd-numeral--${color}`]"
    aria-hidden="true"
  >{{ displayValue }}</span>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { gsap } from '../../motion'

const props = defineProps({
  value: { type: Number, required: true },
  // `ink | sage | sage-deep | dusty`
  color: { type: String, default: 'sage-deep' },
  // Animation length in seconds.
  duration: { type: Number, default: 0.9 }
})

const rootRef = ref(null)
function pad(n) { return String(Math.max(0, Math.floor(n))).padStart(2, '0') }
// Initial render shows the real value so the numeral is visible even if
// the rollup animation never fires (route swap, prefers-reduced-motion).
const displayValue = ref(pad(props.value))

let tween = null

function animateTo(target) {
  if (tween) tween.kill()
  const obj = { n: 0 }
  displayValue.value = '00'
  tween = gsap.to(obj, {
    n: target,
    duration: props.duration,
    ease: 'power2.out',
    snap: { n: 1 },
    onUpdate: () => { displayValue.value = pad(obj.n) },
    onComplete: () => { displayValue.value = pad(target) }
  })
}

onMounted(() => {
  // Defer a frame so any entry transition settles before the counter rolls.
  requestAnimationFrame(() => animateTo(props.value))
})

watch(() => props.value, (next, prev) => {
  if (next === prev) return
  animateTo(next)
})

onBeforeUnmount(() => {
  if (tween) tween.kill()
})
</script>

<style scoped>
.wd-numeral {
  display: inline-block;
  font-family: var(--font-display);
  font-style: italic;
  font-weight: 800;
  /* Slightly smaller than the pop version — the soft style relies more
     on whitespace and texture than on shouting numerals. */
  font-size: clamp(96px, 14vw, 180px);
  line-height: 0.88;
  letter-spacing: -0.04em;
}

.wd-numeral--ink       { color: var(--color-soft-ink); }
.wd-numeral--sage      { color: var(--color-soft-sage); }
.wd-numeral--sage-deep { color: var(--color-soft-sage-deep); }
.wd-numeral--dusty     { color: var(--color-soft-dusty); }
</style>
