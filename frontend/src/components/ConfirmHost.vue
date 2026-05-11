<template>
  <Teleport to="body">
    <Transition name="confirm">
      <div
        v-if="state"
        class="confirm-overlay"
        role="dialog"
        aria-modal="true"
        :aria-labelledby="titleId"
        :aria-describedby="messageId"
        @click.self="cancel"
      >
        <div class="confirm-panel" ref="panelRef" tabindex="-1">
          <h3 :id="titleId" class="confirm-panel__title">{{ state.title }}</h3>
          <p :id="messageId" class="confirm-panel__message">{{ state.message }}</p>
          <div class="confirm-panel__actions">
            <button
              type="button"
              class="confirm-btn confirm-btn--cancel"
              @click="cancel"
              ref="cancelBtnRef"
            >{{ state.cancelText }}</button>
            <button
              type="button"
              class="confirm-btn"
              :class="state.danger ? 'confirm-btn--danger' : 'confirm-btn--primary'"
              @click="confirm"
            >{{ state.confirmText }}</button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { getConfirmStore } from '../motion'

const { state, close } = getConfirmStore()

const titleId = `confirm-title-${Math.random().toString(36).slice(2, 8)}`
const messageId = `confirm-msg-${Math.random().toString(36).slice(2, 8)}`

const panelRef = ref(null)
const cancelBtnRef = ref(null)

function confirm() { close(true) }
function cancel()  { close(false) }

// Focus the cancel button when the dialog opens — defensive default so
// the Enter key does not accidentally confirm a destructive action.
watch(state, async (s) => {
  if (s) {
    await nextTick()
    cancelBtnRef.value?.focus?.()
  }
})

function onKey(e) {
  if (!state.value) return
  if (e.key === 'Escape') {
    e.preventDefault()
    cancel()
  } else if (e.key === 'Enter' && document.activeElement?.classList?.contains('confirm-btn--primary')) {
    // Already handled by the button's click; no-op here.
  }
}

onMounted(() => document.addEventListener('keydown', onKey))
onBeforeUnmount(() => document.removeEventListener('keydown', onKey))
</script>

<style scoped>
.confirm-overlay {
  position: fixed;
  inset: 0;
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  background: rgba(14, 15, 12, 0.42);
  backdrop-filter: blur(6px) saturate(1.2);
  -webkit-backdrop-filter: blur(6px) saturate(1.2);
}

.confirm-panel {
  width: 100%;
  max-width: 420px;
  background: var(--color-surface);
  border-radius: var(--radius-card);
  padding: 28px 28px 22px;
  box-shadow: var(--shadow-modal);
  outline: none;
}

.confirm-panel__title {
  margin: 0 0 10px;
  font-size: 19px;
  font-weight: 800;
  letter-spacing: -0.01em;
  color: var(--color-text);
}

.confirm-panel__message {
  margin: 0 0 22px;
  font-size: 14.5px;
  line-height: 1.55;
  color: var(--color-text-muted);
}

.confirm-panel__actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.confirm-btn {
  appearance: none;
  border: 1px solid transparent;
  font-family: inherit;
  font-weight: 700;
  font-size: 14px;
  padding: 10px 18px;
  border-radius: var(--radius-pill);
  cursor: pointer;
  transition:
    transform 150ms var(--motion-entrance),
    background 180ms var(--motion-entrance),
    border-color 180ms var(--motion-entrance),
    color 180ms var(--motion-entrance);
}
.confirm-btn:focus-visible {
  outline: 2px solid var(--color-primary-text);
  outline-offset: 3px;
}
.confirm-btn:active { transform: scale(0.97); }

.confirm-btn--cancel {
  background: transparent;
  color: var(--color-text-muted);
  border-color: var(--color-border);
}
.confirm-btn--cancel:hover {
  background: var(--color-surface-alt);
  color: var(--color-text);
}

.confirm-btn--primary {
  background: var(--color-primary);
  color: var(--color-primary-text);
}
.confirm-btn--primary:hover {
  background: var(--color-primary-dark);
}

.confirm-btn--danger {
  background: var(--color-danger);
  color: #fff;
}
.confirm-btn--danger:hover {
  filter: brightness(0.95);
}
</style>

<!-- Enter / leave transition classes intentionally live outside the
     scoped block so they match the <Transition> children on the first
     paint cycle — same fix pattern used by ToastHost. -->
<style>
.confirm-enter-active,
.confirm-leave-active {
  transition: opacity 200ms cubic-bezier(0.22, 1, 0.36, 1);
}
.confirm-enter-active .confirm-panel,
.confirm-leave-active .confirm-panel {
  transition: transform 240ms cubic-bezier(0.22, 1, 0.36, 1),
              opacity 200ms cubic-bezier(0.22, 1, 0.36, 1);
}
.confirm-enter-from,
.confirm-leave-to {
  opacity: 0;
}
.confirm-enter-from .confirm-panel,
.confirm-leave-to .confirm-panel {
  transform: scale(0.96) translateY(16px);
  opacity: 0;
}
</style>
