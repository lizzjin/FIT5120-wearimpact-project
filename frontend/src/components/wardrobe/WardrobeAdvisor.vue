<template>
  <section class="wd-chat-page">
    <!-- Page header — back button + title bar, mirroring WardrobeMain layout -->
    <header class="wd-chat-page__head">
      <button type="button" class="wd-chat-page__back" @click="$emit('close')">
        <ArrowLeft :size="16" :stroke-width="2" /> Back to wardrobe
      </button>
      <div class="wd-chat-page__title-block">
        <p ref="eyebrowRef" class="wd-chat-page__eyebrow">AI sustainability advisor</p>
        <h2 class="wd-chat-page__title">
          Grounded in your <em class="wd-chat-page__title-accent">wardrobe.</em>
        </h2>
      </div>
      <span class="wd-chat-page__badge">
        <Sparkles :size="13" :stroke-width="2" />
        {{ garmentCount }} item{{ garmentCount === 1 ? '' : 's' }} analysed
      </span>
    </header>

    <div class="wd-chat" role="region" aria-label="AI advisor conversation">

    <!-- Conversation stream -->
    <div ref="streamRef" class="wd-chat__stream" data-lenis-prevent>
      <!-- Greeting always present at the top -->
      <div class="wd-bubble wd-bubble--ai">
        <span class="wd-bubble__avatar"><Sparkles :size="13" :stroke-width="2" /></span>
        <div class="wd-bubble__body">
          <p>
            Hi — pick a question below and I'll crunch the LCA numbers from your
            <strong>{{ garmentCount }} item{{ garmentCount === 1 ? '' : 's' }}</strong>
            and translate them into plain-English actions.
          </p>
        </div>
      </div>

      <template v-for="(msg, idx) in messages" :key="idx">
        <!-- User question bubble (main + follow-up share style, follow-up indented) -->
        <div
          v-if="msg.role === 'user'"
          class="wd-bubble wd-bubble--user"
          :class="{ 'wd-bubble--indent': msg.isFollowUp }"
        >
          <div class="wd-bubble__body">{{ msg.text }}</div>
        </div>

        <!-- AI typing indicator -->
        <div
          v-else-if="msg.role === 'loading'"
          class="wd-bubble wd-bubble--ai"
          :class="{ 'wd-bubble--indent': msg.isFollowUp }"
        >
          <span class="wd-bubble__avatar"><Sparkles :size="13" :stroke-width="2" /></span>
          <div class="wd-bubble__body wd-bubble__body--typing">
            <span></span><span></span><span></span>
          </div>
        </div>

        <!-- AI error -->
        <div
          v-else-if="msg.role === 'error'"
          class="wd-bubble wd-bubble--ai"
          :class="{ 'wd-bubble--indent': msg.isFollowUp }"
        >
          <span class="wd-bubble__avatar wd-bubble__avatar--alert">
            <CircleAlert :size="13" :stroke-width="2" />
          </span>
          <div class="wd-bubble__body wd-bubble__body--error">{{ msg.text }}</div>
        </div>

        <!-- AI structured advice — layout-driven render -->
        <template v-else-if="msg.role === 'advice'">
          <div class="wd-bubble wd-bubble--ai wd-bubble--advice">
            <span class="wd-bubble__avatar"><Sparkles :size="13" :stroke-width="2" /></span>
            <div class="wd-bubble__body wd-bubble__body--advice">
              <button
                type="button"
                class="wd-bubble__refresh"
                :disabled="busy"
                @click="reAsk(idx)"
                aria-label="Re-answer this question"
                title="Re-answer this question"
              >
                <RefreshCw :size="12" :stroke-width="2.2" />
              </button>
              <AdviceReport
                v-if="layoutFor(msg) === 'report'"
                :advice="msg.advice"
                @follow-up="(p) => askFollowUp(idx, p)"
              />
              <AdvicePlaybook
                v-else-if="layoutFor(msg) === 'playbook'"
                :advice="msg.advice"
                @follow-up="(p) => askFollowUp(idx, p)"
              />
              <AdviceDecision
                v-else-if="layoutFor(msg) === 'decision'"
                :advice="msg.advice"
                @follow-up="(p) => askFollowUp(idx, p)"
              />
              <AdviceCareGuide
                v-else-if="layoutFor(msg) === 'care_guide'"
                :advice="msg.advice"
                @follow-up="(p) => askFollowUp(idx, p)"
              />
              <AdviceMaterialMap
                v-else-if="layoutFor(msg) === 'material_map'"
                :advice="msg.advice"
                @follow-up="(p) => askFollowUp(idx, p)"
              />
            </div>
          </div>

          <!-- Caveats as a small note bubble below -->
          <div v-if="msg.advice.caveats?.length" class="wd-bubble wd-bubble--ai">
            <span class="wd-bubble__avatar wd-bubble__avatar--muted">
              <CircleAlert :size="13" :stroke-width="2" />
            </span>
            <div class="wd-bubble__body wd-bubble__body--note">
              <p v-for="(c, ci) in msg.advice.caveats" :key="ci">{{ c }}</p>
            </div>
          </div>
        </template>

        <!-- Follow-up mini-bubble (compact, indented under parent advice) -->
        <div
          v-else-if="msg.role === 'followup'"
          class="wd-bubble wd-bubble--ai wd-bubble--indent wd-bubble--followup"
        >
          <span class="wd-bubble__avatar"><Sparkles :size="13" :stroke-width="2" /></span>
          <div class="wd-bubble__body wd-bubble__body--followup">
            <p class="wd-followup__headline">{{ msg.followUp.headline }}</p>
            <p class="wd-followup__body">{{ msg.followUp.body }}</p>
            <ul v-if="msg.followUp.mini_facts?.length" class="wd-followup__facts">
              <li v-for="f in msg.followUp.mini_facts" :key="f.label" class="wd-followup__fact">
                <span class="wd-followup__fact-label">{{ f.label }}:</span>
                <strong class="wd-followup__fact-value">{{ f.value }}</strong>
                <span class="wd-followup__fact-ctx">{{ f.context }}</span>
              </li>
            </ul>
            <div v-if="msg.followUp.next_questions?.length" class="wd-followup__chips">
              <button
                v-for="q in msg.followUp.next_questions"
                :key="q"
                type="button"
                class="wd-chip wd-chip--sub"
                :disabled="busy"
                @click="askFollowUp(msg.parentIdx, { focusId: '', prompt: q })"
              >
                {{ q }}
              </button>
            </div>
          </div>
        </div>
      </template>
    </div>

    <!-- Suggestion bar — toggles between preset list and contextual next_questions -->
    <footer class="wd-chat__chips">
      <p class="wd-chat__chips-hint">
        <template v-if="!hasAdvice">Pick a question to start</template>
        <template v-else-if="chipMode === 'context' && contextQuestions.length">Keep exploring</template>
        <template v-else>Ask another</template>
      </p>
      <div class="wd-chat__chip-row">
        <template v-if="chipMode === 'context' && contextQuestions.length">
          <button
            v-for="q in contextQuestions"
            :key="q"
            type="button"
            class="wd-chip"
            :disabled="busy"
            @click="askFollowUp(latestAdviceIdx, { focusId: '', prompt: q })"
          >
            <Sparkles :size="11" :stroke-width="2.2" />
            {{ q }}
          </button>
          <button
            type="button"
            class="wd-chip wd-chip--ghost"
            :disabled="busy"
            @click="chipMode = 'preset'"
          >
            <List :size="11" :stroke-width="2.2" />
            Back to main questions
          </button>
        </template>
        <template v-else>
          <button
            v-for="p in presets"
            :key="p.key"
            type="button"
            class="wd-chip"
            :disabled="busy"
            @click="askPreset(p)"
          >
            <Sparkles :size="11" :stroke-width="2.2" />
            {{ p.label }}
          </button>
        </template>
      </div>
      <p v-if="presetsError" class="wd-chat__chips-error">
        <CircleAlert :size="11" :stroke-width="2" /> {{ presetsError }}
      </p>
    </footer>
    </div>
  </section>
