<template>
  <section id="wardrobe-teaser" class="wt">
    <div
      class="wt__card"
      v-motion
      :initial="{ opacity: 0, y: 32 }"
      :visible-once="{ opacity: 1, y: 0, transition: { duration: 700 } }"
    >
      <div class="wt__header">
        <span class="wt__badge">
          <Sparkles :size="14" :stroke-width="2" />
          Coming soon — available with the Wardrobe module
        </span>
        <h2 class="wt__title">Get AI advice grounded in your own wardrobe.</h2>
        <p class="wt__subtitle">
          Once you start tracking what you own, this assistant will reason about overlap,
          care, and lifecycle — based on your actual closet, not a stock dataset.
        </p>
      </div>

      <div class="wt__chat" aria-hidden="true">
        <div class="wt__bubble wt__bubble--user">
          <span class="wt__bubble-meta">You</span>
          <p>I bought another black hoodie yesterday — was that a smart move?</p>
        </div>

        <div class="wt__bubble wt__bubble--ai">
          <span class="wt__bubble-meta">
            <Sparkles :size="12" :stroke-width="2.2" /> Wardrobe AI
          </span>
          <p>
            You already own 4 black hoodies, and the most-worn one has only logged
            <strong>6 wears</strong> in 14 months. Returning the new one — or pairing it with a
            colour you currently don't own (cream / forest green) — would diversify your
            outfit options without growing the closet.
          </p>
        </div>
      </div>

      <form
        class="wt__composer"
        @submit.prevent
        title="Available with the Wardrobe module"
      >
        <input
          type="text"
          class="wt__input"
          placeholder="Ask about an item in your wardrobe…"
          disabled
          aria-disabled="true"
          title="Available with the Wardrobe module"
        />
        <button
          type="button"
          class="wt__send"
          disabled
          aria-disabled="true"
          aria-label="Send (available with the Wardrobe module)"
          title="Available with the Wardrobe module"
        >
          <Send :size="16" :stroke-width="2" />
        </button>
        <span class="wt__lock-hint">
          <Lock :size="12" :stroke-width="2.2" />
          Unlocks once your wardrobe has at least one item
        </span>
      </form>
    </div>
  </section>
</template>

<script setup>
// Visual placeholder only. This component:
// - imports NO LLM SDK
// - performs NO fetch / axios / WebSocket / SSE call
// - reads NO wardrobe data — every bubble is hand-written copy
// Epic 3 will hydrate this shell with the real advisor.
import { Sparkles, Send, Lock } from 'lucide-vue-next'
</script>

<style scoped>
.wt {
  padding: 60px 20px 140px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.wt__card {
  width: 100%;
  max-width: 760px;
  padding: 40px 36px 32px;
  background: var(--color-kh-glass);
  border: 1px solid var(--color-kh-glass-border);
  border-radius: 24px;
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  box-shadow: var(--shadow-kh-glow);
  display: flex;
  flex-direction: column;
  gap: 28px;
}

.wt__header {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 14px;
}

.wt__badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.04em;
  color: var(--color-kh-accent);
  background: rgba(255, 192, 145, 0.1);
  border: 1px solid rgba(255, 192, 145, 0.3);
  border-radius: 999px;
}

.wt__title {
  margin: 0;
  font-size: clamp(1.6rem, 3vw, 2.2rem);
  line-height: 1.2;
  font-weight: 700;
  color: var(--color-kh-text);
  letter-spacing: -0.01em;
  text-wrap: balance;
}

.wt__subtitle {
  margin: 0;
  font-size: 15px;
  line-height: 1.55;
  color: var(--color-kh-text-muted);
  max-width: 560px;
}

.wt__chat {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.wt__bubble {
  max-width: 80%;
  padding: 14px 18px;
  border-radius: 18px;
  font-size: 14px;
  line-height: 1.55;
  color: var(--color-kh-text);
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.wt__bubble p {
  margin: 0;
  color: var(--color-kh-text);
}

.wt__bubble strong {
  color: var(--color-kh-correct);
  font-weight: 600;
}

.wt__bubble-meta {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--color-kh-text-faint);
}

.wt__bubble--user {
  align-self: flex-end;
  background: rgba(255, 192, 145, 0.1);
  border: 1px solid rgba(255, 192, 145, 0.25);
  border-bottom-right-radius: 6px;
}

.wt__bubble--ai {
  align-self: flex-start;
  background: var(--color-kh-glass-strong);
  border: 1px solid var(--color-kh-glass-border);
  border-bottom-left-radius: 6px;
}

.wt__composer {
  position: relative;
  display: grid;
  grid-template-columns: 1fr auto;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 18px;
  background: var(--color-kh-glass-strong);
  border: 1px solid var(--color-kh-glass-border);
  cursor: not-allowed;
}

.wt__input {
  width: 100%;
  background: transparent;
  border: 0;
  outline: 0;
  padding: 10px 14px;
  font-size: 14px;
  color: var(--color-kh-text);
  cursor: not-allowed;
}

.wt__input::placeholder {
  color: var(--color-kh-text-faint);
}

.wt__input:disabled {
  opacity: 0.7;
}

.wt__send {
  width: 40px;
  height: 40px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  background: rgba(255, 192, 145, 0.16);
  border: 1px solid rgba(255, 192, 145, 0.32);
  color: var(--color-kh-accent);
  cursor: not-allowed;
  opacity: 0.7;
}

.wt__lock-hint {
  position: absolute;
  bottom: -28px;
  left: 4px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--color-kh-text-faint);
}

@media (max-width: 640px) {
  .wt__card {
    padding: 32px 22px 24px;
  }
  .wt__bubble {
    max-width: 100%;
  }
  .wt__lock-hint {
    position: static;
    margin-top: 4px;
  }
}
</style>
