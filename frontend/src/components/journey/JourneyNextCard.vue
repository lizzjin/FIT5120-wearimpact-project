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
.jn-card {
  display: block;
  max-width: 720px;
  margin: 56px auto 24px;
  padding: 28px 32px;
  border-radius: var(--radius-card);
  background: var(--color-surface);
  border: 1px solid var(--color-border-light);
  text-decoration: none;
  color: inherit;
  box-shadow: var(--shadow-card);
  transition:
    transform var(--transition-base),
    box-shadow var(--transition-base),
    border-color var(--transition-base);
}

.jn-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-card-hover);
  border-color: var(--color-primary);
}

.jn-card__eyebrow {
  display: inline-block;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 2px;
  color: var(--color-primary-text);
  margin-bottom: 10px;
}

.jn-card__title {
  font-size: clamp(20px, 2.4vw, 26px);
  font-weight: 800;
  letter-spacing: -0.4px;
  line-height: 1.2;
  color: var(--color-text);
  margin: 0 0 10px;
}

.jn-card__body {
  font-size: 15px;
  line-height: 1.55;
  color: var(--color-text-muted);
  margin: 0 0 18px;
  max-width: 560px;
}

.jn-card__cta {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 700;
  color: var(--color-primary-text);
  letter-spacing: 0.2px;
}

.jn-card__arrow {
  transition: transform var(--transition-base);
}

.jn-card:hover .jn-card__arrow {
  transform: translateX(4px);
}

@media (max-width: 700px) {
  .jn-card {
    margin: 40px 16px 16px;
    padding: 22px 22px;
  }
}
</style>
