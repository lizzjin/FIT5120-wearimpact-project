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
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { splitText, splitInlineHTML, revert, prefersReducedMotion } from '../motion/splitText'

// Word-mask reveal heading. Three input shapes:
//  - text="..."        : plain string, single line
//  - lines=[...]       : explicit multi-line strings (each line is a span)
//  - <slot>...</slot>  : arbitrary inline markup (<strong>, <em>, <span>, <br>)
//                        — auto-handled via splitInlineHTML.
//
// mode='word' (default) : each word rises from yPercent:110 (mask reveal).
// mode='flip'           : each word *flips down from above* on a 3D rotateX
//                         (-85deg → 0). Used as the home hero "wow" entrance.
//
// Optional "paint" colour stagger (set paintFrom to enable):
//   paintFrom → paintTo, line-by-line, kicks in after the word-mask lands.
//   Used on /eco-shop hero so the title visibly shifts from brand lime to
//   final ink, one line at a time — Shelby-style chromatic rhythm.
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
  // Per-word stagger inside one line — drives the left→right sweep speed.
  paintStagger: { type: Number, default: 0.06 },
  paintDuration: { type: Number, default: 0.55 },
  paintDelay: { type: Number, default: null }, // null → auto = delay + duration * 0.6
  // Pause between line N's sweep finishing and line N+1's sweep starting.
  // Negative values overlap the sweeps. null → auto: tiny overlap so the
  // baton hands off naturally line-to-line.
  paintLineGap: { type: Number, default: null },
})

const rootRef = ref(null)
const lineRefs = ref([])
function setLineRef(el, i) { if (el) lineRefs.value[i] = el }

let trigger = null
let revertTargets = []
let paintTargets = []
// Per-line arrays of inner word spans, used so the colour sweep can run
// left→right inside each line and then hand off to the next line.
let linesInners = []

onMounted(() => {
  const root = rootRef.value
  if (!root) return

  if (prefersReducedMotion()) {
    root.style.opacity = '1'
    if (props.paintFrom) {
      // Settle straight to the destination colour, no transition.
      const t = props.lines && props.lines.length ? lineRefs.value.filter(Boolean) : [root]
      t.forEach((el) => (el.style.color = props.paintTo))
    }
    return
  }

  let allInners = []

  if (props.lines && props.lines.length) {
    lineRefs.value.filter(Boolean).forEach((el) => {
      const { inners } = splitText(el, 'word')
      allInners.push(...inners)
      linesInners.push(inners)
      revertTargets.push(el)
    })
    paintTargets = lineRefs.value.filter(Boolean)
  } else {
    // slot (arbitrary inline markup) or `text` prop — split via inline walker.
    const { inners } = splitInlineHTML(root)
    allInners = inners
    linesInners = [inners]
    revertTargets.push(root)
    paintTargets = [root]
  }

  if (!allInners.length) return

  // Initial / animated states differ by mode. flip overrides yPercent with a
  // 3D rotateX so each word looks like a card flipping down from the top.
  const initial = props.mode === 'flip'
    ? { rotateX: -85, yPercent: 60, opacity: 0, transformOrigin: '50% 0%' }
    : { yPercent: 110 }

  const animated = props.mode === 'flip'
    ? { rotateX: 0, yPercent: 0, opacity: 1, duration: props.duration, stagger: props.stagger, delay: props.delay, ease: 'power3.out' }
    : { yPercent: 0, duration: props.duration, stagger: props.stagger, delay: props.delay, ease: 'power3.out' }

  gsap.set(allInners, initial)
  // Paint the lines immediately (inline style) so the brand colour shows up
  // even before the ScrollTrigger fires on the first frame. Inner word spans
  // inherit this colour until the per-word tween overrides them one by one.
  if (props.paintFrom) {
    paintTargets.forEach((el) => { el.style.color = props.paintFrom })
  }

  // Auto-derive when paint should start: shortly after the word-mask is
  // visually at rest, so the colour tween reads as a separate beat.
  const autoPaintDelay = props.delay + props.duration * 0.6
  const paintStart = props.paintDelay !== null ? props.paintDelay : autoPaintDelay

  const play = () => {
    gsap.to(allInners, animated)
    if (props.paintFrom && linesInners.length) {
      // Build a single timeline so each line's colour sweep runs left→right
      // (per-word stagger) and the next line picks up the baton with a small
      // overlap. fromTo + delay sometimes collapses straight to the
      // destination because of GSAP's immediateRender behaviour, so we
      // sequence the colour from→to explicitly per scope.
      const tl = gsap.timeline({ delay: paintStart })
      tl.set(paintTargets, { color: props.paintFrom })
      // Reset any inline colour left on inner spans from a prior cycle.
      tl.set(allInners, { clearProps: 'color' }, 0)

      linesInners.forEach((inners, idx) => {
        if (!inners.length) return
        // Position each line's tween: line 0 starts immediately, then each
        // subsequent line starts a touch before the previous line's last
        // word finishes — so the sweep flows across line breaks.
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
      // Clear per-word colour overrides so the inherited from-colour shows
      // again on replay; then re-paint the line scope.
      gsap.set(allInners, { clearProps: 'color' })
      paintTargets.forEach((el) => { el.style.color = props.paintFrom })
    }
  }

  trigger = ScrollTrigger.create({
    trigger: revertTargets[0] || root,
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
  revertTargets.forEach((el) => {
    if (el?.dataset?.split) revert(el)
  })
})
</script>

<style scoped>
.animated-heading {
  margin: 0;
}
.animated-heading__line {
  display: block;
}
.animated-heading.is-flip {
  /* Enable 3D depth for the flip mode so rotateX on each word is rendered in
     perspective rather than collapsed. */
  perspective: 1200px;
  transform-style: preserve-3d;
}
.animated-heading.is-flip :deep(.split-word) {
  /* Mask is no longer required for flip — overflow:hidden would clip the
     rotated card during the rotation arc. */
  overflow: visible;
}
.animated-heading.is-flip :deep(.split-word__inner) {
  transform-style: preserve-3d;
  backface-visibility: hidden;
}
</style>
