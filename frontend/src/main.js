import { createApp } from 'vue'
import Vue3Lottie from 'vue3-lottie'
import './style.css'
import './styles/tour.css'
import App from './App.vue'
import router from './router'
import { ensurePlugins } from './motion'

// Single point of GSAP plugin registration. Later phases extend
// ensurePlugins() to include Flip, Draggable, and InertiaPlugin — call
// sites stay unchanged.
ensurePlugins()

createApp(App)
  .use(router)
  .use(Vue3Lottie)
  .mount('#app')
