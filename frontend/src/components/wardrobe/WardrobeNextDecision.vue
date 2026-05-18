<template>
  <section class="wd-decide" ref="rootRef">
    <div class="wd-decide__head">
      <p class="wd-decide__eyebrow" ref="eyebrowRef">
        STEP 03 — WHERE TO NEXT?
      </p>
      <h2 class="wd-decide__title" ref="titleRef">
        <span class="wd-decide__title-line">Looking at your <em class="wd-decide__title-accent">wardrobe</em>,</span>
        <span class="wd-decide__title-line">how do you feel?</span>
      </h2>
      <p class="wd-decide__sub" ref="subRef">
        The next step depends on you. Most journeys split here.
      </p>
    </div>

    <div class="wd-decide__cards" ref="cardsRef">
      <router-link
        to="/eco-shop?intent=donate"
        class="wd-decide__card wd-decide__card--declutter"
      >
        <span class="wd-decide__card-eyebrow">Step 04 · Let go</span>
        <h3 class="wd-decide__card-title">I have enough — maybe too much.</h3>
        <p class="wd-decide__card-body">
          Let go of what you no longer wear. Find donation points and textile recyclers near you,
          so nothing ends up in landfill.
        </p>
        <span class="wd-decide__card-cta">
          Find places to donate
          <ArrowRight :size="16" :stroke-width="2" class="wd-decide__card-arrow" />
        </span>
      </router-link>

      <router-link
        to="/knowledge"
        class="wd-decide__card wd-decide__card--shop"
      >
        <span class="wd-decide__card-eyebrow">Step 04 · Learn</span>
        <h3 class="wd-decide__card-title">I'm thinking of buying something new.</h3>
        <p class="wd-decide__card-body">
          Before you spend — learn what materials, supply chains and brands actually deliver.
          Then evaluate. Then shop second-hand.
        </p>
        <span class="wd-decide__card-cta">
          Learn before you buy
          <ArrowRight :size="16" :stroke-width="2" class="wd-decide__card-arrow" />
        </span>
      </router-link>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { ArrowRight } from 'lucide-vue-next'
import { useReveal } from '../../motion/useReveal'
import { useStagger } from '../../motion/useStagger'

const rootRef = ref(null)
const eyebrowRef = ref(null)
const subRef = ref(null)
const cardsRef = ref(null)
const titleRef = ref(null)

useReveal(eyebrowRef, { mode: 'fade-up', y: 12, duration: 0.5 })
useStagger(titleRef, { selector: '.wd-decide__title-line', stagger: 0.1, y: 30, delay: 0.1, duration: 0.6 })
useReveal(subRef, { mode: 'fade-up', y: 16, duration: 0.6, delay: 0.4 })
useStagger(cardsRef, {
  selector: '.wd-decide__card',
  stagger: 0.14,
  y: 32,
  delay: 0.5,
  duration: 0.7,
})
</script>

<style scoped>
.wd-decide {
  max-width: 1200px;
  margin: 80px auto 32px;
  padding: 0 32px;
}

.wd-decide__head {
  text-align: center;
  margin-bottom: 40px;
}

.wd-decide__eyebrow {
  display: inline-block;
  font-family: var(--font-display);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.22em;
  background: var(--color-soft-sage-mist);
  color: var(--color-soft-sage-deep);
  padding: 6px 14px;
  border-radius: var(--radius-soft-pill);
  margin: 0 0 18px;
  text-transform: uppercase;
}

.wd-decide__title {
  font-family: var(--font-display);
  font-size: clamp(26px, 3.8vw, 44px);
  line-height: 1.1;
  letter-spacing: -0.02em;
  font-weight: 700;
  color: var(--color-soft-ink);
  margin: 0 auto 14px;
  max-width: 820px;
}
.wd-decide__title-line { display: block; }
.wd-decide__title-accent {
  color: var(--color-soft-sage);
  font-style: italic;
  font-weight: 800;
}

.wd-decide__sub {
  font-size: 15px;
  color: var(--color-soft-ink-soft);
  margin: 0 auto;
  max-width: 560px;
  line-height: 1.55;
  font-weight: 500;
}

.wd-decide__cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 26px;
}

.wd-decide__card {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding: 30px 30px 28px;
  border-radius: var(--radius-soft);
  border: 1.5px solid var(--color-soft-line-strong);
  text-decoration: none;
  color: var(--color-soft-ink);
  box-shadow: var(--shadow-soft);
  transition: transform 240ms cubic-bezier(0.22, 1, 0.36, 1),
              box-shadow 240ms ease;
  overflow: hidden;
}

.wd-decide__card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-soft-lg);
}

.wd-decide__card--declutter { background: var(--color-soft-dusty-wash); }
.wd-decide__card--shop      { background: var(--color-soft-sage-mist); }

.wd-decide__card-eyebrow {
  font-family: var(--font-display);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.18em;
  color: var(--color-soft-ink-soft);
  background: var(--color-soft-cream);
  padding: 5px 12px;
  border-radius: var(--radius-soft-pill);
  align-self: flex-start;
  text-transform: uppercase;
}

.wd-decide__card-title {
  font-family: var(--font-display);
  font-size: clamp(20px, 2.4vw, 26px);
  line-height: 1.2;
  letter-spacing: -0.01em;
  font-weight: 700;
  color: var(--color-soft-ink);
  margin: 0;
}

.wd-decide__card-body {
  font-size: 14.5px;
  line-height: 1.6;
  color: var(--color-soft-ink);
  opacity: 0.78;
  margin: 0;
  flex: 1;
  font-weight: 500;
}

.wd-decide__card-cta {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 700;
  color: var(--color-soft-sage-deep);
}
.wd-decide__card--declutter .wd-decide__card-cta { color: var(--color-soft-ink); }

.wd-decide__card-arrow {
  transition: transform 180ms ease;
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
    gap: 18px;
  }
  .wd-decide__card {
    padding: 26px 22px 22px;
  }
}
</style>
