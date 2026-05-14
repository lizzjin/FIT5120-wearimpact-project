<template>
  <section class="es-hero">
    <span class="es-hero__index" aria-hidden="true">ES</span>
    <span class="es-hero__label" aria-hidden="true">ECO-SHOP NAVIGATOR — FIND IT NEARBY</span>

    <div class="es-hero__inner">
      <!-- Left column: text + CTA -->
      <div class="es-hero__text">
        <p class="es-hero__eyebrow" ref="eyebrowRef">
          {{ heroCopy.eyebrow }}
        </p>
        <AnimatedHeading
          as="h1"
          class="es-hero__title"
          :lines="['Donate, swap, recycle —', 'right around the corner.']"
          :stagger="0.08"
          :delay="0.1"
          paint-from="#9fe870"
          paint-to="#0e0f0c"
          :paint-stagger="0.07"
          :paint-duration="0.5"
        />
        <p class="es-hero__subtitle" ref="subtitleRef">
          {{ heroCopy.subtitle }}
        </p>

        <div class="es-hero__actions" ref="actionsRef">
          <button
            type="button"
            class="es-hero__cta is-burst-host"
            :disabled="isLocating"
            @click="$emit('use-location')"
          >
            <CtaBurst />
            <CtaFlip>
              <Navigation2 :size="18" :stroke-width="2.2" />
              {{ isLocating ? 'Locating…' : 'Use my location' }}
            </CtaFlip>
          </button>

          <span v-if="isFallback" class="es-hero__fallback">
            Showing Melbourne CBD — allow location for personalised results
          </span>
        </div>
      </div>

      <!-- Right column: Lottie focal art -->
      <div class="es-hero__art" aria-hidden="true" ref="artRef">
        <Vue3Lottie
          :animation-data="heroAnim"
          :loop="true"
          :autoplay="true"
          :height="'100%'"
          :width="'100%'"
          class="es-hero__art-anim"
        />
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Vue3Lottie } from 'vue3-lottie'
import { Navigation2 } from 'lucide-vue-next'
import AnimatedHeading from '../AnimatedHeading.vue'
import CtaBurst from '../CtaBurst.vue'
import CtaFlip from '../CtaFlip.vue'
import { useReveal } from '../../motion/useReveal'
import heroAnim from '../../assets/lottie/eco-shop-hero.json'

const props = defineProps({
  isLocating: { type: Boolean, default: false },
  isFallback: { type: Boolean, default: false },
  // null | 'donate' | 'buy' — drives journey-aware hero copy when the user
  // arrives from Wardrobe's decision card or Brand Search's next-step card.
  intent: { type: String, default: null },
})
defineEmits(['use-location'])

const heroCopy = computed(() => {
  if (props.intent === 'donate') {
    return {
      eyebrow: 'STEP 4 · LET GO — FIND DONATION POINTS',
      subtitle:
        'Showing donation centres and textile recyclers near you. Widen the type filter if you also want to see op-shops or general second-hand stores.',
    }
  }
  if (props.intent === 'buy') {
    return {
      eyebrow: 'STEP 4 · ACT — SHOP SECOND-HAND',
      subtitle:
        'Showing op-shops by default. The kindest piece you can buy is one that already exists — and a great brand bought new still loses to a fine one bought used.',
    }
  }
  return {
    eyebrow: 'STEP 01 · FIND ECO-SHOPS NEAR YOU',
    subtitle:
      'We pull every nearby second-hand shop, donation point and textile recycler within your radius — so the kindest move for that old jacket is also the closest one.',
  }
})

