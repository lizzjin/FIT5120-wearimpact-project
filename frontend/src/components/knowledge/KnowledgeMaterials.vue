<template>
  <section class="kh-mat">
    <header class="kh-mat__head">
      <button type="button" class="kh-mat__back" @click="$emit('back')">
        <ArrowLeft :size="16" :stroke-width="2" /> Back
      </button>
      <div class="kh-mat__heading">
        <p class="kh-mat__eyebrow">STEP 03 · MATERIAL TRUTHS</p>
        <h2 class="kh-mat__title">
          Pick a fibre — see the better alternative.
        </h2>
      </div>
    </header>

    <div class="kh-mat__split">
      <!-- ── Left: conventional fibre picker ─────────────────────────── -->
      <aside class="kh-mat__list" aria-label="Conventional fibres">
        <p class="kh-mat__list-eyebrow">CONVENTIONAL FIBRES</p>
        <ul class="kh-mat__list-items">
          <li v-for="fibre in fibres" :key="fibre.key">
            <button
              type="button"
              class="kh-fibre"
              :class="{ 'kh-fibre--active': selected?.key === fibre.key }"
              @click="selectFibre(fibre)"
            >
              <span class="kh-fibre__name">{{ fibre.label }}</span>
              <span class="kh-fibre__chevron" aria-hidden="true">
                <ArrowRight :size="14" :stroke-width="2" />
              </span>
            </button>
          </li>
        </ul>
      </aside>

      <!-- ── Right: comparison panel ─────────────────────────────────── -->
      <div class="kh-mat__compare">
        <Transition name="kh-cmp" mode="out-in">
          <!-- Empty state -->
          <div v-if="!selected" key="empty" class="kh-mat__empty">
            <Sparkles :size="28" :stroke-width="1.6" />
            <p class="kh-mat__empty-title">Tap a fibre to start</p>
            <p class="kh-mat__empty-hint">
              We'll show its lower-impact alternative — with the actual numbers
              and the trade-offs you should know about.
            </p>
          </div>

          <!-- Linen (preferred fibre special case) -->
          <div v-else-if="selected.is_preferred" :key="selected.key + ':preferred'" class="kh-card kh-card--preferred">
            <header class="kh-card__head">
              <span class="kh-card__badge">
                <Leaf :size="13" :stroke-width="2" /> Already a preferred fibre
              </span>
              <h3 class="kh-card__title">{{ selected.label }}</h3>
            </header>

            <div class="kh-card__metrics">
              <div class="kh-stat">
                <p class="kh-stat__label">CO₂ per kg fabric</p>
                <p class="kh-stat__value">{{ selected.co2_kg }} kg</p>
              </div>
              <div class="kh-stat">
                <p class="kh-stat__label">Water per kg fabric</p>
                <p class="kh-stat__value">{{ formatWater(selected.water_L) }}</p>
              </div>
            </div>

            <section class="kh-card__why">
              <p class="kh-card__why-eyebrow">
                <Sparkles :size="13" :stroke-width="2" /> WHY IT'S A GOOD CHOICE
              </p>
              <p class="kh-card__why-body">{{ selected.preferred_note }}</p>
            </section>

            <section class="kh-card__caveat">
              <p class="kh-card__caveat-eyebrow">
                <CircleAlert :size="13" :stroke-width="2" /> CAVEATS
              </p>
              <p class="kh-card__caveat-body">{{ selected.caveats }}</p>
            </section>
          </div>

          <!-- Standard alternatives list -->
          <div v-else :key="selected.key" class="kh-mat__results">
            <div
              v-for="alt in selected.alternatives"
              :key="alt.key"
              class="kh-card"
            >
              <header class="kh-card__head">
                <p class="kh-card__pair">
                  <span>{{ selected.label }}</span>
                  <ArrowRight :size="14" :stroke-width="2" class="kh-card__pair-arrow" />
                  <span class="kh-card__pair-alt">{{ alt.label }}</span>
                </p>
              </header>

              <!-- CO2 comparison -->
              <section class="kh-bar">
                <div class="kh-bar__head">
                  <span class="kh-bar__label">CO₂ per kg fabric</span>
                  <span class="kh-bar__delta" :class="{ 'kh-bar__delta--neg': alt.co2_reduction_pct < 0 }">
                    {{ formatDelta(alt.co2_reduction_pct) }}
                  </span>
                </div>
                <div class="kh-bar__row">
                  <span class="kh-bar__row-name">Conventional</span>
                  <span class="kh-bar__track">
                    <span class="kh-bar__fill kh-bar__fill--worse" :style="{ width: barPct(selected.co2_kg, maxCo2(selected, alt)) + '%' }"></span>
                  </span>
                  <span class="kh-bar__row-value">{{ selected.co2_kg }} kg</span>
                </div>
                <div class="kh-bar__row">
                  <span class="kh-bar__row-name">{{ alt.label }}</span>
                  <span class="kh-bar__track">
                    <span class="kh-bar__fill kh-bar__fill--better" :style="{ width: barPct(alt.co2_kg, maxCo2(selected, alt)) + '%' }"></span>
                  </span>
                  <span class="kh-bar__row-value">{{ alt.co2_kg }} kg</span>
                </div>
              </section>

              <!-- Water comparison -->
              <section class="kh-bar">
                <div class="kh-bar__head">
                  <span class="kh-bar__label">Water per kg fabric</span>
                  <span class="kh-bar__delta" :class="{ 'kh-bar__delta--neg': alt.water_reduction_pct < 0 }">
                    {{ formatDelta(alt.water_reduction_pct) }}
                  </span>
                </div>
                <div class="kh-bar__row">
                  <span class="kh-bar__row-name">Conventional</span>
                  <span class="kh-bar__track">
                    <span class="kh-bar__fill kh-bar__fill--worse" :style="{ width: barPct(selected.water_L, maxWater(selected, alt)) + '%' }"></span>
                  </span>
                  <span class="kh-bar__row-value">{{ formatWater(selected.water_L) }}</span>
                </div>
                <div class="kh-bar__row">
                  <span class="kh-bar__row-name">{{ alt.label }}</span>
                  <span class="kh-bar__track">
                    <span class="kh-bar__fill kh-bar__fill--better" :style="{ width: barPct(alt.water_L, maxWater(selected, alt)) + '%' }"></span>
                  </span>
                  <span class="kh-bar__row-value">{{ formatWater(alt.water_L) }}</span>
                </div>
              </section>

              <section class="kh-card__why">
                <p class="kh-card__why-eyebrow">
                  <Sparkles :size="13" :stroke-width="2" /> WHY IT'S BETTER
                </p>
                <p class="kh-card__why-body">{{ alt.why_better }}</p>
              </section>

              <section class="kh-card__caveat">
                <p class="kh-card__caveat-eyebrow">
                  <CircleAlert :size="13" :stroke-width="2" /> THE CATCH
                </p>
                <p class="kh-card__caveat-body">{{ alt.caveats }}</p>
              </section>

              <p class="kh-card__source">Source: {{ alt.source }}</p>
            </div>
          </div>
        </Transition>
      </div>
    </div>

    <footer class="kh-mat__nav">
      <button type="button" class="kh-cta kh-cta--ghost" @click="$emit('back')">
        <ArrowLeft :size="16" :stroke-width="2" /> Back
      </button>
      <button type="button" class="kh-cta kh-cta--primary" @click="$emit('next')">
        Next: knowledge cards
        <ArrowRight :size="16" :stroke-width="2" />
      </button>
    </footer>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import {
  ArrowLeft, ArrowRight, CircleAlert, Leaf, Sparkles,
} from 'lucide-vue-next'
import data from '../../data/material-alternatives.json'

