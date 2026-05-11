<template>
  <DialogRoot :open="open" @update:open="(v) => $emit('update:open', v)">
    <DialogPortal>
      <DialogOverlay class="modal-backdrop" />
      <DialogContent class="modal-panel" aria-describedby="brand-detail-desc">
        <DialogTitle class="sr-only">Brand sustainability detail</DialogTitle>
        <DialogDescription id="brand-detail-desc" class="sr-only">
          Detailed sustainability scores and policies for the selected brand.
        </DialogDescription>

        <DialogClose class="modal-close" aria-label="Close">
          <X :size="18" :stroke-width="2" />
        </DialogClose>

        <div class="modal-scroll" data-lenis-prevent>
          <div v-if="isLoading" class="detail-skeleton">
            <div class="sk sk-detail-header"></div>
            <div class="sk sk-detail-body"></div>
            <div class="sk sk-detail-body"></div>
            <div class="sk sk-detail-body-sm"></div>
          </div>

          <template v-else-if="detail">
            <div class="detail-card brand-summary">
              <div class="brand-summary-header">
                <div class="brand-avatar-large" :style="!detailLogoOk ? { background: avatarBg } : {}">
                  <img
                    v-if="detailLogoOk"
                    :src="detailLogoSrc"
                    :alt="detail.company_name"
                    class="detail-logo-img"
                    @error="detailLogoOk = false"
                  />
                  <span v-else>{{ detail.company_name.charAt(0).toUpperCase() }}</span>
                </div>
                <div>
                  <h2>{{ detail.company_name }}</h2>
                  <span class="category-tag">
                    {{ detail.product_category === 'footwear' ? 'Footwear' : 'Apparel' }}
                  </span>
                </div>
              </div>

              <div class="score-row">
                <div
                  class="score-badge"
                  :style="{ background: scoreBg, color: scoreColor, borderColor: scoreColor + '4d' }"
                >
                  <div class="score-badge-inner">
                    <span class="score-number">{{ detail.overall_score }}</span>
                    <span class="score-max">/100</span>
                  </div>
                  <span class="score-label-text">{{ detail.score_label }}</span>
                </div>
              </div>
              <p class="score-desc">{{ scoreDescription }}</p>
            </div>

            <div class="detail-card">
              <h3>Sustainability Scores</h3>
              <p class="scores-desc">
                Three independently measured dimensions from the Fashion Transparency Index.
                Each bar shows how much of the maximum possible score this company achieved.
              </p>
              <MetricBar
                label="Governance & Policies"
                sublabel="Supplier code of conduct, senior accountability"
                :value="Math.round((detail.governance_score / 6) * 100)"
                :raw-score="detail.governance_score"
                :max-score="6"
              />
              <MetricBar
                label="Supply Chain Tracing"
                sublabel="Visibility across all production stages"
                :value="Math.round((detail.tracing_score / 15) * 100)"
                :raw-score="detail.tracing_score"
                :max-score="15"
              />
              <MetricBar
                label="Environmental Sustainability"
                sublabel="Fibre impact, emissions targets, sustainable materials"
                :value="Math.round((detail.env_score / 21) * 100)"
                :raw-score="detail.env_score"
                :max-score="21"
              />
            </div>

            <div class="detail-card">
              <h3>Supply Chain Policies</h3>
              <p class="scores-desc">
                Whether this company has publicly committed to key supply chain and environmental standards.
              </p>
              <div class="policy-list">
                <PolicyRow
                  label="Supplier Code of Conduct published"
                  sublabel="The company has a formal, publicly available document setting ethical and labour standards for its suppliers."
                  :value="detail.has_supplier_code"
                />
                <PolicyRow
                  label="Code of Conduct covers raw materials"
                  sublabel="The Supplier Code of Conduct extends beyond factories to cover raw material sourcing (e.g. cotton farms, textile mills)."
                  :value="detail.code_covers_raw_materials"
                />
                <PolicyRow
                  label="Senior officer accountable for supply chain"
                  sublabel="A named executive (e.g. CEO or Chief Sustainability Officer) holds formal responsibility for supply chain ethics."
                  :value="detail.has_senior_accountability"
                />
                <PolicyRow
                  label="Assessed fibre environmental impact"
                  sublabel="The company has formally evaluated the environmental footprint of the fibres used in its products."
                  :value="detail.assessed_fibre_impact"
                />
                <PolicyRow
                  label="Emissions reduction target published"
                  sublabel="The company has publicly committed to a measurable greenhouse gas emissions reduction goal."
                  :value="detail.has_emissions_target"
                />
              </div>
              <div class="fibre-row">
                <span class="fibre-label">Sustainable fibres in final product</span>
                <span class="fibre-value">{{ detail.sustainable_fibre_pct }}</span>
              </div>
            </div>

            <div v-if="detail.brands && detail.brands.length > 1" class="detail-card">
              <h3>Brands under this Company</h3>
              <div class="brands-chip-list">
                <span v-for="b in detail.brands" :key="b.brand_name" class="brand-chip">
                  {{ b.brand_name }}
                </span>
              </div>
            </div>

            <div class="detail-card data-source-box">
              <h3>Data Source</h3>
              <p>
                Scores are derived from the <strong>Fashion Transparency Index</strong> (Australian market).
                Data reflects publicly available corporate disclosures on supply chain policies,
                environmental commitments, and fibre sourcing.
              </p>
              <a
                href="https://baptistworldaid.org.au/wp-content/uploads/2024/10/Ethical-Fashion-Report-2024-Appendix-1aec741f0a81f5f9.pdf"
                target="_blank"
                rel="noopener noreferrer"
                class="source-link"
              >
                View Full Report
                <ArrowRight :size="15" :stroke-width="2.5" />
              </a>
            </div>
          </template>
        </div>
      </DialogContent>
    </DialogPortal>
  </DialogRoot>
