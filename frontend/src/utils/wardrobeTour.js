/**
 * Wardrobe onboarding tour — driver.js wrapper.
 *
 * Triggered once per browser (localStorage flag `wi_wardrobe_tour_done`) the
 * first time a user lands on WardrobeMain. Steps are filtered to only
 * include anchors that exist in the DOM, so a brand-new wardrobe (no
 * garments) doesn't try to spotlight tiles that haven't rendered yet.
 *
 * Styling overrides the default driver.js theme to match the project's
 * soft-paper magazine aesthetic (cream surfaces, sage primary, pill buttons).
 */
import { driver } from 'driver.js'
import 'driver.js/dist/driver.css'

const STORAGE_KEY = 'wi_wardrobe_tour_done'

const STEPS = [
  {
    selector: '[data-tour="live-count"]',
    popover: {
      title: 'Your closet at a glance',
      description:
        'A live count of every item in your wardrobe. Everything stays on your device — no cloud, no account.',
      side: 'right',
      align: 'start',
    },
  },
  {
    selector: '[data-tour="upload"]',
    popover: {
      title: 'Add clothes here',
      description:
        'Drop or browse photos of your clothes. Our AI auto-detects the category and (optionally) reads the wash-label to extract materials.',
      side: 'left',
      align: 'start',
    },
  },
  {
    selector: '[data-tour="categories"]',
    popover: {
      title: 'Auto-sorted by category',
      description:
        'Tops, one-pieces, bottoms, and shoes appear in their own tiles. Tap any item to see details, washing label, or remove it.',
      side: 'left',
      align: 'start',
    },
  },
  {
    selector: '[data-tour="tryon"]',
    popover: {
      title: 'Virtual try-on',
      description:
        'Pick an item from your closet and our AI dresses a mannequin in it. Try a top and a bottom together to preview a full outfit.',
      side: 'right',
      align: 'start',
    },
  },
]

function buildSteps() {
  return STEPS
    .filter((step) => document.querySelector(step.selector))
    .map((step) => ({
      element: step.selector,
      popover: step.popover,
    }))
}

let activeDriver = null

export function startWardrobeTour({ force = false } = {}) {
  if (typeof window === 'undefined') return
  if (!force && localStorage.getItem(STORAGE_KEY) === '1') return

  const steps = buildSteps()
  if (steps.length === 0) return

  // Tear down a previous instance if any (e.g. user re-triggers via help button).
  if (activeDriver) {
    try { activeDriver.destroy() } catch { /* ignore */ }
    activeDriver = null
  }

  activeDriver = driver({
    showProgress: true,
    progressText: '{{current}} / {{total}}',
    nextBtnText: 'Next',
    prevBtnText: 'Back',
    doneBtnText: 'Got it',
    overlayColor: 'rgba(58, 56, 51, 0.55)',
    overlayOpacity: 1,
    stagePadding: 8,
    stageRadius: 18,
    popoverClass: 'wi-tour-popover',
    onDestroyStarted: () => {
      localStorage.setItem(STORAGE_KEY, '1')
      activeDriver?.destroy()
    },
    steps,
  })

  // Defer one frame so layout settles before the spotlight is positioned.
  requestAnimationFrame(() => activeDriver?.drive())
}

export function hasSeenWardrobeTour() {
  if (typeof window === 'undefined') return true
  return localStorage.getItem(STORAGE_KEY) === '1'
}

export function resetWardrobeTour() {
  if (typeof window === 'undefined') return
  localStorage.removeItem(STORAGE_KEY)
}
