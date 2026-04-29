import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import EcoShopView from '../views/EcoShopView.vue'
import KnowledgeView from '../views/KnowledgeView.vue'
import BrandSearchView from '../views/BrandSearchView.vue'
import WardrobeView from '../views/WardrobeView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/eco-shop',
    name: 'ecoShop',
    component: EcoShopView
  },
  {
    path: '/knowledge',
    name: 'knowledge',
    component: KnowledgeView
  },
  {
    path: '/brand-search',
    name: 'brandSearch',
    component: BrandSearchView
  },
  {
    path: '/wardrobe',
    name: 'wardrobe',
    component: WardrobeView
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