</template>

<script setup>
import { computed, nextTick, onMounted, ref } from 'vue'
import { ArrowLeft, CircleAlert, List, RefreshCw, Sparkles } from 'lucide-vue-next'
import {
  fetchAdviceFollowUp,
  fetchPresetQuestions,
  fetchWardrobeAdvice,
} from '../../services/advisorApi.js'
import { useReveal } from '../../motion/useReveal'
import AdviceReport from './advice/AdviceReport.vue'
import AdvicePlaybook from './advice/AdvicePlaybook.vue'
import AdviceDecision from './advice/AdviceDecision.vue'
import AdviceCareGuide from './advice/AdviceCareGuide.vue'
import AdviceMaterialMap from './advice/AdviceMaterialMap.vue'

const eyebrowRef = ref(null)
useReveal(eyebrowRef, { mode: 'char', stagger: 0.022, duration: 0.5 })

// Defensive fallback: if the backend response is missing or has an unknown
// `advice.layout` (e.g. running an older build), derive the layout from the
// preset key so the bubble never renders empty. Keeps the UI resilient while
// the backend is being rolled forward.
const VALID_LAYOUTS = new Set(['report', 'playbook', 'decision', 'care_guide', 'material_map'])
const PRESET_TO_LAYOUT = {
  impact_summary: 'report',
  reduce_my_footprint: 'playbook',
  rethink_purchases: 'decision',
  extend_garment_life: 'care_guide',
  material_breakdown: 'material_map',
}
function layoutFor(msg) {
  const declared = msg?.advice?.layout
  if (VALID_LAYOUTS.has(declared)) return declared
  const fromPreset = msg?.preset?.layout
  if (VALID_LAYOUTS.has(fromPreset)) return fromPreset
  return PRESET_TO_LAYOUT[msg?.preset?.key] || 'report'
}

