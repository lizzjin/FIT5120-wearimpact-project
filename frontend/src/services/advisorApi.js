/**
 * Epic 3 wardrobe sustainability advisor — frontend API client.
 *
 * Talks to the FastAPI backend at:
 *   - GET  /api/wardrobe/preset-questions
 *   - POST /api/wardrobe/audit
 *
 * Garments are sent stripped of any personal metadata (filename, image_base64,
 * timestamps). The backend only needs the classified labels to compute facts;
 * sending less keeps prompts small and avoids accidentally surfacing user data
 * in LLM logs.
 */

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

/**
 * Fetch the catalogue of preset questions the user can pick.
 * @returns {Promise<Array<{key:string,label:string,description:string}>>}
 */
export async function fetchPresetQuestions() {
  const res = await fetch(`${API_BASE}/api/wardrobe/preset-questions`)
  if (!res.ok) {
    throw new Error(`Failed to load preset questions (HTTP ${res.status}).`)
  }
  return res.json()
}

/**
 * Reduce a Dexie garment record to the minimal payload the backend needs.
 * @param {{ main_category: string, sub_category: string }} g
 */
function toAuditItem(g) {
  return { main_category: g.main_category, sub_category: g.sub_category }
}

/**
 * Run a wardrobe audit and return the structured advice.
 *
 * @param {Array} garments  Items from IndexedDB (full Dexie records).
 * @param {string} preset   One of the keys returned by fetchPresetQuestions().
 * @returns {Promise<Advice>}
 */
export async function fetchWardrobeAdvice(garments, preset) {
  const payload = {
    preset,
    garments: garments.map(toAuditItem),
  }

  const res = await fetch(`${API_BASE}/api/wardrobe/audit`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })

  if (!res.ok) {
    let detail = ''
    try {
      detail = (await res.json())?.detail || ''
    } catch {
      /* response body wasn't JSON; fall through to status-only message */
    }

    if (res.status === 503) {
      throw new Error(detail || 'The AI advisor is temporarily unavailable. Please try again shortly.')
    }
    if (res.status === 422) {
      throw new Error(detail || 'Your wardrobe payload was rejected. Try refreshing and retrying.')
    }
    throw new Error(detail || `Advisor request failed (HTTP ${res.status}).`)
  }

  return res.json()
}
