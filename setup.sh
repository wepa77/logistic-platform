#!/usr/bin/env bash
set -euo pipefail

APP_NAME="${1:-django-logi-frontend}"

echo ">> 1) Create Vite Vue3+TS project: $APP_NAME"
npm create vite@latest "$APP_NAME" -- --template vue-ts >/dev/null <<<'y'

cd "$APP_NAME"

echo ">> 2) Install deps"
npm i axios pinia vue-router element-plus @element-plus/icons-vue dayjs
npm i -D unplugin-auto-import unplugin-vue-components @types/node

echo ">> 3) Configure Vite (auto-import Element Plus)"
cat > vite.config.ts <<'EOF'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'

export default defineConfig({
  plugins: [
    vue(),
    AutoImport({ resolvers: [ElementPlusResolver()] }),
    Components({ resolvers: [ElementPlusResolver()] }),
  ],
})
EOF

echo ">> 4) Env"
cat > .env <<'EOF'
VITE_API_BASE=http://localhost:8000
EOF

echo ">> 5) Base folders"
mkdir -p src/{api/{users,vehicles,cargos,offers,shipments,reviews,wallet},components/{DataTable,FormDialog,UploadImage},layout/{AppLayout,PageHeader},pages/{auth/Login,Dashboard,Vehicles,Cargos,Offers,Shipments,Reviews,Wallet},router,store,types}

echo ">> 6) main.ts & App.vue"
cat > src/main.ts <<'EOF'
import { createApp } from 'vue'
import App from './App.vue'
import { createPinia } from 'pinia'
import { router } from './router'
import 'element-plus/dist/index.css'

createApp(App).use(createPinia()).use(router).mount('#app')
EOF

cat > src/App.vue <<'EOF'
<template>
  <router-view />
</template>
<script setup lang="ts"></script>
EOF

echo ">> 7) Router"
cat > src/router/index.ts <<'EOF'
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/store/auth'

const routes = [
  { path: '/login', component: () => import('@/pages/auth/Login/index.vue') },
  {
    path: '/',
    component: () => import('@/layout/AppLayout/index.vue'),
    children: [
      { path: '', name: 'dashboard', component: () => import('@/pages/Dashboard/index.vue') },
      { path: 'vehicles', component: () => import('@/pages/Vehicles/index.vue') },
      { path: 'cargos', component: () => import('@/pages/Cargos/index.vue') },
      { path: 'offers', component: () => import('@/pages/Offers/index.vue') },
      { path: 'shipments', component: () => import('@/pages/Shipments/index.vue') },
      { path: 'reviews', component: () => import('@/pages/Reviews/index.vue') },
      { path: 'wallet', component: () => import('@/pages/Wallet/index.vue') },
    ]
  }
]

export const router = createRouter({ history: createWebHistory(), routes })

router.beforeEach((to, _from, next) => {
  const auth = useAuthStore()
  if (to.path !== '/login' && !auth.isAuthed) return next('/login')
  if (to.path === '/login' && auth.isAuthed) return next('/')
  next()
})
EOF

echo ">> 8) Store (auth)"
cat > src/store/auth.ts <<'EOF'
import { defineStore } from 'pinia'
import { http } from '@/api/http'
import type { IUser } from '@/types/models'

export const useAuthStore = defineStore('auth', {
  state: () => ({ user: null as IUser | null }),
  getters: {
    isAuthed: (s) => !!s.user,
    isCarrier: (s) => s.user?.user_type === 'carrier',
    isShipper: (s) => s.user?.user_type === 'shipper',
  },
  actions: {
    async login(username: string, password: string) {
      const { data } = await http.post<{access:string; refresh:string}>('/auth/token/', { username, password })
      localStorage.setItem('access', data.access)
      localStorage.setItem('refresh', data.refresh)
      await this.fetchMe()
    },
    async fetchMe() {
      const { data } = await http.get<IUser>('/auth/me/')
      this.user = data
    },
    logout() {
      this.user = null
      localStorage.clear()
    },
  },
})
EOF

echo ">> 9) API http + barrels"
cat > src/api/http.ts <<'EOF'
import axios from 'axios'
export const http = axios.create({ baseURL: import.meta.env.VITE_API_BASE })
http.interceptors.request.use((cfg) => {
  const token = localStorage.getItem('access')
  if (token) cfg.headers.Authorization = `Bearer ${token}`
  return cfg
})
EOF

