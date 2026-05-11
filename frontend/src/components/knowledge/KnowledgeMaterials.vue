<template>
  <section class="kh-mat">
    <header class="kh-mat__head">
      <p ref="eyebrowRef" class="kh-mat__eyebrow">STEP 03 · MATERIAL TRUTHS</p>
      <AnimatedHeading
        as="h2"
        class="kh-mat__title"
        text="Pick a fibre — see the better alternative."
        :stagger="0.06"
        :delay="0.1"
      />
    </header>

    <!-- ── A: Atlas of tilted fibre cards ──────────────────────────── -->
    <div class="kh-mat__atlas">
      <button
        v-for="fibre in fibres"
        :key="fibre.key"
        type="button"
        class="kh-card"
        :class="{
          'kh-card--active': selected.key === fibre.key,
          'kh-card--preferred': fibre.is_preferred,
        }"
        :style="{ '--tilt': tiltOf(fibre) + 'deg' }"
        :aria-pressed="selected.key === fibre.key"
        @click="selectFibre(fibre)"
      >
        <span v-if="selected.key === fibre.key" class="kh-card__pin" aria-hidden="true">
          <Check :size="12" :stroke-width="3" />
        </span>

        <span class="kh-card__icon" aria-hidden="true">
          <!-- Custom per-fibre line illustrations. Each one points at the
               fibre's actual source (cotton boll, oil flask, thread spool,
               polymer chain, tree, sheep, silk cocoon, flax flower) so the
               icon matches the content instead of being a metaphor. -->
          <svg v-if="fibre.key === 'cotton'" width="28" height="28" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="14" r="4.5"/>
            <circle cx="21" cy="14" r="4.5"/>
            <circle cx="16" cy="20" r="4.5"/>
            <path d="M9 24 L11 27"/>
            <path d="M16 24 L16 28"/>
            <path d="M23 24 L21 27"/>
          </svg>
          <svg v-else-if="fibre.key === 'polyester'" width="28" height="28" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
            <path d="M13 5 L19 5"/>
            <path d="M14 5 L14 13 L8 24 Q8 27 11 27 L21 27 Q24 27 24 24 L18 13 L18 5"/>
            <path d="M10 21 L22 21"/>
            <circle cx="16" cy="24" r="1.6" fill="currentColor" stroke="none"/>
          </svg>
          <svg v-else-if="fibre.key === 'nylon'" width="28" height="28" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
            <ellipse cx="16" cy="7" rx="9" ry="2.2"/>
            <path d="M7 7 L7 25"/>
            <path d="M25 7 L25 25"/>
            <ellipse cx="16" cy="25" rx="9" ry="2.2"/>
            <path d="M9 12 L23 14"/>
            <path d="M9 16 L23 18"/>
            <path d="M9 20 L23 22"/>
          </svg>
          <svg v-else-if="fibre.key === 'acrylic'" width="28" height="28" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
            <path d="M4 22 L10 12 L16 22 L22 12 L28 22"/>
            <circle cx="10" cy="12" r="2" fill="currentColor" stroke="none"/>
            <circle cx="22" cy="12" r="2" fill="currentColor" stroke="none"/>
            <circle cx="16" cy="22" r="2" fill="currentColor" stroke="none"/>
          </svg>
          <svg v-else-if="fibre.key === 'viscose'" width="28" height="28" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
            <path d="M16 4 L10 12 L14 12 L8 19 L13 19 L7 26 L25 26 L19 19 L24 19 L18 12 L22 12 Z"/>
            <path d="M14 26 L14 29 L18 29 L18 26"/>
          </svg>
          <svg v-else-if="fibre.key === 'wool'" width="28" height="28" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
            <path d="M20 18 Q24 18 24 14 Q24 10 20 10 Q19 7 15 8 Q11 7 10 10 Q6 10 6 14 Q6 18 10 18 Q10 21 13 21 L17 21 Q20 21 20 18 Z"/>
            <circle cx="24" cy="14" r="2.6"/>
            <circle cx="25" cy="13.5" r="0.5" fill="currentColor" stroke="none"/>
            <path d="M11 21 L11 25"/>
            <path d="M18 21 L18 25"/>
          </svg>
          <svg v-else-if="fibre.key === 'silk'" width="28" height="28" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
            <ellipse cx="16" cy="18" rx="6" ry="9"/>
            <path d="M10 13 Q16 15 22 13"/>
            <path d="M10 18 Q16 20 22 18"/>
            <path d="M10 23 Q16 25 22 23"/>
            <path d="M16 9 L16 4"/>
            <path d="M16 6 Q19 5 20 8"/>
          </svg>
          <svg v-else-if="fibre.key === 'linen'" width="28" height="28" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="16" cy="8" r="3.5"/>
            <circle cx="9" cy="13" r="3.5"/>
            <circle cx="23" cy="13" r="3.5"/>
            <circle cx="12" cy="22" r="3.5"/>
            <circle cx="20" cy="22" r="3.5"/>
            <circle cx="16" cy="16" r="1.8" fill="currentColor" stroke="none"/>
          </svg>
        </span>

        <span class="kh-card__name">{{ shortLabel(fibre) }}</span>

        <span
          class="kh-chip"
          :class="fibre.is_preferred ? 'kh-chip--preferred' : `kh-chip--${fibre.fibre_type}`"
        >
          <Leaf v-if="fibre.is_preferred" :size="9" :stroke-width="2.4" />
          {{ fibre.is_preferred ? 'Preferred' : typeLabel[fibre.fibre_type] }}
        </span>

        <div class="kh-card__bars">
          <span class="kh-card__bar-label">CO₂</span>
          <span class="kh-card__bar-track">
            <span
              class="kh-card__bar-fill"
              :class="severityClass(fibre.co2_kg, GLOBAL_MAX_CO2)"
              :style="{ width: miniPct(fibre.co2_kg, GLOBAL_MAX_CO2) + '%' }"
            ></span>
          </span>
          <span class="kh-card__bar-label">H₂O</span>
          <span class="kh-card__bar-track">
            <span
              class="kh-card__bar-fill"
              :class="severityClass(fibre.water_L, GLOBAL_MAX_WATER)"
              :style="{ width: miniPct(fibre.water_L, GLOBAL_MAX_WATER) + '%' }"
            ></span>
          </span>
        </div>
      </button>
    </div>

    <!-- ── B: Face-off comparison panel ────────────────────────────── -->
    <!-- No <Transition> around the panel: keeping the same <article>
         mounted across fibre swaps means Vue patches text + bar widths in
         place. Bars already have a 700ms width transition, so the swap
         feels alive without any opacity flicker. -->
    <div class="kh-mat__panel-wrap">
      <article class="kh-panel">
          <!-- Preferred branch (Linen): solo celebration card -->
          <template v-if="selected.is_preferred">
            <header class="kh-panel__preferred">
              <span class="kh-panel__badge">
                <Leaf :size="13" :stroke-width="2" /> Already a preferred fibre
              </span>
              <h3 class="kh-panel__name">{{ selected.label }}</h3>
            </header>

            <div class="kh-panel__stats">
              <div class="kh-stat">
                <p class="kh-stat__label">CO₂ per kg fabric</p>
                <p class="kh-stat__value">{{ selected.co2_kg }} kg</p>
              </div>
              <div class="kh-stat">
                <p class="kh-stat__label">Water per kg fabric</p>
                <p class="kh-stat__value">{{ formatWater(selected.water_L) }}</p>
              </div>
            </div>

            <div class="kh-notes">
              <section class="kh-note kh-note--why">
                <p class="kh-note__eyebrow">
                  <Sparkles :size="13" :stroke-width="2" /> WHY IT'S A GOOD CHOICE
                </p>
                <p class="kh-note__body">{{ selected.preferred_note }}</p>
              </section>
              <section class="kh-note kh-note--catch">
                <p class="kh-note__eyebrow">
                  <CircleAlert :size="13" :stroke-width="2" /> CAVEATS
                </p>
                <p class="kh-note__body">{{ selected.caveats }}</p>
              </section>
            </div>
          </template>

          <!-- Standard branch: VS face-off -->
          <template v-else-if="activeAlt">
            <div v-if="selected.alternatives.length > 1" class="kh-panel__alts">
              <button
                v-for="(alt, i) in selected.alternatives"
                :key="alt.key"
                type="button"
                class="kh-alt-chip"
                :class="{ 'kh-alt-chip--active': i === activeAltIndex }"
                :aria-pressed="i === activeAltIndex"
                @click="activeAltIndex = i"
              >
                {{ alt.label }}
              </button>
            </div>

            <div class="kh-panel__data">
                <div class="kh-faceoff">
                  <div class="kh-faceoff__side kh-faceoff__side--from">
                    <p class="kh-faceoff__role">Conventional</p>
                    <h3 class="kh-faceoff__name">{{ selected.label }}</h3>
                    <ul class="kh-faceoff__stats">
                      <li>
                        <span class="kh-faceoff__stat-label">CO₂</span>
                        <span class="kh-faceoff__stat-value">{{ selected.co2_kg }} kg</span>
                      </li>
                      <li>
                        <span class="kh-faceoff__stat-label">H₂O</span>
                        <span class="kh-faceoff__stat-value">{{ formatWater(selected.water_L) }}</span>
                      </li>
                    </ul>
                  </div>

                  <div class="kh-faceoff__middle" aria-hidden="true">
                    <span class="kh-faceoff__arrow">
                      <ArrowRight :size="32" :stroke-width="2.5" />
                    </span>
                    <div class="kh-faceoff__wins">
                      <span class="kh-win kh-win--co2" :class="{ 'kh-win--neg': activeAlt.co2_reduction_pct < 0 }">
                        {{ formatDelta(activeAlt.co2_reduction_pct) }} CO₂
                      </span>
                      <span class="kh-win kh-win--h2o" :class="{ 'kh-win--neg': activeAlt.water_reduction_pct < 0 }">
                        {{ formatDelta(activeAlt.water_reduction_pct) }} H₂O
                      </span>
                    </div>
                  </div>

                  <div class="kh-faceoff__side kh-faceoff__side--to">
                    <p class="kh-faceoff__role">Lower-impact switch</p>
                    <h3 class="kh-faceoff__name">{{ activeAlt.label }}</h3>
                    <ul class="kh-faceoff__stats">
                      <li>
                        <span class="kh-faceoff__stat-label">CO₂</span>
                        <span class="kh-faceoff__stat-value">{{ activeAlt.co2_kg }} kg</span>
                      </li>
                      <li>
                        <span class="kh-faceoff__stat-label">H₂O</span>
                        <span class="kh-faceoff__stat-value">{{ formatWater(activeAlt.water_L) }}</span>
                      </li>
                    </ul>
                  </div>
                </div>

                <div class="kh-bars">
                  <section class="kh-bars__col">
                    <p class="kh-bars__title">CO₂ per kg fabric</p>
                    <div class="kh-bar">
                      <span class="kh-bar__name">{{ selected.label }}</span>
                      <span class="kh-bar__track">
                        <span
                          class="kh-bar__fill kh-bar__fill--worse"
                          :style="{ width: barPct(selected.co2_kg, maxCo2(selected, activeAlt)) + '%' }"
                        ></span>
                      </span>
                    </div>
                    <div class="kh-bar">
                      <span class="kh-bar__name">{{ activeAlt.label }}</span>
                      <span class="kh-bar__track">
                        <span
                          class="kh-bar__fill kh-bar__fill--better"
                          :style="{ width: barPct(activeAlt.co2_kg, maxCo2(selected, activeAlt)) + '%' }"
                        ></span>
                      </span>
                    </div>
                  </section>

                  <section class="kh-bars__col">
                    <p class="kh-bars__title">Water per kg fabric</p>
                    <div class="kh-bar">
                      <span class="kh-bar__name">{{ selected.label }}</span>
                      <span class="kh-bar__track">
                        <span
                          class="kh-bar__fill kh-bar__fill--worse"
                          :style="{ width: barPct(selected.water_L, maxWater(selected, activeAlt)) + '%' }"
                        ></span>
                      </span>
                    </div>
                    <div class="kh-bar">
                      <span class="kh-bar__name">{{ activeAlt.label }}</span>
                      <span class="kh-bar__track">
                        <span
                          class="kh-bar__fill kh-bar__fill--better"
                          :style="{ width: barPct(activeAlt.water_L, maxWater(selected, activeAlt)) + '%' }"
                        ></span>
                      </span>
                    </div>
                  </section>
                </div>

                <div class="kh-notes">
                  <section class="kh-note kh-note--why">
                    <p class="kh-note__eyebrow">
                      <Sparkles :size="13" :stroke-width="2" /> WHY IT'S BETTER
                    </p>
                    <p class="kh-note__body">{{ activeAlt.why_better }}</p>
                  </section>
                  <section class="kh-note kh-note--catch">
                    <p class="kh-note__eyebrow">
                      <CircleAlert :size="13" :stroke-width="2" /> THE CATCH
                    </p>
                    <p class="kh-note__body">{{ activeAlt.caveats }}</p>
                  </section>
                </div>

                <p class="kh-panel__source">Source: {{ activeAlt.source }}</p>
              </div>
          </template>
        </article>
    </div>

    <footer class="kh-mat__nav">
      <button type="button" class="kh-cta kh-cta--ghost" @click="$emit('back')">
        <ArrowLeft :size="16" :stroke-width="2" /> Back
      </button>
      <button type="button" class="kh-cta kh-cta--primary is-burst-host" @click="$emit('next')">
        <CtaBurst />
        <CtaFlip>
          Next: knowledge cards
          <ArrowRight :size="16" :stroke-width="2" />
        </CtaFlip>
      </button>
    </footer>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue'
