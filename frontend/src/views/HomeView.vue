<template>
  <div class="home">
    <el-container>
      <el-header height="80px" class="header">
        <div class="logo">图书借阅系统</div>
        <el-menu :default-active="activeIndex" class="menu" mode="horizontal">
          <el-menu-item index="1">
            <router-link to="/">首页</router-link>
          </el-menu-item>
          <el-menu-item index="2">
            <router-link to="/books">图书</router-link>
          </el-menu-item>
          <el-menu-item index="3">
            <router-link to="/borrow">借阅</router-link>
          </el-menu-item>
          <el-menu-item index="4">
            <router-link to="/profile">个人中心</router-link>
          </el-menu-item>
          <el-menu-item index="5" v-if="!isLoggedIn">
            <router-link to="/login">登录</router-link>
          </el-menu-item>
          <el-menu-item index="6" v-if="!isLoggedIn">
            <router-link to="/register">注册</router-link>
          </el-menu-item>
        </el-menu>
      </el-header>
      <el-main>
        <div class="hero">
          <h1>基于人脸识别的图书借阅系统</h1>
          <p>便捷、高效的图书管理与借阅体验</p>
          <el-button type="primary" size="large" @click="goToBooks">浏览图书</el-button>
        </div>
        <div class="features">
          <el-row :gutter="20">
            <el-col :span="8">
              <el-card shadow="hover">
                <template #header>
                  <div class="card-header">
                    <span>人脸识别</span>
                  </div>
                </template>
                <p>快速身份核验，无需携带证件</p>
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card shadow="hover">
                <template #header>
                  <div class="card-header">
                    <span>智能借阅</span>
                  </div>
                </template>
                <p>线上预约，线下快速借阅</p>
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card shadow="hover">
                <template #header>
                  <div class="card-header">
                    <span>逾期提醒</span>
                  </div>
                </template>
                <p>智能提醒，避免逾期罚款</p>
              </el-card>
            </el-col>
          </el-row>
        </div>
      </el-main>
      <el-footer height="60px" class="footer">
        <p>© 2026 图书借阅系统 - 基于人脸识别技术</p>
      </el-footer>
    </el-container>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const activeIndex = ref('1')
const isLoggedIn = ref(false)

const goToBooks = () => {
  router.push('/books')
}
</script>

<style scoped>
.home {
  min-height: 100vh;
}

.header {
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
}

.logo {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
}

.menu {
  border: none;
}

.hero {
  text-align: center;
  padding: 80px 0;
  background: linear-gradient(135deg, #409EFF 0%, #69c0ff 100%);
  color: white;
  margin-bottom: 40px;
}

.hero h1 {
  font-size: 48px;
  margin-bottom: 20px;
}

.hero p {
  font-size: 20px;
  margin-bottom: 40px;
}

.features {
  padding: 40px 0;
}

.card-header {
  font-weight: bold;
  font-size: 16px;
}

.footer {
  background: #f5f7fa;
  text-align: center;
  line-height: 60px;
  color: #909399;
}
</style>