const eyebrowRef = ref(null)
const subtitleRef = ref(null)
const actionsRef = ref(null)
const artRef = ref(null)
// Eyebrow / subtitle / actions cascade in over ~0.5s, matching the previous
// v-motion delays (0, 250, 450 ms). Art block uses scale-fade per the
// motion plan's "illustration entrance" recipe.
useReveal(eyebrowRef, { mode: 'fade-up', y: 12, duration: 0.5 })
useReveal(subtitleRef, { mode: 'fade-up', y: 18, duration: 0.6, delay: 0.25 })
useReveal(actionsRef, { mode: 'fade-up', y: 20, duration: 0.6, delay: 0.45 })
useReveal(artRef, { mode: 'scale-fade', duration: 0.7, delay: 0.2 })
</script>

<style scoped>
.es-hero {
  position: relative;
  padding: 120px 48px 80px;
  max-width: 1320px;
  margin: 0 auto;
  overflow: hidden;
}

/* ── Decorative giant index + vertical label ───────────────────── */
.es-hero__index {
  position: absolute;
  top: 88px;
  left: 36px;
  font-size: 200px;
  font-weight: 900;
  line-height: 0.8;
  letter-spacing: -0.04em;
  color: var(--color-primary);
  opacity: 0.10;
  pointer-events: none;
  z-index: 1;
  user-select: none;
}

.es-hero__label {
  position: absolute;
  top: 50%;
  left: 16px;
  transform: translateY(-50%) rotate(-90deg);
  transform-origin: left center;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.24em;
  color: var(--color-primary-text);
  opacity: 0.35;
  white-space: nowrap;
  pointer-events: none;
  z-index: 1;
}

/* ── Two-column grid ─────────────────────────────────────────────── */
.es-hero__inner {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1.05fr);
  gap: 64px;
  align-items: center;
  position: relative;
  z-index: 2;
  min-height: 60vh;
}

/* ── Left text ───────────────────────────────────────────────────── */
.es-hero__text {
  display: flex;
  flex-direction: column;
  gap: 22px;
  align-items: flex-start;
}

.es-hero__eyebrow {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--color-primary-text);
  margin: 0;
}

.es-hero__title {
  font-size: clamp(2.4rem, 5vw, 4rem);
  line-height: 0.96;
  font-weight: 900;
  letter-spacing: -0.02em;
  color: var(--color-text);
  margin: 0;
  text-wrap: balance;
}

.es-hero__subtitle {
  font-size: clamp(1rem, 1.5vw, 1.18rem);
  color: var(--color-text-muted);
  max-width: 580px;
  margin: 0;
  line-height: 1.55;
}

.es-hero__actions {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
  margin-top: 4px;
}

.es-hero__cta {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 14px 28px;
  border-radius: var(--radius-pill);
  font-size: 15px;
  font-weight: 700;
  color: var(--color-primary-text);
  background: var(--color-primary);
  border: none;
  cursor: pointer;
  transition:
    transform 200ms var(--motion-entrance),
    background 200ms var(--motion-entrance);
}

.es-hero__cta:hover:not(:disabled) {
  transform: scale(1.03);
  background: var(--color-primary-dark);
}

.es-hero__cta:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.es-hero__fallback {
  font-size: 12px;
  color: var(--color-text-faint);
  letter-spacing: 0.02em;
  background: rgba(255, 255, 255, 0.7);
  padding: 6px 12px;
  border-radius: var(--radius-pill);
  border: 1px solid var(--color-kh-glass-border);
}

/* ── Right Lottie art ────────────────────────────────────────────── */
.es-hero__art {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  min-height: 420px;
}

.es-hero__art-anim {
  width: 100%;
  height: 100%;
  max-width: 580px;
}

/* ── Responsive ───────────────────────────────────────────────────── */
@media (max-width: 1024px) {
  .es-hero__inner {
    grid-template-columns: 1fr;
    gap: 36px;
    min-height: auto;
  }
  .es-hero__title {
    font-size: clamp(2.2rem, 7vw, 3.4rem);
  }
  .es-hero__art {
    min-height: 320px;
    max-height: 380px;
  }
}

@media (max-width: 768px) {
  .es-hero { padding: 80px 20px 50px; }
  .es-hero__index, .es-hero__label { display: none; }
}
</style>