import {
  ArrowLeft, ArrowRight, Check, CircleAlert, Leaf, Sparkles,
} from 'lucide-vue-next'
import data from '../../data/material-alternatives.json'
import AnimatedHeading from '../AnimatedHeading.vue'
import CtaBurst from '../CtaBurst.vue'
import CtaFlip from '../CtaFlip.vue'
import { useReveal } from '../../motion/useReveal'

defineEmits(['back', 'next'])

const eyebrowRef = ref(null)
useReveal(eyebrowRef, { mode: 'char', stagger: 0.022, duration: 0.5 })

const fibres = data.fibres
// Default to first fibre so the comparison panel is always populated.
const selected = ref(fibres[0])
const activeAltIndex = ref(0)

// Atlas card entrance + active "stand up" animations are driven by CSS
// @keyframes (see <style> below) so they don't fight the rotation
// transition or depend on ScrollTrigger.

const GLOBAL_MAX_CO2 = 35.7    // Acrylic
const GLOBAL_MAX_WATER = 11000 // Cotton

const typeLabel = {
  natural: 'Natural',
  synthetic: 'Synthetic',
  cellulosic: 'Cellulosic',
}

const SHORT_LABELS = {
  polyester: 'Polyester',
  nylon: 'Nylon',
  viscose: 'Viscose',
}
function shortLabel(fibre) {
  return SHORT_LABELS[fibre.key] || fibre.label
}

