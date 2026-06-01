import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import axios from 'axios'

import App from './App.vue'
import router from './router'

axios.defaults.withCredentials = true
axios.defaults.baseURL = 'https://class-lunch-ordering-system.onrender.com'

// 我討厭IOS!!!!....
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem('user_token')
  
  if (token) {
    config.withCredentials = false
    config.headers.Authorization = `Bearer ${token}`
  }
  
  return config
}, (error) => {
  return Promise.reject(error)
})

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
