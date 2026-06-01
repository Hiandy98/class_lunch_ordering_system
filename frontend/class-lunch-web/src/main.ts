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

// IOS 自動從 LocalStorage 恢復 Cookie 的機制 ... 我討厭IOS!!!!!!
if (isIOS()) {
  const iosToken = localStorage.getItem('ios_token')
  // 如果 LocalStorage 有 Token，且目前 Cookie 裡找不到 access_token
  if (iosToken && !document.cookie.includes('access_token')) {
    // 強制在前端寫入 Cookie，過期時間設定 14 天，確保跨域請求能帶上
    document.cookie = `access_token=${iosToken}; path=/; max-age=${14 * 86400}; SameSite=None; Secure`;
  }
}

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
