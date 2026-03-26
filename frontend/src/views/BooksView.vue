<template>
  <div class="books">
    <el-container>
      <el-main>
        <div class="books-header">
          <div style="display: flex; align-items: center; gap: 20px;">
            <el-button type="default" @click="router.push('/home')">
              <el-icon><ArrowLeft /></el-icon>
              返回主页
            </el-button>
            <h2>{{ isSearching ? '搜索结果' : '最近借阅' }}</h2>
          </div>
          <div style="display: flex; align-items: center; gap: 10px;">
            <el-input
              v-model="searchQuery"
              placeholder="搜索图书"
              prefix-icon="el-icon-search"
              style="width: 300px"
              @keyup.enter="searchBooks"
            >
              <template #append>
                <el-button @click="searchBooks">搜索</el-button>
              </template>
            </el-input>
            <el-button v-if="isSearching" @click="resetSearch">重置</el-button>
          </div>
        </div>
        <el-row :gutter="20">
          <el-col :span="6" v-for="book in books" :key="book.id">
            <el-card shadow="hover" class="book-card" @click="goToBookDetail(book.id)">
              <img :src="'http://localhost:8000' + book.cover_image" class="book-cover" v-if="book.cover_image" />
              <div class="book-info">
                <h3>{{ book.title }}</h3>
                <p class="author">作者：{{ book.author }}</p>
                <p class="publisher">出版社：{{ book.publisher || '未知' }}</p>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'
import { bookApi } from '../api/index.js'

const router = useRouter()

const books = ref([])
const searchQuery = ref('')
const isSearching = ref(false)

const goToBookDetail = (bookId) => {
  router.push(`/book/${bookId}`)
}

const searchBooks = async () => {
  if (!searchQuery.value.trim()) {
    return
  }
  
  try {
    isSearching.value = true
    const data = await bookApi.searchBooks(searchQuery.value)
    books.value = data
  } catch (error) {
    console.error('搜索图书失败:', error)
  }
}

const resetSearch = () => {
  searchQuery.value = ''
  isSearching.value = false
  fetchRecentBooks()
}

const fetchRecentBooks = async () => {
  try {
    const data = await bookApi.getRecentBooks()
    books.value = data
  } catch (error) {
    console.error('获取最近借阅图书失败:', error)
  }
}

onMounted(() => {
  fetchRecentBooks()
})
</script>

<style scoped>
.books {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 20px 0;
}

.books-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.books-header h2 {
  margin: 0;
  color: #303133;
}

.book-card {
  min-height: 300px;
  display: flex;
  flex-direction: column;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.book-card:hover {
  transform: translateY(-5px);
}

.book-cover {
  width: 100%;
  height: 180px;
  object-fit: contain;
  margin-bottom: 15px;
  background: #f0f0f0;
}

.book-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.book-info h3 {
  margin: 0 0 10px 0;
  font-size: 16px;
  color: #303133;
}

.author, .publisher {
  font-size: 14px;
  color: #606266;
  margin: 5px 0;
}

.status {
  font-size: 12px;
  margin: 10px 0;
  padding: 2px 8px;
  border-radius: 10px;
  display: inline-block;
}

.status.available {
  background: #f0f9eb;
  color: #67c23a;
}

.status.borrowed {
  background: #fef0f0;
  color: #f56c6c;
}

.book-info .el-button {
  margin-top: auto;
  align-self: flex-start;
}
</style>
