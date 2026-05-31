import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import axios from 'axios'

import App from './App.vue'
import router from './router'

if (import.meta.env.PROD) {
  // 正式環境
  axios.defaults.baseURL = 'https://class-lunch-ordering-system.onrender.com'
} else {
  // 開發環境
  axios.defaults.baseURL = ''
}

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
