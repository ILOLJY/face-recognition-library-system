import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import router from './router'
import './style.css'
import App from './App.vue'
import axios from 'axios'

// 配置 axios 全局设置
axios.defaults.withCredentials = true // 携带 cookie
axios.defaults.baseURL = 'http://localhost:8000' // 设置基础 URL

// 请求拦截器
axios.interceptors.request.use(
  config => {
    // 不再从 cookie 中读取 token，而是让浏览器自动携带 cookie
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

const app = createApp(App)
app.use(createPinia())
app.use(ElementPlus)
app.use(router)
app.mount('#app')
