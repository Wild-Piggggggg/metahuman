<template>
    <header class="app-header">
      <div class="header-left">
        <img src="@/assets/logo.png" alt="App Logo" class="logo-img" @error="useLogoPlaceholder">
      </div>
  
      <div class="header-right">
        <img :src="avatarUrl" alt="User Avatar" class="user-avatar" @error="useAvatarPlaceholder">
        <span class="username">用户名</span>
        <button @click="logout" class="logout-button">退出登录</button>
      </div>
    </header>
  </template>
  
  <script>
  export default {
    name: 'AppHeader',
    data() {
      return {
        // 默认头像或从用户信息中获取
        avatarUrl: '@/assets/avatar.png',
        // 备用 SVG 占位符
        logoPlaceholderSvg: "data:image/svg+xml;charset=UTF-8,%3Csvg%20width%3D%22150%22%20height%3D%2240%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Crect%20width%3D%22150%22%20height%3D%2240%22%20fill%3D%22%23E0E0E0%22%2F%3E%3Ctext%20x%3D%2275%22%20y%3D%2225%22%20font-family%3D%22Arial%22%20font-size%3D%2216%22%20fill%3D%22%23333%22%20text-anchor%3D%22middle%22%20alignment-baseline%3D%22middle%22%3ELogo%3C%2Ftext%3E%3C%2Fsvg%3E",
        avatarPlaceholderSvg: "data:image/svg+xml;charset=UTF-8,%3Csvg%20width%3D%2236%22%20height%3D%2236%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Cg%20fill%3D%22none%22%20fill-rule%3D%22evenodd%22%3E%3Ccircle%20fill%3D%22%23CCC%22%20cx%3D%2218%22%20cy%3D%2218%22%20r%3D%2218%22%2F%3E%3Cpath%20d%3D%22M18%2011c-1.657%200-3%201.343-3%203s1.343%203%203%203%203-1.343%203-3-1.343-3-3-3zm0%208c-3.314%200-6%201.343-6%203v2h12v-2c0-1.657-2.686-3-6-3z%22%20fill%3D%22%23FFF%22%2F%3E%3C%2Fg%3E%3C%2Fsvg%3E"
      };
    },
    methods: {
      logout() {
        // 清除本地存储或执行其他登出操作
        localStorage.removeItem('token');
        localStorage.removeItem('userIdentity');
        // 重定向到登录页面
        this.$router.push('/');
      },
      useLogoPlaceholder(event) {
        // 如果 logo.png 加载失败，则使用 SVG 占位符
        event.target.src = this.logoPlaceholderSvg;
        console.warn("Logo not found at @/assets/logo.png. Using placeholder.");
      },
      useAvatarPlaceholder(event) {
        // 如果头像加载失败，则使用 SVG 占位符
        event.target.src = this.avatarPlaceholderSvg;
         console.warn("Avatar not found. Using placeholder.");
      }
    },
    mounted() {
      // 尝试预加载以触发错误处理（如果需要）
      // 或者在这里检查文件是否存在/从 API 获取 URL
    }
  }
  </script>
  
  <style scoped>
  .app-header {
    /* --- 核心样式 --- */
    position: fixed; /* 固定定位 */
    top: 0;
    left: 0;
    width: 100%;
    height: 80px; /* 确保与 App.vue 中的 padding 和按钮位置一致 */
    transform: translateY(-100%); /* 默认隐藏在上方 */
    transition: transform 0.4s ease-in-out; /* 平滑过渡 */
    z-index: 1000; /* 确保在内容之上 */

    /* --- 原有样式 --- */
    background-color: #ffffff;
    padding: 10px 30px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #ddd;
    box-sizing: border-box;
  }

  /* 当 .is-pinned 类存在时，滑入视口 */
  .app-header.is-pinned {
    transform: translateY(0);
  }

  /* --- 其他内部元素样式保持不变 --- */
  .header-left {
    width: 200px;
    background-color: rgb(255, 255, 255);
    height: 100%;
    display: flex;
    align-items: center;
  }
  .header-right {
    width: 250px;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    background-color: rgb(255, 255, 255);
    height: 100%;
  }

  .logo-img {
    height: 60px;
    width: 200px;
    vertical-align: middle;
    background-color: #ffffff;
  }

  .user-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    margin-right: 10px;
    object-fit: cover;
    border: 1px solid #eee;
    background-color: #eee;
  }

  .username {
      margin-right: 15px;
      font-weight: 500;
      color: #333;
  }

  .logout-button {
    background-color: #f44336;
    color: white;
    border: none;
    padding: 8px 15px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.3s ease;
  }

  .logout-button:hover {
    background-color: #d32f2f;
  }
</style>