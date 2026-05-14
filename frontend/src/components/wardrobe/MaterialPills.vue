<template>
  <ul v-if="materials && materials.length" class="wd-mat-pills">
    <li v-for="m in materials" :key="m.key + '-' + m.percent" class="wd-mat-pill">
      <span class="wd-mat-pill__icon" v-html="iconSvg(m.icon)" />
      <span class="wd-mat-pill__label">{{ m.name_en }} {{ Math.round(m.percent) }}%</span>
    </li>
  </ul>
</template>

<script setup>
defineProps({
  materials: { type: Array, default: () => [] }
})

// 11 fabric-bucket icons. Each canonical material in
// material_recognition.py points at one of these buckets via `icon`.
const COMMON = ' width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true"'
const STROKE = ' stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"'

const ICONS = {
  cotton:    `<svg${COMMON}><ellipse cx="12" cy="13" rx="7" ry="5"${STROKE}/><path d="M8 10c2-2 6-2 8 0"${STROKE}/><path d="M9 16c1.5 1 4.5 1 6 0"${STROKE}/></svg>`,
  polyester: `<svg${COMMON}><path d="M5 18c3-6 5-10 7-14M9 18c2.5-5 4.5-9 6.5-13M13 18c2-4 3.5-7.5 5-11"${STROKE}/></svg>`,
  wool:      `<svg${COMMON}><path d="M7 16c2-6 6-9 10-9-1 4-3 8-6 11-2-2-3-4-4-2z"${STROKE}/></svg>`,
  silk:      `<svg${COMMON}><path d="M12 4v16M8 8c4 2 8 2 8-2"${STROKE}/><circle cx="12" cy="6" r="1.2" fill="currentColor"/></svg>`,
  linen:     `<svg${COMMON}><path d="M12 3v18M8 7h8M8 12h8M8 17h5"${STROKE}/></svg>`,
  viscose:   `<svg${COMMON}><path d="M6 18c0-8 4-12 6-14 2 4 4 9 4 14"${STROKE}/><path d="M9 14h6"${STROKE}/></svg>`,
  nylon:     `<svg${COMMON}><rect x="5" y="5" width="14" height="14" rx="3"${STROKE}/><path d="M9 9l6 6M15 9l-6 6"${STROKE}/></svg>`,
  spandex:   `<svg${COMMON}><path d="M7 17c4-3 7-7 10-12M6 8c3 3 6 6 10 8"${STROKE}/></svg>`,
  acrylic:   `<svg${COMMON}><circle cx="12" cy="12" r="7"${STROKE}/><circle cx="12" cy="12" r="3"${STROKE}/></svg>`,
  down:      `<svg${COMMON}><path d="M12 4c-3 4-5 8-5 12 0 3 2 5 5 5s5-2 5-5c0-4-2-8-5-12z"${STROKE}/></svg>`,
  leather:   `<svg${COMMON}><path d="M5 8c3-2 7-2 10 0v10c-3 2-7 2-10 0V8z"${STROKE}/></svg>`,
}

function iconSvg(id) {
  return ICONS[id] || ICONS.cotton
}
</script>

<style scoped>
.wd-mat-pills {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

/* Soft chip per material — rotating through 4 muted morandi tones so a
   row of materials reads as a tidy garment-label palette. */
.wd-mat-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: var(--color-soft-sage-mist);
  color: var(--color-soft-sage-deep);
  padding: 5px 11px;
  border-radius: var(--radius-soft-pill);
  font-size: 12px;
  font-weight: 600;
  letter-spacing: -0.01em;
}
.wd-mat-pill:nth-child(2n)   { background: var(--color-soft-dusty-wash); color: var(--color-soft-ink); }
.wd-mat-pill:nth-child(3n)   { background: #eadfc7; color: #6b5b3a; }
.wd-mat-pill:nth-child(4n)   { background: #d9e2d5; color: var(--color-soft-sage-deep); }

.wd-mat-pill__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  line-height: 0;
}

.wd-mat-pill__label {
  white-space: nowrap;
}
</style>
