/**
 * Sustainable Fashion Knowledge Hub — quiz question bank.
 *
 * Schema (each entry):
 *   id            string                 stable identifier (e.g. "q1")
 *   question      string                 question text shown on the card
 *   options       string[]               2–4 multiple-choice options
 *   correctIndex  integer                index into `options` of the correct answer
 *   explanation   string (≤ 280 chars)   one-sentence takeaway shown after reveal
 *   source        string                 short citation (org / report / year)
 *
 * NOTE: copy and exact figures are provisional. Final wording, numbers,
 * and source URLs are pending editorial sign-off before merge.
 */

export const quizQuestions = Object.freeze([
  Object.freeze({
    id: 'q1',
    question: 'How many new garments are produced globally each year?',
    options: ['~20 billion', '~50 billion', '~100 billion', '~150 billion'],
    correctIndex: 2,
    explanation:
      'Global apparel output has roughly doubled since 2000 — fast fashion is the engine. Buying less and choosing quality over quantity is the highest-leverage personal action.',
    source: 'Ellen MacArthur Foundation, A New Textiles Economy (2017)',
  }),
  Object.freeze({
    id: 'q2',
    question: 'Which fabric typically has the largest water footprint per kilogram?',
    options: ['Polyester', 'Cotton', 'Linen', 'Wool'],
    correctIndex: 1,
    explanation:
      'A single conventional cotton T-shirt can take ~2,700 litres of water to produce — most of it for irrigation. Organic and rain-fed cotton cuts that significantly.',
    source: 'WWF Cotton Farming Report',
  }),
  Object.freeze({
    id: 'q3',
    question: 'What share of ocean microplastics comes from washing synthetic clothing?',
    options: ['~5%', '~15%', '~35%', '~60%'],
    correctIndex: 2,
    explanation:
      'Every synthetic wash sheds millions of plastic microfibres into waterways. Washing less, in cold water, with a microfibre filter or bag meaningfully reduces shedding.',
    source: 'IUCN, Primary Microplastics in the Oceans (2017)',
  }),
  Object.freeze({
    id: 'q4',
    question: 'Roughly how long does polyester take to break down in the environment?',
    options: ['5–10 years', '~50 years', '200+ years', 'It never fully breaks down'],
    correctIndex: 2,
    explanation:
      'Polyester is essentially plastic. Discarded synthetic clothing persists for centuries in landfill — making reuse, repair, and recycling far more impactful than disposal.',
    source: 'UNEP, Sustainability and Circularity in the Textile Value Chain (2020)',
  }),
  Object.freeze({
    id: 'q5',
    question: 'Extending a garment’s active life by 9 months reduces its carbon footprint by about:',
    options: ['~5%', '~15%', '~30%', '~50%'],
    correctIndex: 2,
    explanation:
      'WRAP’s research found that wearing clothes for nine extra months cuts carbon, water, and waste footprints by roughly 20–30%. Wear longer, repair, and rewear.',
    source: 'WRAP UK, Valuing Our Clothes (2017)',
  }),
])

if (import.meta.env.DEV) {
  // Dev-only schema sanity check — surfaces malformed entries fast during development.
  for (const q of quizQuestions) {
    const optionCount = Array.isArray(q.options) ? q.options.length : 0
    const valid =
      typeof q.id === 'string' &&
      typeof q.question === 'string' &&
      optionCount >= 2 &&
      optionCount <= 4 &&
      Number.isInteger(q.correctIndex) &&
      q.correctIndex >= 0 &&
      q.correctIndex < optionCount &&
      typeof q.explanation === 'string' &&
      q.explanation.length <= 280 &&
      typeof q.source === 'string'
    if (!valid) {
      throw new Error(`[quizQuestions] malformed entry: ${q?.id ?? '<unknown>'}`)
    }
  }
}
