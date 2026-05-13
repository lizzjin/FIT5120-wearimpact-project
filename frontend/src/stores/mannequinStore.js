/**
 * Epic 3.6 — Mannequin selection (Try-On).
 *
 * The project does not pull in Pinia for one small piece of state, so
 * this module just exposes a singleton reactive ref backed by
 * localStorage. Components import `mannequinStore.selected` and read it
 * straight; the store re-hydrates on first import.
 *
 * Tryon result images are persisted in IndexedDB (see wardrobeDb.js
 * `tryon_cache` table) so a single garment + mannequin combination
 * survives reloads without bloating localStorage past its 5 MB cap.
 */
import { reactive, watch } from 'vue'

const STORAGE_KEY = 'wearimpact.mannequin.v1'

const DEFAULT_SELECTION = { category: 'Female', filename: 'model-03.png' }

function loadInitial() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return { ...DEFAULT_SELECTION }
    const parsed = JSON.parse(raw)
    if (parsed && typeof parsed.category === 'string' && typeof parsed.filename === 'string') {
      return parsed
    }
  } catch {
    // localStorage may be disabled (private mode / quota) — fall back silently.
  }
  return { ...DEFAULT_SELECTION }
}

export const mannequinStore = reactive({
  selected: loadInitial()
})

watch(
  () => mannequinStore.selected,
  (val) => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(val))
    } catch {
      // Ignore; selection still works in-memory.
    }
  },
  { deep: true }
)

export function setMannequin({ category, filename }) {
  mannequinStore.selected = { category, filename }
}

export function getMannequinImageUrl(selection) {
  if (!selection) return ''
  return `/person-models/${selection.category}/${selection.filename}`
}
