import { createApp } from 'vue'
import axios from 'axios'
import { createRouter, createWebHashHistory } from 'vue-router'
import App from './App.vue'

import Login from './components/Login.vue'
import Applicant from './components/Applicant.vue'
import Manager from './components/Manager.vue'
import { ref } from 'vue'
const jobs = ref([
  { name: "Job1", desc:"测试描述测试描述测试描述测试描述" },
  { name: "Job2", desc:"测试描述测试描述测试描述测试描述" },
  { name: "Job3", desc:"测试描述测试描述测试描述测试描述" },
])

axios.defaults.baseURL = import.meta.env.VITE_RESUMEEE_BACKEND_URL
axios.defaults.withCredentials = true

const routes = [
  { path: '/', component: Login },
  { path: '/login', component: Login },
  { path: '/applicant', component: Applicant },
  { path: '/mgr', component: Manager }
]

const router = createRouter({
  // 4. Provide the history implementation to use. We are using the hash history for simplicity here.
  history: createWebHashHistory(),
  routes, // short for `routes: routes`
})

const app = createApp(App).use(router).mount('#app')