import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Consultation from '../views/Consultation.vue'
import Diagnosis from '../views/Diagnosis.vue'
import Prescription from '../views/Prescription.vue'
import Knowledge from '../views/Knowledge.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/consultation',
    name: 'Consultation',
    component: Consultation
  },
  {
    path: '/diagnosis',
    name: 'Diagnosis',
    component: Diagnosis
  },
  {
    path: '/prescription',
    name: 'Prescription',
    component: Prescription
  },
  {
    path: '/knowledge',
    name: 'Knowledge',
    component: Knowledge
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router