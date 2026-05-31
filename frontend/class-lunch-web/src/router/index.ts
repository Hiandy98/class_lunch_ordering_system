import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import StoreView from '@/views/StoresView.vue'
import MenuView from '@/views/MenuView.vue'
import AccountView from '@/views/AccountView.vue'
import OrdersView from '@/views/OrdersView.vue'
import CreateView from '@/views/CreateView.vue'
import axios from 'axios'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: "/login",
      name: "login",
      component: LoginView,
    },
    {
      path: "/stores",
      name: "stores",
      component: StoreView,
      meta: { requiresAuth: true },
    },
    {
      path: "/menu",
      name: "menu",
      component: MenuView,
      meta: { requiresAuth: true },
    },
    {
      path: "/user",
      name: "user",
      component: AccountView,
      meta: { requiresAuth: true },
    },
    {
      path: "/order",
      name: "order",
      component: OrdersView,
      meta: { requiresAuth: true },
    },
    {
      path: "/create",
      name: "create",
      component: CreateView,
      meta: { requiresAuth: true },
    },
  ],
})

router.beforeEach(async (to, from) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  if (!requiresAuth) {
    return true;
  }

  try {
    await axios.get('/api/v1/auth/verify', { withCredentials: true });
    return true;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.error('JWT 驗證失敗:', error.response?.data?.detail || '請先登入');
    }
     return { name: 'login' };
  }
})



export default router
