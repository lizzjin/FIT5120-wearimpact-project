<template>
  <div class="search-box" role="search">
    <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
    </svg>
    <input
      v-model="inputValue"
      type="text"
      placeholder="Search for a brand or company..."
      aria-label="Search clothing brands"
      @input="onInput"
      @keyup.enter="onEnter"
    />
    <Transition name="clear-fade">
      <button v-if="inputValue" class="clear-btn" @click="clear" aria-label="Clear search">
        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path d="M18 6 6 18M6 6l12 12"/>
        </svg>
      </button>
    </Transition>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: { type: String, default: '' },
})

const emit = defineEmits(['update:modelValue', 'search'])

const inputValue = ref(props.modelValue)

watch(() => props.modelValue, (val) => {
  inputValue.value = val
})

function onInput() {
  emit('update:modelValue', inputValue.value)
}

function onEnter() {
  emit('search', inputValue.value)
}

function clear() {
  inputValue.value = ''
  emit('update:modelValue', '')
}
</script>

<style scoped>
.search-box {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 16px;
  color: var(--color-text-faint);
  pointer-events: none;
}

.search-box input {
  width: 100%;
  padding: 16px 44px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-pill);
  font-size: 16px;
  font-weight: 500;
  background: white;
  color: var(--color-text);
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.search-box input:focus {
  border-color: var(--color-primary-text);
  box-shadow: 0 0 0 3px rgba(159, 232, 112, 0.4);
}

.clear-btn {
  position: absolute;
  right: 14px;
  background: var(--color-surface-alt);
  border: none;
  border-radius: 50%;
  width: 26px;
  height: 26px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-subtle);
  cursor: pointer;
  padding: 0;
  transition: background var(--transition-base), color var(--transition-base), transform var(--transition-base);
}

.clear-btn:hover {
  background: var(--color-primary-light);
  color: var(--color-primary-text);
  transform: scale(1.05);
}

/* Clear button fade transition */
.clear-fade-enter-active { transition: opacity 150ms ease, transform 150ms ease; }
.clear-fade-leave-active { transition: opacity 100ms ease, transform 100ms ease; }
.clear-fade-enter-from { opacity: 0; transform: scale(0.8); }
.clear-fade-leave-to { opacity: 0; transform: scale(0.8); }
</style>
