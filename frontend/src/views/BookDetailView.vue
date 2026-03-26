<template>
  <div class="book-detail">
    <el-container>
      <el-main>
        <div class="book-detail-header">
          <el-button type="default" @click="router.push('/books')">
            <el-icon><ArrowLeft /></el-icon>
            返回图书列表
          </el-button>
          <h2>图书详情</h2>
        </div>
        <el-row :gutter="20" v-if="book">
          <el-col :span="8">
            <el-card shadow="hover">
              <img :src="'http://localhost:8000' + book.cover_image" class="book-cover" v-if="book.cover_image" />
              <div v-else class="no-cover">
                <el-icon><Picture /></el-icon>
                <p>暂无封面</p>
              </div>
            </el-card>
          </el-col>
          <el-col :span="16">
            <el-card shadow="hover">
              <h3>{{ book.title }}</h3>
              <div class="book-info">
                <p><strong>作者：</strong>{{ book.author }}</p>
                <p><strong>出版社：</strong>{{ book.publisher || '未知' }}</p>
                <p><strong>ISBN：</strong>{{ book.isbn || '未知' }}</p>
                <p><strong>出版日期：</strong>{{ book.publish_date ? formatDate(book.publish_date) : '未知' }}</p>
                <p><strong>分类：</strong>{{ book.category || '未知' }}</p>
                <p><strong>总册数：</strong>{{ book.total_copies }}</p>
                <p><strong>可借册数：</strong>{{ book.available_copies }}</p>
                <p><strong>存放位置：</strong>{{ book.location || '未知' }}</p>
                <p><strong>状态：</strong>{{ getStatusText(book.status) }}</p>
              </div>
              <div class="book-description">
                <h4>图书简介</h4>
                <p>{{ book.description || '暂无简介' }}</p>
              </div>
              <el-button type="primary" @click="borrowBook" :disabled="book.available_copies <= 0">
                借阅
              </el-button>
            </el-card>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ArrowLeft, Picture } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const router = useRouter()
const route = useRoute()

const book = ref(null)

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString()
}

const getStatusText = (status) => {
  const statusUpper = status.toUpperCase()
  switch (statusUpper) {
    case 'AVAILABLE': return '可借阅'
    case 'BORROWED': return '已借出'
    case 'RESERVED': return '已预约'
    case 'DAMAGED': return '损坏'
    case 'LOST': return '丢失'
    default: return status
  }
}

const borrowBook = async () => {
  try {
    const response = await axios.post('/api/borrow/borrow', {
      book_id: book.value.id
    })
    ElMessage.success('借阅成功')
    // 重新获取图书详情，更新可借册数和状态
    fetchBookDetail()
  } catch (error) {
    console.error('借阅失败:', error)
    ElMessage.error('借阅失败：' + (error.response?.data?.detail || '请检查网络连接'))
  }
}

const fetchBookDetail = async () => {
  const bookId = route.params.id
  try {
    const response = await axios.get(`/api/books/${bookId}`)
    book.value = response.data
  } catch (error) {
    console.error('获取图书详情失败:', error)
  }
}

onMounted(() => {
  fetchBookDetail()
})
</script>

<style scoped>
.book-detail {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 20px 0;
}

.book-detail-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 30px;
}

.book-detail-header h2 {
  margin: 0;
  color: #303133;
}

.book-cover {
  width: 100%;
  height: 300px;
  object-fit: contain;
  background: #f0f0f0;
}

.no-cover {
  width: 100%;
  height: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #f0f0f0;
  color: #909399;
}

.no-cover el-icon {
  font-size: 48px;
  margin-bottom: 10px;
}

.book-info {
  margin: 20px 0;
  line-height: 1.8;
}

.book-description {
  margin: 20px 0;
}

.book-description h4 {
  margin: 0 0 10px 0;
  color: #303133;
}

.book-description p {
  line-height: 1.6;
  color: #606266;
}
</style>
