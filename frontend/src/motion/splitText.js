/**
 * Word/char splitter modelled on shelby.ashfall.studio's hero markup: each
 * word is wrapped in a double span — outer is the overflow:hidden mask,
 * inner is the element GSAP translates. Pure DOM, zero deps.
 *
 * - splitText(el, 'word' | 'char') — for plain-text headings/eyebrows.
 * - splitInlineHTML(el)            — when the heading contains <strong>,
 *   <em>, <span class="*-accent">, <br> etc. Walks the DOM and splits each
 *   text node in place, preserving inline structure.
 * - revert(el)                     — restore the original text.
 */

const REDUCED = () =>
  typeof window !== 'undefined' &&
  window.matchMedia('(prefers-reduced-motion: reduce)').matches

function buildWord(word) {
  const outer = document.createElement('span')
  outer.className = 'split-word'
  outer.setAttribute('aria-hidden', 'true')
  outer.style.cssText =
    'display:inline-block;overflow:hidden;vertical-align:top;line-height:1.05;padding-bottom:0.05em;'

  const inner = document.createElement('span')
  inner.className = 'split-word__inner'
  inner.style.cssText = 'display:inline-block;will-change:transform;'
  inner.textContent = word

  outer.appendChild(inner)
  return { outer, inner }
}

function buildChar(ch) {
  const span = document.createElement('span')
  span.className = 'split-char'
  span.setAttribute('aria-hidden', 'true')
  span.style.cssText = 'display:inline-block;will-change:transform,opacity;'
  span.textContent = ch
  return span
}

export function splitText(el, mode = 'word') {
  if (!el) return emptyResult()
  if (el.dataset.split) return readExisting(el)

  const original = el.innerHTML
  const text = el.textContent || ''
  if (!el.getAttribute('aria-label')) {
    el.setAttribute('aria-label', text.trim())
  }
  el.dataset.splitOriginal = original
  el.dataset.split = mode
  el.innerHTML = ''

  const words = []
  const chars = []
  const inners = []

  const tokens = text.split(/(\s+)/)
  tokens.forEach((tok) => {
    if (tok === '') return
    if (/^\s+$/.test(tok)) {
      el.appendChild(document.createTextNode(tok))
      return
    }
    if (mode === 'char') {
      const wordWrap = document.createElement('span')
      wordWrap.className = 'split-word'
      wordWrap.setAttribute('aria-hidden', 'true')
      wordWrap.style.cssText = 'display:inline-block;'
      ;[...tok].forEach((ch) => {
        const c = buildChar(ch)
        chars.push(c)
        wordWrap.appendChild(c)
      })
      words.push(wordWrap)
      el.appendChild(wordWrap)
    } else {
      const { outer, inner } = buildWord(tok)
      words.push(outer)
      inners.push(inner)
      el.appendChild(outer)
    }
  })

  return { words, chars, inners, revert: () => revert(el) }
}

/**
 * Walks an element's tree and splits each text node into word masks,
 * keeping inline elements (<strong>, <em>, <span>, <br>) intact. The same
 * GSAP timeline can drive `inners` regardless of how the heading is marked
 * up — i.e. a heading like <h1>Your closet,<br><span>made visible.</span></h1>
 * still rises word-by-word.
 */
export function splitInlineHTML(el) {
  if (!el) return emptyResult()
  if (el.dataset.split === 'inline') return readExisting(el)

  const original = el.innerHTML
  if (!el.getAttribute('aria-label')) {
    el.setAttribute('aria-label', (el.textContent || '').trim())
  }
  el.dataset.splitOriginal = original
  el.dataset.split = 'inline'

  const words = []
  const inners = []

  const walk = (node) => {
    const children = Array.from(node.childNodes)
    children.forEach((child) => {
      if (child.nodeType === Node.TEXT_NODE) {
        const text = child.textContent || ''
        if (!text.trim()) return
        const frag = document.createDocumentFragment()
        const tokens = text.split(/(\s+)/)
        tokens.forEach((tok) => {
          if (tok === '') return
          if (/^\s+$/.test(tok)) {
            frag.appendChild(document.createTextNode(tok))
            return
          }
          const { outer, inner } = buildWord(tok)
          words.push(outer)
          inners.push(inner)
          frag.appendChild(outer)
        })
        child.parentNode.replaceChild(frag, child)
      } else if (child.nodeType === Node.ELEMENT_NODE) {
        if (child.tagName === 'BR') return
        walk(child)
      }
    })
  }

  walk(el)
  return { words, chars: [], inners, revert: () => revert(el) }
}

function readExisting(el) {
  return {
    words: Array.from(el.querySelectorAll('.split-word')),
    chars: Array.from(el.querySelectorAll('.split-char')),
    inners: Array.from(el.querySelectorAll('.split-word__inner')),
    revert: () => revert(el),
  }
}

export function revert(el) {
  if (!el || !el.dataset.split) return
  el.innerHTML = el.dataset.splitOriginal || ''
  delete el.dataset.split
  delete el.dataset.splitOriginal
}

function emptyResult() {
  return { words: [], chars: [], inners: [], revert: () => {} }
}

export { REDUCED as prefersReducedMotion }
