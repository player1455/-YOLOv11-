import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../store/modules/auth'
import Home from '../views/Home.vue'
import Flying from '../views/Flying.vue'
import Login from '../views/Login.vue'
import ControlDrone from '../views/ControlDrone.vue'
import ControlUser from '../views/ControlUser.vue'
import Analyze from '../views/Analyze.vue'
import Map from '../views/Map.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/flying',
    name: 'Flying',
    component: Flying,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/control/drone',
    name: 'ControlDrone',
    component: ControlDrone,
    meta: { requiresAuth: true, requiresRole: 'admin' }
  },
  {
    path: '/control/user',
    name: 'ControlUser',
    component: ControlUser,
    meta: { requiresAuth: true, requiresRole: 'admin' }
  },
  {
    path: '/analyze',
    name: 'Analyze',
    component: Analyze,
    meta: { requiresAuth: true }
  },
  {
    path: '/map',
    name: 'Map',
    component: Map,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.path === '/login') {
    if (authStore.isLoggedIn) {
      next('/')
    } else {
      next()
    }
    return
  }

  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    next('/login')
    return
  }

  if (to.meta.requiresRole && to.meta.requiresRole !== authStore.userRole) {
    next('/')
    return
  }

  next()
})

export default router
