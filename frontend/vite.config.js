import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

const basePath = process.env.VITE_BASE_PATH || '/'
console.log('[vite.config] VITE_BASE_PATH =', JSON.stringify(process.env.VITE_BASE_PATH))
console.log('[vite.config] resolved base =', JSON.stringify(basePath))

export default defineConfig({
  base: basePath,
  plugins: [tailwindcss(), vue()],
})
