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
  
  // 管理员登录
  adminLogin: async (loginData) => {
    const response = await api.post('/api/auth/admin/login', loginData)
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

export const userApi = {
  // 获取用户个人信息
  getProfile: async () => {
    const response = await api.get('/api/users/profile')
    return response.data
  },
  
  // 修改用户名
  updateUsername: async (username) => {
    const response = await api.put('/api/users/profile/username', { username })
    return response.data
  },
  
  // 修改密码
  updatePassword: async (oldPassword, newPassword) => {
    const response = await api.put('/api/users/profile/password', {
      old_password: oldPassword,
      new_password: newPassword
    })
    return response.data
  },
  
  // 上传头像
  uploadAvatar: async (file) => {
    const formData = new FormData()
    formData.append('file', file)
    const response = await api.post('/api/users/profile/avatar', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  }
}

export const bookApi = {
  // 获取所有图书
  getAllBooks: async () => {
    const response = await api.get('/api/admin/books')
    return response.data
  },
  
  // 添加图书
  addBook: async (bookData) => {
    const response = await api.post('/api/admin/books', bookData)
    return response.data
  },
  
  // 编辑图书
  updateBook: async (bookId, bookData) => {
    const response = await api.put(`/api/admin/books/${bookId}`, bookData)
    return response.data
  },
  
  // 删除图书
  deleteBook: async (bookId) => {
    const response = await api.delete(`/api/admin/books/${bookId}`)
    return response.data
  },
  
  // 上传图书封面
  uploadCover: async (bookId, file) => {
    const formData = new FormData()
    formData.append('file', file)
    const response = await api.post(`/api/admin/books/${bookId}/cover`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  }
}

export default api