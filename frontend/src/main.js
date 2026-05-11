import { createApp } from 'vue'
import { MotionPlugin } from '@vueuse/motion'
import Vue3Lottie from 'vue3-lottie'
import './style.css'
import App from './App.vue'
import router from './router'
import { ensurePlugins } from './motion'

// Single point of GSAP plugin registration. Later phases extend
// ensurePlugins() to include SplitText, ScrollSmoother, Flip, Draggable,
// and InertiaPlugin — call sites stay unchanged.
ensurePlugins()

createApp(App)
  .use(router)
  .use(MotionPlugin)
  .use(Vue3Lottie)
  .mount('#app')
