<template>
  <div class="adv-report">
    <p class="adv-report__headline">{{ advice.headline }}</p>
    <p class="adv-report__summary">{{ advice.summary }}</p>

    <div class="adv-report__hero">
      <p class="adv-report__hero-label">{{ heroFact.label }}</p>
      <p class="adv-report__hero-value">{{ heroFact.value }}</p>
      <p class="adv-report__hero-ctx">{{ heroFact.context }}</p>
    </div>

    <ul v-if="sideFacts.length" class="adv-report__side">
      <li v-for="f in sideFacts" :key="f.label" class="adv-report__side-item">
        <p class="adv-report__side-label">{{ f.label }}</p>
        <p class="adv-report__side-value">{{ f.value }}</p>
        <p class="adv-report__side-ctx">{{ f.context }}</p>
      </li>
    </ul>

    <section class="adv-report__actions">
      <p class="adv-report__section-label">Two moves worth making</p>
      <ul class="adv-report__rec-list">
        <li v-for="r in advice.recommendations" :key="r.id" class="adv-report__rec">
          <div class="adv-report__rec-text">
            <p class="adv-report__rec-action">{{ r.action }}</p>
            <p class="adv-report__rec-impact">{{ r.impact }}</p>
            <div v-if="r.follow_up_prompts?.length" class="adv-report__rec-chips">
              <button
                v-for="p in r.follow_up_prompts"
                :key="p"
                type="button"
                class="adv-chip adv-chip--sub"
                @click="$emit('follow-up', { focusId: r.id, prompt: p })"
              >
                {{ p }}
                <ArrowRight :size="11" :stroke-width="2.2" />
              </button>
            </div>
          </div>
          <span
            class="adv-report__rec-diff"
            :class="`adv-report__rec-diff--${r.difficulty}`"
          >{{ r.difficulty }}</span>
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

const heroFact = computed(() => props.advice.key_facts[0])
const sideFacts = computed(() => props.advice.key_facts.slice(1))
</script>

<style scoped>
.adv-report {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.adv-report__headline {
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: var(--color-soft-ink);
  line-height: 1.3;
}
.adv-report__summary {
  font-size: 13.5px;
  line-height: 1.55;
  color: var(--color-soft-ink);
}

.adv-report__hero {
  background: var(--color-soft-sage-deep);
  color: var(--color-soft-cream);
  border-radius: 16px;
  padding: 18px 20px;
  box-shadow: var(--shadow-soft);
}
.adv-report__hero-label {
  font-family: var(--font-display);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  opacity: 0.7;
  margin-bottom: 6px;
}
.adv-report__hero-value {
  font-family: var(--font-display);
  font-size: 30px;
  font-weight: 800;
  letter-spacing: -0.02em;
  line-height: 1.05;
  color: var(--color-soft-sage);
  margin-bottom: 6px;
}
.adv-report__hero-ctx {
  font-size: 12.5px;
  line-height: 1.5;
  opacity: 0.85;
}

.adv-report__side {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 8px;
}
.adv-report__side-item {
  background: var(--color-soft-cream);
  border-radius: 12px;
  padding: 10px 12px;
  box-shadow: var(--shadow-soft-sm);
}
.adv-report__side-label {
  font-family: var(--font-display);
  font-size: 9.5px;
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--color-soft-ink-soft);
  margin-bottom: 4px;
}
.adv-report__side-value {
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 700;
  color: var(--color-soft-sage-deep);
  letter-spacing: -0.01em;
  margin-bottom: 2px;
}
.adv-report__side-ctx {
  font-size: 11.5px;
  line-height: 1.4;
  color: var(--color-soft-ink-soft);
}

.adv-report__actions {
  border-top: 1px dashed var(--color-soft-line);
  padding-top: 12px;
}
.adv-report__section-label {
  font-family: var(--font-display);
  font-size: 10.5px;
  font-weight: 700;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--color-soft-sage-deep);
  margin-bottom: 10px;
}
.adv-report__rec-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.adv-report__rec {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 10px;
  align-items: start;
  background: var(--color-soft-cream);
  border-radius: 14px;
  padding: 10px 12px;
  box-shadow: var(--shadow-soft-sm);
}
.adv-report__rec-action {
  font-size: 13.5px;
  font-weight: 600;
  color: var(--color-soft-ink);
  line-height: 1.35;
  margin-bottom: 2px;
}
.adv-report__rec-impact {
  font-size: 12px;
  color: var(--color-soft-ink-soft);
  line-height: 1.45;
}
.adv-report__rec-chips {
  margin-top: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.adv-report__rec-diff {
  align-self: start;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.06em;
  padding: 3px 9px;
  border-radius: 999px;
  text-transform: uppercase;
}
.adv-report__rec-diff--easy   { background: var(--color-soft-sage-mist); color: var(--color-soft-sage-deep); }
.adv-report__rec-diff--medium { background: var(--color-soft-oat); color: var(--color-soft-ink); }
.adv-report__rec-diff--hard   { background: var(--color-soft-dusty-wash); color: var(--color-soft-ink); }

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
.adv-chip--sub { font-size: 11px; }
.adv-chip > svg { color: var(--color-soft-sage-deep); }
</style>