cat > src/api/index.ts <<'EOF'
export * as UsersApi from './users'
export * as VehiclesApi from './vehicles'
export * as CargosApi from './cargos'
export * as OffersApi from './offers'
export * as ShipmentsApi from './shipments'
export * as ReviewsApi from './reviews'
export * as WalletApi from './wallet'
export * as TopupsApi from './wallet/topups'
EOF

echo ">> 10) API endpoints"
cat > src/api/users/index.ts <<'EOF'
import { http } from '../http'
import type { IUser } from '@/types/models'
export const me = () => http.get<IUser>('/auth/me/')
EOF

cat > src/api/vehicles/index.ts <<'EOF'
import { http } from '../http'
import type { IVehicle } from '@/types/models'
export const list = (params?: any) => http.get<IVehicle[]>('/vehicles/', { params })
export const create = (payload: Partial<IVehicle>) => http.post<IVehicle>('/vehicles/', payload)
export const update = (id:number, payload: Partial<IVehicle>) => http.patch<IVehicle>(`/vehicles/${id}/`, payload)
export const remove = (id:number) => http.delete(`/vehicles/${id}/`)
EOF

cat > src/api/cargos/index.ts <<'EOF'
import { http } from '../http'
import type { ICargo } from '@/types/models'
export const list = (p?: any)=> http.get<ICargo[]>('/cargos/', { params:p })
export const create = (payload: Partial<ICargo>) => http.post<ICargo>('/cargos/', payload)
export const update = (id:number, payload: Partial<ICargo>) => http.patch<ICargo>(`/cargos/${id}/`, payload)
export const remove = (id:number) => http.delete(`/cargos/${id}/`)
EOF

cat > src/api/offers/index.ts <<'EOF'
import { http } from '../http'
import type { IOffer } from '@/types/models'
export const list = (p?: any)=> http.get<IOffer[]>('/offers/', { params:p })
export const create = (payload: Partial<IOffer>) => http.post<IOffer>('/offers/', payload)
export const update = (id:number, payload: Partial<IOffer>) => http.patch<IOffer>(`/offers/${id}/`, payload)
export const remove = (id:number) => http.delete(`/offers/${id}/`)
EOF

cat > src/api/shipments/index.ts <<'EOF'
import { http } from '../http'
import type { IShipment } from '@/types/models'
export const list = (p?: any)=> http.get<IShipment[]>('/shipments/', { params:p })
export const create = (payload: Partial<IShipment>) => http.post<IShipment>('/shipments/', payload)
export const update = (id:number, payload: Partial<IShipment>) => http.patch<IShipment>(`/shipments/${id}/`, payload)
EOF

cat > src/api/reviews/index.ts <<'EOF'
import { http } from '../http'
import type { IReview } from '@/types/models'
export const list = (p?: any)=> http.get<IReview[]>('/reviews/', { params:p })
export const create = (payload: Partial<IReview>) => http.post<IReview>('/reviews/', payload)
export const update = (id:number, payload: Partial<IReview>) => http.patch<IReview>(`/reviews/${id}/`, payload)
export const remove = (id:number) => http.delete(`/reviews/${id}/`)
EOF

cat > src/api/wallet/index.ts <<'EOF'
import { http } from '../http'
import type { IWalletTx } from '@/types/models'
export const list = () => http.get<IWalletTx[]>('/wallet/')
export const balance = () => http.get<{balance:string}>('/topups/balance/')
EOF

cat > src/api/wallet/topups.ts <<'EOF'
import { http } from '../http'
import type { ITopUp } from '@/types/models'
export const list = () => http.get<ITopUp[]>('/topups/')
export const create = (amount:number) => http.post<ITopUp>('/topups/', { amount })
EOF

