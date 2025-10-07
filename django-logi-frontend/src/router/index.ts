// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import { defineAsyncComponent } from 'vue'
import { useAuthStore } from '@/store/auth'

// Lazy loaded pages (defineAsyncComponent gives better error messages)
const DashboardPage = defineAsyncComponent(() => import('@/pages/Dashboard/index.vue'))
const VehiclesPage = defineAsyncComponent(() => import('@/pages/Vehicles/index.vue'))
const CargosPage = defineAsyncComponent(() => import('@/pages/Cargos/index.vue'))
const OffersPage = defineAsyncComponent(() => import('@/pages/Offers/index.vue'))
const ShipmentsPage = defineAsyncComponent(() => import('@/pages/Shipments/index.vue'))
const ReviewsPage = defineAsyncComponent(() => import('@/pages/Reviews/index.vue'))
const WalletPage = defineAsyncComponent(() => import('@/pages/Wallet/index.vue'))
const AppLayout = defineAsyncComponent(() => import('@/layout/AppLayout/index.vue'))
const LoginPage = defineAsyncComponent(() => import('@/pages/auth/Login/index.vue'))
const RegisterPage = defineAsyncComponent(() => import('@/pages/auth/Register/index.vue'))

const routes = [
    {
        path: '/',
        component: AppLayout,
        children: [
            { path: '', name: 'dashboard', component: DashboardPage, meta: { title: 'Dashboard' } },
            { path: 'vehicles', name: 'vehicles', component: VehiclesPage, meta: { title: 'Vehicles' } },
            { path: 'cargos', name: 'cargos', component: CargosPage, meta: { title: 'Cargos' } },
            { path: 'offers', name: 'offers', component: OffersPage, meta: { title: 'Offers' } },
            { path: 'shipments', name: 'shipments', component: ShipmentsPage, meta: { title: 'Shipments' } },
            { path: 'reviews', name: 'reviews', component: ReviewsPage, meta: { title: 'Reviews' } },
            { path: 'wallet', name: 'wallet', component: WalletPage, meta: { title: 'Wallet' } }
        ]
    },
    { path: '/login', name: 'login', component: LoginPage, meta: { title: 'Login' } },
    { path: '/register', name: 'register', component: RegisterPage, meta: { title: 'Register' } },
    { path: '/:pathMatch(.*)*', redirect: '/' }
]

export const router = createRouter({
    history: createWebHistory(),
    routes
})

// ✅ Auth guard
router.beforeEach((to, _from, next) => {
    const auth = useAuthStore()
    if (!auth.isAuthed && to.path !== '/login' && to.path !== '/register') return next('/login')
    if (auth.isAuthed && (to.path === '/login' || to.path === '/register')) return next('/')
    next()
})
