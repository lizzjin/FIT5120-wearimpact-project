<template>
  <div
    class="toast-host"
    role="region"
    aria-live="polite"
    aria-atomic="true"
    aria-label="Notifications"
  >
    <TransitionGroup name="toast" tag="div" class="toast-host__stack">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="toast"
        :class="`toast--${toast.type}`"
        role="status"
        @click="dismiss(toast.id)"
      >
        <span class="toast__message">{{ toast.message }}</span>
        <button
          type="button"
          class="toast__close"
          aria-label="Dismiss"
          @click.stop="dismiss(toast.id)"
        >×</button>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup>
import { provideToast } from '../motion'

const { toasts, dismiss } = provideToast()
</script>

<style scoped>
.toast-host {
  position: fixed;
  right: 24px;
  bottom: 24px;
  z-index: 9999;
  pointer-events: none;
}
.toast-host__stack {
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: flex-end;
}
.toast {
  pointer-events: auto;
  display: inline-flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px 12px 18px;
  min-width: 220px;
  max-width: 360px;
  border-radius: var(--radius-card-sm);
  background: var(--color-surface);
  color: var(--color-text);
  box-shadow: 0 12px 32px rgba(14, 15, 12, 0.18), 0 0 0 1px var(--color-border);
  font-size: 14px;
  line-height: 1.4;
  cursor: pointer;
}
.toast--success { border-left: 4px solid var(--color-positive); }
.toast--error   { border-left: 4px solid var(--color-danger); }
.toast--warning { border-left: 4px solid var(--color-score-start); }
.toast--info    { border-left: 4px solid var(--color-primary); }

.toast__message {
  flex: 1;
  word-break: break-word;
}
.toast__close {
  background: transparent;
  border: none;
  color: var(--color-text-subtle);
  font-size: 20px;
  line-height: 1;
  cursor: pointer;
  padding: 2px 6px;
  border-radius: var(--radius-input);
}
.toast__close:hover {
  background: var(--color-surface-alt);
  color: var(--color-text);
}

/* TransitionGroup choreography — y + opacity, spring-in. */
.toast-enter-active {
  transition: transform 300ms cubic-bezier(0.34, 1.56, 0.64, 1),
              opacity 240ms cubic-bezier(0.22, 1, 0.36, 1);
}
.toast-leave-active {
  transition: transform 200ms cubic-bezier(0.22, 1, 0.36, 1),
              opacity 180ms cubic-bezier(0.22, 1, 0.36, 1);
}
.toast-enter-from {
  transform: translateY(24px);
  opacity: 0;
}
.toast-leave-to {
  transform: translateY(-8px);
  opacity: 0;
}
.toast-move {
  transition: transform 280ms cubic-bezier(0.22, 1, 0.36, 1);
}

@media (max-width: 768px) {
  .toast-host {
    right: 12px;
    bottom: 12px;
    left: 12px;
  }
  .toast {
    max-width: none;
    width: 100%;
  }
}
</style>
