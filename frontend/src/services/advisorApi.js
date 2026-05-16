/**
 * Epic 3 wardrobe sustainability advisor — frontend API client.
 *
 * Talks to the FastAPI backend at:
 *   - GET  /api/wardrobe/preset-questions
 *   - POST /api/wardrobe/audit
 *   - POST /api/wardrobe/advice/follow-up
 *
 * Garments are sent stripped of any personal metadata (filename, image_base64,
 * timestamps). The backend only needs the classified labels to compute facts;
 * sending less keeps prompts small and avoids accidentally surfacing user data
 * in LLM logs.
 */

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

/**
 * Fetch the catalogue of preset questions the user can pick.
 * @returns {Promise<Array<{key:string,label:string,description:string,layout:string}>>}
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

async function readErrorDetail(res) {
  try {
    return (await res.json())?.detail || ''
  } catch {
    return ''
  }
}

function mapAdvisorError(res, detail) {
  if (res.status === 503) {
    return new Error(detail || 'The AI advisor is temporarily unavailable. Please try again shortly.')
  }
  if (res.status === 429) {
    return new Error(detail || 'You\'ve asked a lot just now — please wait a moment before trying again.')
  }
  if (res.status === 422) {
    return new Error(detail || 'Your wardrobe payload was rejected. Try refreshing and retrying.')
  }
  return new Error(detail || `Advisor request failed (HTTP ${res.status}).`)
}

/**
 * Run a wardrobe audit and return the structured advice.
 *
 * @param {Array} garments  Items from IndexedDB (full Dexie records).
 * @param {string} preset   One of the keys returned by fetchPresetQuestions().
 * @param {object} [opts]
 * @param {boolean} [opts.forceRefresh=false]  Bypass server cache so Claude
 *   generates a fresh answer. Used by the "Re-answer this" button on each
 *   advice bubble to break the cached-feels-canned perception.
 * @returns {Promise<Advice>}
 */
export async function fetchWardrobeAdvice(garments, preset, { forceRefresh = false } = {}) {
  const payload = {
    preset,
    garments: garments.map(toAuditItem),
  }

  const url = forceRefresh
    ? `${API_BASE}/api/wardrobe/audit?refresh=1`
    : `${API_BASE}/api/wardrobe/audit`

  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })

  if (!res.ok) {
    throw mapAdvisorError(res, await readErrorDetail(res))
  }

  return res.json()
}

/**
 * Ask Claude a follow-up question grounded in the user's wardrobe + a parent
 * preset answer. Returns a compact FollowUpAdvice rendered as a mini-bubble.
 *
 * @param {Array} garments         Same shape as fetchWardrobeAdvice.
 * @param {string} parentPreset    The preset key the user originally asked.
 * @param {string} focus           Slug of the recommendation tapped, or ''.
 * @param {string} subPrompt       The human-readable follow-up question text.
 * @returns {Promise<FollowUpAdvice>}
 */
export async function fetchAdviceFollowUp(garments, parentPreset, focus, subPrompt) {
  const payload = {
    garments: garments.map(toAuditItem),
    parent_preset: parentPreset,
    focus: focus || '',
    sub_prompt: subPrompt,
  }

  const res = await fetch(`${API_BASE}/api/wardrobe/advice/follow-up`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })

  if (!res.ok) {
    throw mapAdvisorError(res, await readErrorDetail(res))
  }

  return res.json()
}
