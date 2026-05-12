<template>
  <section class="wd-decide" ref="rootRef">
    <div class="wd-decide__head">
      <p class="wd-decide__eyebrow" ref="eyebrowRef">
        STEP 1 COMPLETE — WHAT'S NEXT?
      </p>
      <AnimatedHeading
        as="h2"
        class="wd-decide__title"
        text="Looking at your wardrobe, how do you feel?"
        :stagger="0.05"
        :delay="0.1"
      />
      <p class="wd-decide__sub" ref="subRef">
        The next step depends on you. Most journeys split here.
      </p>
    </div>

    <div class="wd-decide__cards" ref="cardsRef">
      <router-link
        to="/eco-shop?intent=donate"
        class="wd-decide__card wd-decide__card--declutter"
      >
        <span class="wd-decide__card-eyebrow">STEP 2 · LET GO</span>
        <h3 class="wd-decide__card-title">I have enough — maybe too much.</h3>
        <p class="wd-decide__card-body">
          Let go of what you no longer wear. Find donation points and textile recyclers near you,
          so nothing ends up in landfill.
        </p>
        <span class="wd-decide__card-cta">
          Find places to donate
          <ArrowRight :size="16" :stroke-width="2.4" class="wd-decide__card-arrow" />
        </span>
      </router-link>

      <router-link
        to="/knowledge"
        class="wd-decide__card wd-decide__card--shop"
      >
        <span class="wd-decide__card-eyebrow">STEP 2 · LEARN</span>
        <h3 class="wd-decide__card-title">I'm thinking of buying something new.</h3>
        <p class="wd-decide__card-body">
          Before you spend — learn what materials, supply chains and brands actually deliver.
          Then evaluate. Then shop second-hand.
        </p>
        <span class="wd-decide__card-cta">
          Learn before you buy
          <ArrowRight :size="16" :stroke-width="2.4" class="wd-decide__card-arrow" />
        </span>
      </router-link>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { ArrowRight } from 'lucide-vue-next'
import AnimatedHeading from '../AnimatedHeading.vue'
import { useReveal } from '../../motion/useReveal'
import { useStagger } from '../../motion/useStagger'

const rootRef = ref(null)
const eyebrowRef = ref(null)
const subRef = ref(null)
const cardsRef = ref(null)

useReveal(eyebrowRef, { mode: 'fade-up', y: 12, duration: 0.5 })
useReveal(subRef, { mode: 'fade-up', y: 16, duration: 0.6, delay: 0.25 })
useStagger(cardsRef, {
  selector: '.wd-decide__card',
  stagger: 0.14,
  y: 32,
  delay: 0.35,
  duration: 0.7,
})
</script>

<style scoped>
.wd-decide {
  max-width: 1100px;
  margin: 72px auto 32px;
  padding: 0 32px;
}

.wd-decide__head {
  text-align: center;
  margin-bottom: 36px;
}

.wd-decide__eyebrow {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 2.4px;
  color: var(--color-primary-text);
  margin: 0 0 12px;
  text-transform: uppercase;
}

.wd-decide__title {
  font-size: clamp(26px, 3.4vw, 36px);
  font-weight: 800;
  letter-spacing: -0.6px;
  line-height: 1.12;
  color: var(--color-text);
  margin: 0 0 12px;
  max-width: 720px;
  margin-left: auto;
  margin-right: auto;
}

.wd-decide__sub {
  font-size: 15px;
  color: var(--color-text-muted);
  margin: 0 auto;
  max-width: 560px;
  line-height: 1.55;
}

.wd-decide__cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.wd-decide__card {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 32px 28px 28px;
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
  overflow: hidden;
}

.wd-decide__card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 4px;
  background: currentColor;
  opacity: 0.85;
}

.wd-decide__card:hover {
  transform: translateY(-6px);
  box-shadow: var(--shadow-card-hover);
  border-color: currentColor;
}

.wd-decide__card--declutter {
  color: #c08457;
}

.wd-decide__card--shop {
  color: var(--color-primary-text);
}

.wd-decide__card-eyebrow {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 2px;
  color: currentColor;
  text-transform: uppercase;
}

.wd-decide__card-title {
  font-size: clamp(20px, 2.2vw, 24px);
  font-weight: 800;
  letter-spacing: -0.4px;
  line-height: 1.22;
  color: var(--color-text);
  margin: 0;
}

.wd-decide__card-body {
  font-size: 14.5px;
  line-height: 1.55;
  color: var(--color-text-muted);
  margin: 0;
  flex: 1;
}

.wd-decide__card-cta {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
  font-size: 14px;
  font-weight: 700;
  color: currentColor;
  letter-spacing: 0.2px;
}

.wd-decide__card-arrow {
  transition: transform var(--transition-base);
}

.wd-decide__card:hover .wd-decide__card-arrow {
  transform: translateX(5px);
}

@media (max-width: 800px) {
  .wd-decide {
    margin: 56px 0 24px;
    padding: 0 20px;
  }
  .wd-decide__cards {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  .wd-decide__card {
    padding: 26px 22px 22px;
  }
}
</style>
