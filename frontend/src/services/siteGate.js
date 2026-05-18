/**
 * Tiny client-side gate. NOT real auth — anyone with devtools can read the
 * password or flip the sessionStorage flag. The point is to keep the site
 * out of search engines and stop random visitors during demo time.
 *
 * To rotate the password: change SITE_PASSWORD here. There's nothing else.
 */

export const SITE_PASSWORD = 'wearimpact2026'

const STORAGE_KEY = 'wi_gate'
const UNLOCKED_VALUE = 'ok'

export function isUnlocked() {
  if (typeof window === 'undefined') return false
  try {
    return window.sessionStorage.getItem(STORAGE_KEY) === UNLOCKED_VALUE
  } catch {
    return false
  }
}

export function tryUnlock(input) {
  if (typeof input !== 'string') return false
  if (input.trim() !== SITE_PASSWORD) return false
  try {
    window.sessionStorage.setItem(STORAGE_KEY, UNLOCKED_VALUE)
  } catch {
    // sessionStorage might be blocked (private mode, etc.) — still let the
    // user in for the current page load even if we can't persist.
  }
  return true
}

export function lock() {
  try {
    window.sessionStorage.removeItem(STORAGE_KEY)
  } catch {
    /* ignore */
  }
}
