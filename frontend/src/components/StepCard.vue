<template>
  <div class="step-card">
    <div class="step-circle">{{ step }}</div>
    <h3>{{ title }}</h3>
    <p>{{ description }}</p>
  </div>
</template>

<script setup>
defineProps({
  step: String,
  title: String,
  description: String
})
</script>

<style scoped>
.step-card {
  background: white;
  border-radius: var(--radius-card);
  padding: 32px 24px;
  text-align: center;
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-card);
  transition: box-shadow 200ms ease, transform 200ms ease;
}

.step-card:hover {
  box-shadow: var(--shadow-card-hover);
  transform: scale(1.03);
}

.step-circle {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: var(--color-primary);
  color: var(--color-primary-text);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
  font-weight: 700;
  font-size: 18px;
}

.step-card h3 {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 10px;
  color: var(--color-text);
}

.step-card p {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-muted);
  line-height: 1.5;
}
</style>