defineEmits(['back', 'next'])

const fibres = data.fibres
const selected = ref(null)

function selectFibre(fibre) {
  // Toggle off if the user clicks the active fibre again — gives a quick
  // way to clear the panel without a separate "close" button.
  selected.value = selected.value?.key === fibre.key ? null : fibre
}

// Bar-chart math: each metric scales the two bars against the larger of the
// two values so the worse one always reaches 100% and the better one shows
// its proportional share.
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
  max-width: 1280px;
  margin: 0 auto;
  padding: 32px 32px 72px;
}

/* ── Header ─────────────────────────────────────────────────── */
.kh-mat__head {
  display: flex; align-items: center; gap: 18px;
  margin-bottom: 28px; flex-wrap: wrap;
}
.kh-mat__back {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 8px 14px;
  border-radius: var(--radius-pill);
  background: transparent;
  border: 1px solid var(--color-border-strong);
  color: var(--color-text-muted);
  font-size: 13px; font-weight: 600;
  cursor: pointer;
  transition: color var(--transition-base), background var(--transition-base);
}
.kh-mat__back:hover {
  color: var(--color-text); background: var(--color-surface-alt);
}
.kh-mat__heading { flex: 1; min-width: 240px; }
.kh-mat__eyebrow {
  font-size: 11px; font-weight: 700; letter-spacing: 2px;
  color: var(--color-primary-text);
  text-transform: uppercase;
  margin-bottom: 6px;
}
.kh-mat__title {
  font-size: clamp(22px, 3vw, 30px);
  font-weight: 800; letter-spacing: -0.6px;
  line-height: 1.18;
  color: var(--color-text);
}

