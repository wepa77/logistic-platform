// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import { defineAsyncComponent } from 'vue'
import { useAuthStore } from '@/store/auth'

// Lazy loaded pages (defineAsyncComponent gives better error messages)
const DashboardPage = defineAsyncComponent(() => import('@/pages/Dashboard/index.vue'))
const VehiclesPage = defineAsyncComponent(() => import('@/pages/Vehicles/index.vue'))
const VehiclesAddPage = defineAsyncComponent(() => import('@/pages/Vehicles/Add.vue'))
const CargosPage = defineAsyncComponent(() => import('@/pages/Cargos/index.vue'))
const CargosAddPage = defineAsyncComponent(() => import('@/pages/Cargos/Add.vue'))
const OffersPage = defineAsyncComponent(() => import('@/pages/Offers/index.vue'))
const ShipmentsPage = defineAsyncComponent(() => import('@/pages/Shipments/index.vue'))
const ReviewsPage = defineAsyncComponent(() => import('@/pages/Reviews/index.vue'))
const WalletPage = defineAsyncComponent(() => import('@/pages/Wallet/index.vue'))
const AppLayout = defineAsyncComponent(() => import('@/layout/AppLayout/index.vue'))
const LoginPage = defineAsyncComponent(() => import('@/pages/auth/Login/index.vue'))
const RegisterPage = defineAsyncComponent(() => import('@/pages/auth/Register/index.vue'))
// Public Home and Marketplace (no auth required)
const HomePage = defineAsyncComponent(() => import('@/pages/Home/index.vue'))
const MarketPage = defineAsyncComponent(() => import('@/pages/Marketplace/index.vue'))
// Driver request page
const DriverRequestPage = defineAsyncComponent(() => import('@/pages/DriverRequest/index.vue'))

const routes = [
    // Public routes
    { path: '/home', name: 'home', component: HomePage, meta: { title: 'Home', public: true } },
    { path: '/market', name: 'market', component: MarketPage, meta: { title: 'Marketplace', public: true } },
    {
        path: '/',
        component: AppLayout,
        children: [
            { path: '', name: 'dashboard', component: DashboardPage, meta: { title: 'Dashboard' } },
            { path: 'vehicles', name: 'vehicles', component: VehiclesPage, meta: { title: 'Vehicles' } },
            { path: 'vehicles/add', name: 'vehicle-add', component: VehiclesAddPage, meta: { title: 'Add Vehicle' } },
            { path: 'cargos', name: 'cargos', component: CargosPage, meta: { title: 'Cargos' } },
            { path: 'cargos/add', name: 'cargo-add', component: CargosAddPage, meta: { title: 'Add Cargo' } },
            { path: 'offers', name: 'offers', component: OffersPage, meta: { title: 'Offers' } },
            { path: 'shipments', name: 'shipments', component: ShipmentsPage, meta: { title: 'Shipments' } },
            { path: 'reviews', name: 'reviews', component: ReviewsPage, meta: { title: 'Reviews' } },
            { path: 'wallet', name: 'wallet', component: WalletPage, meta: { title: 'Wallet' } },
            { path: 'driver-request', name: 'driver-request', component: DriverRequestPage, meta: { title: 'Driver Request' } }
        ]
    },
    { path: '/login', name: 'login', component: LoginPage, meta: { title: 'Login', public: true } },
    { path: '/register', name: 'register', component: RegisterPage, meta: { title: 'Register', public: true } },
    // Default to market for unknown routes
    { path: '/:pathMatch(.*)*', redirect: '/market' }
]

export const router = createRouter({
    history: createWebHistory(),
    routes
})

// ✅ Auth guard (allows public routes)
router.beforeEach((to, _from, next) => {
    const auth = useAuthStore()
    const isPublic = Boolean(to.meta.public) || to.path === '/market'
    if (!auth.isAuthed && !isPublic) return next('/market')
    if (auth.isAuthed && (to.path === '/login' || to.path === '/register')) return next('/')
    next()
})
