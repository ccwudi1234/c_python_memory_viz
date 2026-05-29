import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import PythonAnalysis from '../views/PythonAnalysis.vue'
import CAnalysis from '../views/CAnalysis.vue'
import Examples from '../views/Examples.vue'
import UserCenter from '../views/UserCenter.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/analyze/python',
    name: 'PythonAnalysis',
    component: PythonAnalysis
  },
  {
    path: '/analyze/c',
    name: 'CAnalysis',
    component: CAnalysis
  },
  {
    path: '/examples',
    name: 'Examples',
    component: Examples
  },
  {
    path: '/user-center',
    name: 'UserCenter',
    component: UserCenter
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