</template>

<script setup>
import { computed, defineComponent, h, ref, watch } from 'vue'
import { ArrowRight, CheckCircle2, MinusCircle, X, XCircle } from 'lucide-vue-next'
import { DialogClose, DialogContent, DialogDescription, DialogOverlay, DialogPortal, DialogRoot, DialogTitle } from 'radix-vue'
import MetricBar from '../MetricBar.vue'

const props = defineProps({
  open: { type: Boolean, default: false },
  detail: { type: Object, default: null },
  isLoading: { type: Boolean, default: false },
})
defineEmits(['update:open'])

const POLICY_CONFIG = {
  Yes:     { icon: CheckCircle2, color: '#054d28' },
  No:      { icon: XCircle,      color: '#d03238' },
  Partial: { icon: MinusCircle,  color: '#b45309' },
}

const PolicyRow = defineComponent({
  props: { label: String, sublabel: String, value: String },
  setup(p) {
    return () => {
      const cfg = POLICY_CONFIG[p.value] ?? { icon: MinusCircle, color: '#868685' }
      return h('div', {
        style: {
          display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start',
          gap: '12px', padding: '12px 0', borderBottom: '1px solid rgba(14,15,12,0.08)',
        },
      }, [
        h('div', { style: { display: 'flex', flexDirection: 'column', gap: '3px', flex: '1' } }, [
          h('span', { style: { fontSize: '14px', color: '#0e0f0c', fontWeight: '600' } }, p.label),
          p.sublabel
            ? h('span', { style: { fontSize: '13px', color: '#868685', lineHeight: '1.4', fontWeight: '500' } }, p.sublabel)
            : null,
        ]),
        h('span', {
          style: {
            display: 'inline-flex', alignItems: 'center', gap: '5px',
            fontSize: '13px', fontWeight: '700', flexShrink: '0', color: cfg.color,
          },
        }, [
          h(cfg.icon, { size: 16, strokeWidth: 2.5 }),
          h('span', {}, p.value),
        ]),
      ])
    }
  },
})

const LABEL_COLORS = {
  'Great': '#054d28', 'Good': '#16a34a', "It's a Start": '#ca8a04',
  'Below Average': '#ea580c', 'Avoid': '#d03238',
}
const LABEL_BG = {
  'Great': '#e2f6d5', 'Good': '#ecfccb', "It's a Start": '#fef9c3',
  'Below Average': '#ffedd5', 'Avoid': '#fee2e2',
}
const LABEL_DESCRIPTIONS = {
  'Great':         'This company leads on sustainability and transparency.',
  'Good':          'Good overall performance with some room to improve.',
  "It's a Start":  'Some initiatives in place but significant gaps remain.',
  'Below Average': 'Limited transparency and sustainability efforts.',
  'Avoid':         'Very little evidence of sustainable or ethical practices.',
}

const AVATAR_PALETTE = ['#dbeafe', '#e2f6d5', '#fef9c3', '#fce7f3', '#ede9fe', '#ffedd5']

