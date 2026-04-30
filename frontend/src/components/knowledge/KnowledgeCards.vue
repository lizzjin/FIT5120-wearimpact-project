<template>
  <section class="kh-cards">
    <header class="kh-cards__head">
      <button type="button" class="kh-cards__back" @click="$emit('back')">
        <ArrowLeft :size="16" :stroke-width="2" /> Back
      </button>
      <div class="kh-cards__heading">
        <p class="kh-cards__eyebrow">STEP 04 · DEEP-DIVE CARDS</p>
        <h2 class="kh-cards__title">
          Fourteen short reads — the numbers behind the slogans.
        </h2>
        <p class="kh-cards__subtitle">
          Tap any card to see the full story, the data, and where it comes from.
        </p>
      </div>
    </header>

    <!-- Theme filter chips -->
    <div class="kh-cards__filters" role="tablist" aria-label="Filter by theme">
      <button
        type="button"
        class="kh-chip"
        :class="{ 'kh-chip--active': activeTheme === 'all' }"
        role="tab"
        :aria-selected="activeTheme === 'all'"
        @click="activeTheme = 'all'"
      >
        All themes
      </button>
      <button
        v-for="theme in themes"
        :key="theme.key"
        type="button"
        class="kh-chip"
        :class="{ 'kh-chip--active': activeTheme === theme.key }"
        role="tab"
        :aria-selected="activeTheme === theme.key"
        @click="activeTheme = theme.key"
      >
        {{ theme.label }}
      </button>
    </div>

    <!-- Masonry wall -->
    <div class="kh-cards__wall">
      <article
        v-for="(card, idx) in visibleCards"
        :key="card.id"
        class="kh-card-tile"
        v-motion
        :initial="{ opacity: 0, y: 24 }"
        :visible="{ opacity: 1, y: 0, transition: { duration: 500, delay: (idx % 6) * 60 } }"
        tabindex="0"
        role="button"
        :aria-label="`Open: ${card.title}`"
        @click="openCard(card)"
        @keydown.enter.prevent="openCard(card)"
        @keydown.space.prevent="openCard(card)"
      >
        <div class="kh-card-tile__media">
          <img
            :src="card.image"
            :alt="card.title"
            loading="lazy"
            @error="handleImgError"
          />
          <span class="kh-card-tile__theme-tag">
            {{ themeLabel(card.theme) }}
          </span>
        </div>
        <div class="kh-card-tile__body">
          <h3 class="kh-card-tile__title">{{ card.title }}</h3>
          <p class="kh-card-tile__summary">{{ card.summary }}</p>
          <span class="kh-card-tile__more">
            Read more <ArrowRight :size="14" :stroke-width="2" />
          </span>
        </div>
      </article>
    </div>

    <!-- Modal -->
    <Transition name="kh-modal">
      <div
        v-if="activeCard"
        class="kh-modal__backdrop"
        role="dialog"
        aria-modal="true"
        :aria-label="activeCard.title"
        @click.self="closeCard"
        @keydown.esc="closeCard"
      >
        <div class="kh-modal__panel" tabindex="-1" ref="modalRef">
          <button
            type="button"
            class="kh-modal__close"
            aria-label="Close"
            @click="closeCard"
          >
            <X :size="18" :stroke-width="2" />
          </button>

          <div class="kh-modal__media">
            <img
              :src="activeCard.image"
              :alt="activeCard.title"
              @error="handleImgError"
            />
          </div>

          <div class="kh-modal__body">
            <span class="kh-modal__theme">
              {{ themeLabel(activeCard.theme) }}
            </span>
            <h3 class="kh-modal__title">{{ activeCard.title }}</h3>
            <p class="kh-modal__summary">{{ activeCard.summary }}</p>

            <div class="kh-modal__paragraphs">
              <p v-for="(p, i) in activeCard.body" :key="i">{{ p }}</p>
            </div>

            <p class="kh-modal__source">
              <BookOpen :size="13" :stroke-width="2" />
              <span><strong>Source:</strong> {{ activeCard.source }}</span>
            </p>
          </div>
        </div>
      </div>
    </Transition>
  </section>
</template>

<script setup>
import { ref, computed, watch, nextTick, onBeforeUnmount } from 'vue'
import { ArrowLeft, ArrowRight, BookOpen, X } from 'lucide-vue-next'
import data from '../../data/knowledge-cards.json'

defineEmits(['back'])

const themes = data.themes
const cards = data.cards

const activeTheme = ref('all')
const activeCard = ref(null)
const modalRef = ref(null)

const themeMap = Object.fromEntries(themes.map((t) => [t.key, t.label]))
function themeLabel(key) { return themeMap[key] || key }

