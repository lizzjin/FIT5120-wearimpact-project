<template>
  <router-link :to="to" custom v-slot="{ href, navigate }">
    <a :href="href" class="jn-card" ref="rootRef" @click="navigate">
      <span class="jn-card__eyebrow">{{ eyebrow }}</span>
      <h3 class="jn-card__title">{{ title }}</h3>
      <p v-if="body" class="jn-card__body">{{ body }}</p>
      <span class="jn-card__cta">
        {{ cta }}
        <ArrowRight :size="16" :stroke-width="2.4" class="jn-card__arrow" />
      </span>
    </a>
  </router-link>
</template>

<script setup>
import { ref } from 'vue'
import { ArrowRight } from 'lucide-vue-next'
import { useReveal } from '../../motion/useReveal'

defineProps({
  to: { type: [String, Object], required: true },
  eyebrow: { type: String, required: true },
  title: { type: String, required: true },
  body: { type: String, default: '' },
  cta: { type: String, default: 'Continue' },
})

const rootRef = ref(null)
useReveal(rootRef, { mode: 'fade-up', y: 24, duration: 0.7, delay: 0.05 })
</script>

<style scoped>
/* Match the soft-tactile look of WardrobeNextDecision's split cards: sage-mist
   wash background, cream-pill eyebrow, font-display headline, soft shadow.
   Single card here (vs. wardrobe's two-up grid) so we centre it. */
.jn-card {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 14px;
  max-width: 720px;
  margin: 56px auto 24px;
  padding: 30px 30px 28px;
  border-radius: var(--radius-soft, 24px);
  border: 1.5px solid var(--color-soft-line-strong, rgba(14, 15, 12, 0.14));
  background: var(--color-soft-sage-mist, #e2f6d5);
  color: var(--color-soft-ink, #0e0f0c);
  text-decoration: none;
  box-shadow: var(--shadow-soft, 0 12px 32px rgba(14, 15, 12, 0.08), 0 4px 8px rgba(14, 15, 12, 0.05));
  transition: transform 240ms cubic-bezier(0.22, 1, 0.36, 1),
              box-shadow 240ms ease;
  overflow: hidden;
}

.jn-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-soft-lg, 0 24px 56px rgba(14, 15, 12, 0.10), 0 8px 16px rgba(14, 15, 12, 0.06));
}

.jn-card__eyebrow {
  font-family: var(--font-display, 'Inter', sans-serif);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.18em;
  color: var(--color-soft-ink-soft, #454745);
  background: var(--color-soft-cream, #faf7f2);
  padding: 5px 12px;
  border-radius: var(--radius-soft-pill, 9999px);
  align-self: flex-start;
  text-transform: uppercase;
}

.jn-card__title {
  font-family: var(--font-display, 'Inter', sans-serif);
  font-size: clamp(20px, 2.4vw, 26px);
  line-height: 1.2;
  letter-spacing: -0.01em;
  font-weight: 700;
  color: var(--color-soft-ink, #0e0f0c);
  margin: 0;
}

.jn-card__body {
  font-size: 14.5px;
  line-height: 1.6;
  color: var(--color-soft-ink, #0e0f0c);
  opacity: 0.78;
  margin: 0;
  max-width: 560px;
  font-weight: 500;
}

.jn-card__cta {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
  font-family: var(--font-display, 'Inter', sans-serif);
  font-size: 14px;
  font-weight: 700;
  color: var(--color-soft-sage-deep, #163300);
}

.jn-card__arrow {
  transition: transform 180ms ease;
}

.jn-card:hover .jn-card__arrow {
  transform: translateX(5px);
}

@media (max-width: 700px) {
  .jn-card {
    margin: 40px 16px 16px;
    padding: 26px 22px 22px;
  }
}
</style>
