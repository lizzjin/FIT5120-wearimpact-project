/**
 * Text splitting backed by the official GSAP SplitText plugin. Replaces the
 * hand-built motion/splitText.js (162 lines of DOM walking) with the
 * battle-tested implementation that ships in the gsap npm package since
 * Webflow's acquisition made every plugin free.
 *
 * Two API shapes:
 *
 *   splitElement(el, opts) — imperative. Returns immediately with the
 *     split structure. Use from inside an existing onMounted, gsap.context,
 *     or any code that already owns its own DOM ref. HomeView and
 *     AnimatedHeading both call this form.
 *
 *   useTextSplit(elRef, opts) — composable. Splits on mount, reverts on
 *     unmount. Use when the only thing the component does with the split
 *     is reveal-on-scroll.
 *
 * The returned object preserves backward-compatible field names from the
 * old splitText.js:
 *   - chars   — per-character elements (when type includes 'chars')
 *   - words   — per-word elements (when type includes 'words')
 *   - lines   — per-line elements (when type includes 'lines')
 *   - masks   — overflow-clip wrappers (when `mask` is set)
 *   - inners  — alias for the animation target (words by default, chars
 *               when type is chars-only). Lets old call-sites that
 *               iterated `inners` keep working.
 *   - revert() — restore original markup.
 *   - instance — the underlying SplitText instance for advanced usage.
 *
 * Reduced-motion: if prefers-reduced-motion is on, returns an empty shape
 * with a no-op revert. Callers' `if (!inners.length) return` guards keep
 * working, so no text is ever wrapped in spans for users who opted out.
 */
import { onMounted, onBeforeUnmount } from 'vue'
import { SplitText, ensurePlugins } from '../registry'
import { isReduced } from '../matchMedia'

const EMPTY = Object.freeze({
  chars: [],
  words: [],
  lines: [],
  masks: [],
  inners: [],
  instance: null,
  revert: () => {},
})

function pickInners(instance, type) {
  if (type.includes('words')) return instance.words || []
  if (type.includes('chars')) return instance.chars || []
  if (type.includes('lines')) return instance.lines || []
  return []
}

export function splitElement(el, opts = {}) {
  if (!el) return EMPTY
  if (isReduced()) return EMPTY

  ensurePlugins()

  const {
    type = 'words',
    mask = false,
    wordsClass = 'split-word',
    charsClass = 'split-char',
    linesClass = 'split-line',
    tag = 'span',
    aria = 'auto',
    autoSplit = false,
    onSplit = null,
    ...rest
  } = opts

  const instance = SplitText.create(el, {
    type,
    mask,
    wordsClass,
    charsClass,
    linesClass,
    tag,
    aria,
    autoSplit,
    onSplit,
    ...rest,
  })

  return {
    chars: instance.chars || [],
    words: instance.words || [],
    lines: instance.lines || [],
    masks: instance.masks || [],
    inners: pickInners(instance, type),
    instance,
    revert: () => instance.revert(),
  }
}

export function useTextSplit(elRef, opts = {}) {
  let split = EMPTY

  onMounted(() => {
    const el = elRef?.value
    if (!el) return
    split = splitElement(el, opts)
  })

  onBeforeUnmount(() => {
    split.revert()
  })

  return {
    get chars() { return split.chars },
    get words() { return split.words },
    get lines() { return split.lines },
    get masks() { return split.masks },
    get inners() { return split.inners },
    get instance() { return split.instance },
  }
}