const visibleCards = computed(() => {
  if (activeTheme.value === 'all') return cards
  return cards.filter((c) => c.theme === activeTheme.value)
})

function lockScroll() {
  document.documentElement.style.overflow = 'hidden'
  document.body.style.overflow = 'hidden'
}
function unlockScroll() {
  document.documentElement.style.overflow = ''
  document.body.style.overflow = ''
}

function openCard(card) {
  activeCard.value = card
  lockScroll()
  nextTick(() => modalRef.value?.focus())
}
function closeCard() {
  activeCard.value = null
  unlockScroll()
}

function handleImgError(e) {
  // Hide broken images so the gradient placeholder behind them shows through.
  e.target.style.opacity = '0'
}

// Esc-to-close at document level so modal closes even if focus has drifted.
function onKey(e) { if (e.key === 'Escape') closeCard() }
watch(activeCard, (v) => {
  if (v) document.addEventListener('keydown', onKey)
  else document.removeEventListener('keydown', onKey)
})
onBeforeUnmount(() => {
  document.removeEventListener('keydown', onKey)
  unlockScroll()
})
</script>

<style scoped>
.kh-cards {
  position: relative;
  max-width: 1200px;
  margin: 0 auto;
  padding: 64px 32px 80px;
}

/* ── Header ───────────────────────────────────────────────────── */
.kh-cards__head {
  display: flex;
  align-items: flex-start;
  gap: 24px;
  margin-bottom: 28px;
}

