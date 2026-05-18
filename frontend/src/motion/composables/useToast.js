/**
 * Toast queue primitive — single source of truth for ephemeral feedback
 * (upload success / API error / cache cleared / etc.).
 *
 * Architecture: `provideToast()` creates a reactive queue + push/dismiss
 * functions and provides them at the app root via Vue's provide/inject.
 * `useToast()` injects the API for any descendant component.
 *
 *   // In ToastHost.vue (mounted once in App.vue):
 *   const { toasts, dismiss } = provideToast()
 *
 *   // Anywhere else:
 *   const { push } = useToast()
 *   push('Upload complete', { type: 'success' })
 *   push('Network error', { type: 'error', timeout: 6000 })
 *
 * Toasts auto-dismiss after `timeout` ms (default 4000). type is a free
 * string; ToastHost styles `success | error | info | warning` by class.
 */
import { ref, provide, inject } from 'vue'

const TOAST_KEY = Symbol('motion-toast')

export function provideToast() {
  const toasts = ref([])
  let nextId = 0

  function push(message, options = {}) {
    const toast = {
      id: ++nextId,
      message,
      type: options.type || 'info',
      timeout: options.timeout ?? 4000,
    }
    toasts.value.push(toast)
    if (toast.timeout > 0) {
      setTimeout(() => dismiss(toast.id), toast.timeout)
    }
    return toast.id
  }

  function dismiss(id) {
    const idx = toasts.value.findIndex((t) => t.id === id)
    if (idx >= 0) toasts.value.splice(idx, 1)
  }

  const api = { toasts, push, dismiss }
  provide(TOAST_KEY, api)
  return api
}

export function useToast() {
  const api = inject(TOAST_KEY, null)
  if (!api) {
    // Fallback when no ToastHost is mounted: silent no-op so call sites
    // never throw, even in storybook/test contexts.
    return {
      toasts: ref([]),
      push: () => 0,
      dismiss: () => {},
    }
  }
  return api
}