const activeAlt = computed(() => {
  const alts = selected.value?.alternatives
  return alts && alts.length ? alts[activeAltIndex.value] : null
})

function selectFibre(fibre) {
  if (selected.value?.key === fibre.key) return
  selected.value = fibre
  activeAltIndex.value = 0
}

// Visual tilt encodes data: the worse a fibre's combined footprint, the
// further it leans over (max ±3°). Preferred fibres stand up straight.
function tiltOf(fibre) {
  if (fibre.is_preferred) return 0
  const co2Pct = fibre.co2_kg / GLOBAL_MAX_CO2
  const waterPct = fibre.water_L / GLOBAL_MAX_WATER
  const severity = (co2Pct + waterPct) / 2
  const sign = fibres.indexOf(fibre) % 2 === 0 ? -1 : 1
  return Math.round(severity * 3 * sign * 10) / 10
}

function severityClass(value, max) {
  const pct = (value / max) * 100
  if (pct >= 66) return 'kh-mini__fill--high'
  if (pct >= 33) return 'kh-mini__fill--mid'
  return 'kh-mini__fill--low'
}
function miniPct(value, max) {
  if (!max) return 0
  return Math.max(3, Math.round((value / max) * 100))
}

function maxCo2(orig, alt) {
  return Math.max(orig.co2_kg, alt.co2_kg)
}
function maxWater(orig, alt) {
  return Math.max(orig.water_L, alt.water_L)
}
function barPct(v, max) {
  if (!max) return 0
  return Math.max(2, Math.round((v / max) * 100))
}