/* ── Split layout ───────────────────────────────────────────── */
.kh-mat__split {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 28px;
  align-items: start;
}

/* ── Left list ──────────────────────────────────────────────── */
.kh-mat__list {
  position: sticky;
  top: 92px;
  background: var(--color-surface);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-card-lg);
  padding: 18px 16px 14px;
  box-shadow: var(--shadow-card);
}
.kh-mat__list-eyebrow {
  font-size: 10px; font-weight: 700; letter-spacing: 1.6px;
  color: var(--color-text-subtle);
  text-transform: uppercase;
  margin-bottom: 10px;
  padding: 0 4px;
}
.kh-mat__list-items {
  list-style: none; padding: 0; margin: 0;
  display: flex; flex-direction: column; gap: 4px;
}
.kh-fibre {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  width: 100%;
  padding: 12px 14px;
  background: transparent;
  border: 1px solid transparent;
  border-radius: var(--radius-card-sm);
  text-align: left;
  cursor: pointer;
  transition:
    background var(--transition-base),
    border-color var(--transition-base);
}
.kh-fibre:hover {
  background: var(--color-surface-alt);
}
.kh-fibre__name {
  font-size: 14px; font-weight: 700;
  color: var(--color-text);
}
.kh-fibre__chevron {
  color: var(--color-text-subtle);
  display: flex; align-items: center;
  flex-shrink: 0;
  transition: transform var(--transition-base);
}
.kh-fibre--active {
  background: var(--color-primary-lighter);
  border-color: var(--color-primary-text);
}
.kh-fibre--active .kh-fibre__name { color: var(--color-primary-text); }
.kh-fibre--active .kh-fibre__chevron { color: var(--color-primary-text); transform: translateX(2px); }

/* ── Right compare panel ────────────────────────────────────── */
.kh-mat__compare {
  min-height: 480px;
}

/* Empty state */
.kh-mat__empty {
  background: var(--color-surface);
  border: 1.5px dashed var(--color-border-strong);
  border-radius: var(--radius-card-lg);
  padding: 56px 32px;
  text-align: center;
  color: var(--color-text-muted);
}
.kh-mat__empty :first-child {
  color: var(--color-primary-text);
  margin-bottom: 12px;
}
.kh-mat__empty-title {
  font-size: 18px; font-weight: 800;
  color: var(--color-text);
  margin-bottom: 6px;
}
.kh-mat__empty-hint {
  font-size: 13px; line-height: 1.55;
  max-width: 420px; margin: 0 auto;
}

/* Results stack (one or two cards) */
.kh-mat__results {
  display: flex; flex-direction: column; gap: 16px;
}

/* ── Compare card ───────────────────────────────────────────── */
.kh-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-card-lg);
  padding: 24px 26px;
  box-shadow: var(--shadow-card);
}
.kh-card__head { margin-bottom: 18px; }
.kh-card__pair {
  display: inline-flex; align-items: center; gap: 8px;
  font-size: 16px; font-weight: 700;
  color: var(--color-text);
}
.kh-card__pair-arrow {
  color: var(--color-text-subtle);
  flex-shrink: 0;
}
.kh-card__pair-alt {
  color: var(--color-primary-text);
}
.kh-card__badge {
  display: inline-flex; align-items: center; gap: 5px;
  padding: 4px 10px;
  border-radius: 999px;
  background: var(--color-primary-light);
  color: var(--color-primary-text);
  font-size: 10px; font-weight: 800; letter-spacing: 1.2px;
  text-transform: uppercase;
  margin-bottom: 10px;
}
.kh-card__title {
  font-size: 22px; font-weight: 800;
  color: var(--color-text);
  letter-spacing: -0.4px;
}

.kh-card__metrics {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 18px;
}
.kh-stat {
  background: var(--color-primary-lighter);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-card-sm);
  padding: 12px 14px;
}
.kh-stat__label {
  font-size: 10px; font-weight: 700; letter-spacing: 1.2px;
  color: var(--color-primary-text);
  text-transform: uppercase;
  margin-bottom: 4px;
}
.kh-stat__value {
  font-size: 20px; font-weight: 800;
  color: var(--color-text);
  letter-spacing: -0.4px;
}

