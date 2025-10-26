// src/main.ts
import { createApp } from 'vue'
import App from './App.vue'
import { router } from './router'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
// Element Plus dark theme (CSS variables)
import 'element-plus/theme-chalk/dark/css-vars.css'
import i18n from './i18n'
import { useAuthStore } from '@/store/auth'

// MDI Icons
import '@mdi/font/css/materialdesignicons.css'

// Initialize theme ASAP to avoid FOUC
const savedTheme = localStorage.getItem('theme')
const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
const startDark = (savedTheme || (prefersDark ? 'dark' : 'light')) === 'dark'
if (startDark) document.documentElement.classList.add('dark')
else document.documentElement.classList.remove('dark')

const app = createApp(App)
const pinia = createPinia()

// Install Pinia first so stores are available to router guards
app.use(pinia)
   .use(router)
   .use(ElementPlus)
   .use(i18n)

// Bootstrap auth on app start so sidebar role menus persist on refresh
const auth = useAuthStore()
if (auth.access) {
  // fire-and-forget; sidebar will update once user is fetched
  auth.fetchMe()
}

app.mount('#app')