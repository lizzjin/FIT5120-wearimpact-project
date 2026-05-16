<template>
  <div class="adv-mat">
    <header class="adv-mat__head">
      <p class="adv-mat__eyebrow">
        <Layers :size="11" :stroke-width="2.4" /> Fibre map
      </p>
      <p class="adv-mat__headline">{{ advice.headline }}</p>
      <p class="adv-mat__summary">{{ advice.summary }}</p>
    </header>

    <ul class="adv-mat__cards">
      <li
        v-for="f in advice.key_facts"
        :key="f.label"
        class="adv-mat__card"
        :class="`adv-mat__card--${fibreTypeFor(f.label)}`"
      >
        <span class="adv-mat__icon" v-html="iconFor(f.label)" />
        <div class="adv-mat__card-text">
          <p class="adv-mat__card-label">{{ f.label }}</p>
          <p class="adv-mat__card-value">{{ f.value }}</p>
          <p class="adv-mat__card-ctx">{{ f.context }}</p>
        </div>
      </li>
    </ul>

    <section class="adv-mat__actions">
      <p class="adv-mat__section-label">Fibre-specific moves</p>
      <ul class="adv-mat__rec-list">
        <li v-for="r in advice.recommendations" :key="r.id" class="adv-mat__rec">
          <div class="adv-mat__rec-text">
            <p class="adv-mat__rec-action">{{ r.action }}</p>
            <p class="adv-mat__rec-impact">{{ r.impact }}</p>
            <div v-if="r.follow_up_prompts?.length" class="adv-mat__rec-chips">
              <button
                v-for="p in r.follow_up_prompts"
                :key="p"
                type="button"
                class="adv-chip"
                @click="$emit('follow-up', { focusId: r.id, prompt: p })"
              >
                {{ p }}
                <ArrowRight :size="11" :stroke-width="2.2" />
              </button>
            </div>
          </div>
          <span
            class="adv-mat__rec-diff"
            :class="`adv-mat__rec-diff--${r.difficulty}`"
          >{{ r.difficulty }}</span>
        </li>
      </ul>
    </section>
  </div>
</template>

<script setup>
import { ArrowRight, Layers } from 'lucide-vue-next'

defineProps({
  advice: { type: Object, required: true },
})
defineEmits(['follow-up'])

// Mirror MaterialPills.vue's icon set so the same SVG marks each fibre in the
// wardrobe view and in the advisor map — keeps the visual language consistent.
const COMMON = ' width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true"'
const STROKE = ' stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"'

const ICONS = {
  cotton:    `<svg${COMMON}><ellipse cx="12" cy="13" rx="7" ry="5"${STROKE}/><path d="M8 10c2-2 6-2 8 0"${STROKE}/><path d="M9 16c1.5 1 4.5 1 6 0"${STROKE}/></svg>`,
  polyester: `<svg${COMMON}><path d="M5 18c3-6 5-10 7-14M9 18c2.5-5 4.5-9 6.5-13M13 18c2-4 3.5-7.5 5-11"${STROKE}/></svg>`,
  wool:      `<svg${COMMON}><path d="M7 16c2-6 6-9 10-9-1 4-3 8-6 11-2-2-3-4-4-2z"${STROKE}/></svg>`,
  silk:      `<svg${COMMON}><path d="M12 4v16M8 8c4 2 8 2 8-2"${STROKE}/><circle cx="12" cy="6" r="1.2" fill="currentColor"/></svg>`,
  linen:     `<svg${COMMON}><path d="M12 3v18M8 7h8M8 12h8M8 17h5"${STROKE}/></svg>`,
  viscose:   `<svg${COMMON}><path d="M6 18c0-8 4-12 6-14 2 4 4 9 4 14"${STROKE}/><path d="M9 14h6"${STROKE}/></svg>`,
  nylon:     `<svg${COMMON}><rect x="5" y="5" width="14" height="14" rx="3"${STROKE}/><path d="M9 9l6 6M15 9l-6 6"${STROKE}/></svg>`,
  spandex:   `<svg${COMMON}><path d="M7 17c4-3 7-7 10-12M6 8c3 3 6 6 10 8"${STROKE}/></svg>`,
  acrylic:   `<svg${COMMON}><circle cx="12" cy="12" r="7"${STROKE}/><circle cx="12" cy="12" r="3"${STROKE}/></svg>`,
  down:      `<svg${COMMON}><path d="M12 4c-3 4-5 8-5 12 0 3 2 5 5 5s5-2 5-5c0-4-2-8-5-12z"${STROKE}/></svg>`,
  leather:   `<svg${COMMON}><path d="M5 8c3-2 7-2 10 0v10c-3 2-7 2-10 0V8z"${STROKE}/></svg>`,
}
const FALLBACK_ICON = `<svg${COMMON}><circle cx="12" cy="12" r="7"${STROKE}/></svg>`

const NATURAL = new Set(['cotton', 'wool', 'silk', 'linen', 'down', 'leather'])
const SYNTHETIC = new Set(['polyester', 'nylon', 'acrylic', 'spandex'])
const CELLULOSIC = new Set(['viscose'])

