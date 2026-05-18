/**
 * Public motion API. Import from './motion' (or '../motion') anywhere in
 * the codebase so internal file paths stay private.
 *
 * Phase 1 surface:
 *   - ensurePlugins()       register GSAP plugins once at app boot
 *   - tokens                DUR / EASE / STAGGER / Y plus entrance()
 *   - scrollManager         armScrollTriggers / onRouteSettled / refreshNow
 *   - matchMedia            motionMatch / isReduced / isTouch / QUERIES
 *   - useGsapContext        component-scoped GSAP cleanup
 *
 * Later phases add useReveal, useStagger, useTextSplit, useScrub,
 * useHover, useFocusRing, useModal, useDrawer, useTabIndicator,
 * useDropdown, useTooltip, useToast, useAccordion, useChip,
 * useFlipReorder, useDragInteract, useCarouselSlide, useMapMarker,
 * useNavbarScroll, useImageReveal, useSkeletonShimmer.
 */
export {
  ensurePlugins,
  gsap,
  ScrollTrigger,
  SplitText,
  Flip,
  Draggable,
  InertiaPlugin,
} from './registry'
export {
  DUR,
  EASE,
  STAGGER,
  Y,
  entrance,
  entranceLg,
  resetTokenCache,
} from './tokens'
export {
  armScrollTriggers,
  onRouteSettled,
  refreshNow,
} from './scrollManager'
export {
  motionMatch,
  isReduced,
  isTouch,
  killMatchMedia,
  QUERIES,
} from './matchMedia'
export { useGsapContext } from './composables/useGsapContext'
export { splitElement, useTextSplit } from './composables/useTextSplit'
export { useReveal } from './useReveal'
export { useStagger } from './useStagger'
// Phase 6 — interaction primitives
export { useHover } from './composables/useHover'
export { useFocusRing } from './composables/useFocusRing'
export { useRipple } from './composables/useRipple'
export { useShake } from './composables/useShake'
export { useToast, provideToast } from './composables/useToast'
export { useConfirm, getConfirmStore } from './composables/useConfirm'
// Phase 7 — composite interaction primitives
export { useModal } from './composables/useModal'
export { useDrawer } from './composables/useDrawer'
export { useTabIndicator } from './composables/useTabIndicator'
export { useDropdown } from './composables/useDropdown'
export { useTooltip } from './composables/useTooltip'
export { useChip } from './composables/useChip'
export { useAccordion } from './composables/useAccordion'
export { useFlipReorder } from './composables/useFlipReorder'
export { useDragInteract } from './composables/useDragInteract'
export { useCarouselSlide } from './composables/useCarouselSlide'
export { useMapMarker } from './composables/useMapMarker'
export { useNavbarScroll } from './composables/useNavbarScroll'
export { useImageReveal } from './composables/useImageReveal'
export { useSkeletonShimmer } from './composables/useSkeletonShimmer'
export {
  startLenis,
  stopLenis,
  getLenis,
  scrollToTopImmediate,
} from './lenis'
