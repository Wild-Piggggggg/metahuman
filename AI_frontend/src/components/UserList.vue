<template>
  <div class="page-container">
    <div class="card admin-card">
      <div class="header">
        <h2 class="title">用户管理</h2>
        <div class="nav-buttons">
          <router-link to="/question-bank" class="btn-primary">题库管理</router-link>
        </div>
        <button @click="logout" class="btn btn-secondary">退出登录</button>
      </div>
      
      <div v-if="isLoading" class="loading">
        加载中...
      </div>
      
      <div v-else class="table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>用户名</th>
              <th>身份</th>
              <th>分数/专业</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.id }}</td>
              <td>{{ user.username }}</td>
              <td>{{ user.identity === 'student' ? '学生' : '管理员' }}</td>
              <td>
                {{ user.identity === 'student' ? (user.score ?? 'N/A') : (user.major ?? 'N/A') }}
              </td>
              <td>
                <button @click="deleteUser(user.id)" class="btn-delete">删除</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import '../assets/common.css'

export default {
  data() {
    return {
      users: [],
      isLoading: false
    }
  },
  async created() {
    await this.fetchUsers()
  },
  methods: {
    async fetchUsers() {
      this.isLoading = true
      try {
        const token = localStorage.getItem('token')
        const response = await axios.get('http://localhost:5000/users', {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.users = response.data
      } catch(error) {
        console.error('获取用户列表失败:', error.response?.data)
        this.$router.push('/')
      } finally {
        this.isLoading = false
      }
    },
    async deleteUser(id) {
      if (!confirm('确定要删除这个用户吗？')) {
        return
      }
      
      try {
        const token = localStorage.getItem('token')
        await axios.delete(`http://localhost:5000/user/${id}`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        await this.fetchUsers()
      } catch (error) {
        console.error('删除用户失败:', error.response?.data)
        alert('删除失败: ' + (error.response?.data?.message || '未知错误'))
      }
    },
    logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('userId')
      localStorage.removeItem('userIdentity')
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.admin-card {
  max-width: 900px;
  width: 100%;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.header .btn {
  width: auto;
  padding: 8px 20px;
}

.nav-buttons {
  display: flex;
  gap: 10px;
}

.btn-primary {
  background: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
}

.btn-primary:hover {
  background: #45a049;
}

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  background: white;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

th {
  background-color: #f8f9fa;
  font-weight: 600;
  color: #333;
}

tr:hover {
  background-color: #f8f9fa;
}

.btn-delete {
  padding: 6px 12px;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-delete:hover {
  background-color: #c82333;
}

.loading {
  text-align: center;
  margin: 30px 0;
  color: #666;
}
</style>