function formatWater(litres) {
  if (litres >= 1000) return `${(litres / 1000).toFixed(litres % 1000 === 0 ? 0 : 1)}k L`
  return `${litres} L`
}

function formatDelta(pct) {
  if (pct == null || Number.isNaN(pct)) return ''
  if (pct > 0) return `−${pct}%`
  if (pct < 0) return `+${Math.abs(pct)}%`
  return '0%'
}
</script>

<style scoped>
.kh-mat {
  --kh-content-width: 1080px;
  --kh-amber-soft-bg: rgba(255, 192, 145, 0.32);
  --kh-amber-soft-border: rgba(255, 192, 145, 0.55);
  --kh-amber-soft-text: #8a4a18;
  --kh-danger-soft: rgba(208, 50, 56, 0.55);
  --kh-danger-soft-strong: rgba(208, 50, 56, 0.9);

  max-width: 1280px;
  margin: 0 auto;
  padding: 32px 32px 72px;
}

/* ── Header (no in-page back; footer keeps the single back) ────── */
.kh-mat__head {
  max-width: var(--kh-content-width);
  margin: 0 auto 30px;
  text-align: center;
}
.kh-mat__eyebrow {
  font-size: 11px; font-weight: 700; letter-spacing: 2px;
  color: var(--color-primary-text);
  text-transform: uppercase;
  margin-bottom: 8px;
}
.kh-mat__title {
  font-size: clamp(24px, 3.4vw, 34px);
  font-weight: 800; letter-spacing: -0.6px;
  line-height: 1.15;
  color: var(--color-text);
}

