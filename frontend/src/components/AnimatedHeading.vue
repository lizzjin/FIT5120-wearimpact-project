<template>
  <component
    :is="as"
    class="animated-heading"
    :class="{ 'is-flip': mode === 'flip' }"
    ref="rootRef"
  >
    <template v-if="lines && lines.length">
      <span
        v-for="(line, i) in lines"
        :key="i"
        :ref="(el) => setLineRef(el, i)"
        class="animated-heading__line"
      >{{ line }}</span>
    </template>
    <template v-else>
      <slot>{{ text }}</slot>
    </template>
  </component>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { gsap } from 'gsap'
import { ScrollTrigger, ensurePlugins } from '../motion/registry'
import { isReduced } from '../motion/matchMedia'
import { splitElement } from '../motion/composables/useTextSplit'

// Word-mask reveal heading. Three input shapes:
//  - text="..."        : plain string, single line
//  - lines=[...]       : explicit multi-line strings (each line is a span)
//  - <slot>...</slot>  : arbitrary inline markup (<strong>, <em>, <span>, <br>)
//                        — SplitText handles inline tags natively.
//
// mode='word' (default) : each word rises from yPercent:110 (mask reveal).
// mode='flip'           : each word *flips down from above* on a 3D rotateX
//                         (-85deg → 0). Used as the home hero "wow" entrance.
//
// Optional "paint" colour stagger (set paintFrom to enable):
//   paintFrom → paintTo, line-by-line, kicks in after the word-mask lands.
const props = defineProps({
  as: { type: String, default: 'h2' },
  text: { type: String, default: '' },
  lines: { type: Array, default: null },
  mode: { type: String, default: 'word' }, // 'word' | 'flip'
  start: { type: String, default: 'top 85%' },
  stagger: { type: Number, default: 0.07 },
  delay: { type: Number, default: 0 },
  duration: { type: Number, default: 0.95 },
  replay: { type: Boolean, default: false },
  paintFrom: { type: String, default: null },
  paintTo: { type: String, default: '#0e0f0c' },
  paintStagger: { type: Number, default: 0.06 },
  paintDuration: { type: Number, default: 0.55 },
  paintDelay: { type: Number, default: null },
  paintLineGap: { type: Number, default: null },
})

const rootRef = ref(null)
const lineRefs = ref([])
function setLineRef(el, i) { if (el) lineRefs.value[i] = el }

let trigger = null
let splits = []
// Per-line arrays of inner word spans, used so the colour sweep can run
// left→right inside each line and then hand off to the next line.
let linesInners = []

onMounted(() => {
  ensurePlugins()
  const root = rootRef.value
  if (!root) return

  if (isReduced()) {
    root.style.opacity = '1'
    if (props.paintFrom) {
      const t = props.lines && props.lines.length ? lineRefs.value.filter(Boolean) : [root]
      t.forEach((el) => (el.style.color = props.paintTo))
    }
    return
  }

  // Flip mode rotates each word as a 3D card; the mask would clip the
  // rotated arc, so the word splitter must NOT add a mask wrapper. Plain
  // word mode uses mask: 'words' for the overflow-clip reveal effect.
  const splitOpts = props.mode === 'flip'
    ? { type: 'words' }
    : { type: 'words', mask: 'words' }

  let allInners = []
  let paintTargets = []

  if (props.lines && props.lines.length) {
    lineRefs.value.filter(Boolean).forEach((el) => {
      const split = splitElement(el, splitOpts)
      splits.push(split)
      allInners.push(...split.words)
      linesInners.push(split.words)
    })
    paintTargets = lineRefs.value.filter(Boolean)
  } else {
    // Slot (arbitrary inline markup) or `text` prop. SplitText preserves
    // inline elements (<strong>, <em>, <br>) automatically.
    const split = splitElement(root, splitOpts)
    splits.push(split)
    allInners = split.words
    linesInners = [split.words]
    paintTargets = [root]
  }

  if (!allInners.length) return

  const initial = props.mode === 'flip'
    ? { rotateX: -85, yPercent: 60, opacity: 0, transformOrigin: '50% 0%' }
    : { yPercent: 110 }

  const animated = props.mode === 'flip'
    ? { rotateX: 0, yPercent: 0, opacity: 1, duration: props.duration, stagger: props.stagger, delay: props.delay, ease: 'power3.out' }
    : { yPercent: 0, duration: props.duration, stagger: props.stagger, delay: props.delay, ease: 'power3.out' }

  gsap.set(allInners, initial)
  if (props.paintFrom) {
    paintTargets.forEach((el) => { el.style.color = props.paintFrom })
  }

  const autoPaintDelay = props.delay + props.duration * 0.6
  const paintStart = props.paintDelay !== null ? props.paintDelay : autoPaintDelay

  const play = () => {
    gsap.to(allInners, animated)
    if (props.paintFrom && linesInners.length) {
      const tl = gsap.timeline({ delay: paintStart })
      tl.set(paintTargets, { color: props.paintFrom })
      tl.set(allInners, { clearProps: 'color' }, 0)

      linesInners.forEach((inners, idx) => {
        if (!inners.length) return
        const sweepLength = inners.length * props.paintStagger + props.paintDuration
        const autoLineGap = -Math.min(props.paintDuration * 0.45, sweepLength * 0.25)
        const offset = idx === 0
          ? 0
          : (props.paintLineGap !== null ? `>${props.paintLineGap}` : `>${autoLineGap}`)
        tl.to(inners, {
          color: props.paintTo,
          duration: props.paintDuration,
          stagger: props.paintStagger,
          ease: 'power2.out',
        }, offset)
      })
    }
  }

  const reset = () => {
    gsap.set(allInners, initial)
    if (props.paintFrom) {
      gsap.set(allInners, { clearProps: 'color' })
      paintTargets.forEach((el) => { el.style.color = props.paintFrom })
    }
  }

  trigger = ScrollTrigger.create({
    trigger: root,
    start: props.start,
    once: !props.replay,
    onEnter: play,
    onEnterBack: props.replay ? play : undefined,
    onLeave: props.replay ? reset : undefined,
    onLeaveBack: props.replay ? reset : undefined,
  })
})

onBeforeUnmount(() => {
  trigger?.kill?.()
  splits.forEach((s) => s.revert())
  splits = []
  linesInners = []
})
</script>

<style scoped>
.animated-heading {
  margin: 0;
}
.animated-heading__line {
  display: block;
}

/* SplitText with mask:'words' produces:
     <span class="split-word-mask">  ← mask wrapper, overflow:clip auto
       <span class="split-word">     ← animation target (yPercent here)
   The mask wrapper needs inline-block + line-height so the word baseline
   matches the heading; .split-word stays inline-block so transforms apply. */
.animated-heading :deep(.split-word-mask) {
  display: inline-block;
  vertical-align: top;
  line-height: 1.05;
  padding-bottom: 0.05em;
}
.animated-heading :deep(.split-word) {
  display: inline-block;
  will-change: transform;
}

.animated-heading.is-flip {
  /* Enable 3D depth for the flip mode so rotateX on each word renders in
     perspective rather than collapsed. */
  perspective: 1200px;
  transform-style: preserve-3d;
}
/* flip mode does not use mask, so the .split-word-mask rule never matches.
   The flipping card itself needs preserved 3D and a steady back-face. */
.animated-heading.is-flip :deep(.split-word) {
  transform-style: preserve-3d;
  backface-visibility: hidden;
}
</style>