const props = defineProps({
  garments: { type: Array, default: () => [] },
})
defineEmits(['close'])

const garmentCount = computed(() => props.garments.length)

const presets = ref([])
const presetsError = ref('')
// Stream of conversation entries. Each is { role, ... }.
const messages = ref([])
const busy = ref(false)
const streamRef = ref(null)
// 'preset' (fixed 4 questions) | 'context' (next_questions from latest advice).
const chipMode = ref('preset')

const hasAdvice = computed(() =>
  messages.value.some((m) => m.role === 'advice')
)

const latestAdviceIdx = computed(() => {
  for (let i = messages.value.length - 1; i >= 0; i--) {
    if (messages.value[i].role === 'advice') return i
  }
  return -1
})

const contextQuestions = computed(() => {
  const idx = latestAdviceIdx.value
  if (idx < 0) return []
  return messages.value[idx].advice?.next_questions || []
})

onMounted(async () => {
  try {
    presets.value = await fetchPresetQuestions()
  } catch (err) {
    presetsError.value = err?.message || 'Could not load preset questions.'
  }
})

// Backfill any fields a stale-backend response might be missing so the
// template renders gracefully instead of leaving the bubble body empty.
// Mirrors the layout fallback used by layoutFor() above.
function slugify(text) {
  return String(text || '')
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 40) || 'rec'
}

function normalizeAdvice(advice, presetKey) {
  if (!advice || typeof advice !== 'object') return advice

  const layout = VALID_LAYOUTS.has(advice.layout)
    ? advice.layout
    : PRESET_TO_LAYOUT[presetKey] || 'report'

  const recommendations = Array.isArray(advice.recommendations)
    ? advice.recommendations.map((r, i) => ({
        ...r,
        id: r?.id || slugify(r?.action) || `rec-${i + 1}`,
        follow_up_prompts: Array.isArray(r?.follow_up_prompts) ? r.follow_up_prompts : [],
      }))
    : []

  return {
    ...advice,
    layout,
    recommendations,
    key_facts: Array.isArray(advice.key_facts) ? advice.key_facts : [],
    caveats: Array.isArray(advice.caveats) ? advice.caveats : [],
    next_questions: Array.isArray(advice.next_questions) ? advice.next_questions : [],
  }
}