/* ── A · Atlas: fibre cards with personality ──────────────────── */
.kh-mat__atlas {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px 16px;
  max-width: var(--kh-content-width);
  margin: 0 auto 36px;
  /* Keep enough room above so rotated cards don't get clipped. */
  padding: 16px 4px;
}

@keyframes kh-card-enter {
  from {
    opacity: 0;
    transform: rotate(var(--tilt)) translateY(28px) scale(0.92);
  }
  to {
    opacity: 1;
    transform: rotate(var(--tilt)) translateY(0) scale(1);
  }
}
@keyframes kh-panel-enter {
  from { opacity: 0; transform: translateY(28px) scale(0.985); }
  to   { opacity: 1; transform: translateY(0) scale(1); }
}
/* Gentle float on the active card — feels alive. */
/* Gentle float on the active card — used as a *second* animation on top
   of `kh-card-enter`, so toggling `--active` only adds/removes this one
   without re-triggering the entrance. */
@keyframes kh-card-bob {
  0%, 100% { transform: rotate(0deg) translateY(-6px) scale(1.04); }
  50%      { transform: rotate(0deg) translateY(-10px) scale(1.04); }
}
/* Pulse the central arrow toward the alternative. */
@keyframes kh-arrow-pulse {
  0%, 100% { transform: translateX(0); }
  50%      { transform: translateX(6px); }
}

.kh-card {
  --tilt: 0deg;
  --enter-delay: 0s;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 18px 16px 16px;
  background: var(--color-surface);
  border: 1.5px solid var(--color-border-light);
  border-radius: 18px;
  box-shadow: var(--shadow-card);
  text-align: center;
  cursor: pointer;
  transform: rotate(var(--tilt));
  /* Delay lives in a CSS variable so the active rule below can reuse the
     same per-card delay without re-stating it — keeps animation-name list
     index 0 (kh-card-enter) byte-identical, so toggling `--active`
     doesn't re-trigger the entrance. */
  animation: kh-card-enter 0.55s var(--motion-spring) var(--enter-delay) both;
  transition:
    transform 320ms var(--motion-spring),
    box-shadow 240ms var(--motion-entrance),
    border-color 240ms var(--motion-entrance),
    background 240ms var(--motion-entrance);
}
.kh-card:nth-child(1) { --enter-delay: 0.18s; }
.kh-card:nth-child(2) { --enter-delay: 0.24s; }
.kh-card:nth-child(3) { --enter-delay: 0.30s; }
.kh-card:nth-child(4) { --enter-delay: 0.36s; }
.kh-card:nth-child(5) { --enter-delay: 0.42s; }
.kh-card:nth-child(6) { --enter-delay: 0.48s; }
.kh-card:nth-child(7) { --enter-delay: 0.54s; }
.kh-card:nth-child(8) { --enter-delay: 0.60s; }

.kh-card:hover {
  /* Standing up to greet the cursor. */
  transform: rotate(0deg) translateY(-4px) scale(1.02);
  box-shadow: 0 14px 30px -16px rgba(14, 15, 12, 0.22), var(--shadow-card);
}
.kh-card:focus-visible {
  outline: 2px solid var(--color-primary-text);
  outline-offset: 3px;
}

.kh-card--active {
  background: var(--color-primary-lighter);
  border-color: var(--color-primary-text);
  box-shadow: 0 18px 36px -18px rgba(22, 51, 0, 0.35), 0 0 0 4px rgba(159, 232, 112, 0.35);
  /* Static "stood up" pose covers the click-time transform transition;
     bob then takes over the transform at 0.3s and starts cycling.
     The animation list keeps `kh-card-enter` at index 0 with the exact
     same delay, so toggling --active never replays the entrance. */
  transform: rotate(0deg) translateY(-6px) scale(1.04);
  animation:
    kh-card-enter 0.55s var(--motion-spring) var(--enter-delay) both,
    kh-card-bob 3.2s ease-in-out 0.3s infinite;
}
.kh-card--preferred {
  background: linear-gradient(180deg, var(--color-primary-lighter) 0%, var(--color-surface) 100%);
}
.kh-card--preferred.kh-card--active {
  background: var(--color-primary-lighter);
}

.kh-card__pin {
  position: absolute;
  top: -10px; right: -10px;
  width: 26px; height: 26px;
  display: flex; align-items: center; justify-content: center;
  border-radius: 999px;
  background: var(--color-primary);
  color: var(--color-primary-text);
  border: 2px solid var(--color-primary-text);
  box-shadow: 0 6px 14px -4px rgba(22, 51, 0, 0.35);
  /* Spin in with a tiny rotation flourish. */
  transform: rotate(-12deg);
  z-index: 2;
}

