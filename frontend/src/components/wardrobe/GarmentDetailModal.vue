<template>
  <DialogRoot :open="open" @update:open="(v) => { if (!v) $emit('close') }">
    <DialogPortal>
      <DialogOverlay class="wd-modal__backdrop" />
      <DialogContent class="wd-modal__panel" aria-describedby="wd-garment-detail-desc">
        <DialogTitle class="sr-only">Garment detail</DialogTitle>
        <DialogDescription id="wd-garment-detail-desc" class="sr-only">
          Photo, washing label, subcategory and actions for the selected garment.
        </DialogDescription>

        <GarmentDetailPanel
          :garment="displayGarment"
          @close="$emit('close')"
          @delete="onDelete"
          @refresh="$emit('refresh')"
          @try-on="onTryOn"
        />
      </DialogContent>
    </DialogPortal>
  </DialogRoot>
</template>

<script setup>
import { ref, watch, onBeforeUnmount } from 'vue'
import {
  DialogContent, DialogDescription, DialogOverlay, DialogPortal, DialogRoot, DialogTitle,
} from 'radix-vue'
import GarmentDetailPanel from './GarmentDetailPanel.vue'
import { getLenis } from '../../motion'

const props = defineProps({
  open: { type: Boolean, default: false },
  garment: { type: Object, default: null },
})
const emit = defineEmits(['close', 'delete', 'refresh', 'try-on'])

// Hold on to the last non-null garment so the close animation doesn't
// flash the GarmentDetailPanel's "Pick a piece" empty state. The parent
// flips both `garment` and `open` to null/false at the same tick, so
// without this cache the panel re-renders as the placeholder for the
// ~220ms exit animation. We only update on non-null inputs; when the
// modal next opens with a different garment the new one replaces this.
const displayGarment = ref(props.garment)
watch(
  () => props.garment,
  (g) => { if (g) displayGarment.value = g },
)

// While the modal is open Lenis keeps reacting to wheel input and scrolling
// the page behind the blurred backdrop, which looks broken. radix-vue's
// built-in body-scroll lock sets `overflow: hidden` on body but Lenis runs
// its own wheel handler that ignores that. Stop Lenis while open, resume on
// close. `getLenis()` returns null on touch / reduced-motion (Lenis is
// disabled in those environments) so the guard handles those branches too.
watch(() => props.open, (isOpen) => {
  const lenis = getLenis()
  if (!lenis) return
  if (isOpen) lenis.stop()
  else lenis.start()
})

onBeforeUnmount(() => {
  // Defensive: if the modal unmounts while still open (e.g. route change),
  // make sure Lenis is re-armed so the next page can scroll.
  getLenis()?.start()
})

function onDelete(id) {
  emit('delete', id)
}

function onTryOn(garment) {
  emit('try-on', garment)
}
</script>

<style scoped>
.sr-only {
  position: absolute;
  width: 1px; height: 1px;
  padding: 0; margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.wd-modal__backdrop {
  position: fixed; inset: 0;
  background: rgba(14, 15, 12, 0.42);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  z-index: 200;
}

/* radix-vue toggles data-state on enter/exit. Hooking animations to those
   states (instead of a one-shot on mount) gives us a real close animation,
   not a jump-cut. */
.wd-modal__backdrop[data-state="open"] {
  animation: wd-modal-fade-in 240ms cubic-bezier(0.22, 1, 0.36, 1);
}
.wd-modal__backdrop[data-state="closed"] {
  animation: wd-modal-fade-out 200ms cubic-bezier(0.55, 0, 0.78, 0.4);
}

.wd-modal__panel {
  position: fixed; top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  width: calc(100% - 48px);
  max-width: 480px;
  max-height: 88vh;
  background: var(--color-soft-cream);
  border: 1.5px solid var(--color-soft-line-strong);
  border-radius: var(--radius-soft-lg);
  overflow: hidden;
  /* Belt-and-braces: even though .wd-detail__scroll inside already declares
     contain, mirror it on the panel itself so a wheel landing in the
     non-scrollable header/footer area can't chain to <html> either. */
  overscroll-behavior: contain;
  display: flex; flex-direction: column;
  z-index: 201;
  box-shadow: var(--shadow-modal);
  /* Keep transform-origin centered so the scale tweak grows from the middle,
     not the top-left, even though `translate(-50%, -50%)` is on the element. */
  will-change: transform, opacity;
}

.wd-modal__panel[data-state="open"] {
  animation: wd-modal-scale-in 320ms cubic-bezier(0.34, 1.4, 0.64, 1);
}
.wd-modal__panel[data-state="closed"] {
  animation: wd-modal-scale-out 220ms cubic-bezier(0.55, 0, 0.78, 0.4);
}

@keyframes wd-modal-fade-in {
  from { opacity: 0; }
  to   { opacity: 1; }
}
@keyframes wd-modal-fade-out {
  from { opacity: 1; }
  to   { opacity: 0; }
}
@keyframes wd-modal-scale-in {
  from {
    opacity: 0;
    transform: translate(-50%, -46%) scale(0.92);
  }
  to {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1);
  }
}
@keyframes wd-modal-scale-out {
  from {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1);
  }
  to {
    opacity: 0;
    transform: translate(-50%, -48%) scale(0.96);
  }
}

@media (prefers-reduced-motion: reduce) {
  .wd-modal__backdrop[data-state="open"],
  .wd-modal__backdrop[data-state="closed"],
  .wd-modal__panel[data-state="open"],
  .wd-modal__panel[data-state="closed"] {
    animation-duration: 1ms;
  }
}

/* GarmentDetailPanel already owns its own inner scroll (.wd-detail__scroll
   with data-lenis-prevent) so we don't need to add another scroller here.
   Make sure the embedded panel fills the flex parent. */
.wd-modal__panel :deep(.wd-detail) {
  flex: 1;
  min-height: 0;
}

@media (max-width: 640px) {
  .wd-modal__panel {
    width: calc(100% - 24px);
    max-height: 92vh;
  }
}
</style>
