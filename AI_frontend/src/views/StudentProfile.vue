<template>
  <div class="profile-page-container">
    <div class="profile-main-grid">
      <section class="profile-panel">
        <h2 class="panel-title">个人信息 (User Profile)</h2>
        <div class="info-grid">
          <div class="info-item">
            <label><i class="fas fa-user icon"></i>用户名：</label>
            <span>{{ userInfo.username || '加载中...' }}</span>
          </div>
          <div class="info-item">
            <label><i class="fas fa-id-badge icon"></i>身份：</label>
            <span>{{ userInfo.identity || '加载中...' }}</span>
          </div>
          <div class="info-item">
            <label><i class="fas fa-star icon"></i>分数：</label>
            <span>{{ userInfo.score !== null ? userInfo.score : '加载中...' }}</span>
          </div>
        </div>

        <h2 class="panel-title camera-title">摄像头预览 (Camera Preview)</h2>
        <Camera />
      </section>
    </div>
  </div>
</template>

<script>
import Camera from '@/components/Camera.vue'

export default {
  name: 'StudentProfile',
  components: {
    Camera
  },
  data() {
    return {
      userInfo: {
        username: '',
        identity: '',
        score: null
      }
    }
  },
  async mounted() {
    await this.fetchUserInfo()
    this.loadFontAwesome();
  },
  methods: {
    loadFontAwesome() {
        if (!document.querySelector('link[href*="font-awesome"]')) {
            const link = document.createElement('link');
            link.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css';
            link.rel = 'stylesheet';
            document.head.appendChild(link);
        }
    },
    async fetchUserInfo() {
      try {
        const token = localStorage.getItem('token')
        const response = await fetch('http://localhost:5000/users', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const users = await response.json()
        const currentUser = users.find(user => user.identity === 'student')
        if (currentUser) {
          this.userInfo = currentUser
        } else {
            console.warn('未找到学生用户。');
            this.userInfo = { username: 'N/A', identity: 'N/A', score: 'N/A' };
        }
      } catch (error) {
        console.error('获取用户信息失败:', error)
        this.userInfo = { username: '获取失败', identity: '获取失败', score: '获取失败' };
      }
    }
  }
}
</script>

<style scoped>
/* 引入示例中的颜色变量 */
:root {
  --primary-gradient: linear-gradient(208.5deg, #7c0378, #e46f00);
  --secondary-gradient: linear-gradient(208.5deg, #e46f00, #7c0378);
  --text-dark: #2d2d2d;
  --text-light: #666;
  --bg-light: #f8f9fa;
  --white: #ffffff;
  --border-radius: 8px;
  --box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 全局页面容器样式 */
.profile-page-container {
  font-family: 'Arial', sans-serif;
  background: var(--bg-light);
  color: var(--text-dark);
  line-height: 1.6;
  min-height: 100vh;
  padding: 2rem 1rem;
  box-sizing: border-box;
}

/* 主网格布局 */
.profile-main-grid {
  max-width: 1600px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}

/* 卡片面板通用样式 */
.profile-panel {
  background: var(--white);
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  padding: 2rem;
}

/* 标题样式 */
.panel-title {
  background: var(--primary-gradient);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  text-align: left;
  margin-bottom: 2rem;
  font-size: 1.75rem;
  font-weight: 700;
  border-bottom: 2px solid #eee;
  padding-bottom: 0.5rem;
}

.camera-title {
    margin-top: 2.5rem;
}

/* 个人信息网格 */
.info-grid {
  display: grid;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.1rem;
  padding: 0.5rem 0;
  border-bottom: 1px solid #f0f0f0;
}

.info-item:last-child {
    border-bottom: none;
}

.info-item label {
  font-weight: 600;
  color: var(--text-light);
  min-width: 100px;
  display: flex;
  align-items: center;
}

.info-item span {
  color: var(--text-dark);
  font-weight: 500;
}

.icon {
  margin-right: 8px;
  color: #7c0378;
  width: 16px;
  text-align: center;
}

/* 调整 Camera 组件样式 */
:deep(.camera-container) {
  margin: 0;
  padding: 0;
  max-width: none;
  border: 1px solid #ddd;
  border-radius: var(--border-radius);
  overflow: hidden;
}

:deep(.camera-box) {
  padding-top: 75%;
  border-radius: var(--border-radius) var(--border-radius) 0 0;
}

:deep(.camera-controls) {
  margin-top: 1rem;
  padding: 0 1rem 1rem 1rem;
  text-align: center;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .profile-page-container {
    padding: 1rem 0.5rem;
  }
  .profile-panel {
    padding: 1.5rem;
  }
  .panel-title {
    font-size: 1.5rem;
  }
  .info-item {
      font-size: 1rem;
  }
}
</style>