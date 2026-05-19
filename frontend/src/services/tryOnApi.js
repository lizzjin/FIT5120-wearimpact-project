/**
 * Epic 3.6 — WearImpact Try-On client.
 *
 * Talks to the Gradio Space at VITE_TRYON_SERVICE_URL through
 * `@gradio/client`. Inputs are derived entirely from the garment record
 * already sitting in IndexedDB (the classifier wrote `main_category`,
 * `sub_category`, and a transparent-PNG `image_base64` at upload time),
 * so the try-on service never re-runs classification.
 */
import { Client } from '@gradio/client'

const TRYON_URL = import.meta.env.VITE_TRYON_SERVICE_URL || ''
const HF_TOKEN = import.meta.env.VITE_HF_TOKEN || ''

let clientPromise = null

function getClient() {
  if (!TRYON_URL) {
    return Promise.reject(new Error('VITE_TRYON_SERVICE_URL is not configured'))
  }
  if (!clientPromise) {
    // Passing `hf_token` makes ZeroGPU bill the call to the caller's HF
    // quota (Pro = 8× free). Without it the call lands in the anonymous
    // pool, which gets exhausted in minutes during demo testing.
    const opts = HF_TOKEN ? { hf_token: HF_TOKEN } : undefined
    clientPromise = Client.connect(TRYON_URL, opts).catch((err) => {
      // Clear the cached promise so a transient cold-start failure
      // doesn't permanently break try-on for this session.
      clientPromise = null
      throw err
    })
  }
  return clientPromise
}

function unwrapPrediction(result) {
  if (!result) {
    throw new Error('Empty response from try-on service')
  }
  // gradio-client returns { data: [...] } where each element matches the
  // function's return position. Our Gradio APIs return a single dict.
  const payload = Array.isArray(result.data) ? result.data[0] : result.data
  if (!payload) {
    throw new Error('Try-on service returned no payload')
  }
  if (payload.ok === false) {
    throw new Error(payload.error || 'Try-on service rejected the request')
  }
  return payload
}

/**
 * Run a single-garment try-on. Throws on validation failure or server
 * error; returns the data-URL `result_image` on success.
 */
export async function tryOnSingle({ mannequin, garment }) {
  if (!mannequin?.category || !mannequin?.filename) {
    throw new Error('Pick a mannequin first.')
  }
  if (!garment) {
    throw new Error('No garment selected.')
  }
  if (garment.main_category === 'footwear') {
    throw new Error('FASHN VTON v1.5 does not support footwear try-on yet.')
  }
  if (!garment.image_base64) {
    throw new Error('This garment has no cut-out image; re-upload it to enable try-on.')
  }

  const client = await getClient()
  const result = await client.predict('/try_on_single', [
    mannequin.category,
    mannequin.filename,
    garment.image_base64,
    garment.main_category,
    garment.sub_category || ''
  ])
  return unwrapPrediction(result)
}

export async function tryOnOutfit({ mannequin, upperGarment, lowerGarment }) {
  if (!mannequin?.category || !mannequin?.filename) {
    throw new Error('Pick a mannequin first.')
  }
  if (!upperGarment && !lowerGarment) {
    throw new Error('Select at least one upper-body or lower-body item.')
  }

  const client = await getClient()
  const result = await client.predict('/try_on_outfit', [
    mannequin.category,
    mannequin.filename,
    upperGarment?.image_base64 || '',
    upperGarment?.sub_category || '',
    lowerGarment?.image_base64 || '',
    lowerGarment?.sub_category || ''
  ])
  return unwrapPrediction(result)
}

export function tryOnCacheKey(garmentId, mannequin) {
  if (!garmentId || !mannequin?.category || !mannequin?.filename) return ''
  return `${garmentId}::${mannequin.category}/${mannequin.filename}`
}

export function tryOnOutfitCacheKey({ upperId, lowerId, mannequin }) {
  if (!mannequin?.category || !mannequin?.filename) return ''
  if (upperId == null && lowerId == null) return ''
  const u = upperId ?? 'none'
  const l = lowerId ?? 'none'
  return `outfit::${u}+${l}::${mannequin.category}/${mannequin.filename}`
}