async function askPreset(preset, { forceRefresh = false } = {}) {
  if (busy.value) return
  busy.value = true

  messages.value.push({ role: 'user', text: preset.label })
  messages.value.push({ role: 'loading' })
  await scrollToBottom()

  try {
    const raw = await fetchWardrobeAdvice(props.garments, preset.key, { forceRefresh })
    const advice = normalizeAdvice(raw, preset.key)
    messages.value.splice(messages.value.length - 1, 1, {
      role: 'advice',
      advice,
      preset,
    })
    chipMode.value = advice.next_questions.length ? 'context' : 'preset'
  } catch (err) {
    messages.value.splice(messages.value.length - 1, 1, {
      role: 'error',
      text: err?.message || 'Failed to get advice. Please try again.',
    })
  } finally {
    busy.value = false
    await scrollToBottom()
  }
}

function reAsk(adviceIdx) {
  const msg = messages.value[adviceIdx]
  if (!msg || msg.role !== 'advice' || !msg.preset) return
  askPreset(msg.preset, { forceRefresh: true })
}

async function askFollowUp(parentIdx, { focusId, prompt }) {
  if (busy.value || !prompt) return
  const parent = messages.value[parentIdx]
  if (!parent || parent.role !== 'advice') return

  busy.value = true
  messages.value.push({ role: 'user', text: prompt, isFollowUp: true })
  messages.value.push({ role: 'loading', isFollowUp: true })
  await scrollToBottom()

  try {
    const followUp = await fetchAdviceFollowUp(
      props.garments,
      parent.preset.key,
      focusId || '',
      prompt,
    )
    messages.value.splice(messages.value.length - 1, 1, {
      role: 'followup',
      followUp,
      parentIdx,
      focusId: focusId || '',
      prompt,
    })
  } catch (err) {
    messages.value.splice(messages.value.length - 1, 1, {
      role: 'error',
      isFollowUp: true,
      text: err?.message || 'Failed to get a follow-up. Please try again.',
    })
  } finally {
    busy.value = false
    await scrollToBottom()
  }
}

async function scrollToBottom() {
  await nextTick()
  const el = streamRef.value
  if (el) el.scrollTo({ top: el.scrollHeight, behavior: 'smooth' })
}
</script>

<style scoped>
/* ── Page wrapper ────────────────────────────────────────────── */
.wd-chat-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 32px 64px;
  font-family: 'Inter', system-ui, -apple-system, Arial, sans-serif;

  min-height: calc(100vh - 88px);
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.wd-chat-page__head {
  display: flex;
  align-items: flex-end;
  gap: 22px;
  margin-bottom: 26px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--color-soft-line);
  flex-wrap: wrap;
}
.wd-chat-page__back {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 8px 16px;
  border-radius: var(--radius-soft-pill);
  background: var(--color-soft-cream);
  border: none;
  color: var(--color-soft-ink-soft);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: var(--shadow-soft-sm);
  transition: background 200ms ease, color 200ms ease, transform 200ms ease;
}
.wd-chat-page__back:hover {
  background: var(--color-soft-milk);
  color: var(--color-soft-ink);
  transform: translateY(-1px);
}
.wd-chat-page__title-block {
  flex: 1; min-width: 240px;
}
.wd-chat-page__eyebrow {
  display: inline-block;
  font-family: var(--font-display);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.22em;
  background: var(--color-soft-sage-mist);
  color: var(--color-soft-sage-deep);
  padding: 5px 12px;
  border-radius: var(--radius-soft-pill);
  margin-bottom: 10px;
  text-transform: uppercase;
}
.wd-chat-page__title {
  font-family: var(--font-display);
  font-size: clamp(26px, 3.6vw, 40px);
  line-height: 1.1;
  letter-spacing: -0.02em;
  font-weight: 700;
  color: var(--color-soft-ink);
}
.wd-chat-page__title-accent {
  color: var(--color-soft-sage-deep);
  font-style: italic;
  font-weight: 800;
}
.wd-chat-page__badge {
  display: inline-flex; align-items: center; gap: 6px;
  font-size: 12px;
  font-weight: 600;
  background: var(--color-soft-sage-mist);
  color: var(--color-soft-sage-deep);
  padding: 7px 14px;
  border-radius: var(--radius-soft-pill);
}

/* ── Chat container ──────────────────────────────────────────── */
.wd-chat {
  display: flex;
  flex-direction: column;
  background: var(--color-soft-cream);
  border-radius: var(--radius-soft-lg);
  border: 1.5px solid var(--color-soft-line-strong);
  box-shadow: var(--shadow-soft);
  overflow: hidden;
  min-height: 580px;
}

