<template>
  <div class="adv-decide">
    <p class="adv-decide__headline">{{ advice.headline }}</p>
    <p class="adv-decide__summary">{{ advice.summary }}</p>

    <div class="adv-decide__compare">
      <article
        v-for="(f, idx) in compareFacts"
        :key="f.label"
        class="adv-decide__side"
        :class="idx === 0 ? 'adv-decide__side--you' : 'adv-decide__side--world'"
      >
        <p class="adv-decide__side-label">{{ idx === 0 ? 'You' : 'For reference' }}</p>
        <p class="adv-decide__side-fact">{{ f.label }}</p>
        <p class="adv-decide__side-value">{{ f.value }}</p>
        <p class="adv-decide__side-ctx">{{ f.context }}</p>
      </article>
    </div>

    <p v-if="trailingFact" class="adv-decide__footnote">
      <span class="adv-decide__footnote-label">{{ trailingFact.label }}:</span>
      {{ trailingFact.value }} — {{ trailingFact.context }}
    </p>

    <section class="adv-decide__actions">
      <p class="adv-decide__section-label">If you do buy, do it like this</p>
      <ul class="adv-decide__rec-list">
        <li v-for="r in advice.recommendations" :key="r.id" class="adv-decide__rec">
          <div class="adv-decide__rec-row">
            <p class="adv-decide__rec-action">{{ r.action }}</p>
            <span
              class="adv-decide__rec-diff"
              :class="`adv-decide__rec-diff--${r.difficulty}`"
            >{{ r.difficulty }}</span>
          </div>
          <p class="adv-decide__rec-impact">{{ r.impact }}</p>
          <div v-if="r.follow_up_prompts?.length" class="adv-decide__rec-chips">
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
        </li>
      </ul>
    </section>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { ArrowRight } from 'lucide-vue-next'

const props = defineProps({
  advice: { type: Object, required: true },
})
defineEmits(['follow-up'])

const compareFacts = computed(() => props.advice.key_facts.slice(0, 2))
const trailingFact = computed(() => props.advice.key_facts[2] || null)
</script>

<style scoped>
.adv-decide {
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.adv-decide__headline {
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: var(--color-soft-ink);
  line-height: 1.3;
}
.adv-decide__summary {
  font-size: 13.5px;
  line-height: 1.55;
  color: var(--color-soft-ink);
  font-style: italic;
}

.adv-decide__compare {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}
.adv-decide__side {
  border-radius: 16px;
  padding: 14px;
  box-shadow: var(--shadow-soft-sm);
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.adv-decide__side--you {
  background: var(--color-soft-sage);
  color: var(--color-soft-sage-deep);
}
.adv-decide__side--world {
  background: var(--color-soft-cream);
  color: var(--color-soft-ink);
}
.adv-decide__side-label {
  font-family: var(--font-display);
  font-size: 9.5px;
  font-weight: 700;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  opacity: 0.7;
}
.adv-decide__side-fact {
  font-size: 11.5px;
  font-weight: 600;
  line-height: 1.35;
  opacity: 0.85;
}
.adv-decide__side-value {
  font-family: var(--font-display);
  font-size: 22px;
  font-weight: 800;
  letter-spacing: -0.02em;
  line-height: 1.1;
  margin-top: 2px;
}
.adv-decide__side-ctx {
  font-size: 11.5px;
  line-height: 1.45;
  opacity: 0.78;
  margin-top: 4px;
}

.adv-decide__footnote {
  font-size: 11.5px;
  line-height: 1.5;
  color: var(--color-soft-ink-soft);
  background: var(--color-soft-milk);
  padding: 8px 12px;
  border-radius: 10px;
}
.adv-decide__footnote-label {
  font-family: var(--font-display);
  font-weight: 700;
  letter-spacing: 0.05em;
  color: var(--color-soft-sage-deep);
}

.adv-decide__actions {
  border-top: 1px dashed var(--color-soft-line);
  padding-top: 12px;
}
.adv-decide__section-label {
  font-family: var(--font-display);
  font-size: 10.5px;
  font-weight: 700;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--color-soft-sage-deep);
  margin-bottom: 10px;
}
.adv-decide__rec-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.adv-decide__rec {
  background: var(--color-soft-cream);
  border-radius: 14px;
  padding: 10px 12px;
  box-shadow: var(--shadow-soft-sm);
}
.adv-decide__rec-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 4px;
}
.adv-decide__rec-action {
  font-size: 13.5px;
  font-weight: 600;
  color: var(--color-soft-ink);
  line-height: 1.35;
}
.adv-decide__rec-impact {
  font-size: 12px;
  color: var(--color-soft-ink-soft);
  line-height: 1.45;
}
.adv-decide__rec-diff {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.06em;
  padding: 3px 9px;
  border-radius: 999px;
  text-transform: uppercase;
}
.adv-decide__rec-diff--easy   { background: var(--color-soft-sage-mist); color: var(--color-soft-sage-deep); }
.adv-decide__rec-diff--medium { background: var(--color-soft-oat); color: var(--color-soft-ink); }
.adv-decide__rec-diff--hard   { background: var(--color-soft-dusty-wash); color: var(--color-soft-ink); }
.adv-decide__rec-chips {
  margin-top: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
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

@media (max-width: 540px) {
  .adv-decide__compare { grid-template-columns: 1fr; }
}
</style>
