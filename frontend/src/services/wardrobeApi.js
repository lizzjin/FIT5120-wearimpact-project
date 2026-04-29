/**
 * Epic 3 — Client for the HuggingFace Space classifier.
 *
 * Calls POST /extract-items with preview_mode=high so the returned
 * preview_image is a transparent, high-quality cutout. When the high
 * preview is not yet ready, the response includes preview_token and we
 * poll GET /preview-result/<token> until the hi-res image arrives.
 */
import imageCompression from 'browser-image-compression'

const BASE_URL = (import.meta.env.VITE_MODEL_SERVICE_URL || '').replace(/\/$/, '')

const COMPRESS_OPTIONS = {
  maxSizeMB: 2,
  maxWidthOrHeight: 1024,
  useWebWorker: true,
  fileType: 'image/jpeg'
}

const POLL_INTERVAL_MS = 2000
const POLL_MAX_ATTEMPTS = 30

async function compress(file) {
  // Pre-resize on the client to stay well under the 10 MB upload cap and
  // mirror the server-side MAX_INPUT_IMAGE_SIDE = 1024 limit.
  try {
    return await imageCompression(file, COMPRESS_OPTIONS)
  } catch {
    return file
  }
}

export async function extractItems(files, { mode = 'high' } = {}) {
  if (!BASE_URL) {
    throw new Error('VITE_MODEL_SERVICE_URL is not configured')
  }
  if (!files || files.length === 0) {
    throw new Error('No files selected')
  }

  const compressed = await Promise.all(Array.from(files).map(compress))

  const form = new FormData()
  for (const f of compressed) {
    form.append('files', f, f.name || 'upload.jpg')
  }
  form.append('preview_mode', mode)

  const res = await fetch(`${BASE_URL}/extract-items`, {
    method: 'POST',
    body: form
  })

  if (!res.ok) {
    const text = await res.text().catch(() => '')
    throw new Error(`Classifier request failed (${res.status}): ${text || res.statusText}`)
  }

  return res.json()
}

export async function pollPreview(token, { onUpdate } = {}) {
  if (!BASE_URL || !token) return null

  for (let attempt = 0; attempt < POLL_MAX_ATTEMPTS; attempt++) {
    await new Promise((r) => setTimeout(r, POLL_INTERVAL_MS))
    try {
      const res = await fetch(`${BASE_URL}/preview-result/${encodeURIComponent(token)}`)
      if (!res.ok) continue
      const data = await res.json()
      if (data.ready && data.preview_image) {
        if (onUpdate) onUpdate(data.preview_image)
        return data.preview_image
      }
    } catch {
      // transient — keep polling until POLL_MAX_ATTEMPTS exhausted
    }
  }
  return null
}

export async function checkHealth() {
  if (!BASE_URL) return { status: 'offline' }
  try {
    const res = await fetch(`${BASE_URL}/health`)
    if (!res.ok) return { status: 'down' }
    return res.json()
  } catch {
    return { status: 'unreachable' }
  }
}