/* ── Conversation stream ─────────────────────────────────────── */
.wd-chat__stream {
  flex: 1;
  overflow-y: auto;
  padding: 28px 28px 14px;
  display: flex; flex-direction: column;
  gap: 14px;
  background: var(--color-soft-milk);
  scroll-behavior: smooth;
  min-height: 360px;
  max-height: 60vh;
  scrollbar-width: thin;
  scrollbar-color: rgba(58, 56, 51, 0.18) transparent;
}
.wd-chat__stream::-webkit-scrollbar { width: 6px; }
.wd-chat__stream::-webkit-scrollbar-thumb {
  background: rgba(58, 56, 51, 0.18);
  border-radius: 999px;
}

/* ── Bubbles ─────────────────────────────────────────────────── */
.wd-bubble {
  display: flex;
  gap: 10px;
  max-width: 100%;
}
.wd-bubble--ai {
  align-self: flex-start;
  max-width: 78%;
}
.wd-bubble--user {
  align-self: flex-end;
  max-width: 70%;
  flex-direction: row-reverse;
}
.wd-bubble--indent { margin-left: 24px; }
.wd-bubble--user.wd-bubble--indent { margin-left: 0; margin-right: 24px; }

.wd-bubble__avatar {
  width: 28px; height: 28px;
  border-radius: 999px;
  background: var(--color-soft-sage-mist);
  color: var(--color-soft-sage-deep);
  display: grid; place-items: center;
  flex-shrink: 0;
  margin-top: 4px;
}
.wd-bubble__avatar--alert {
  background: var(--color-soft-dusty-wash);
  color: var(--color-soft-ink);
}
.wd-bubble__avatar--muted {
  background: var(--color-soft-milk);
  color: var(--color-soft-ink-soft);
}
.wd-bubble__body {
  background: var(--color-soft-sage-mist);
  border-radius: 18px;
  padding: 12px 16px;
  font-size: 14px; line-height: 1.55;
  color: var(--color-soft-ink);
  box-shadow: var(--shadow-soft-sm);
  font-weight: 500;
}
.wd-bubble--ai .wd-bubble__body {
  border-top-left-radius: 6px;
}
.wd-bubble--user .wd-bubble__body {
  background: var(--color-soft-dusty-wash);
  color: var(--color-soft-ink);
  border-top-right-radius: 6px;
}
.wd-bubble__body--error {
  background: var(--color-soft-dusty);
  color: var(--color-soft-ink);
}
.wd-bubble__body--note {
  background: var(--color-soft-cream);
  font-size: 12px; line-height: 1.5;
  color: var(--color-soft-ink-soft);
  font-style: italic;
}
.wd-bubble__body--note p + p { margin-top: 4px; }

/* Advice bubble carries the layout body — wider, neutral background so the
   child layout can paint its own visual texture inside. */
.wd-bubble--advice { max-width: 92%; }
.wd-bubble__body--advice {
  background: var(--color-soft-milk);
  padding: 16px 16px 18px;
  position: relative;
  width: 100%;
}

.wd-bubble__refresh {
  position: absolute;
  top: 10px; right: 10px;
  width: 26px; height: 26px;
  border-radius: 999px;
  border: 1px solid var(--color-soft-line);
  background: var(--color-soft-cream);
  color: var(--color-soft-ink-soft);
  display: grid; place-items: center;
  cursor: pointer;
  transition: background 180ms ease, color 180ms ease, transform 180ms ease;
}
.wd-bubble__refresh:hover:not(:disabled) {
  background: var(--color-soft-sage-mist);
  color: var(--color-soft-sage-deep);
  transform: rotate(-30deg);
}
.wd-bubble__refresh:disabled { opacity: 0.45; cursor: not-allowed; }

