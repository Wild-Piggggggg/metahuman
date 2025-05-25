<template>
  <div class="page-container">
    <div class="card">
      <div class="card-header">
        <h2 class="title">创建账号</h2>
        <p class="subtitle">加入我们的社区</p>
      </div>
      <form @submit.prevent="register" class="register-form">
        <div class="form-group">
          <div class="input-wrapper">
            <input 
              v-model="username" 
              placeholder="用户名" 
              required 
              @focus="handleFocus('username')"
              @blur="handleBlur('username')"
              :class="{ 'focused': focusedField === 'username' }"
            />
            <span class="input-icon">👤</span>
          </div>
        </div>
        <div class="form-group">
          <div class="input-wrapper">
            <input 
              v-model="password" 
              type="password" 
              placeholder="密码" 
              required 
              @focus="handleFocus('password')"
              @blur="handleBlur('password')"
              :class="{ 'focused': focusedField === 'password' }"
            />
            <span class="input-icon">🔒</span>
          </div>
        </div>
        <div class="form-group">
          <div class="input-wrapper">
            <select 
              v-model="identity" 
              required
              @focus="handleFocus('identity')"
              @blur="handleBlur('identity')"
              :class="{ 'focused': focusedField === 'identity' }"
            >
              <option value="" disabled>请选择身份</option>
              <option value="student">学生</option>
              <option value="officer">管理员</option>
            </select>
            <span class="input-icon">👥</span>
          </div>
        </div>
        <div class="form-group" v-if="identity === 'student'">
          <div class="input-wrapper">
            <input 
              v-model="score" 
              type="number" 
              step="0.1" 
              placeholder="分数" 
              @focus="handleFocus('score')"
              @blur="handleBlur('score')"
              :class="{ 'focused': focusedField === 'score' }"
            />
            <span class="input-icon">📊</span>
          </div>
        </div>
        <div class="form-group" v-if="identity === 'officer'">
          <div class="input-wrapper">
            <input 
              v-model="major" 
              placeholder="专业" 
              @focus="handleFocus('major')"
              @blur="handleBlur('major')"
              :class="{ 'focused': focusedField === 'major' }"
            />
            <span class="input-icon">🎓</span>
          </div>
        </div>
        <button type="submit" class="btn" :class="{ 'loading': isLoading }">
          <span v-if="!isLoading">注册</span>
          <span v-else class="loading-spinner"></span>
        </button>
        <router-link to="/" class="link">返回登录</router-link>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import '../assets/common.css'

export default {
  data() {
    return {
      username: '',
      password: '',
      identity: '',
      score: 0,
      major: '计算机科学',
      focusedField: '',
      isLoading: false
    }
  },
  methods: {
    handleFocus(field) {
      this.focusedField = field;
    },
    handleBlur(field) {
      if (this.focusedField === field) {
        this.focusedField = '';
      }
    },
    resetFields() {
      this.score = '';
      this.major = '';
    },
    async register() {
      this.isLoading = true;
      try {
        const payload = {
          username: this.username,
          password: this.password,
          identity: this.identity
        };
        if (this.identity === 'student') {
          payload.score = this.score;
        } else if (this.identity === 'officer') {
          payload.major = this.major;
        }
        await axios.post('http://localhost:5000/register', payload);
        this.resetFields();
        this.$router.push('/');
      } catch (error) {
        alert('注册失败: ' + (error.response?.data?.message || '未知错误'))
      } finally {
        this.isLoading = false;
      }
    }
  }
}
</script>

<style scoped>
.card-header {
  text-align: center;
  margin-bottom: 30px;
}

.title {
  font-size: 28px;
  color: #333;
  margin-bottom: 8px;
  font-weight: 600;
}

.subtitle {
  color: #666;
  font-size: 16px;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 12px;
  color: #666;
  font-size: 18px;
}

input, select {
  width: 100%;
  padding: 12px 12px 12px 40px;
  border: 2px solid #e1e1e1;
  border-radius: 8px;
  font-size: 16px;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.9);
}

input:focus, select:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
}

input.focused, select.focused {
  border-color: var(--primary-color);
}

select {
  appearance: none;
  cursor: pointer;
  padding-right: 40px;
}

select::-ms-expand {
  display: none;
}

.btn {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, var(--primary-color), var(--primary-hover));
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.2);
}

.btn.loading {
  cursor: not-allowed;
  opacity: 0.8;
}

.loading-spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.link {
  display: block;
  text-align: center;
  margin-top: 10px;
  color: var(--secondary-color);
  text-decoration: none;
  font-size: 14px;
  transition: all 0.3s ease;
}

.link:hover {
  color: var(--primary-color);
  text-decoration: underline;
}
</style>