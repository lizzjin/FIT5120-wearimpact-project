<template>
  <div class="tag-input" :class="{ 'tag-input--full': isFull }">
    <div class="tag-input__shell" @click="focusInput">
      <span
        v-for="tag in tags"
        :key="tag.company_id"
        class="tag-chip"
      >
        <img
          v-if="tag.logo && !tag._logoErr"
          :src="tag.logo"
          alt=""
          class="tag-chip__avatar"
          @error="tag._logoErr = true"
        />
        <span v-else class="tag-chip__avatar tag-chip__avatar--fallback">
          {{ tag.company_name.charAt(0).toUpperCase() }}
        </span>
        <span class="tag-chip__name">{{ tag.company_name }}</span>
        <button
          type="button"
          class="tag-chip__remove"
          :aria-label="`Remove ${tag.company_name}`"
          @click.stop="removeTag(tag.company_id)"
        >
          <X :size="14" :stroke-width="2.5" />
        </button>
      </span>

      <input
        ref="inputEl"
        v-model="query"
        type="text"
        class="tag-input__field"
        :placeholder="isFull ? 'Max 3 — remove one to add another' : (tags.length === 0 ? 'Type a brand name…' : 'Add another…')"
        :disabled="isFull"
        @input="onInput"
        @keydown.enter.prevent="onEnter"
        @keydown.backspace="onBackspace"
        @keydown.down.prevent="moveCursor(1)"
        @keydown.up.prevent="moveCursor(-1)"
        @keydown.escape="closeDropdown"
        @focus="reopenIfHasResults"
      />
    </div>

    <!-- Fuzzy autocomplete dropdown -->
    <Transition name="tag-drop">
      <div v-if="showDropdown" class="tag-input__dropdown">
        <div v-if="isLoading" class="tag-input__hint">Searching…</div>
        <template v-else-if="filteredResults.length > 0">
          <button
            v-for="(item, i) in filteredResults"
            :key="item.company_id"
            type="button"
            class="tag-row"
            :class="{ 'tag-row--cursor': i === cursor }"
            @mouseenter="cursor = i"
            @click="addTag(item)"
          >
            <img
              v-if="!rowLogoErr[item.company_id]"
              :src="logoFor(item.company_name)"
              alt=""
              class="tag-row__avatar"
              @error="rowLogoErr[item.company_id] = true"
            />
            <span v-else class="tag-row__avatar tag-row__avatar--fallback">
              {{ item.company_name.charAt(0).toUpperCase() }}
            </span>
            <span class="tag-row__name">{{ item.company_name }}</span>
            <span v-if="item.matched_brand && item.matched_brand !== item.company_name" class="tag-row__matched">
              via {{ item.matched_brand }}
            </span>
          </button>
        </template>
        <div v-else-if="query.trim().length >= 1" class="tag-input__hint">No matches. Try a different spelling.</div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { computed, nextTick, reactive, ref, watch } from 'vue'
import { X } from 'lucide-vue-next'
import { searchBrands } from '../../services/brandService'

const props = defineProps({
  modelValue: { type: Array, default: () => [] },
  max: { type: Number, default: 3 },
})
const emit = defineEmits(['update:modelValue'])

const tags = computed(() => props.modelValue)
const isFull = computed(() => tags.value.length >= props.max)

const inputEl = ref(null)
const query = ref('')
const results = ref([])
const isLoading = ref(false)
const cursor = ref(0)
const showDropdown = ref(false)
const rowLogoErr = reactive({})

let debounceTimer = null

function logoFor(name) {
  return `https://img.logo.dev/${guessDomain(name)}?token=pk_LbFI27UJRDWnSoDCC_4GYA&size=40`
}

function guessDomain(name) {
  const overrides = {
    'H&M': 'hm.com', 'H&M Group': 'hm.com', 'Inditex': 'inditex.com',
    'Levi Strauss & Co': 'levi.com', 'PVH Corp': 'pvh.com', 'VF Corporation': 'vfc.com',
    'Hanesbrands': 'hanes.com', 'Fast Retailing': 'fastretailing.com', 'Kering': 'kering.com',
    'LVMH': 'lvmh.com', 'Adidas': 'adidas.com', 'Nike': 'nike.com', 'Puma': 'puma.com',
    'Patagonia': 'patagonia.com',
  }
  if (overrides[name]) return overrides[name]
  return name.toLowerCase().replace(/[^a-z0-9]/g, '') + '.com'
}

const filteredResults = computed(() => {
  const taken = new Set(tags.value.map((t) => t.company_id))
  return results.value.filter((r) => !taken.has(r.company_id)).slice(0, 8)
})

watch(filteredResults, (rs) => {
  if (cursor.value >= rs.length) cursor.value = Math.max(0, rs.length - 1)
})

