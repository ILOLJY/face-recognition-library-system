import { createRouter, createWebHistory } from 'vue-router'
import { authApi } from '../api/index.js'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('../views/HomeView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/LoginView.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/RegisterView.vue')
  },
  {
    path: '/books',
    name: 'Books',
    component: () => import('../views/BooksView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/borrow',
    name: 'Borrow',
    component: () => import('../views/BorrowView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/ProfileView.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  // 检查是否需要认证
  if (to.matched.some(record => record.meta.requiresAuth)) {
    console.log('需要认证的页面:', to.path)
    try {
        // 调用 /me 接口检查登录状态
        console.log('调用 /api/auth/me 接口检查登录状态')
        const data = await authApi.getCurrentUser()
        console.log('登录状态检查成功:', data)
        // 登录成功，继续导航
        next()
    } catch (error) {
      console.log('登录状态检查失败:', error.response?.status || error.message)
      // 登录失败，跳转到登录页面
      next('/login')
    }
  } else {
    // 不需要认证的页面，直接导航
    next()
  }
})

export default router
