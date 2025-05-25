import { createRouter, createWebHistory} from 'vue-router'  //createRouter 用于创建路由实例;createWebHistory 用于创建基于 HTML5 History API 的路由模式
// 导入三个 Vue 组件，分别用于不同路由路径的展示
import UserList from './components/UserList.vue'
import Login from './components/Login.vue'
import Register from './components/Register.vue'
import StudentProfile from './views/StudentProfile.vue'
import QuestionBank from './views/QuestionBank.vue'

//定义路由配置数组，包含三个路由对象：
const routes = [
    {path:'/', component:Login},  // 根路径 / 对应 Login 组件
    {path:'/register', component:Register},  // /register 路径对应 Register 组件
    {path:'/users', component:UserList},  // /users 路径对应 UserList 组件
    {path:'/student-profile', component:StudentProfile},
    {
        path: '/question-bank',
        name: 'QuestionBank',
        component: QuestionBank,
        meta: { requiresAuth: true, requiresOfficer: true }
    }
]

// 创建路由实例
const router = createRouter({
    history:createWebHistory(),  // 使用 createWebHistory() 创建基于 HTML5 History API 的路由模式
    routes  // 传入之前定义的 routes 配置
})

// 添加全局前置守卫
router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('token')
    const userIdentity = localStorage.getItem('userIdentity')
    
    // 需要登录的路由
    if (to.meta.requiresAuth) {
        if (!token) {
            next('/')
            return
        }
        
        // 检查用户权限
        if (to.meta.requiresOfficer && userIdentity !== 'officer') {
            next('/users')
            return
        }
    }

    // 特定路由的权限控制
    if (to.path === '/users' && userIdentity !== 'officer') {
        next('/student-profile')
        return
    }
    
    if (to.path === '/student-profile' && userIdentity !== 'student') {
        next('/users')
        return
    }

    next()
})

export default router  // 导出路由实例，以便在 Vue 应用中使用