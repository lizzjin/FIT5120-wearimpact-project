import { createApp } from 'vue'
import { MotionPlugin } from '@vueuse/motion'
import Vue3Lottie from 'vue3-lottie'
import './style.css'
import App from './App.vue'
import router from './router'

createApp(App)
  .use(router)
  .use(MotionPlugin)
  .use(Vue3Lottie)
  .mount('#app')
