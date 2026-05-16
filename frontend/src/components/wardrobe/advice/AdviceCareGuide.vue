<template>
  <div class="adv-care">
    <header class="adv-care__head">
      <p class="adv-care__eyebrow">
        <Scissors :size="11" :stroke-width="2.4" /> Care guide
      </p>
      <p class="adv-care__headline">{{ advice.headline }}</p>
      <p class="adv-care__summary">{{ advice.summary }}</p>
    </header>

    <ul class="adv-care__cards">
      <li v-for="r in advice.recommendations" :key="r.id" class="adv-care__card">
        <div class="adv-care__card-perforation"></div>
        <div class="adv-care__card-body">
          <p class="adv-care__card-action">{{ r.action }}</p>
          <p class="adv-care__card-impact">{{ r.impact }}</p>
          <div class="adv-care__card-foot">
            <span
              class="adv-care__card-diff"
              :class="`adv-care__card-diff--${r.difficulty}`"
            >{{ r.difficulty }} effort</span>
            <div v-if="r.follow_up_prompts?.length" class="adv-care__card-chips">
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
        </div>
      </li>
    </ul>

    <footer class="adv-care__numbers">
      <p class="adv-care__numbers-label">By the numbers</p>
      <ul class="adv-care__numbers-row">
        <li v-for="f in advice.key_facts" :key="f.label" class="adv-care__numbers-item">
          <p class="adv-care__numbers-fact">{{ f.label }}</p>
          <p class="adv-care__numbers-value">{{ f.value }}</p>
          <p class="adv-care__numbers-ctx">{{ f.context }}</p>
        </li>
      </ul>
    </footer>
  </div>
</template>

<script setup>
import { ArrowRight, Scissors } from 'lucide-vue-next'

defineProps({
  advice: { type: Object, required: true },
})
defineEmits(['follow-up'])
</script>

<style scoped>
.adv-care {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.adv-care__head {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.adv-care__eyebrow {
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
.adv-care__headline {
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: var(--color-soft-ink);
  line-height: 1.3;
}
.adv-care__summary {
  font-size: 13.5px;
  line-height: 1.55;
  color: var(--color-soft-ink);
}

.adv-care__cards {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.adv-care__card {
  position: relative;
  display: grid;
  grid-template-columns: 24px 1fr;
  align-items: stretch;
  background: var(--color-soft-cream);
  border-radius: 14px;
  border-left: 3px dashed var(--color-soft-sage);
  box-shadow: var(--shadow-soft-sm);
  overflow: hidden;
}
.adv-care__card-perforation {
  background:
    radial-gradient(circle at 6px 8px, var(--color-soft-milk) 3px, transparent 3.5px) 0 0 / 12px 14px;
  opacity: 0.55;
}
.adv-care__card-body {
  padding: 12px 14px 12px 4px;
}
.adv-care__card-action {
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 700;
  letter-spacing: -0.005em;
  color: var(--color-soft-ink);
  line-height: 1.3;
  margin-bottom: 4px;
}
.adv-care__card-impact {
  font-size: 12px;
  color: var(--color-soft-ink-soft);
  line-height: 1.5;
  margin-bottom: 8px;
}
.adv-care__card-foot {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
}
.adv-care__card-diff {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.08em;
  padding: 3px 9px;
  border-radius: 999px;
  text-transform: uppercase;
}
.adv-care__card-diff--easy   { background: var(--color-soft-sage-mist); color: var(--color-soft-sage-deep); }
.adv-care__card-diff--medium { background: var(--color-soft-oat); color: var(--color-soft-ink); }
.adv-care__card-diff--hard   { background: var(--color-soft-dusty-wash); color: var(--color-soft-ink); }
.adv-care__card-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.adv-care__numbers {
  background: var(--color-soft-milk);
  border-radius: 14px;
  padding: 12px 14px;
}
.adv-care__numbers-label {
  font-family: var(--font-display);
  font-size: 10.5px;
  font-weight: 700;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--color-soft-sage-deep);
  margin-bottom: 8px;
}
.adv-care__numbers-row {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 8px;
}
.adv-care__numbers-item {
  background: var(--color-soft-cream);
  border-radius: 10px;
  padding: 8px 10px;
  box-shadow: var(--shadow-soft-sm);
}
.adv-care__numbers-fact {
  font-family: var(--font-display);
  font-size: 9.5px;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--color-soft-ink-soft);
  margin-bottom: 3px;
}
.adv-care__numbers-value {
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 700;
  color: var(--color-soft-sage-deep);
  margin-bottom: 2px;
}
.adv-care__numbers-ctx {
  font-size: 11px;
  line-height: 1.4;
  color: var(--color-soft-ink-soft);
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
</style>
