<template>
  <div class="gate" role="dialog" aria-modal="true" aria-labelledby="gate-title">
    <div class="gate__card" :class="{ 'is-shaking': error }">
      <div class="gate__brand" id="gate-title">
        <span class="gate__brand-mark">Wear</span><span class="gate__brand-tail">Impact</span>
      </div>
      <p class="gate__hint">This site is invite-only · Enter the access key to continue.</p>
      <form class="gate__form" @submit.prevent="onSubmit">
        <input
          ref="inputRef"
          v-model="pwd"
          type="password"
          class="gate__input"
          :class="{ 'has-error': error }"
          placeholder="Access key"
          autocomplete="off"
          autocapitalize="off"
          spellcheck="false"
          required
        />
        <button type="submit" class="gate__btn">Enter</button>
      </form>
      <p v-if="error" class="gate__error" role="alert">Wrong key — try again.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { tryUnlock } from '../services/siteGate'

const emit = defineEmits(['unlocked'])

const pwd = ref('')
const error = ref(false)
const inputRef = ref(null)
let errorTimer = null

onMounted(() => {
  // autofocus attribute is unreliable across some routers — ensure the field
  // takes focus once the gate is mounted.
  inputRef.value?.focus?.()
})

function onSubmit() {
  if (tryUnlock(pwd.value)) {
    emit('unlocked')
    return
  }
  error.value = true
  if (errorTimer) clearTimeout(errorTimer)
  errorTimer = setTimeout(() => { error.value = false }, 800)
  // Keep focus + clear so the user can retry immediately.
  pwd.value = ''
  inputRef.value?.focus?.()
}
</script>

<style scoped>
.gate {
  position: fixed;
  inset: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  background: var(--color-warm-cream, #f6f0e6);
  font-family: 'Inter', system-ui, -apple-system, Arial, sans-serif;
  color: var(--color-text, #0e0f0c);
}

.gate__card {
  width: 100%;
  max-width: 400px;
  padding: 36px 32px 28px;
  background: #fff;
  border: 1px solid var(--color-border-light, #ece6dc);
  border-radius: var(--radius-card-sm, 16px);
  box-shadow: 0 18px 48px rgba(14, 15, 12, 0.08);
}

.gate__card.is-shaking {
  animation: gate-shake 0.4s cubic-bezier(0.36, 0.07, 0.19, 0.97);
}

.gate__brand {
  font-size: 26px;
  font-weight: 900;
  letter-spacing: -0.4px;
  line-height: 1;
  margin-bottom: 18px;
}
.gate__brand-mark { color: var(--color-primary-text, #163300); }
.gate__brand-tail { color: var(--color-text, #0e0f0c); }

.gate__hint {
  font-size: 13px;
  line-height: 1.5;
  color: var(--color-text-muted, #454745);
  margin: 0 0 22px;
}

.gate__form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.gate__input {
  width: 100%;
  padding: 12px 14px;
  font-size: 15px;
  font-family: inherit;
  color: var(--color-text, #0e0f0c);
  background: var(--color-warm-cream, #f6f0e6);
  border: 1px solid var(--color-border-strong, #d6cebd);
  border-radius: 10px;
  outline: none;
  transition: border-color 180ms ease, box-shadow 180ms ease;
}
.gate__input:focus {
  border-color: var(--color-primary-text, #163300);
  box-shadow: 0 0 0 3px rgba(159, 232, 112, 0.35);
}
.gate__input.has-error {
  border-color: #c74040;
  box-shadow: 0 0 0 3px rgba(199, 64, 64, 0.18);
}

.gate__btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 12px 18px;
  font-size: 15px;
  font-weight: 700;
  font-family: inherit;
  color: var(--color-primary-text, #163300);
  background: var(--color-primary, #9fe870);
  border: none;
  border-radius: 999px;
  cursor: pointer;
  transition: transform 180ms ease, background 180ms ease;
}
.gate__btn:hover { background: var(--color-primary-dark, #cdffad); transform: translateY(-1px); }
.gate__btn:active { transform: translateY(0); }

.gate__error {
  margin: 14px 0 0;
  font-size: 12.5px;
  font-weight: 600;
  color: #c74040;
}

@keyframes gate-shake {
  10%, 90% { transform: translateX(-2px); }
  20%, 80% { transform: translateX(4px); }
  30%, 50%, 70% { transform: translateX(-6px); }
  40%, 60% { transform: translateX(6px); }
}

@media (max-width: 480px) {
  .gate__card { padding: 28px 22px 22px; }
  .gate__brand { font-size: 22px; }
}
</style>
