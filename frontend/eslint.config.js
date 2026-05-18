// ESLint flat config — opt-in linting for the Vue 3 frontend.
//
// Activation: `npm run lint`. This config is NOT wired into `vite build`,
// so production builds are unaffected. Rules deliberately use "warn" rather
// than "error" so the lint command surfaces issues without breaking CI or
// pre-commit on first introduction.

import js from '@eslint/js'
import pluginVue from 'eslint-plugin-vue'
import globals from 'globals'

export default [
  {
    ignores: [
      'dist/**',
      'node_modules/**',
      'public/version1/**',
      'public/version2/**',
      '.vite/**',
    ],
  },
  js.configs.recommended,
  ...pluginVue.configs['flat/essential'],
  {
    files: ['**/*.{js,vue}'],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'module',
      globals: {
        ...globals.browser,
        ...globals.node,
      },
    },
    rules: {
      // Soft introduction — warn everywhere, error nowhere
      'no-unused-vars': ['warn', { argsIgnorePattern: '^_', varsIgnorePattern: '^_' }],
      'no-undef': 'warn',
      'no-empty': ['warn', { allowEmptyCatch: true }],
      'no-prototype-builtins': 'warn',

      // Vue-specific noise we don't want surfaced on a first pass
      'vue/multi-word-component-names': 'off',
      'vue/no-v-html': 'off', // documented as safe in comments next to each usage
      'vue/require-default-prop': 'off',
    },
  },
]
