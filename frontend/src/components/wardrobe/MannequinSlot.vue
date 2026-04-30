<template>
  <div class="wd-mannequin" aria-hidden="true">
    <Vue3Lottie
      :animation-data="mannequinAnim"
      :loop="true"
      :autoplay="true"
      class="wd-mannequin__lottie"
    />
    <p class="wd-mannequin__hint">Outfit preview</p>
  </div>
</template>

<script setup>
import { Vue3Lottie } from 'vue3-lottie'
import mannequinAnim from '../../assets/lottie/my-wardrobe.json'
</script>

<style scoped>
.wd-mannequin {
  /* Transparent so the Lottie blends into the page cream — no card frame. */
  background: transparent;
  padding: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  /* Fill all leftover vertical space in the rail above the upload card. */
  flex: 1;
  min-height: 0;
}

.wd-mannequin__lottie {
  width: 100%;
  flex: 1;
  min-height: 0;
  background: transparent;
}

.wd-mannequin__hint {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.4px;
  color: var(--color-primary-text);
  text-transform: uppercase;
  flex-shrink: 0;
}
</style>
