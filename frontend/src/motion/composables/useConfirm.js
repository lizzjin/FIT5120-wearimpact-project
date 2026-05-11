/**
 * Promise-based confirmation dialog API. Mirrors the ergonomics of
 * `window.confirm` but routes through the in-app ConfirmHost so the
 * dialog matches the brand surface + motion system rather than the
 * browser's native chrome.
 *
 *   const confirm = useConfirm()
 *   const ok = await confirm({
 *     title: 'Clear wardrobe',
 *     message: 'Delete every item? This cannot be undone.',
 *     confirmText: 'Delete all',
 *     danger: true,
 *   })
 *   if (!ok) return
 *
 * The store is module-level (singleton) because there is at most one
 * confirm dialog open at a time. ConfirmHost reads `state` to render and
 * calls `close(result)` to settle the pending promise.
 */
import { ref } from 'vue'

const state = ref(null)
let lastFocus = null

function show(options = {}) {
  return new Promise((resolve) => {
    // Remember where focus was so we can restore on close.
    lastFocus = typeof document !== 'undefined' ? document.activeElement : null
    state.value = {
      title: options.title || 'Are you sure?',
      message: options.message || '',
      confirmText: options.confirmText || 'Confirm',
      cancelText: options.cancelText || 'Cancel',
      danger: options.danger === true,
      resolve,
    }
  })
}

function close(result) {
  if (!state.value) return
  state.value.resolve(result)
  state.value = null
  // Restore focus to whoever opened the dialog.
  if (lastFocus && typeof lastFocus.focus === 'function') {
    lastFocus.focus()
  }
  lastFocus = null
}

/**
 * Returned function takes options and resolves to true (confirmed) or
 * false (cancelled / dismissed). Safe to call outside `setup()` because
 * the store is module-level.
 */
export function useConfirm() {
  return show
}

/** Internal — ConfirmHost reads state + dispatches close. */
export function getConfirmStore() {
  return { state, close }
}