echo ">> 11) Types"
cat > src/types/models.ts <<'EOF'
export type UserType = 'shipper' | 'carrier'
export interface IUser {
  id: number
  username: string
  email: string
  phone?: string
  company_name?: string
  address?: string
  user_type: UserType
  verified: boolean
  balance?: string
  deposit_balance?: string
}
export interface IVehicle {
  id: number
  plate_number: string
  brand?: string
  model?: string
  year?: number
  capacity_kg: number
  volume_m3?: string
  truck_type?: string
  gps_enabled: boolean
  owner?: IUser
  owner_id?: number
  photo?: string
}
export interface ICargo {
  id: number
  title: string
  description?: string
  weight_kg: number
  volume_m3?: string
  pickup_address: string
  delivery_address: string
  pickup_date: string
  delivery_date?: string
  price_offer?: string
  status: 'open'|'in_progress'|'delivered'|'cancelled'
  created_at: string
  shipper?: IUser
  shipper_id?: number
  photo?: string
}
export interface IOffer {
  id: number
  price: string
  note?: string
  status: 'pending'|'accepted'|'rejected'
  created_at: string
  cargo: number | ICargo
  carrier?: IUser
  carrier_id?: number
  vehicle?: IVehicle
  vehicle_id?: number
}
export interface IShipment {
  id: number
  cargo: number | ICargo
  carrier?: IUser
  carrier_id?: number
  vehicle?: IVehicle
  vehicle_id?: number
  start_time: string
  end_time?: string
  total_price?: string
  distance_km?: string
  commission_amount: string
  payment_type: 'stripe'|'cash'|'bank'
  payment_status: 'pending'|'paid'|'failed'
  cash_received_by?: string
  received_date?: string
}
export interface IReview {
  id: number
  shipment: number | IShipment
  reviewer?: IUser
  reviewer_id?: number
  rating: number
  comment?: string
  created_at: string
}
export interface IWalletTx {
  id: number
  tx_type: 'top_up'|'commission'|'refund'|'deposit_top_up'|'deposit_commission'
  amount: string
  description?: string
  created_at: string
  success: boolean
}
export interface ITopUp {
  id: number
  amount: string
  stripe_session_id?: string
  created_at: string
  paid: boolean
}
EOF

echo ">> 12) Layout & components"
cat > src/layout/AppLayout/index.vue <<'EOF'
<template>
  <el-container style="height:100vh">
    <el-aside width="240px" class="p-3">
      <h3 class="mb-4">Logi Panel</h3>
      <el-menu router default-active="/">
        <el-menu-item index="/">Dashboard</el-menu-item>
        <el-menu-item index="/vehicles">Vehicles</el-menu-item>
        <el-menu-item index="/cargos">Cargos</el-menu-item>
        <el-menu-item index="/offers">Offers</el-menu-item>
        <el-menu-item index="/shipments">Shipments</el-menu-item>
        <el-menu-item index="/reviews">Reviews</el-menu-item>
        <el-menu-item index="/wallet">Wallet</el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="flex justify-between items-center">
        <div />
        <div><el-button @click="logout" type="danger" plain>Logout</el-button></div>
      </el-header>
      <el-main><router-view /></el-main>
    </el-container>
  </el-container>
</template>
<script setup lang="ts">
import { useAuthStore } from '@/store/auth'
const auth = useAuthStore()
const logout = () => auth.logout()
</script>
<style scoped>
.mb-4{margin-bottom:1rem}.p-3{padding:1rem}.flex{display:flex}
.justify-between{justify-content:space-between}.items-center{align-items:center}
</style>
EOF
cat > src/layout/AppLayout/index.ts <<'EOF'
export { default } from './index.vue'
EOF

cat > src/components/DataTable/index.vue <<'EOF'
<template>
  <div>
    <div class="mb-2"><slot name="actions"></slot></div>
    <el-table :data="rows" stripe border @selection-change="onSel"><el-table-column type="selection" width="45"/><slot /></el-table>
    <div class="mt-2 flex justify-end">
      <el-pagination layout="prev, pager, next" :page-size="pageSize" :total="total" @current-change="$emit('page', $event)" />
    </div>
  </div>
</template>
<script setup lang="ts">
defineProps<{ rows:any[]; total:number; pageSize?:number }>()
const emit = defineEmits<{ (e:'selection', val:any[]):void; (e:'page', p:number):void }>()
const onSel = (val:any[]) => emit('selection', val)
</script>
<style scoped>
.mb-2{margin-bottom:.5rem}.mt-2{margin-top:.5rem}.flex{display:flex}.justify-end{justify-content:flex-end}
</style>
EOF
cat > src/components/DataTable/index.ts <<'EOF'
export { default } from './index.vue'
EOF

cat > src/components/FormDialog/index.vue <<'EOF'
<template>
  <el-dialog v-model="open" :title="title" width="520px" destroy-on-close>
    <slot></slot>
    <template #footer>
      <el-space>
        <el-button @click="open=false">Cancel</el-button>
        <el-button type="primary" @click="$emit('submit')">Save</el-button>
      </el-space>
    </template>
  </el-dialog>
