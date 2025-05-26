<template>
  <div class="page-container">
    <div class="card">
      <div class="card-header">
        <h2 class="title">欢迎回来</h2>
        <p class="subtitle">请登录您的账号</p>
      </div>
      <form @submit.prevent="login" class="login-form">
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
        <button type="submit" class="btn" :class="{ 'loading': isLoading }">
          <span v-if="!isLoading">登录</span>
          <span v-else class="loading-spinner"></span>
        </button>
        <router-link to="/register" class="link">还没有账号？立即注册</router-link>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import '../assets/common.css'

export default {
    data(){
        return {
            username:'',
            password:'',
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
        async login() {
            this.isLoading = true;
            try {
                const response = await axios.post('http://localhost:5000/login', {
                    username: this.username,
                    password: this.password
                })
                
                localStorage.setItem('token', response.data.token)
                localStorage.setItem('userIdentity', response.data.identity)
                
                // 根据身份跳转到不同页面
                if (response.data.identity === 'officer') {
                    this.$router.push('/users')
                } else {
                    this.$router.push('/student-profile')
                }
            } catch (error) {
                this.error = error.response?.data?.message || '登录失败'
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

.login-form {
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

input {
  width: 100%;
  padding: 12px 12px 12px 40px;
  border: 2px solid #e1e1e1;
  border-radius: 8px;
  font-size: 16px;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.9);
}

input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
}

input.focused {
  border-color: var(--primary-color);
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
  box-shadow: 0 4px 12px rgba(58, 206, 98, 0.2);
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