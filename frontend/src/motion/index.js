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
export { ensurePlugins, gsap, ScrollTrigger } from './registry'
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
