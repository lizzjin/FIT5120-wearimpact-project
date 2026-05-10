<template>
  <div class="section-intro" :class="{ 'is-centered': centered }">
    <div ref="tagRef" v-if="tag" class="section-intro__tag">{{ tag }}</div>
    <AnimatedHeading
      v-if="title"
      :as="titleAs"
      :text="title"
      class="section-intro__title"
      mode="word"
      :stagger="0.07"
    />
    <p v-if="body" ref="bodyRef" class="section-intro__body">{{ body }}</p>
    <slot />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AnimatedHeading from './AnimatedHeading.vue'
import { useReveal } from '../motion/useReveal'

// Standardised section header: tag (char fade) + heading (word mask) + body
// (fade up). Same enter contract as the section-intro module on
// shelby.ashfall.studio so all WearImpact views share one motion rhythm.
defineProps({
  tag: { type: String, default: '' },
  title: { type: String, default: '' },
  body: { type: String, default: '' },
  titleAs: { type: String, default: 'h2' },
  centered: { type: Boolean, default: false },
})

const tagRef = ref(null)
const bodyRef = ref(null)
useReveal(tagRef, { mode: 'char', stagger: 0.025, duration: 0.5 })
useReveal(bodyRef, { mode: 'fade-up', y: 24, delay: 0.15 })
</script>

<style scoped>
.section-intro {
  display: flex;
  flex-direction: column;
  gap: 18px;
  max-width: 720px;
}

.section-intro.is-centered {
  margin-left: auto;
  margin-right: auto;
  text-align: center;
  align-items: center;
}

.section-intro__tag {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--color-primary-text, #163300);
  opacity: 0.85;
}

.section-intro__title {
  font-size: clamp(36px, 5vw, 64px);
  font-weight: 900;
  line-height: 0.92;
  letter-spacing: -0.01em;
  color: var(--color-text, #14210b);
}

.section-intro__body {
  font-size: 17px;
  line-height: 1.55;
  color: var(--color-text-muted, #555);
  margin: 0;
  max-width: 56ch;
}
</style>
