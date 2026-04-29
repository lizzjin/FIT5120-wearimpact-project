<template>
  <div class="wd-mannequin" aria-hidden="true">
    <div class="wd-mannequin__placeholder">
      <PersonStanding :size="34" :stroke-width="1.4" />
      <p class="wd-mannequin__title">Mannequin animation</p>
      <p class="wd-mannequin__hint">Outfit preview — TBD</p>
    </div>
  </div>
</template>

<script setup>
import { PersonStanding } from 'lucide-vue-next'
</script>

<style scoped>
.wd-mannequin {
  background: var(--color-surface);
  border-radius: var(--radius-card);
  padding: 14px;
  box-shadow: var(--shadow-card);
}

.wd-mannequin__placeholder {
  width: 100%;
  aspect-ratio: 4 / 5;
  border-radius: var(--radius-card-sm);
  background:
    repeating-linear-gradient(
      45deg,
      rgba(159, 232, 112, 0.08) 0 12px,
      transparent 12px 24px
    ),
    var(--color-primary-lighter);
  border: 1.5px dashed rgba(22, 51, 0, 0.18);
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  gap: 6px;
  color: var(--color-primary-text);
  text-align: center;
  padding: 12px;
}
.wd-mannequin__title {
  font-size: 12px; font-weight: 700; letter-spacing: 0.5px;
}
.wd-mannequin__hint {
  font-size: 11px; color: var(--color-text-subtle);
}
</style>