function onInput() {
  if (debounceTimer) clearTimeout(debounceTimer)
  const q = query.value.trim()
  if (!q) {
    results.value = []
    showDropdown.value = false
    return
  }
  isLoading.value = true
  showDropdown.value = true
  debounceTimer = setTimeout(async () => {
    try {
      const data = await searchBrands(q)
      results.value = data.results ?? []
      cursor.value = 0
    } catch {
      results.value = []
    } finally {
      isLoading.value = false
    }
  }, 220)
}

function reopenIfHasResults() {
  if (filteredResults.value.length > 0) showDropdown.value = true
}

function closeDropdown() { showDropdown.value = false }

function moveCursor(delta) {
  if (!showDropdown.value) return
  const len = filteredResults.value.length
  if (len === 0) return
  cursor.value = (cursor.value + delta + len) % len
}

function onEnter() {
  if (showDropdown.value && filteredResults.value[cursor.value]) {
    addTag(filteredResults.value[cursor.value])
  }
}

function onBackspace() {
  if (query.value === '' && tags.value.length > 0) {
    const next = tags.value.slice(0, -1)
    emit('update:modelValue', next)
  }
}

function addTag(item) {
  if (isFull.value) return
  if (tags.value.some((t) => t.company_id === item.company_id)) return
  const enriched = {
    company_id: item.company_id,
    company_name: item.company_name,
    overall_score: item.overall_score,
    score_label: item.score_label,
    logo: logoFor(item.company_name),
    _logoErr: false,
  }
  emit('update:modelValue', [...tags.value, enriched])
  query.value = ''
  results.value = []
  showDropdown.value = false
  nextTick(() => focusInput())
}

function removeTag(id) {
  emit('update:modelValue', tags.value.filter((t) => t.company_id !== id))
}

function focusInput() {
  if (!isFull.value) inputEl.value?.focus()
}

defineExpose({ focusInput })
</script>

<style scoped>
.tag-input {
  position: relative;
  width: 100%;
}

.tag-input__shell {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 10px 14px;
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid var(--color-kh-glass-border);
  border-radius: 18px;
  min-height: 56px;
  align-items: center;
  cursor: text;
  transition: border-color 180ms var(--motion-entrance), box-shadow 180ms var(--motion-entrance);
}

.tag-input__shell:focus-within {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 4px rgba(159, 232, 112, 0.22);
}

.tag-input--full .tag-input__shell {
  border-color: rgba(22, 51, 0, 0.18);
  background: rgba(255, 255, 255, 0.65);
}

/* Chip */
.tag-chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 4px 10px 4px 4px;
  background: var(--color-primary);
  color: var(--color-primary-text);
  border-radius: var(--radius-pill);
  font-size: 13px;
  font-weight: 700;
  max-width: 220px;
}

.tag-chip__avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: white;
  object-fit: contain;
  padding: 2px;
  flex-shrink: 0;
}

.tag-chip__avatar--fallback {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: var(--color-primary-text);
  font-weight: 800;
}

.tag-chip__name {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.tag-chip__remove {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  background: transparent;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  color: var(--color-primary-text);
  opacity: 0.6;
  transition: opacity 160ms var(--motion-entrance), background 160ms var(--motion-entrance);
}

.tag-chip__remove:hover {
  opacity: 1;
  background: rgba(22, 51, 0, 0.1);
}

/* Input field */
.tag-input__field {
  flex: 1;
  min-width: 140px;
  border: none;
  outline: none;
  background: transparent;
  font-size: 15px;
  color: var(--color-text);
  font-family: inherit;
  padding: 6px 4px;
}

.tag-input__field::placeholder {
  color: var(--color-text-faint);
}

.tag-input__field:disabled {
  cursor: not-allowed;
  color: var(--color-text-faint);
}

/* Dropdown */
.tag-input__dropdown {
  position: absolute;
  top: calc(100% + 6px);
  left: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.98);
  border: 1px solid var(--color-kh-glass-border);
  border-radius: 16px;
  box-shadow: 0 16px 40px rgba(22, 51, 0, 0.12);
  overflow: hidden;
  z-index: 30;
  max-height: 320px;
  overflow-y: auto;
}

.tag-input__hint {
  padding: 16px 20px;
  font-size: 13px;
  color: var(--color-text-faint);
}

.tag-row {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  padding: 10px 14px;
  background: transparent;
  border: none;
  cursor: pointer;
  text-align: left;
  font-family: inherit;
  transition: background 140ms var(--motion-entrance);
}

.tag-row--cursor,
.tag-row:hover {
  background: rgba(159, 232, 112, 0.16);
}

.tag-row__avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: white;
  object-fit: contain;
  padding: 3px;
  flex-shrink: 0;
  border: 1px solid var(--color-kh-glass-border);
}

.tag-row__avatar--fallback {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 800;
  color: var(--color-text);
}

.tag-row__name {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text);
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.tag-row__matched {
  font-size: 12px;
  color: var(--color-text-faint);
  flex-shrink: 0;
}

.tag-drop-enter-active, .tag-drop-leave-active {
  transition: opacity 160ms var(--motion-entrance), transform 160ms var(--motion-entrance);
}
.tag-drop-enter-from, .tag-drop-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>
