import { createApp } from 'vue'
import { MotionPlugin } from '@vueuse/motion'
import Vue3Lottie from 'vue3-lottie'
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import './style.css'
import App from './App.vue'
import router from './router'

// Register GSAP plugins once at app boot so any view that imports gsap can
// rely on ScrollTrigger being available.
gsap.registerPlugin(ScrollTrigger)

createApp(App)
  .use(router)
  .use(MotionPlugin)
  .use(Vue3Lottie)
  .mount('#app')
