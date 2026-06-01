import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import axios from 'axios'

import App from './App.vue'
import router from './router'

axios.defaults.withCredentials = true

if (import.meta.env.PROD) {
  // 正式環境
  axios.defaults.baseURL = 'https://class-lunch-ordering-system.onrender.com'
} else {
  // 開發環境
  axios.defaults.baseURL = ''
}

const isIOS = () => {
  return /iPad|iPhone|iPod/.test(navigator.userAgent) || 
         (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
}
// IOS的處理 我討厭IOS!!!!!!
axios.interceptors.request.use((config) => {
  if (isIOS()) {
    const iosToken = localStorage.getItem('ios_token')
    if (iosToken) {
      config.headers.Authorization = `Bearer ${iosToken}`
    }
  }
  return config
}, (error) => {
  return Promise.reject(error)
})


const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