function normaliseFibre(label) {
  if (!label) return null
  const slug = String(label).toLowerCase()
  for (const key of Object.keys(ICONS)) {
    if (slug.includes(key)) return key
  }
  return null
}

function iconFor(label) {
  const key = normaliseFibre(label)
  return key ? ICONS[key] : FALLBACK_ICON
}

function fibreTypeFor(label) {
  const key = normaliseFibre(label)
  if (!key) return 'generic'
  if (NATURAL.has(key)) return 'natural'
  if (SYNTHETIC.has(key)) return 'synthetic'
  if (CELLULOSIC.has(key)) return 'cellulosic'
  return 'generic'
}
</script>

<style scoped>
.adv-mat {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.adv-mat__head {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.adv-mat__eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-family: var(--font-display);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--color-soft-sage-deep);
  background: var(--color-soft-sage-mist);
  padding: 4px 10px;
  border-radius: 999px;
  align-self: flex-start;
}
.adv-mat__headline {
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: var(--color-soft-ink);
  line-height: 1.3;
}
.adv-mat__summary {
  font-size: 13.5px;
  line-height: 1.55;
  color: var(--color-soft-ink);
}

/* Fibre cards — left icon, big value, soft tint per fibre family. */
.adv-mat__cards {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.adv-mat__card {
  display: grid;
  grid-template-columns: 40px 1fr;
  gap: 12px;
  align-items: start;
  background: var(--color-soft-cream);
  border-radius: 16px;
  padding: 12px 14px;
  box-shadow: var(--shadow-soft-sm);
  border-left: 3px solid var(--color-soft-sage);
}
.adv-mat__card--natural    { border-left-color: #b9a06b; background: #f3ecdc; }
.adv-mat__card--synthetic  { border-left-color: #6f86b8; background: #e6ecf7; }
.adv-mat__card--cellulosic { border-left-color: #7ea08d; background: #e3ede5; }
.adv-mat__card--generic    { border-left-color: var(--color-soft-sage-deep); }

.adv-mat__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 12px;
  background: var(--color-soft-milk);
  color: var(--color-soft-sage-deep);
  flex-shrink: 0;
}
.adv-mat__card--natural .adv-mat__icon { background: rgba(185, 160, 107, 0.18); color: #6b5b3a; }
.adv-mat__card--synthetic .adv-mat__icon { background: rgba(111, 134, 184, 0.16); color: #324a78; }
.adv-mat__card--cellulosic .adv-mat__icon { background: rgba(126, 160, 141, 0.22); color: #2e4a3a; }

.adv-mat__card-label {
  font-family: var(--font-display);
  font-size: 13px;
  font-weight: 700;
  letter-spacing: -0.005em;
  color: var(--color-soft-ink);
  text-transform: capitalize;
}
.adv-mat__card-value {
  font-family: var(--font-display);
  font-size: 18px;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: var(--color-soft-sage-deep);
  margin-top: 2px;
}
.adv-mat__card-ctx {
  font-size: 11.5px;
  line-height: 1.45;
  color: var(--color-soft-ink-soft);
  margin-top: 4px;
}

/* Recommendations — share visual rhythm with other layouts. */
.adv-mat__actions {
  border-top: 1px dashed var(--color-soft-line);
  padding-top: 12px;
}
.adv-mat__section-label {
  font-family: var(--font-display);
  font-size: 10.5px;
  font-weight: 700;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--color-soft-sage-deep);
  margin-bottom: 10px;
}
.adv-mat__rec-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.adv-mat__rec {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 10px;
  align-items: start;
  background: var(--color-soft-cream);
  border-radius: 14px;
  padding: 10px 12px;
  box-shadow: var(--shadow-soft-sm);
}
.adv-mat__rec-action {
  font-size: 13.5px;
  font-weight: 600;
  color: var(--color-soft-ink);
  line-height: 1.35;
  margin-bottom: 2px;
}
.adv-mat__rec-impact {
  font-size: 12px;
  color: var(--color-soft-ink-soft);
  line-height: 1.45;
}
.adv-mat__rec-chips {
  margin-top: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.adv-mat__rec-diff {
  align-self: start;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.06em;
  padding: 3px 9px;
  border-radius: 999px;
  text-transform: uppercase;
}
.adv-mat__rec-diff--easy   { background: var(--color-soft-sage-mist); color: var(--color-soft-sage-deep); }
.adv-mat__rec-diff--medium { background: var(--color-soft-oat); color: var(--color-soft-ink); }
.adv-mat__rec-diff--hard   { background: var(--color-soft-dusty-wash); color: var(--color-soft-ink); }

.adv-chip {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 5px 10px;
  border-radius: 999px;
  background: var(--color-soft-milk);
  border: 1px solid var(--color-soft-line);
  color: var(--color-soft-ink);
  font-size: 11.5px;
  font-weight: 600;
  cursor: pointer;
  transition: background 180ms ease, color 180ms ease, transform 180ms ease;
}
.adv-chip:hover {
  background: var(--color-soft-sage-mist);
  color: var(--color-soft-sage-deep);
  transform: translateY(-1px);
}
.adv-chip > svg { color: var(--color-soft-sage-deep); }
</style>