</template>
<script setup lang="ts">
const open = defineModel<boolean>('open', { required: true })
defineProps<{ title:string }>()
defineEmits<{ (e:'submit'):void }>()
</script>
EOF
cat > src/components/FormDialog/index.ts <<'EOF'
export { default } from './index.vue'
EOF

echo ">> 13) Pages"

# Login
cat > src/pages/auth/Login/index.vue <<'EOF'
<template>
  <div class="login">
    <el-card class="card">
      <h2>Sign In</h2>
      <el-form :model="form" @keyup.enter="doLogin">
        <el-form-item label="Username"><el-input v-model="form.username" /></el-form-item>
        <el-form-item label="Password"><el-input v-model="form.password" type="password" /></el-form-item>
        <el-button type="primary" @click="doLogin" :loading="loading">Login</el-button>
      </el-form>
    </el-card>
  </div>
</template>
<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useAuthStore } from '@/store/auth'
import { useRouter } from 'vue-router'
const auth = useAuthStore(); const router = useRouter()
const form = reactive({ username:'', password:'' }); const loading = ref(false)
const doLogin = async () => { loading.value = true; try { await auth.login(form.username, form.password); router.push('/') } finally { loading.value = false } }
</script>
<style scoped>.login{display:grid;place-items:center;height:100vh}.card{width:360px}</style>
EOF
cat > src/pages/auth/Login/index.ts <<'EOF'
export { default } from './index.vue'
EOF

# Dashboard
cat > src/pages/Dashboard/index.vue <<'EOF'
<template>
  <div>
    <el-page-header title="Dashboard" content="Overview" class="mb-2" />
    <el-card>
      <p>Welcome, {{ user?.username }} ({{ user?.user_type }})</p>
      <p v-if="user?.balance">Balance: {{ user?.balance }} TMT</p>
      <p v-if="user?.deposit_balance">Deposit: {{ user?.deposit_balance }} TMT</p>
    </el-card>
  </div>
</template>
<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/store/auth'
const auth = useAuthStore(); const { user } = storeToRefs(auth)
</script>
<style scoped>.mb-2{margin-bottom:.75rem}</style>
EOF
cat > src/pages/Dashboard/index.ts <<'EOF'
export { default } from './index.vue'
EOF

# Vehicles
cat > src/pages/Vehicles/index.vue <<'EOF'
<template>
  <div>
    <el-page-header content="Manage your vehicles" title="Vehicles" class="mb-2" />
    <el-space class="mb-2">
      <el-button type="primary" @click="open=true">Add Vehicle</el-button>
      <el-input v-model="filters.search" placeholder="Search plate/brand/model" style="width:260px" @change="fetchRows"/>
    </el-space>

    <DataTable :rows="rows" :total="total" @page="fetchRows">
      <el-table-column prop="plate_number" label="Plate" />
      <el-table-column prop="brand" label="Brand" />
      <el-table-column prop="model" label="Model" />
      <el-table-column prop="capacity_kg" label="Capacity (kg)" width="140"/>
      <el-table-column prop="truck_type" label="Type" />
      <el-table-column fixed="right" label="Actions" width="140">
        <template #default="{ row }">
          <el-button size="small" @click="edit(row)">Edit</el-button>
          <el-popconfirm title="Delete vehicle?" @confirm="del(row.id)">
            <template #reference><el-button size="small" type="danger">Delete</el-button></template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </DataTable>

    <FormDialog v-model:open="open" :title="form.id ? 'Edit Vehicle' : 'Add Vehicle'" @submit="save">
      <el-form :model="form" label-width="130px">
        <el-form-item label="Plate Number"><el-input v-model="form.plate_number" /></el-form-item>
        <el-form-item label="Brand"><el-input v-model="form.brand" /></el-form-item>
        <el-form-item label="Model"><el-input v-model="form.model" /></el-form-item>
        <el-form-item label="Capacity (kg)"><el-input v-model.number="form.capacity_kg" /></el-form-item>
        <el-form-item label="Truck Type"><el-input v-model="form.truck_type" /></el-form-item>
      </el-form>
    </FormDialog>
  </div>
</template>
<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import DataTable from '@/components/DataTable'
import FormDialog from '@/components/FormDialog'
import * as Vehicles from '@/api/vehicles'
import type { IVehicle } from '@/types/models'

const rows = ref<IVehicle[]>([]); const total = ref(0); const open = ref(false)
const form = reactive<Partial<IVehicle>>({ capacity_kg: 1000 })
const filters = reactive({ search: '' })