const scoreColor       = computed(() => LABEL_COLORS[props.detail?.score_label] || '#868685')
const scoreBg          = computed(() => LABEL_BG[props.detail?.score_label]     || '#e8ebe6')
const scoreDescription = computed(() => LABEL_DESCRIPTIONS[props.detail?.score_label] || '')
const avatarBg         = computed(() => {
  const n = props.detail?.company_name || 'A'
  return AVATAR_PALETTE[n.charCodeAt(0) % AVATAR_PALETTE.length]
})

const detailLogoOk = ref(true)
const detailLogoSrc = computed(() => {
  if (!props.detail) return ''
  return `https://img.logo.dev/${guessDomain(props.detail.company_name)}?token=pk_LbFI27UJRDWnSoDCC_4GYA&size=80`
})

watch(() => props.detail, () => { detailLogoOk.value = true })

// Lock background scroll while the modal is open. Setting overflow:hidden
// on BOTH <html> and <body> (and compensating for scrollbar width so the
// page doesn't jump) is the standard Radix/MUI pattern. An earlier
// position:fixed-on-body approach also locked the background but broke
// wheel scrolling inside the modal in some browsers.
let savedHtmlOverflow = ''
let savedBodyOverflow = ''
let savedBodyPadRight = ''
watch(() => props.open, (v) => {
  const html = document.documentElement
  const body = document.body
  if (v) {
    savedHtmlOverflow = html.style.overflow
    savedBodyOverflow = body.style.overflow
    savedBodyPadRight = body.style.paddingRight
    const scrollbarWidth = window.innerWidth - html.clientWidth
    html.style.overflow = 'hidden'
    body.style.overflow = 'hidden'
    if (scrollbarWidth > 0) {
      body.style.paddingRight = `${scrollbarWidth}px`
    }
  } else {
    html.style.overflow = savedHtmlOverflow
    body.style.overflow = savedBodyOverflow
    body.style.paddingRight = savedBodyPadRight
  }
})

function guessDomain(name) {
  const overrides = {
    'H&M': 'hm.com', 'H&M Group': 'hm.com', 'Inditex': 'inditex.com',
    'Levi Strauss & Co': 'levi.com', 'PVH Corp': 'pvh.com', 'VF Corporation': 'vfc.com',
    'Hanesbrands': 'hanes.com', 'Fast Retailing': 'fastretailing.com', 'Kering': 'kering.com',
    'LVMH': 'lvmh.com', 'Adidas': 'adidas.com', 'Nike': 'nike.com', 'Puma': 'puma.com',
    'Patagonia': 'patagonia.com',
  }
  if (overrides[name]) return overrides[name]
  return name.toLowerCase().replace(/[^a-z0-9]/g, '') + '.com'
}
</script>

<style scoped>
.sr-only {
  position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px;
  overflow: hidden; clip: rect(0, 0, 0, 0); white-space: nowrap; border-width: 0;
}

.modal-backdrop {
  position: fixed; inset: 0;
  background: rgba(22, 51, 0, 0.4);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  z-index: 200;
  animation: fadeIn 200ms ease;
}

.modal-panel {
  position: fixed; top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  width: calc(100% - 48px);
  max-width: 640px;
  max-height: 88vh;
  background: var(--color-warm-cream);
  border-radius: var(--radius-card-lg);
  overflow: hidden;
  display: flex; flex-direction: column;
  z-index: 201;
  box-shadow: var(--shadow-modal);
  animation: modalScaleIn 280ms cubic-bezier(0.22, 1, 0.36, 1);
}

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes modalScaleIn {
  from { opacity: 0; transform: translate(-50%, -50%) scale(0.95); }
  to   { opacity: 1; transform: translate(-50%, -50%) scale(1); }
}

.modal-close {
  position: absolute; top: 16px; right: 16px;
  width: 36px; height: 36px;
  border-radius: 50%;
  border: 1px solid var(--color-kh-glass-border);
  background: var(--color-warm-cream);
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  color: var(--color-text-subtle);
  z-index: 1;
  transition: background 0.15s, transform 0.15s;
}

.modal-close:hover {
  background: rgba(159, 232, 112, 0.22);
  color: var(--color-primary-text);
  transform: scale(1.05);
}

