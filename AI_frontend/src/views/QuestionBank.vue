<template>
  <div class="question-bank">
    <div class="header">
      <h2>题库管理</h2>
      <div class="nav-buttons">
        <router-link to="/users" class="btn-secondary">返回用户管理</router-link>
      </div>
    </div>
    
    <!-- 创建题目表单 -->
    <div class="create-question">
      <h3>创建新题目</h3>
      <form @submit.prevent="createQuestion">
        <div class="form-group">
          <label>主题：</label>
          <input v-model="newQuestion.topic" required maxlength="100">
        </div>
        <div class="form-group">
          <label>内容：</label>
          <textarea v-model="newQuestion.content" required></textarea>
        </div>
        <button type="submit" class="btn-primary">创建题目</button>
      </form>
    </div>

    <!-- 题目列表 -->
    <div class="questions-list">
      <h3>题目列表</h3>
      <div v-if="loading">加载中...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else>
        <div v-for="question in questions" :key="question.id" class="question-card">
          <div class="question-header">
            <h4>{{ question.topic }}</h4>
            <div class="question-actions">
              <button @click="editQuestion(question)" class="btn-edit">编辑</button>
              <button @click="deleteQuestion(question.id)" class="btn-delete">删除</button>
            </div>
          </div>
          <p class="question-content">{{ question.content }}</p>
          <div class="question-footer">
            <span>创建时间：{{ formatDate(question.created_at) }}</span>
            <span>更新时间：{{ formatDate(question.updated_at) }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 编辑题目对话框 -->
    <div v-if="showEditDialog" class="edit-dialog">
      <div class="dialog-content">
        <h3>编辑题目</h3>
        <form @submit.prevent="updateQuestion">
          <div class="form-group">
            <label>主题：</label>
            <input v-model="editingQuestion.topic" required maxlength="100">
          </div>
          <div class="form-group">
            <label>内容：</label>
            <textarea v-model="editingQuestion.content" required></textarea>
          </div>
          <div class="dialog-actions">
            <button type="submit" class="btn-primary">保存</button>
            <button type="button" @click="showEditDialog = false" class="btn-secondary">取消</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'QuestionBank',
  data() {
    return {
      questions: [],
      loading: false,
      error: null,
      newQuestion: {
        topic: '',
        content: ''
      },
      showEditDialog: false,
      editingQuestion: null
    };
  },
  created() {
    this.fetchQuestions();
  },
  methods: {
    async fetchQuestions() {
      this.loading = true;
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://localhost:5000/questions', {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.questions = response.data;
      } catch (error) {
        this.error = error.response?.data?.message || '获取题目失败';
      } finally {
        this.loading = false;
      }
    },
    async createQuestion() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.post('http://localhost:5000/questions', this.newQuestion, {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.questions.unshift(response.data.question);
        this.newQuestion = { topic: '', content: '' };
      } catch (error) {
        this.error = error.response?.data?.message || '创建题目失败';
      }
    },
    editQuestion(question) {
      this.editingQuestion = { ...question };
      this.showEditDialog = true;
    },
    async updateQuestion() {
      try {
        const token = localStorage.getItem('token');
        await axios.put(`http://localhost:5000/questions/${this.editingQuestion.id}`, this.editingQuestion, {
          headers: { Authorization: `Bearer ${token}` }
        });
        const index = this.questions.findIndex(q => q.id === this.editingQuestion.id);
        if (index !== -1) {
          this.questions[index] = { ...this.editingQuestion };
        }
        this.showEditDialog = false;
      } catch (error) {
        this.error = error.response?.data?.message || '更新题目失败';
      }
    },
    async deleteQuestion(id) {
      if (!confirm('确定要删除这道题目吗？')) return;
      
      try {
        const token = localStorage.getItem('token');
        await axios.delete(`http://localhost:5000/questions/${id}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.questions = this.questions.filter(q => q.id !== id);
      } catch (error) {
        this.error = error.response?.data?.message || '删除题目失败';
      }
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleString('zh-CN');
    }
  }
};
</script>

<style scoped>
.question-bank {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.nav-buttons {
  display: flex;
  gap: 10px;
}

.btn-secondary {
  background: #666;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
}

.btn-secondary:hover {
  background: #555;
}

.create-question {
  background: #f5f5f5;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.form-group textarea {
  min-height: 100px;
}

.question-card {
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.question-actions {
  display: flex;
  gap: 10px;
}

.question-content {
  margin: 10px 0;
  line-height: 1.5;
}

.question-footer {
  display: flex;
  justify-content: space-between;
  color: #666;
  font-size: 0.9em;
}

.btn-primary {
  background: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
}

.btn-edit {
  background: #2196F3;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}

.btn-delete {
  background: #f44336;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}

.edit-dialog {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.dialog-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.error {
  color: #f44336;
  padding: 10px;
  background: #ffebee;
  border-radius: 4px;
  margin: 10px 0;
}
</style> 