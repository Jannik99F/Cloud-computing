import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import AboutView from '@/views/AboutView.vue'
import ProductCatalog from '@/views/ProductCatalog.vue'
import ProductDetails from '@/views/ProductDetails.vue'
import BasketView from '@/views/BasketView.vue'
import RegisterView from '@/views/RegisterView.vue'
import LoginView from '@/views/LoginView.vue'
import LogoutView from '@/views/LogoutView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView,
    },
    {
      path: '/catalog',
      name: 'catalog',
      component: ProductCatalog,
    },
    {
      path: '/catalog/:id',
      name: 'product',
      component: ProductDetails,
    },
    {
      path: '/basket',
      name: 'basket',
      component: BasketView,
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/logout',
      name: 'logout',
      component: LogoutView,
    },
  ],
})

export default router
