import axios from 'axios'

// 创建 axios 实例
const api = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true // 携带 cookie
})

// 接口封装
export const authApi = {
  // 发送验证码
  sendVerificationCode: async (email) => {
    const response = await api.post('/api/auth/send-code/register', { email })
    return response.data
  },
  
  // 注册
  register: async (userData) => {
    const response = await api.post('/api/auth/register', userData)
    return response.data
  },
  
  // 登录
  login: async (loginData) => {
    const response = await api.post('/api/auth/login', loginData)
    return response.data
  },
  
  // 获取当前用户信息（登录验证）
  getCurrentUser: async () => {
    const response = await api.get('/api/auth/me')
    return response.data
  },
  
  // 注销登录
  logout: async () => {
    const response = await api.post('/api/auth/logout')
    return response.data
  }
}

export default api