async function fetchRows(){ const { data } = await Vehicles.list({ search: filters.search }); rows.value = data; total.value = data.length }
function edit(row: IVehicle){ Object.assign(form, row); open.value = true }
async function del(id:number){ await Vehicles.remove(id); fetchRows() }
async function save(){
  if (form.id) await Vehicles.update(form.id, form)
  else await Vehicles.create({ ...form })
  Object.keys(form).forEach(k=> (form as any)[k]=undefined)
  open.value = false; fetchRows()
}
onMounted(fetchRows)
</script>
<style scoped>.mb-2{margin-bottom:.75rem}</style>
EOF
cat > src/pages/Vehicles/index.ts <<'EOF'
export { default } from './index.vue'
EOF

# Shipments
cat > src/pages/Shipments/index.vue <<'EOF'
<template>
  <div>
    <el-page-header title="Shipments" content="All shipments" class="mb-2"/>
    <el-table :data="rows" stripe border>
      <el-table-column prop="cargo.title" label="Cargo" />
      <el-table-column prop="carrier.username" label="Carrier" />
      <el-table-column label="Status">
        <template #default="{row}">
          <el-tag :type="row.payment_status==='paid'?'success':row.payment_status==='pending'?'warning':'danger'">
            {{ row.payment_status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="commission_amount" label="Commission" />
      <el-table-column prop="start_time" label="Start" />
    </el-table>
  </div>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import * as Shipments from '@/api/shipments'
import type { IShipment } from '@/types/models'
const rows = ref<IShipment[]>([])
onMounted(async ()=>{ rows.value = (await Shipments.list()).data })
</script>
<style scoped>.mb-2{margin-bottom:.75rem}</style>
EOF
cat > src/pages/Shipments/index.ts <<'EOF'
export { default } from './index.vue'
EOF

# Wallet
cat > src/pages/Wallet/index.vue <<'EOF'
<template>
  <div>
    <el-page-header title="Wallet" content="Balance & Top-ups" class="mb-2"/>
    <el-space class="mb-2">
      <el-tag>Balance: {{ balance || '0' }} TMT</el-tag>
      <el-input v-model.number="amount" type="number" placeholder="Top-up amount" style="width:180px"/>
      <el-button type="primary" @click="topup">Create Top-up</el-button>
    </el-space>

    <h3 class="mb-1">Transactions</h3>
    <el-table :data="txs" stripe border>
      <el-table-column prop="created_at" label="Date" width="180"/>
      <el-table-column prop="tx_type" label="Type"/>
      <el-table-column prop="amount" label="Amount"/>
      <el-table-column prop="description" label="Description"/>
      <el-table-column prop="success" label="OK" width="80">
        <template #default="{row}">
          <el-tag :type="row.success ? 'success' : 'danger'">{{ row.success ? 'Yes' : 'No' }}</el-tag>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import * as Wallet from '@/api/wallet'
import * as Topups from '@/api/wallet/topups'
import type { IWalletTx } from '@/types/models'

const balance = ref<string>('0'); const txs = ref<IWalletTx[]>([])
const amount = ref<number>(50)

async function load(){ balance.value = (await Wallet.balance()).data.balance; txs.value = (await Wallet.list()).data }
async function topup(){ await Topups.create(amount.value); await load() }
onMounted(load)
</script>
<style scoped>.mb-2{margin-bottom:.75rem}.mb-1{margin-bottom:.5rem}</style>
EOF
cat > src/pages/Wallet/index.ts <<'EOF'
export { default } from './index.vue'
EOF

# Minimal stubs for other pages
for P in Cargos Offers Reviews; do
cat > "src/pages/$P/index.vue" <<'EOF'
<template><div><el-page-header :title="title" class="mb-2"/></div></template>
<script setup lang="ts">const title = __filename.split('/').slice(-2,-1)[0]</script>
<style scoped>.mb-2{margin-bottom:.75rem}</style>
EOF
cat > "src/pages/$P/index.ts" <<'EOF'
export { default } from './index.vue'
EOF
done

echo ">> 14) Path aliases (tsconfig)"
# ensure @ alias works
jq '.compilerOptions.paths={"@/*":["./src/*"]} | .compilerOptions.baseUrl="."' tsconfig.json > tsconfig.tmp.json && mv tsconfig.tmp.json tsconfig.json

echo ">> All set!
Run:
  cd $APP_NAME
  npm run dev
Make sure your Django API is running at VITE_API_BASE (default http://localhost:8000)."