.kh-cards__back {
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  background: var(--color-surface, #fff);
  border: 1px solid var(--color-border, rgba(0, 0, 0, 0.08));
  border-radius: var(--radius-btn, 999px);
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text);
  cursor: pointer;
  transition: transform var(--transition-base), background var(--transition-base);
}
.kh-cards__back:hover { transform: translateX(-2px); background: var(--color-bg-soft, #f5f1e8); }

.kh-cards__heading { flex: 1; }

.kh-cards__eyebrow {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 2px;
  color: var(--color-primary-text);
  margin: 0 0 10px;
}
.kh-cards__title {
  font-size: clamp(28px, 3.4vw, 40px);
  font-weight: 800;
  letter-spacing: -1px;
  line-height: 1.1;
  color: var(--color-text);
  margin: 0 0 12px;
}
.kh-cards__subtitle {
  font-size: 15.5px;
  line-height: 1.55;
  color: var(--color-text-muted);
  max-width: 620px;
  margin: 0;
}

/* ── Filter chips ─────────────────────────────────────────────── */
.kh-cards__filters {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 32px;
}
.kh-chip {
  padding: 8px 16px;
  border-radius: 999px;
  border: 1px solid var(--color-border, rgba(0, 0, 0, 0.1));
  background: var(--color-surface, #fff);
  color: var(--color-text-muted);
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.2px;
  cursor: pointer;
  transition: all var(--transition-base);
}
.kh-chip:hover { background: var(--color-bg-soft, #f5f1e8); color: var(--color-text); }
.kh-chip--active {
  background: var(--color-primary);
  color: var(--color-primary-text);
  border-color: transparent;
}

/* ── Masonry wall (CSS columns) ───────────────────────────────── */
.kh-cards__wall {
  column-count: 3;
  column-gap: 24px;
}

.kh-card-tile {
  display: block;
  break-inside: avoid;
  -webkit-column-break-inside: avoid;
  page-break-inside: avoid;
  margin-bottom: 24px;
  background: var(--color-surface, #fff);
  border: 1px solid var(--color-border, rgba(0, 0, 0, 0.06));
  border-radius: var(--radius-card-lg, 20px);
  overflow: hidden;
  cursor: pointer;
  transition:
    transform var(--transition-base),
    box-shadow var(--transition-base),
    border-color var(--transition-base);
}
.kh-card-tile:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-card, 0 12px 32px rgba(22, 51, 0, 0.08));
  border-color: var(--color-primary);
}
.kh-card-tile:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 3px;
}

.kh-card-tile__media {
  position: relative;
  background: linear-gradient(135deg, #d9f4b9 0%, #9fe870 100%);
}
.kh-card-tile__media img {
  display: block;
  width: 100%;
  height: auto;
  object-fit: cover;
  transition: opacity 200ms ease;
}
.kh-card-tile__theme-tag {
  position: absolute;
  top: 12px; left: 12px;
  padding: 5px 10px;
  background: rgba(255, 255, 255, 0.92);
  color: var(--color-primary-text);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.5px;
  border-radius: 999px;
  backdrop-filter: blur(4px);
}

.kh-card-tile__body { padding: 18px 20px 20px; }
.kh-card-tile__title {
  font-size: 17px;
  font-weight: 700;
  line-height: 1.35;
  color: var(--color-text);
  margin: 0 0 8px;
  letter-spacing: -0.2px;
}
.kh-card-tile__summary {
  font-size: 13.5px;
  line-height: 1.55;
  color: var(--color-text-muted);
  margin: 0 0 14px;
}
.kh-card-tile__more {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 12.5px;
  font-weight: 700;
  letter-spacing: 0.4px;
  color: var(--color-primary-text);
}
.kh-card-tile:hover .kh-card-tile__more svg { transform: translateX(3px); }
.kh-card-tile__more svg { transition: transform var(--transition-base); }

/* ── Modal ────────────────────────────────────────────────────── */
.kh-modal__backdrop {
  position: fixed;
  inset: 0;
  z-index: 100;
  background: rgba(22, 51, 0, 0.45);
  backdrop-filter: blur(6px);
  display: grid;
  place-items: center;
  padding: 24px;
  overflow-y: auto;
}

.kh-modal__panel {
  position: relative;
  width: 100%;
  max-width: 720px;
  max-height: calc(100vh - 48px);
  background: var(--color-surface, #fff);
  border-radius: var(--radius-card-lg, 24px);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  outline: none;
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.2);
}

.kh-modal__close {
  position: absolute;
  top: 16px; right: 16px;
  z-index: 2;
  width: 36px; height: 36px;
  border-radius: 999px;
  border: none;
  background: rgba(255, 255, 255, 0.92);
  color: var(--color-text);
  cursor: pointer;
  display: grid; place-items: center;
  transition: background var(--transition-base), transform var(--transition-base);
}
.kh-modal__close:hover { background: #fff; transform: scale(1.05); }

.kh-modal__media {
  background: linear-gradient(135deg, #d9f4b9 0%, #9fe870 100%);
  flex-shrink: 0;
}
.kh-modal__media img {
  display: block;
  width: 100%;
  height: 280px;
  object-fit: cover;
}

.kh-modal__body {
  padding: 28px 36px 32px;
  overflow-y: auto;
}

.kh-modal__theme {
  display: inline-block;
  padding: 4px 10px;
  background: var(--color-primary-light, #e8f9d4);
  color: var(--color-primary-text);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1px;
  border-radius: 999px;
  margin-bottom: 14px;
  text-transform: uppercase;
}

.kh-modal__title {
  font-size: clamp(22px, 2.6vw, 28px);
  font-weight: 800;
  line-height: 1.2;
  letter-spacing: -0.5px;
  color: var(--color-text);
  margin: 0 0 12px;
}

.kh-modal__summary {
  font-size: 15.5px;
  line-height: 1.55;
  color: var(--color-text-muted);
  font-style: italic;
  margin: 0 0 20px;
  padding-left: 14px;
  border-left: 3px solid var(--color-primary);
}

.kh-modal__paragraphs p {
  font-size: 15px;
  line-height: 1.7;
  color: var(--color-text);
  margin: 0 0 14px;
}
.kh-modal__paragraphs p:last-child { margin-bottom: 20px; }

.kh-modal__source {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  margin: 12px 0 0;
  padding: 14px 16px;
  background: var(--color-bg-soft, #f5f1e8);
  border-radius: 12px;
  font-size: 12.5px;
  line-height: 1.5;
  color: var(--color-text-muted);
}
.kh-modal__source svg {
  flex-shrink: 0;
  margin-top: 2px;
  color: var(--color-primary-text);
}

/* ── Modal transition ─────────────────────────────────────────── */
.kh-modal-enter-active,
.kh-modal-leave-active {
  transition: opacity 220ms ease;
}
.kh-modal-enter-active .kh-modal__panel,
.kh-modal-leave-active .kh-modal__panel {
  transition: transform 280ms cubic-bezier(0.22, 1, 0.36, 1), opacity 220ms ease;
}
.kh-modal-enter-from,
.kh-modal-leave-to { opacity: 0; }
.kh-modal-enter-from .kh-modal__panel { transform: translateY(20px) scale(0.97); opacity: 0; }
.kh-modal-leave-to   .kh-modal__panel { transform: translateY(8px)  scale(0.99); opacity: 0; }

/* ── Responsive ──────────────────────────────────────────────── */
@media (max-width: 1024px) {
  .kh-cards__wall { column-count: 2; }
}
@media (max-width: 640px) {
  .kh-cards { padding: 48px 20px 64px; }
  .kh-cards__head { flex-direction: column; gap: 16px; }
  .kh-cards__wall { column-count: 1; }
  .kh-modal__media img { height: 200px; }
  .kh-modal__body { padding: 22px 22px 26px; }
}
</style>