.modal-scroll {
  flex: 1 1 auto;
  /* `min-height: 0` is the bit that actually makes a flex child overflow:
     without it the child can't shrink below its content size and the
     `overflow-y: auto` never has anything to scroll. */
  min-height: 0;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  overscroll-behavior: contain;
  padding: 56px 24px 28px;
  display: flex; flex-direction: column; gap: 16px;
}

.detail-skeleton { display: flex; flex-direction: column; gap: 16px; }
.sk {
  background: linear-gradient(90deg, #ede5d4 25%, #e3d9c2 50%, #ede5d4 75%);
  background-size: 200% 100%;
  animation: shimmer 1.4s infinite;
  border-radius: 14px;
}
.sk-detail-header  { height: 160px; border-radius: 20px; }
.sk-detail-body    { height: 180px; border-radius: 20px; }
.sk-detail-body-sm { height: 100px; border-radius: 20px; }
@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.detail-card {
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid var(--color-kh-glass-border);
  border-radius: 20px;
  padding: 24px;
}

.detail-card h3 {
  font-size: 22px;
  font-weight: 700;
  letter-spacing: -0.01em;
  line-height: 1.25;
  color: var(--color-text);
  margin-bottom: 8px;
}

.brand-summary-header { display: flex; gap: 16px; align-items: center; margin-bottom: 20px; }

.brand-avatar-large {
  width: 54px; height: 54px;
  border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 22px;
  color: var(--color-text);
  flex-shrink: 0;
  overflow: hidden;
  border: 1px solid var(--color-kh-glass-border);
  background: white;
}

.detail-logo-img {
  width: 100%; height: 100%;
  object-fit: contain; padding: 6px;
}

.brand-summary-header h2 {
  font-size: 26px; font-weight: 700;
  letter-spacing: -0.01em; line-height: 1.23;
  color: var(--color-text);
  margin-bottom: 6px;
}

.category-tag {
  font-size: 12px;
  background: rgba(22, 51, 0, 0.06);
  color: var(--color-text-muted);
  padding: 3px 10px;
  border-radius: var(--radius-pill);
  font-weight: 500;
}

.score-row { display: flex; align-items: center; gap: 16px; flex-wrap: wrap; margin-bottom: 12px; }

.score-badge {
  display: inline-flex; flex-direction: column; align-items: center; gap: 4px;
  padding: 14px 24px;
  border-radius: 14px;
  border: 2px solid transparent;
}

.score-badge-inner { display: flex; align-items: baseline; gap: 3px; }
.score-number { font-size: 44px; font-weight: 900; line-height: 0.85; letter-spacing: -0.02em; }
.score-max { font-size: 15px; font-weight: 500; opacity: 0.65; }
.score-label-text { font-size: 14px; font-weight: 700; }
.score-desc { font-size: 14px; font-weight: 500; color: var(--color-text-muted); line-height: 1.5; margin: 0; }

.scores-desc { font-size: 13px; color: var(--color-text-subtle); margin-bottom: 16px; line-height: 1.5; }

.policy-list { margin-bottom: 14px; }

.fibre-row {
  display: flex; justify-content: space-between; align-items: center;
  padding-top: 12px;
  border-top: 1px solid rgba(22, 51, 0, 0.08);
}

.fibre-label { font-size: 14px; color: var(--color-text-muted); }
.fibre-value { font-size: 14px; font-weight: 700; color: var(--color-text); }

.brands-chip-list { display: flex; flex-wrap: wrap; gap: 8px; }

.brand-chip {
  background: rgba(159, 232, 112, 0.22);
  color: var(--color-primary-text);
  padding: 6px 14px;
  border-radius: var(--radius-pill);
  font-size: 13px;
  font-weight: 600;
}

.data-source-box {
  background: rgba(159, 232, 112, 0.12);
  border-color: rgba(22, 51, 0, 0.12);
}
.data-source-box p { color: var(--color-text-muted); line-height: 1.5; font-size: 14px; margin: 0 0 14px; }

.source-link {
  display: inline-flex;
  align-items: center; gap: 6px;
  padding: 10px 20px;
  background: var(--color-primary);
  color: var(--color-primary-text);
  border-radius: var(--radius-pill);
  font-size: 14px; font-weight: 700;
  text-decoration: none;
  transition: transform 200ms var(--motion-entrance);
}

.source-link:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(22, 51, 0, 0.18); }

@media (max-width: 768px) {
  .modal-panel { max-height: 94vh; border-radius: var(--radius-card); }
}
</style>
