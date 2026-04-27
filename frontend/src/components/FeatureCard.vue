<template>
  <router-link :to="link" class="feature-card">
    <div v-if="image" class="card-image">
      <img :src="image" :alt="title" loading="lazy" />
    </div>
    <div class="card-body">
      <div class="icon-box">
        <component :is="iconComponent" :size="32" :stroke-width="1.75" />
      </div>
      <h3>{{ title }}</h3>
      <p>{{ description }}</p>
      <span class="explore-link">
        Explore
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path d="M5 12h14M12 5l7 7-7 7"/>
        </svg>
      </span>
    </div>
  </router-link>
</template>

<script setup>
import { computed } from 'vue'
import { MapPin, Search, BookOpen, Star } from 'lucide-vue-next'

const ICON_MAP = { MapPin, Search, BookOpen, Star }

const props = defineProps({
  icon: { type: String, default: 'Star' },
  title: String,
  description: String,
  link: { type: String, default: '/' },
  image: { type: String, default: null }
})

const iconComponent = computed(() => ICON_MAP[props.icon] ?? Star)
</script>

<style scoped>
.feature-card {
  display: flex;
  flex-direction: column;
  background: white;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-card);
  overflow: hidden;
  box-shadow: var(--shadow-card);
  text-align: left;
  text-decoration: none;
  cursor: pointer;
  transition: border-color 200ms ease, box-shadow 200ms ease, transform 200ms ease;
}

.feature-card:hover {
  border-color: var(--color-primary);
  box-shadow: var(--shadow-card-hover);
  transform: scale(1.02);
}

.card-image {
  width: 100%;
  height: 180px;
  overflow: hidden;
  flex-shrink: 0;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 400ms ease;
}

.feature-card:hover .card-image img {
  transform: scale(1.04);
}

.card-body {
  display: flex;
  flex-direction: column;
  padding: 24px;
  flex: 1;
}

.icon-box {
  width: 56px;
  height: 56px;
  border-radius: var(--radius-card-sm);
  background: var(--color-primary-light);
  color: var(--color-primary-text);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
  border: 1px solid var(--color-border);
  flex-shrink: 0;
}

.feature-card h3 {
  font-size: 22px;
  font-weight: 700;
  letter-spacing: -0.396px;
  margin-bottom: 10px;
  color: var(--color-text);
  line-height: 1.25;
}

.feature-card p {
  color: var(--color-text-muted);
  font-weight: 500;
  line-height: 1.5;
  margin-bottom: 20px;
  flex: 1;
  font-size: 15px;
}

.explore-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: var(--color-primary-text);
  font-weight: 700;
  font-size: 14px;
  transition: gap 150ms ease;
}

.feature-card:hover .explore-link {
  gap: 10px;
}
</style>
