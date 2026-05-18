<template>
  <div class="adv-play">
    <div class="adv-play__intro">
      <p class="adv-play__eyebrow">
        <Flame :size="11" :stroke-width="2.4" /> Coach's plays
      </p>
      <p class="adv-play__headline">{{ advice.headline }}</p>
      <p class="adv-play__summary">{{ advice.summary }}</p>
    </div>

    <ul class="adv-play__stats">
      <li v-for="f in advice.key_facts" :key="f.label" class="adv-play__stat">
        <span class="adv-play__stat-label">{{ f.label }}</span>
        <span class="adv-play__stat-value">{{ f.value }}</span>
      </li>
    </ul>

    <ol class="adv-play__list">
      <li
        v-for="(r, idx) in advice.recommendations"
        :key="r.id"
        class="adv-play__move"
      >
        <span class="adv-play__rank">{{ idx + 1 }}</span>
        <div class="adv-play__move-body">
          <p class="adv-play__move-action">{{ r.action }}</p>
          <div class="adv-play__move-meta">
            <span
              class="adv-play__move-diff"
              :class="`adv-play__move-diff--${r.difficulty}`"
            >{{ r.difficulty }}</span>
            <p class="adv-play__move-impact">{{ r.impact }}</p>
          </div>
          <div v-if="r.follow_up_prompts?.length" class="adv-play__move-chips">
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
      </li>
    </ol>
  </div>
</template>

<script setup>
import { ArrowRight, Flame } from 'lucide-vue-next'

defineProps({
  advice: { type: Object, required: true },
})
defineEmits(['follow-up'])
</script>

<style scoped>
.adv-play {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.adv-play__intro {
  background: var(--color-soft-cream);
  border-radius: 14px;
  padding: 14px 16px;
  box-shadow: var(--shadow-soft-sm);
}
.adv-play__eyebrow {
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
  margin-bottom: 8px;
}
.adv-play__headline {
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: var(--color-soft-ink);
  line-height: 1.3;
  margin-bottom: 6px;
}
.adv-play__summary {
  font-size: 13.5px;
  line-height: 1.55;
  color: var(--color-soft-ink);
}

.adv-play__stats {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.adv-play__stat {
  display: inline-flex;
  align-items: baseline;
  gap: 8px;
  background: var(--color-soft-milk);
  border-radius: 10px;
  padding: 6px 12px;
}
.adv-play__stat-label {
  font-family: var(--font-display);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--color-soft-ink-soft);
}
.adv-play__stat-value {
  font-family: var(--font-display);
  font-size: 13px;
  font-weight: 700;
  color: var(--color-soft-sage-deep);
}

.adv-play__list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
  counter-reset: play;
}
.adv-play__move {
  display: grid;
  grid-template-columns: 36px 1fr;
  gap: 12px;
  align-items: start;
  background: var(--color-soft-cream);
  border-radius: 16px;
  padding: 12px 14px;
  box-shadow: var(--shadow-soft-sm);
  position: relative;
}
.adv-play__rank {
  width: 32px; height: 32px;
  border-radius: 999px;
  background: var(--color-soft-sage);
  color: var(--color-soft-sage-deep);
  font-family: var(--font-display);
  font-size: 15px;
  font-weight: 800;
  display: grid;
  place-items: center;
}
.adv-play__move-action {
  font-family: var(--font-display);
  font-size: 14.5px;
  font-weight: 700;
  letter-spacing: -0.005em;
  color: var(--color-soft-ink);
  line-height: 1.3;
  margin-bottom: 6px;
}
.adv-play__move-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}
.adv-play__move-impact {
  font-size: 12px;
  color: var(--color-soft-ink-soft);
  line-height: 1.45;
}
.adv-play__move-diff {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.06em;
  padding: 3px 9px;
  border-radius: 999px;
  text-transform: uppercase;
}
.adv-play__move-diff--easy   { background: var(--color-soft-sage-mist); color: var(--color-soft-sage-deep); }
.adv-play__move-diff--medium { background: var(--color-soft-oat); color: var(--color-soft-ink); }
.adv-play__move-diff--hard   { background: var(--color-soft-dusty-wash); color: var(--color-soft-ink); }

.adv-play__move-chips {
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
</style>
