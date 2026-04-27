<template>
  <span ref="rootRef" class="odometer">
    <span
      v-for="(ch, i) in chars"
      :key="`${i}-${ch}`"
      :class="ch.kind === 'digit' ? 'odometer__reel' : 'odometer__static'"
    >
      <template v-if="ch.kind === 'digit'">
        <span class="odometer__strip" :data-target="ch.value">
          <span v-for="d in 10" :key="d - 1" class="odometer__digit">{{ d - 1 }}</span>
        </span>
      </template>
      <template v-else>{{ ch.value }}</template>
    </span>
  </span>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'

const props = defineProps({
  value: { type: Number, required: true },
  duration: { type: Number, default: 1200 },
  // Minimum number of digit places (e.g. padTo: 2 → "07" for value=7).
  padTo: { type: Number, default: 0 },
  // Optional decimal places to display.
  decimals: { type: Number, default: 0 },
})

const rootRef = ref(null)
const hasAnimated = ref(false)
let gsapLib = null
let observer = null

// Render the number as a string then split into characters. Digits become
// reels; non-digit characters (the decimal point, padding zeros are also
// digits but treated identically) render as static text.
const formatted = computed(() => {
  const v = props.value
  let s = (props.decimals > 0 ? v.toFixed(props.decimals) : Math.round(v).toString())
  if (props.padTo > 0) {
    const intPart = s.split('.')[0]
    if (intPart.length < props.padTo) {
      s = intPart.padStart(props.padTo, '0') + (s.includes('.') ? `.${s.split('.')[1]}` : '')
    }
  }
  return s
})

const chars = computed(() =>
  Array.from(formatted.value).map((c) => {
    if (/[0-9]/.test(c)) return { kind: 'digit', value: Number(c) }
    return { kind: 'static', value: c }
  }),
)

function prefersReducedMotion() {
  return window.matchMedia?.('(prefers-reduced-motion: reduce)').matches ?? false
}

function snapToTarget() {
  if (!rootRef.value) return
  const strips = rootRef.value.querySelectorAll('.odometer__strip')
  strips.forEach((strip) => {
    const target = Number(strip.getAttribute('data-target') ?? 0)
    strip.style.transform = `translateY(-${target}em)`
  })
}

async function animateToTarget() {
  await nextTick()
  if (!rootRef.value) return
  const strips = rootRef.value.querySelectorAll('.odometer__strip')
  if (prefersReducedMotion() || !gsapLib) {
    snapToTarget()
    return
  }
  strips.forEach((strip, i) => {
    const target = Number(strip.getAttribute('data-target') ?? 0)
    gsapLib.fromTo(
      strip,
      { y: 0 },
      {
        y: -target * strip.offsetHeight / 10, // each digit row is 1em ≈ height/10
        duration: props.duration / 1000,
        ease: 'power3.out',
        delay: i * 0.06,
      },
    )
  })
}

watch(
  () => props.value,
  () => {
    if (hasAnimated.value) animateToTarget()
  },
)

onMounted(async () => {
  // Snap initially to 0 (strips start at translateY 0 anyway). On first
  // viewport entry, run the animation once.
  try {
    const mod = await import('gsap')
    gsapLib = mod.gsap ?? mod.default ?? mod
  } catch {
    gsapLib = null
  }

  if (!('IntersectionObserver' in window) || !rootRef.value) {
    hasAnimated.value = true
    animateToTarget()
    return
  }

  observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          hasAnimated.value = true
          animateToTarget()
          observer.disconnect()
          break
        }
      }
    },
    { threshold: 0.4 },
  )
  observer.observe(rootRef.value)
})

onBeforeUnmount(() => {
  if (observer) observer.disconnect()
})
</script>

<style scoped>
.odometer {
  display: inline-flex;
  align-items: baseline;
  font-variant-numeric: tabular-nums;
  line-height: 1;
}

.odometer__reel {
  display: inline-block;
  height: 1em;
  overflow: hidden;
  vertical-align: baseline;
}

.odometer__strip {
  display: flex;
  flex-direction: column;
  transform: translateY(0);
  will-change: transform;
}

.odometer__digit {
  display: block;
  height: 1em;
  line-height: 1;
}

.odometer__static {
  display: inline-block;
}

@media (prefers-reduced-motion: reduce) {
  .odometer__strip {
    transition: none !important;
  }
}
</style>
