<template>
  <div class="app-wrapper" :class="{ 'header-is-pinned': isHeaderPinned }">
    <Header v-if="showLayout" :class="{ 'is-pinned': isHeaderPinned }" />

    <button v-if="showLayout"
            class="header-pin-toggle"
            @click="toggleHeaderPin"
            :class="{ 'is-pinned': isHeaderPinned }"
            aria-label="Toggle Header Pin">
      </button>

    <main class="main-content">
      <router-view />
    </main>

    <Footer v-if="showLayout" />
  </div>
</template>

<script>
// <script> 部分保持不变
import Header from './components/Header.vue';
import Footer from './components/Footer.vue';

export default {
  name: 'App',
  components: {
    Header,
    Footer
  },
  data() {
    return {
      isHeaderPinned: false, // 默认不固定 (隐藏)
    };
  },
  computed: {
    showLayout() {
      const noLayoutRoutes = ['/', '/register'];
      return !noLayoutRoutes.includes(this.$route.path);
    }
  },
  methods: {
    toggleHeaderPin() {
      this.isHeaderPinned = !this.isHeaderPinned;
    }
  }
}
</script>

<style>
/* ... 保留 .app-wrapper, .main-content, .app-footer 的样式 ... */

.app-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding-top: 0;
  transition: padding-top 0.4s ease-in-out;
}

.app-wrapper.header-is-pinned .main-content {
  padding-top: 60px;
}

.main-content > * {
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* --- 修改按钮样式 --- */
.header-pin-toggle {
    position: fixed;
    top: 0px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 1001;
    cursor: pointer;
    transition: top 0.4s ease-in-out;
    opacity: 0.7;

    /* --- 按钮本身透明化，并设置点击区域 --- */
    background-color: transparent;
    border: none;
    padding: 15px 15px 5px 15px; /* 增大点击区域 (上/左右/下) */
    line-height: 0; /* 移除可能的行高影响 */
    width: auto; /* 宽度由内容决定 (现在是伪元素) */
    height: auto; /* 高度由内容决定 */
    border-radius: 0; /* 移除圆角 */
    box-shadow: none; /* 移除阴影 */
}

.header-pin-toggle:hover {
    opacity: 1;
}

/* --- 使用 ::before 伪元素绘制三角形 --- */
.header-pin-toggle::before {
    content: '';
    display: block;
    width: 0;
    height: 0;
    transition: border-color 0.3s ease, border-width 0.3s ease; /* 添加过渡效果 */

    /* 默认：倒三角形 (向下) */
    border-left: 8px solid transparent; /* 三角形底边的一半 */
    border-right: 8px solid transparent; /* 三角形底边的一半 */
    border-top: 10px solid #2196F3; /* 三角形的高度和颜色 (蓝色) */
    border-bottom: none;
}

/* 当固定时：正三角形 (向上) */
.header-pin-toggle.is-pinned::before {
    border-top: none;
    border-bottom: 10px solid #4CAF50; /* 三角形的高度和颜色 (绿色) */
}

/* 当 Header 固定时，按钮移动到 Header 下方 */
.header-pin-toggle.is-pinned {
    top: 60px; /* Header 的高度 */
    /* 调整 padding 使其在下方时点击区域更合理 */
    padding: 5px 15px 15px 15px;
}
</style>