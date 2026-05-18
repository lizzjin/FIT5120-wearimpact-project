/**
 * Convert raw error / status messages into kind, actionable copy.
 *
 * Principle (per project UX charter): say it plainly, tell the user
 * what to do next, never blame. Pass either an Error, a string, or a
 * { status, message } shape and an optional context tag.
 */

const NETWORK_HINTS = [
  'failed to fetch',
  'networkerror',
  'load failed',
  'network request failed',
  'fetch failed',
  'err_internet',
]

const PATTERNS = [
  {
    test: (msg) => /unsupported file/i.test(msg),
    map: (msg) => {
      const name = msg.replace(/.*unsupported file:\s*/i, '').trim()
      return name
        ? `That "${name}" file isn't supported yet — try JPG, PNG, or WEBP.`
        : `That file format isn't supported yet — try JPG, PNG, or WEBP.`
    },
  },
  {
    test: (msg) => /total size\s*>/i.test(msg),
    map: () => `These photos add up to more than 10 MB — drop a couple of the big ones, or shrink them first.`,
  },
  {
    test: (msg) => /max\s*\d+\s*photos/i.test(msg),
    map: () => `Up to 8 photos at a time — we kept the first 8 for you.`,
  },
  {
    test: (msg) => /ai advisor is temporarily unavailable|advisor temporarily unavailable/i.test(msg),
    map: () => `The AI advisor is taking a quick nap — give it ~30s and try again.`,
  },
  {
    test: (msg) => /payload was rejected|payload rejected/i.test(msg),
    map: () => `That request didn't go through — refresh the page and try once more.`,
  },
  {
    test: (msg) => /advisor request failed/i.test(msg),
    map: () => `The AI advisor didn't reply this time — wait a few seconds and tap the question again.`,
  },
  {
    test: (msg) => /no route found/i.test(msg),
    map: () => `Couldn't draw this route — try a different travel mode and we'll have another go.`,
  },
  {
    test: (msg) => /could not generate directions/i.test(msg),
    map: () => `Directions didn't come through this time — try again or pick a different store.`,
  },
  {
    test: (msg) => /map unavailable/i.test(msg),
    map: () => `The map can't load right now — the list below still works while we look into it.`,
  },
  {
    test: (msg) => /no matches in this radius/i.test(msg),
    map: () => `Nothing found in this range — widen the radius or switch the store type to see more.`,
  },
  {
    test: (msg) => /failed to load preset questions/i.test(msg),
    map: () => `Couldn't load the question list — refresh the page and we'll try again.`,
  },
  {
    test: (msg) => /failed\.\s*please retry|please retry/i.test(msg),
    map: () => `That didn't go through — tap once more and we'll retry.`,
  },
  {
    test: (msg) => /could not load details/i.test(msg),
    map: () => `Couldn't open the details — tap the card again.`,
  },
  {
    test: (msg) => /failed to load eco-shops|nearby search failed/i.test(msg),
    map: () => `Couldn't pull nearby shops — widen the radius or try again in a moment.`,
  },
  {
    test: (msg) => /failed to get advice/i.test(msg),
    map: () => `The AI advisor didn't reply — wait a few seconds and tap the question again.`,
  },
  {
    test: (msg) => /failed to get a follow-up/i.test(msg),
    map: () => `Couldn't pull a follow-up answer — try tapping the chip again.`,
  },
  {
    test: (msg) => /could not load preset questions/i.test(msg),
    map: () => `Couldn't load the question list — refresh the page and we'll try again.`,
  },
]

function rawMessage(err) {
  if (!err) return ''
  if (typeof err === 'string') return err
  if (err.message) return err.message
  if (err.detail) return err.detail
  try {
    return String(err)
  } catch {
    return ''
  }
}

/**
 * Turn an unknown error-like value into a single friendly sentence.
 *
 * @param {unknown} err
 * @param {object}  [opts]
 * @param {string}  [opts.context]  Optional context tag: 'upload' | 'advisor' | 'location' | 'route' | 'generic'.
 * @param {string}  [opts.fallback] Fallback copy if nothing matches.
 * @returns {string}
 */
export function humanize(err, opts = {}) {
  const { context = 'generic', fallback } = opts
  const msg = rawMessage(err).trim()

  if (!msg) {
    return fallback || defaultFallback(context)
  }

  const lower = msg.toLowerCase()
  if (NETWORK_HINTS.some((hint) => lower.includes(hint))) {
    return `The connection slipped — check your network and tap again.`
  }

  for (const { test, map } of PATTERNS) {
    if (test(msg)) return map(msg)
  }

  return fallback || defaultFallback(context, msg)
}

function defaultFallback(context, msg = '') {
  switch (context) {
    case 'upload':
      return `Something paused mid-upload — tap "Classify & save" once more and we'll keep going.`
    case 'advisor':
      return `The advisor went quiet for a moment — tap the question again in a few seconds.`
    case 'location':
      return `Couldn't get your location — we'll keep going with a default starting point.`
    case 'route':
      return `Couldn't draw that route just now — try another travel mode.`
    default:
      return msg || `Something didn't work out — give it another try.`
  }
}
