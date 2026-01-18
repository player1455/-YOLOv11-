import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Flying from '../views/Flying.vue'
import Login from '../views/Login.vue'
import ControlDrone from '../views/ControlDrone.vue'
import ControlUser from '../views/ControlUser.vue'
import Analyze from '../views/Analyze.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/flying',
    name: 'Flying',
    component: Flying
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/control/drone',
    name: 'ControlDrone',
    component: ControlDrone
  },
  {
    path: '/control/user',
    name: 'ControlUser',
    component: ControlUser
  },
  {
    path: '/analyze',
    name: 'Analyze',
    component: Analyze
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
