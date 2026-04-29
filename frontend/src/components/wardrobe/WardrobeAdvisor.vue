<template>
  <section class="wd-chat-page">
    <!-- Page header — back button + title bar, mirroring WardrobeMain layout -->
    <header class="wd-chat-page__head">
      <button type="button" class="wd-chat-page__back" @click="$emit('close')">
        <ArrowLeft :size="16" :stroke-width="2" /> Back to wardrobe
      </button>
      <div class="wd-chat-page__title-block">
        <p class="wd-chat-page__eyebrow">AI Sustainability Advisor</p>
        <h2 class="wd-chat-page__title">
          Grounded in your wardrobe — answers in seconds.
        </h2>
      </div>
      <span class="wd-chat-page__badge">
        <Sparkles :size="13" :stroke-width="2" />
        {{ garmentCount }} item{{ garmentCount === 1 ? '' : 's' }} analysed
      </span>
    </header>

    <div class="wd-chat" role="region" aria-label="AI advisor conversation">

    <!-- Conversation stream -->
    <div ref="streamRef" class="wd-chat__stream">
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
        <!-- User question bubble -->
        <div v-if="msg.role === 'user'" class="wd-bubble wd-bubble--user">
          <div class="wd-bubble__body">{{ msg.text }}</div>
        </div>

        <!-- AI typing indicator -->
        <div v-else-if="msg.role === 'loading'" class="wd-bubble wd-bubble--ai">
          <span class="wd-bubble__avatar"><Sparkles :size="13" :stroke-width="2" /></span>
          <div class="wd-bubble__body wd-bubble__body--typing">
            <span></span><span></span><span></span>
          </div>
        </div>

        <!-- AI error -->
        <div v-else-if="msg.role === 'error'" class="wd-bubble wd-bubble--ai">
          <span class="wd-bubble__avatar wd-bubble__avatar--alert">
            <CircleAlert :size="13" :stroke-width="2" />
          </span>
          <div class="wd-bubble__body wd-bubble__body--error">{{ msg.text }}</div>
        </div>

        <!-- AI structured advice — split into 3-4 bubbles for rhythm -->
        <template v-else-if="msg.role === 'advice'">
          <!-- 1. Headline + summary -->
          <div class="wd-bubble wd-bubble--ai">
            <span class="wd-bubble__avatar"><Sparkles :size="13" :stroke-width="2" /></span>
            <div class="wd-bubble__body">
              <p class="wd-bubble__headline">{{ msg.advice.headline }}</p>
              <p class="wd-bubble__summary">{{ msg.advice.summary }}</p>
            </div>
          </div>

          <!-- 2. Key facts as inline mini-cards -->
          <div class="wd-bubble wd-bubble--ai">
            <span class="wd-bubble__avatar"><Sparkles :size="13" :stroke-width="2" /></span>
            <div class="wd-bubble__body wd-bubble__body--facts">
              <p class="wd-bubble__line">By the numbers:</p>
              <ul class="wd-facts">
                <li v-for="f in msg.advice.key_facts" :key="f.label" class="wd-facts__item">
                  <p class="wd-facts__label">{{ f.label }}</p>
                  <p class="wd-facts__value">{{ f.value }}</p>
                  <p class="wd-facts__ctx">{{ f.context }}</p>
                </li>
              </ul>
            </div>
          </div>

          <!-- 3. Recommendations -->
          <div class="wd-bubble wd-bubble--ai">
            <span class="wd-bubble__avatar"><Sparkles :size="13" :stroke-width="2" /></span>
            <div class="wd-bubble__body">
              <p class="wd-bubble__line">What you can do:</p>
              <ol class="wd-recs">
                <li v-for="(r, i) in msg.advice.recommendations" :key="i" class="wd-recs__item">
                  <div>
                    <p class="wd-recs__action">{{ r.action }}</p>
                    <p class="wd-recs__impact">{{ r.impact }}</p>
                  </div>
                  <span
                    class="wd-recs__diff"
                    :class="`wd-recs__diff--${r.difficulty}`"
                  >{{ r.difficulty }}</span>
                </li>
              </ol>
            </div>
          </div>

          <!-- 4. Caveats — only if present -->
          <div v-if="msg.advice.caveats?.length" class="wd-bubble wd-bubble--ai">
            <span class="wd-bubble__avatar wd-bubble__avatar--muted">
              <CircleAlert :size="13" :stroke-width="2" />
            </span>
            <div class="wd-bubble__body wd-bubble__body--note">
              <p v-for="(c, ci) in msg.advice.caveats" :key="ci">{{ c }}</p>
            </div>
          </div>
        </template>
      </template>
    </div>

    <!-- Preset chip bar (always visible, doubles as suggestion bar) -->
    <footer class="wd-chat__chips">
      <p v-if="!messages.length" class="wd-chat__chips-hint">
        Pick a question to start
      </p>
      <p v-else class="wd-chat__chips-hint">
        Ask another
      </p>
      <div class="wd-chat__chip-row">
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
import { ArrowLeft, CircleAlert, Sparkles } from 'lucide-vue-next'
import { fetchPresetQuestions, fetchWardrobeAdvice } from '../../services/advisorApi.js'

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

