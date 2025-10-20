// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import { defineAsyncComponent } from 'vue'
import { useAuthStore } from '@/store/auth'

// Lazy loaded pages (defineAsyncComponent gives better error messages)
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
// Search pages
const SearchVehiclesPage = defineAsyncComponent(() => import('@/pages/Search/Vehicles.vue'))
const SearchCargosPage = defineAsyncComponent(() => import('@/pages/Search/Cargos.vue'))

const routes = [
    // Public routes
    { path: '/market', name: 'market', component: MarketPage, meta: { title: 'Marketplace', public: true } },
    {
        path: '/',
        component: AppLayout,
        children: [
            { path: '', name: 'home', component: HomePage, meta: { title: 'Home', public: true } },
            // Public search routes
            { path: 'search/vehicles', name: 'search-vehicles', component: SearchVehiclesPage, meta: { title: 'Search Vehicles', public: true } },
            { path: 'search/cargos', name: 'search-cargos', component: SearchCargosPage, meta: { title: 'Search Cargos', public: true } },
            // Personal sections
            { path: 'vehicles', name: 'vehicles', component: VehiclesPage, meta: { title: 'Vehicles', public: true } },
            { path: 'vehicles/add', name: 'vehicle-add', component: VehiclesAddPage, meta: { title: 'Add Vehicle' } },
            { path: 'cargos', name: 'cargos', component: CargosPage, meta: { title: 'Cargos', public: true } },
            { path: 'cargos/add', name: 'cargo-add', component: CargosAddPage, meta: { title: 'Add Cargo' } },
            { path: 'offers', name: 'offers', component: OffersPage, meta: { title: 'Offers', public: true } },
            { path: 'shipments', name: 'shipments', component: ShipmentsPage, meta: { title: 'Shipments', public: true } },
            { path: 'reviews', name: 'reviews', component: ReviewsPage, meta: { title: 'Reviews', public: true } },
            { path: 'wallet', name: 'wallet', component: WalletPage, meta: { title: 'Wallet' } },
            { path: 'driver-request', name: 'driver-request', component: DriverRequestPage, meta: { title: 'Driver Request', public: true } }
        ]
    },
    { path: '/login', name: 'login', component: LoginPage, meta: { title: 'Login', public: true } },
    { path: '/register', name: 'register', component: RegisterPage, meta: { title: 'Register', public: true } },
    // Default to market for unknown routes
    { path: '/:pathMatch(.*)*', redirect: '/market' }
]

export const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
})

// ✅ Auth guard (allows public routes)
router.beforeEach((to, _from, next) => {
    const auth = useAuthStore()
    const isPublic = Boolean(to.meta.public) || to.path === '/market'
    if (!auth.isAuthed) {
        if (!isPublic) return next('/market')
    }
    if (auth.isAuthed && (to.path === '/login' || to.path === '/register')) return next('/')
    next()
})