.kh-card__icon {
  display: flex; align-items: center; justify-content: center;
  width: 48px; height: 48px;
  border-radius: 14px;
  background: var(--color-surface-alt);
  color: var(--color-primary-text);
  margin-bottom: 2px;
}
.kh-card--active .kh-card__icon {
  background: var(--color-primary);
  color: var(--color-primary-text);
}
.kh-card--preferred .kh-card__icon {
  background: var(--color-primary-light);
}

.kh-card__name {
  font-size: 15px; font-weight: 800;
  color: var(--color-text);
  letter-spacing: -0.2px;
  line-height: 1.15;
}

.kh-chip {
  display: inline-flex; align-items: center; gap: 3px;
  padding: 3px 8px;
  border-radius: 999px;
  font-size: 9px; font-weight: 800; letter-spacing: 1px;
  text-transform: uppercase;
  white-space: nowrap;
}
.kh-chip--natural    { background: #f4ead5; color: #7a5e1c; }
.kh-chip--synthetic  { background: #e8e8e3; color: #5d5d5d; }
.kh-chip--cellulosic { background: #ecd9c9; color: #7a4d2c; }
.kh-chip--preferred  { background: var(--color-primary-light); color: var(--color-primary-text); }

.kh-card__bars {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 4px 6px;
  align-items: center;
  width: 100%;
  margin-top: 4px;
}
.kh-card__bar-label {
  font-size: 8px; font-weight: 800;
  color: var(--color-text-subtle);
  letter-spacing: 0.4px;
}
.kh-card__bar-track {
  height: 5px;
  background: var(--color-surface-alt);
  border-radius: 999px;
  overflow: hidden;
}
.kh-card__bar-fill {
  display: block;
  height: 100%;
  border-radius: 999px;
  transition: width 700ms var(--motion-entrance);
}
.kh-mini__fill--low  { background: linear-gradient(90deg, rgba(159, 232, 112, 0.65), var(--color-primary)); }
.kh-mini__fill--mid  { background: linear-gradient(90deg, rgba(255, 200, 145, 0.7), rgba(255, 154, 74, 0.95)); }
.kh-mini__fill--high { background: linear-gradient(90deg, var(--kh-danger-soft), var(--kh-danger-soft-strong)); }

/* ── B · Face-off panel ─────────────────────────────────────── */
.kh-mat__panel-wrap {
  max-width: var(--kh-content-width);
  margin: 0 auto 28px;
  animation: kh-panel-enter 0.6s var(--motion-spring) 0.72s both;
}
.kh-panel {
  position: relative;
  background: var(--color-surface);
  border: 1.5px solid var(--color-border-light);
  border-radius: 28px;
  padding: 32px 36px 30px;
  box-shadow: 0 18px 40px -24px rgba(14, 15, 12, 0.2), var(--shadow-card);
}

.kh-panel__alts {
  display: flex; flex-wrap: wrap; gap: 6px;
  margin-bottom: 20px;
}
.kh-alt-chip {
  padding: 7px 14px;
  border-radius: 999px;
  border: 1px solid var(--color-border-strong);
  background: transparent;
  color: var(--color-text-muted);
  font-size: 12px; font-weight: 700;
  cursor: pointer;
  transition:
    background var(--transition-base),
    border-color var(--transition-base),
    color var(--transition-base);
}
.kh-alt-chip:hover {
  background: var(--color-surface-alt);
  color: var(--color-text);
}
.kh-alt-chip--active {
  background: var(--color-primary);
  border-color: var(--color-primary-text);
  color: var(--color-primary-text);
}

/* Face-off header: left dimmed, middle live arrow + wins, right bright */
.kh-faceoff {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  gap: 24px;
  margin-bottom: 28px;
}
.kh-faceoff__side {
  display: flex; flex-direction: column; gap: 6px;
  min-width: 0;
}
.kh-faceoff__side--from { text-align: right; }
.kh-faceoff__side--to   { text-align: left; }
.kh-faceoff__role {
  font-size: 10px; font-weight: 800; letter-spacing: 1.4px;
  text-transform: uppercase;
  color: var(--color-text-subtle);
}
.kh-faceoff__side--to .kh-faceoff__role { color: var(--color-primary-text); }
.kh-faceoff__name {
  font-size: clamp(20px, 2.6vw, 28px);
  font-weight: 800;
  letter-spacing: -0.5px;
  line-height: 1.1;
}
.kh-faceoff__side--from .kh-faceoff__name {
  color: var(--color-text-muted);
  text-decoration: line-through;
  text-decoration-thickness: 2px;
  text-decoration-color: rgba(208, 50, 56, 0.45);
}
.kh-faceoff__side--to .kh-faceoff__name { color: var(--color-primary-text); }

.kh-faceoff__stats {
  list-style: none; padding: 0; margin: 4px 0 0;
  display: flex; flex-direction: column; gap: 3px;
}
.kh-faceoff__side--from .kh-faceoff__stats { align-items: flex-end; }
.kh-faceoff__side--to   .kh-faceoff__stats { align-items: flex-start; }
.kh-faceoff__stats li {
  display: inline-flex; gap: 8px;
  font-size: 13px;
  font-variant-numeric: tabular-nums;
}
.kh-faceoff__stat-label {
  font-weight: 800; letter-spacing: 0.4px;
  color: var(--color-text-subtle);
  font-size: 10px;
  align-self: center;
}
.kh-faceoff__side--from .kh-faceoff__stat-value {
  color: var(--color-text-muted);
  opacity: 0.7;
}
.kh-faceoff__side--to .kh-faceoff__stat-value {
  color: var(--color-text);
  font-weight: 800;
}

.kh-faceoff__middle {
  display: flex; flex-direction: column; align-items: center; gap: 10px;
  flex-shrink: 0;
}
.kh-faceoff__arrow {
  display: inline-flex;
  color: var(--color-primary-text);
  animation: kh-arrow-pulse 1.8s ease-in-out infinite;
}
.kh-faceoff__wins {
  display: flex; flex-direction: column; gap: 6px;
  align-items: center;
}

/* Win stickers: slightly rotated to feel hand-stuck. */
.kh-win {
  padding: 6px 14px;
  border-radius: 999px;
  background: var(--color-primary);
  color: var(--color-primary-text);
  font-size: 11px; font-weight: 800;
  letter-spacing: 0.5px;
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
  box-shadow: 0 4px 10px -4px rgba(22, 51, 0, 0.25);
}
.kh-win--co2 { transform: rotate(-3deg); }
.kh-win--h2o { transform: rotate(2deg); }
.kh-win--neg {
  background: var(--kh-amber-soft-bg);
  color: var(--kh-amber-soft-text);
  box-shadow: 0 4px 10px -4px rgba(208, 100, 30, 0.25);
}

/* Detail bars below the face-off */
.kh-bars {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 26px;
}
.kh-bars__col {
  padding: 14px 16px;
  background: var(--color-surface-alt);
  border-radius: 16px;
  border: 1px solid var(--color-border-light);
}
.kh-bars__title {
  font-size: 11px; font-weight: 800; letter-spacing: 1.2px;
  text-transform: uppercase;
  color: var(--color-text-muted);
  margin-bottom: 10px;
}
.kh-bar {
  display: grid;
  grid-template-columns: 110px 1fr;
  align-items: center;
  gap: 10px;
  padding: 3px 0;
}
.kh-bar__name {
  font-size: 11px; font-weight: 600;
  color: var(--color-text-muted);
  white-space: nowrap;
  overflow: hidden; text-overflow: ellipsis;
}
.kh-bar__track {
  height: 10px;
  background: var(--color-surface);
  border-radius: 999px;
  overflow: hidden;
  border: 1px solid var(--color-border-light);
}
.kh-bar__fill {
  display: block;
  height: 100%;
  border-radius: 999px;
  transition: width 700ms var(--motion-entrance);
}
.kh-bar__fill--worse {
  background: linear-gradient(90deg, var(--kh-danger-soft), var(--kh-danger-soft-strong));
}
.kh-bar__fill--better {
  background: linear-gradient(90deg, rgba(159, 232, 112, 0.7), var(--color-primary));
}

/* Sticky-note style Why / Catch */
.kh-notes {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}
.kh-note {
  position: relative;
  padding: 16px 18px;
  border-radius: 14px;
  font-size: 13px; line-height: 1.55;
  box-shadow: 0 10px 22px -14px rgba(14, 15, 12, 0.2);
}
.kh-note--why {
  background: var(--color-primary-lighter);
  border: 1px solid var(--color-border-light);
  transform: rotate(-1.2deg);
}
.kh-note--catch {
  background: var(--kh-amber-soft-bg);
  border: 1px solid var(--kh-amber-soft-border);
  transform: rotate(1.4deg);
}
.kh-note__eyebrow {
  display: inline-flex; align-items: center; gap: 5px;
  font-size: 10px; font-weight: 800; letter-spacing: 1.4px;
  text-transform: uppercase;
  margin-bottom: 6px;
}
.kh-note--why .kh-note__eyebrow   { color: var(--color-primary-text); }
.kh-note--catch .kh-note__eyebrow { color: var(--kh-amber-soft-text); }
.kh-note__body { color: var(--color-text); }

.kh-panel__source {
  margin-top: 16px;
  font-size: 11px; font-style: italic;
  color: var(--color-text-subtle);
  text-align: right;
}

/* Preferred branch (Linen) */
.kh-panel__preferred {
  text-align: center;
  margin-bottom: 22px;
}
.kh-panel__badge {
  display: inline-flex; align-items: center; gap: 5px;
  padding: 5px 14px;
  border-radius: 999px;
  background: var(--color-primary-light);
  color: var(--color-primary-text);
  font-size: 11px; font-weight: 800; letter-spacing: 1px;
  text-transform: uppercase;
  margin-bottom: 12px;
}
.kh-panel__name {
  font-size: clamp(26px, 3.4vw, 34px);
  font-weight: 800;
  letter-spacing: -0.5px;
  color: var(--color-primary-text);
}
.kh-panel__stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 14px;
  margin-bottom: 22px;
}
.kh-stat {
  background: var(--color-primary-lighter);
  border: 1px solid var(--color-border-light);
  border-radius: 16px;
  padding: 16px 18px;
}
.kh-stat__label {
  font-size: 10px; font-weight: 800; letter-spacing: 1.2px;
  color: var(--color-primary-text);
  text-transform: uppercase;
  margin-bottom: 6px;
}
.kh-stat__value {
  font-size: 26px; font-weight: 800;
  color: var(--color-text);
  letter-spacing: -0.4px;
  font-variant-numeric: tabular-nums;
}

/* ── Bottom nav ─────────────────────────────────────────────── */
.kh-mat__nav {
  display: flex; justify-content: space-between;
  margin: 30px auto 0;
  max-width: var(--kh-content-width);
  flex-wrap: wrap; gap: 12px;
}
.kh-cta {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 13px 22px;
  border-radius: var(--radius-btn);
  font-size: 14px; font-weight: 700;
  border: 1px solid transparent;
  cursor: pointer;
  transition: transform var(--transition-base), background var(--transition-base);
}
.kh-cta--primary {
  background: var(--color-primary);
  color: var(--color-primary-text);
}
.kh-cta--primary:hover { transform: scale(1.03); background: var(--color-primary-dark); }
.kh-cta--ghost {
  background: transparent;
  color: var(--color-text);
  border-color: var(--color-border-strong);
}
.kh-cta--ghost:hover {
  background: var(--color-surface-alt);
  transform: scale(1.02);
}

/* No Vue Transition on the panel: the same <article> stays mounted and
   Vue patches text / numbers / inline bar widths in place. The bars'
   own `transition: width 700ms` then carries the visual continuity, and
   there is no opacity dip in between. */

/* Honour OS reduced-motion. */
@media (prefers-reduced-motion: reduce) {
  .kh-card,
  .kh-card--active,
  .kh-mat__panel-wrap,
  .kh-faceoff__arrow {
    animation: none !important;
  }
  .kh-card { transform: rotate(var(--tilt)); }
  .kh-card--active { transform: rotate(0deg); }
}

/* ── Responsive ─────────────────────────────────────────────── */
@media (max-width: 1099px) {
  .kh-mat__atlas {
    grid-template-columns: repeat(4, 1fr);
    gap: 16px 12px;
  }
  .kh-faceoff {
    grid-template-columns: 1fr;
    text-align: center;
    gap: 14px;
  }
  .kh-faceoff__side--from,
  .kh-faceoff__side--to { text-align: center; }
  .kh-faceoff__side--from .kh-faceoff__stats,
  .kh-faceoff__side--to .kh-faceoff__stats { align-items: center; }
  .kh-faceoff__arrow { transform: rotate(90deg); }
}
@media (max-width: 760px) {
  .kh-bars { grid-template-columns: 1fr; }
  .kh-notes { grid-template-columns: 1fr; }
  .kh-mat__atlas {
    grid-template-columns: repeat(2, 1fr);
    gap: 18px 14px;
  }
}
@media (max-width: 480px) {
  .kh-mat { padding: 22px 18px 56px; }
  .kh-panel { padding: 24px 22px 22px; border-radius: 22px; }
  .kh-mat__atlas { gap: 16px 10px; }
  .kh-bar { grid-template-columns: 90px 1fr; gap: 8px; }
}
</style>