onMounted(async () => {
  try {
    presets.value = await fetchPresetQuestions()
  } catch (err) {
    presetsError.value = err?.message || 'Could not load preset questions.'
  }
})

async function askPreset(preset) {
  if (busy.value) return
  busy.value = true

  messages.value.push({ role: 'user', text: preset.label })
  messages.value.push({ role: 'loading' })
  await scrollToBottom()

  try {
    const advice = await fetchWardrobeAdvice(props.garments, preset.key)
    // Replace the trailing loading bubble with the structured advice entry.
    messages.value.splice(messages.value.length - 1, 1, {
      role: 'advice',
      advice,
    })
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

async function scrollToBottom() {
  await nextTick()
  const el = streamRef.value
  if (el) el.scrollTo({ top: el.scrollHeight, behavior: 'smooth' })
}
</script>

<style scoped>
/* ── Page wrapper ────────────────────────────────────────────── */
.wd-chat-page {
  max-width: 1100px;
  margin: 0 auto;
  padding: 32px 32px 64px;
  font-family: 'Inter', system-ui, -apple-system, Arial, sans-serif;

  /* Vertically centre the [header + chat] block in the viewport area
     left below the global navbar. When the conversation grows past the
     viewport, this still falls back to natural flow because the chat
     itself is constrained by max-height + scroll. */
  min-height: calc(100vh - 88px);
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.wd-chat-page__head {
  display: flex;
  align-items: center;
  gap: 18px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}
.wd-chat-page__back {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 8px 14px;
  border-radius: var(--radius-pill);
  background: transparent;
  border: 1px solid var(--color-border-strong);
  color: var(--color-text-muted);
  font-size: 13px; font-weight: 600;
  cursor: pointer;
  transition: color var(--transition-base), background var(--transition-base);
}
.wd-chat-page__back:hover {
  color: var(--color-text);
  background: var(--color-surface-alt);
}
.wd-chat-page__title-block {
  flex: 1; min-width: 220px;
}
.wd-chat-page__eyebrow {
  font-size: 11px; font-weight: 700; letter-spacing: 2px;
  color: var(--color-primary-text);
  text-transform: uppercase;
  margin-bottom: 4px;
}
.wd-chat-page__title {
  font-size: clamp(20px, 3vw, 24px);
  font-weight: 800; letter-spacing: -0.4px;
  line-height: 1.25;
  color: var(--color-text);
}
.wd-chat-page__badge {
  display: inline-flex; align-items: center; gap: 6px;
  font-size: 12px; font-weight: 700;
  background: var(--color-primary-light);
  color: var(--color-primary-text);
  padding: 6px 12px;
  border-radius: var(--radius-pill);
  border: 1px solid var(--color-border-light);
}

/* ── Chat container (lives inside the page) ─────────────────── */
.wd-chat {
  display: flex;
  flex-direction: column;
  background: var(--color-surface);
  border-radius: var(--radius-card-lg);
  box-shadow: var(--shadow-card);
  overflow: hidden;
  min-height: 560px;
}

/* ── Conversation stream ─────────────────────────────────────── */
.wd-chat__stream {
  flex: 1;
  overflow-y: auto;
  padding: 28px 28px 14px;
  display: flex; flex-direction: column;
  gap: 14px;
  background: var(--color-bg);
  scroll-behavior: smooth;
  min-height: 360px;
  max-height: 60vh;
}

/* ── Bubbles ─────────────────────────────────────────────────── */
.wd-bubble {
  display: flex;
  gap: 8px;
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
.wd-bubble__avatar {
  width: 26px; height: 26px;
  border-radius: 999px;
  background: var(--color-primary);
  color: var(--color-primary-text);
  display: grid; place-items: center;
  flex-shrink: 0;
  margin-top: 2px;
}
.wd-bubble__avatar--alert {
  background: rgba(208, 50, 56, 0.14);
  color: var(--color-danger);
}
.wd-bubble__avatar--muted {
  background: var(--color-surface-alt);
  color: var(--color-text-subtle);
}
.wd-bubble__body {
  background: var(--color-surface);
  border: 1px solid var(--color-border-light);
  border-radius: 16px;
  padding: 12px 14px;
  font-size: 14px; line-height: 1.55;
  color: var(--color-text);
  box-shadow: 0 1px 2px rgba(22, 51, 0, 0.04);
}
.wd-bubble--ai .wd-bubble__body {
  border-top-left-radius: 4px;
}
.wd-bubble--user .wd-bubble__body {
  background: var(--color-primary);
  color: var(--color-primary-text);
  border-color: var(--color-primary);
  border-top-right-radius: 4px;
  font-weight: 600;
}
.wd-bubble__body--error {
  background: rgba(208, 50, 56, 0.08);
  border-color: rgba(208, 50, 56, 0.4);
  color: var(--color-danger);
}
.wd-bubble__body--note {
  background: var(--color-surface-alt);
  border-style: dashed;
  font-size: 12px; line-height: 1.5;
  color: var(--color-text-subtle);
  font-style: italic;
}
.wd-bubble__body--note p + p { margin-top: 4px; }

/* Typing indicator */
.wd-bubble__body--typing {
  display: inline-flex; gap: 4px;
  padding: 14px 16px;
}
.wd-bubble__body--typing span {
  width: 6px; height: 6px;
  border-radius: 999px;
  background: var(--color-text-subtle);
  animation: wd-typing 1.2s infinite ease-in-out;
}
.wd-bubble__body--typing span:nth-child(2) { animation-delay: 0.15s; }
.wd-bubble__body--typing span:nth-child(3) { animation-delay: 0.3s; }
@keyframes wd-typing {
  0%, 60%, 100% { opacity: 0.3; transform: translateY(0); }
  30%           { opacity: 1;   transform: translateY(-3px); }
}

/* Headline / summary */
.wd-bubble__headline {
  font-size: 15px; font-weight: 700;
  margin-bottom: 6px;
  letter-spacing: -0.2px;
  line-height: 1.35;
}
.wd-bubble__summary {
  font-size: 13.5px; line-height: 1.55;
  color: var(--color-text-muted);
}
.wd-bubble__line {
  font-size: 12px; font-weight: 700; letter-spacing: 0.8px;
  color: var(--color-primary-text);
  text-transform: uppercase;
  margin-bottom: 8px;
}

/* Facts inline mini-cards */
.wd-bubble__body--facts { padding: 12px; }
.wd-facts {
  list-style: none; padding: 0;
  display: grid;
  grid-template-columns: 1fr;
  gap: 6px;
}
.wd-facts__item {
  background: var(--color-primary-lighter);
  border: 1px solid var(--color-border-light);
  border-radius: 10px;
  padding: 8px 10px;
}
.wd-facts__label {
  font-size: 10px; font-weight: 700; letter-spacing: 1.2px;
  color: var(--color-primary-text);
  text-transform: uppercase;
  margin-bottom: 2px;
}
.wd-facts__value {
  font-size: 16px; font-weight: 800;
  color: var(--color-text);
  letter-spacing: -0.3px;
  margin-bottom: 2px;
}
.wd-facts__ctx {
  font-size: 11.5px; line-height: 1.45;
  color: var(--color-text-muted);
}

/* Recommendations list */
.wd-recs {
  list-style: none; padding: 0;
  counter-reset: rec;
  display: flex; flex-direction: column; gap: 6px;
}
.wd-recs__item {
  display: grid;
  grid-template-columns: 22px 1fr auto;
  align-items: center;
  gap: 10px;
  padding: 8px 4px;
  counter-increment: rec;
}
.wd-recs__item::before {
  content: counter(rec);
  width: 22px; height: 22px;
  border-radius: 999px;
  background: var(--color-primary);
  color: var(--color-primary-text);
  display: grid; place-items: center;
  font-size: 11px; font-weight: 800;
}
.wd-recs__action {
  font-size: 13px; font-weight: 700;
  color: var(--color-text);
  margin-bottom: 1px;
  line-height: 1.3;
}
.wd-recs__impact {
  font-size: 11.5px;
  color: var(--color-text-muted);
  line-height: 1.4;
}
.wd-recs__diff {
  font-size: 9px; font-weight: 800; letter-spacing: 0.8px;
  padding: 3px 8px;
  border-radius: 999px;
  text-transform: uppercase;
}
.wd-recs__diff--easy {
  background: var(--color-primary-light);
  color: var(--color-primary-text);
}
.wd-recs__diff--medium {
  background: rgba(255, 192, 145, 0.25);
  color: #8a4a18;
}
.wd-recs__diff--hard {
  background: rgba(208, 50, 56, 0.12);
  color: var(--color-danger);
}

/* ── Preset chip bar ─────────────────────────────────────────── */
.wd-chat__chips {
  border-top: 1px solid var(--color-border-light);
  padding: 18px 24px 22px;
  background: var(--color-surface);
}
.wd-chat__chips-hint {
  font-size: 11px; font-weight: 700; letter-spacing: 1.6px;
  color: var(--color-text-subtle);
  text-transform: uppercase;
  margin-bottom: 10px;
}
.wd-chat__chip-row {
  display: flex; flex-wrap: wrap; gap: 8px;
}
.wd-chip {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 9px 14px;
  border-radius: 999px;
  background: var(--color-surface);
  border: 1px solid var(--color-border-strong);
  color: var(--color-text);
  font-size: 13px; font-weight: 600;
  cursor: pointer;
  transition:
    transform var(--transition-base),
    background var(--transition-base),
    border-color var(--transition-base);
}
.wd-chip:hover:not(:disabled) {
  background: var(--color-primary-lighter);
  border-color: var(--color-primary-text);
  transform: translateY(-1px);
}
.wd-chip:disabled { opacity: 0.5; cursor: not-allowed; }
.wd-chip > :first-child { color: var(--color-primary-text); }

.wd-chat__chips-error {
  display: inline-flex; align-items: center; gap: 4px;
  margin-top: 8px;
  font-size: 11px;
  color: var(--color-danger);
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
  .wd-bubble__body { font-size: 13.5px; }
}
</style>