/* Follow-up mini-bubble — compact, indented, slightly cooler tone. */
.wd-bubble--followup { max-width: 70%; }
.wd-bubble__body--followup {
  background: var(--color-soft-cream);
  border-left: 3px solid var(--color-soft-sage);
  padding: 12px 14px;
}
.wd-followup__headline {
  font-family: var(--font-display);
  font-size: 13.5px;
  font-weight: 700;
  letter-spacing: -0.005em;
  color: var(--color-soft-ink);
  margin-bottom: 6px;
  line-height: 1.3;
}
.wd-followup__body {
  font-size: 13px;
  line-height: 1.55;
  color: var(--color-soft-ink);
}
.wd-followup__facts {
  list-style: none;
  margin: 8px 0 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.wd-followup__fact {
  font-size: 11.5px;
  color: var(--color-soft-ink-soft);
  line-height: 1.45;
}
.wd-followup__fact-label {
  font-family: var(--font-display);
  font-weight: 700;
  letter-spacing: 0.05em;
  color: var(--color-soft-sage-deep);
  margin-right: 4px;
}
.wd-followup__fact-value {
  font-family: var(--font-display);
  color: var(--color-soft-sage-deep);
  font-weight: 700;
  margin-right: 4px;
}
.wd-followup__chips {
  margin-top: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

/* Typing indicator */
.wd-bubble__body--typing {
  display: inline-flex; gap: 4px;
  padding: 14px 16px;
}
.wd-bubble__body--typing span {
  width: 7px; height: 7px;
  border-radius: 999px;
  background: var(--color-soft-ink-soft);
  animation: wd-typing 1.2s infinite ease-in-out;
}
.wd-bubble__body--typing span:nth-child(2) { animation-delay: 0.15s; }
.wd-bubble__body--typing span:nth-child(3) { animation-delay: 0.3s; }
@keyframes wd-typing {
  0%, 60%, 100% { opacity: 0.3; transform: translateY(0); }
  30%           { opacity: 1;   transform: translateY(-3px); }
}

/* ── Preset chip bar ─────────────────────────────────────────── */
.wd-chat__chips {
  border-top: 1px solid var(--color-soft-line);
  padding: 18px 24px 22px;
  background: var(--color-soft-cream);
}
.wd-chat__chips-hint {
  font-family: var(--font-display);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.18em;
  color: var(--color-soft-ink-soft);
  margin-bottom: 12px;
  text-transform: uppercase;
}
.wd-chat__chip-row {
  display: flex; flex-wrap: wrap; gap: 8px;
}
.wd-chip {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 9px 16px;
  border-radius: var(--radius-soft-pill);
  background: var(--color-soft-cream);
  border: 1px solid var(--color-soft-line);
  color: var(--color-soft-ink);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: background 200ms ease, color 200ms ease,
              border-color 200ms ease, transform 200ms ease;
}
.wd-chip:hover:not(:disabled) {
  background: var(--color-soft-sage-mist);
  color: var(--color-soft-sage-deep);
  border-color: transparent;
  transform: translateY(-1px);
}
.wd-chip:disabled { opacity: 0.5; cursor: not-allowed; }
.wd-chip > :first-child { color: var(--color-soft-sage-deep); }
.wd-chip--sub {
  padding: 6px 12px;
  font-size: 12px;
}
.wd-chip--ghost {
  background: transparent;
  border-style: dashed;
  color: var(--color-soft-ink-soft);
}

.wd-chat__chips-error {
  display: inline-flex; align-items: center; gap: 4px;
  margin-top: 8px;
  font-size: 11.5px;
  color: var(--color-soft-dusty);
}

/* ── Mobile ──────────────────────────────────────────────────── */
@media (max-width: 700px) {
  .wd-chat-page {
    padding: 20px 16px 48px;
    min-height: 0;
    justify-content: flex-start;
  }
  .wd-chat { border-radius: var(--radius-card); min-height: 480px; }
  .wd-chat__stream { padding: 18px 16px 10px; max-height: 56vh; }
  .wd-chat__chips { padding: 14px 16px 18px; }
  .wd-bubble--ai { max-width: 92%; }
  .wd-bubble--user { max-width: 88%; }
  .wd-bubble--advice { max-width: 98%; }
  .wd-bubble--followup { max-width: 88%; }
  .wd-bubble__body { font-size: 13.5px; }
  .wd-bubble--indent { margin-left: 12px; }
  .wd-bubble--user.wd-bubble--indent { margin-left: 0; margin-right: 12px; }
}
</style>
