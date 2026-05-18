/**
 * Map marker entrance + click + selected-pulse primitive. Used by
 * EcoShopMap to give Mapbox markers a coordinated bounce when they
 * enter the map view, a click pulse, and an optional persistent pulse
 * for the currently selected marker.
 *
 *   const { enter, click, activate, deactivate } = useMapMarker()
 *   enter(markerEl, index)         // staggered bounce-in
 *   click(markerEl)                // scale 1 -> 1.2 -> 1
 *   activate(markerEl)             // start persistent pulse
 *   deactivate(markerEl)           // kill pulse
 */
import { gsap } from 'gsap'
import { ensurePlugins } from '../registry'
import { isReduced } from '../matchMedia'
import { EASE } from '../tokens'

const activeTweens = new WeakMap()

export function useMapMarker(options = {}) {
  const {
    enterDuration = 0.4,
    clickDuration = 0.35,
    pulseScale = 1.08,
    pulseDuration = 1.2,
  } = options

  ensurePlugins()

  function enter(el, index = 0) {
    if (!el || isReduced()) {
      if (el) gsap.set(el, { opacity: 1, scale: 1, y: 0 })
      return
    }
    gsap.fromTo(el,
      { opacity: 0, scale: 0, y: -8 },
      {
        opacity: 1,
        scale: 1,
        y: 0,
        duration: enterDuration,
        delay: index * 0.04,
        ease: EASE.spring,
      },
    )
  }

  function click(el) {
    if (!el || isReduced()) return
    gsap.fromTo(el,
      { scale: 1 },
      {
        scale: 1.2,
        duration: clickDuration / 2,
        ease: 'power2.out',
        yoyo: true,
        repeat: 1,
      },
    )
  }

  function activate(el) {
    if (!el || isReduced()) return
    deactivate(el) // ensure no stacking
    const tween = gsap.to(el, {
      scale: pulseScale,
      duration: pulseDuration,
      ease: 'sine.inOut',
      repeat: -1,
      yoyo: true,
    })
    activeTweens.set(el, tween)
  }

  function deactivate(el) {
    if (!el) return
    const tween = activeTweens.get(el)
    if (tween) {
      tween.kill()
      activeTweens.delete(el)
      gsap.set(el, { scale: 1 })
    }
  }

  return { enter, click, activate, deactivate }
}
