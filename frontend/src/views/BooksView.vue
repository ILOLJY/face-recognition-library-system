<template>
  <div class="books">
    <el-container>
      <el-main>
        <div class="books-header">
          <h2>图书列表</h2>
          <el-input
            v-model="searchQuery"
            placeholder="搜索图书"
            prefix-icon="el-icon-search"
            style="width: 300px"
          ></el-input>
        </div>
        <el-row :gutter="20">
          <el-col :span="6" v-for="book in books" :key="book.id">
            <el-card shadow="hover" class="book-card">
              <img :src="book.cover" class="book-cover" v-if="book.cover" />
              <div class="book-info">
                <h3>{{ book.title }}</h3>
                <p class="author">作者：{{ book.author }}</p>
                <p class="category">分类：{{ book.category }}</p>
                <p class="status" :class="book.status === 'AVAILABLE' ? 'available' : 'borrowed'">
                  {{ book.status === 'AVAILABLE' ? '可借阅' : '已借出' }}
                </p>
                <el-button type="primary" size="small" @click="borrowBook(book)" :disabled="book.status !== 'AVAILABLE'">
                  借阅
                </el-button>
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
import axios from 'axios'

const searchQuery = ref('')
const books = ref([
  {
    id: 1,
    title: 'Python 编程从入门到实践',
    author: 'Eric Matthes',
    category: '计算机',
    status: 'AVAILABLE',
    cover: ''
  },
  {
    id: 2,
    title: '深入理解计算机系统',
    author: 'Randal E. Bryant',
    category: '计算机',
    status: 'BORROWED',
    cover: ''
  },
  {
    id: 3,
    title: '算法导论',
    author: 'Thomas H. Cormen',
    category: '计算机',
    status: 'AVAILABLE',
    cover: ''
  },
  {
    id: 4,
    title: 'JavaScript 高级程序设计',
    author: 'Nicholas C. Zakas',
    category: '计算机',
    status: 'AVAILABLE',
    cover: ''
  }
])

const borrowBook = (book) => {
  console.log('借阅图书:', book)
  // 这里需要实现借阅逻辑
}

onMounted(() => {
  // 这里需要从后端获取图书列表
  // fetchBooks()
})

const fetchBooks = async () => {
  try {
    // const response = await axios.get('/api/books')
    // books.value = response.data
  } catch (error) {
    console.error('获取图书列表失败:', error)
  }
}
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
  height: 300px;
  display: flex;
  flex-direction: column;
}

.book-cover {
  width: 100%;
  height: 150px;
  object-fit: cover;
  margin-bottom: 15px;
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

.author, .category {
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
