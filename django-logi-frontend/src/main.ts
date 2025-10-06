// src/main.ts
import { createApp } from 'vue'
import App from './App.vue'
import { router } from './router'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import i18n from './i18n'

// MDI Icons
import '@mdi/font/css/materialdesignicons.css'

const app = createApp(App)

app.use(router)
   .use(createPinia())
   .use(ElementPlus)
   .use(i18n)
   .mount('#app')