/* ── Bar comparison ─────────────────────────────────────────── */
.kh-bar { margin-bottom: 16px; }
.kh-bar__head {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 8px;
}
.kh-bar__label {
  font-size: 12px; font-weight: 700; letter-spacing: 1px;
  color: var(--color-text);
  text-transform: uppercase;
}
.kh-bar__delta {
  font-size: 12px; font-weight: 800;
  color: var(--color-positive, #2c7a2c);
  background: var(--color-primary-light);
  padding: 3px 10px;
  border-radius: 999px;
  letter-spacing: 0.4px;
}
.kh-bar__delta--neg {
  color: #8a4a18;
  background: rgba(255, 192, 145, 0.3);
}
.kh-bar__row {
  display: grid;
  grid-template-columns: 110px 1fr 90px;
  align-items: center;
  gap: 10px;
  padding: 4px 0;
}
.kh-bar__row-name {
  font-size: 11px; font-weight: 600;
  color: var(--color-text-muted);
}
.kh-bar__track {
  height: 10px;
  background: var(--color-surface-alt);
  border-radius: 999px;
  overflow: hidden;
  position: relative;
}
.kh-bar__fill {
  display: block;
  height: 100%;
  border-radius: 999px;
  transition: width 600ms cubic-bezier(0.22, 1, 0.36, 1);
}
.kh-bar__fill--worse {
  background: linear-gradient(
    90deg,
    rgba(208, 50, 56, 0.5),
    rgba(208, 50, 56, 0.85)
  );
}
.kh-bar__fill--better {
  background: linear-gradient(
    90deg,
    rgba(159, 232, 112, 0.7),
    var(--color-primary)
  );
}
.kh-bar__row-value {
  font-size: 12px; font-weight: 700;
  color: var(--color-text);
  text-align: right;
  font-variant-numeric: tabular-nums;
}

/* ── Why/Caveat sections ────────────────────────────────────── */
.kh-card__why,
.kh-card__caveat {
  padding: 12px 14px;
  border-radius: var(--radius-card-sm);
  margin-top: 12px;
  font-size: 13px; line-height: 1.55;
}
.kh-card__why {
  background: var(--color-primary-lighter);
  border: 1px solid var(--color-border-light);
}
.kh-card__caveat {
  background: rgba(255, 192, 145, 0.16);
  border: 1px solid rgba(255, 192, 145, 0.45);
}
.kh-card__why-eyebrow,
.kh-card__caveat-eyebrow {
  display: inline-flex; align-items: center; gap: 5px;
  font-size: 10px; font-weight: 800; letter-spacing: 1.4px;
  text-transform: uppercase;
  margin-bottom: 6px;
}
.kh-card__why-eyebrow { color: var(--color-primary-text); }
.kh-card__caveat-eyebrow { color: #8a4a18; }
.kh-card__why-body { color: var(--color-text); }
.kh-card__caveat-body { color: var(--color-text); }
.kh-card__source {
  margin-top: 14px;
  font-size: 11px; font-style: italic;
  color: var(--color-text-subtle);
  text-align: right;
}

/* ── Bottom nav ─────────────────────────────────────────────── */
.kh-mat__nav {
  display: flex; justify-content: space-between;
  margin-top: 36px;
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

/* ── Compare-panel transitions ──────────────────────────────── */
.kh-cmp-enter-active,
.kh-cmp-leave-active {
  transition:
    opacity 240ms cubic-bezier(0.22, 1, 0.36, 1),
    transform 240ms cubic-bezier(0.22, 1, 0.36, 1);
}
.kh-cmp-enter-from { opacity: 0; transform: translateY(8px); }
.kh-cmp-leave-to   { opacity: 0; transform: translateY(-6px); }

/* ── Responsive ─────────────────────────────────────────────── */
@media (max-width: 1000px) {
  .kh-mat__split {
    grid-template-columns: 1fr;
    gap: 18px;
  }
  .kh-mat__list {
    position: static;
  }
  .kh-mat__list-items {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 6px;
  }
  .kh-mat__compare { min-height: auto; }
}
@media (max-width: 700px) {
  .kh-mat { padding: 22px 18px 56px; }
  .kh-card { padding: 20px 18px; }
  .kh-bar__row {
    grid-template-columns: 90px 1fr 70px;
    gap: 8px;
  }
  .kh-card__metrics { grid-template-columns: 1fr; }
}
</style>
