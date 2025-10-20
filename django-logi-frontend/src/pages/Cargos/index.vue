<template>
  <div class="cargos-page">
    <!-- Header -->
    <div class="page-header" v-if="!embedded">
      <div class="header-content">
        <div class="header-left">
          <h1 class="page-title">
            <i class="mdi mdi-package-variant-closed"></i>
            {{ $t('cargos.title') }}
          </h1>
          <p class="page-subtitle">{{ $t('cargos.subtitle') }}</p>
        </div>
        <div class="header-actions">
          <router-link to="/cargos/add">
            <el-button type="primary" size="large" class="add-btn">
              <i class="mdi mdi-plus"></i>
              {{ $t('cargos.addNew') }}
            </el-button>
          </router-link>
        </div>
      </div>
    </div>

    <!-- Prefilter Summary from marketplace -->
    <el-alert
      v-if="prefilterSummary"
      :title="prefilterSummary"
      type="info"
      class="prefilter-banner"
      show-icon
      :closable="false"
    />

    <!-- Filters -->
    <el-card class="filters-card" shadow="never" v-if="!embedded">
      <div class="filters-container">
        <el-input
          v-model="searchQuery"
          :placeholder="$t('cargos.searchPlaceholder') as string"
          class="search-input"
          clearable
        >
          <template #prefix><i class="mdi mdi-magnify"></i></template>
        </el-input>
        <el-select v-model="statusFilter" :placeholder="$t('cargos.filterByStatus') as string" clearable class="status-filter">
          <el-option :label="$t('cargos.allStatus') as string" value="" />
          <el-option :label="$t('cargos.open') as string" value="open" />
          <el-option :label="$t('cargos.inProgress') as string" value="in_progress" />
          <el-option :label="$t('cargos.delivered') as string" value="delivered" />
          <el-option :label="$t('cargos.cancelled') as string" value="cancelled" />
        </el-select>
        <el-button class="filter-btn" @click="refresh">
          <i class="mdi mdi-refresh"></i>
        </el-button>
      </div>
    </el-card>

    <!-- Stats -->
    <div class="stats-grid" v-if="!embedded">
      <div class="stat-card">
        <div class="stat-icon total"><i class="mdi mdi-package-variant"></i></div>
        <div class="stat-content">
          <div class="stat-value">{{ cargos.length }}</div>
          <div class="stat-label">{{ $t('cargos.totalCargos') }}</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon weight"><i class="mdi mdi-weight-kilogram"></i></div>
        <div class="stat-content">
          <div class="stat-value">{{ totalWeight.toFixed(0) }}</div>
          <div class="stat-label">{{ $t('cargos.totalWeightKg') }}</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon volume"><i class="mdi mdi-cube-outline"></i></div>
        <div class="stat-content">
          <div class="stat-value">{{ totalVolume.toFixed(1) }}</div>
          <div class="stat-label">{{ $t('cargos.totalVolumeM3') }}</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon open"><i class="mdi mdi-clock-outline"></i></div>
        <div class="stat-content">
          <div class="stat-value">{{ openCount }}</div>
          <div class="stat-label">{{ $t('cargos.open') }}</div>
        </div>
      </div>
    </div>

    <!-- Cargos Table -->
    <el-card class="table-card" shadow="never">
      <el-table :data="filteredCargos" style="width: 100%" class="modern-table">
        <el-table-column :label="$t('cargos.table.cargo')" min-width="220">
          <template #default="{ row }">
            <div class="cargo-cell">
              <div class="cargo-title">{{ row.title || ($t('cargos.untitled') as string) }}</div>
              <div class="cargo-meta">
                <i class="mdi mdi-truck"></i>
                <span>{{ row.body_type ? bodyTypes[row.body_type] : ($t('cargos.general') as string) }}</span>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column :label="$t('cargos.table.route')" min-width="260">
          <template #default="{ row }">
            <div class="route">
              <span class="from">{{ row.pickup_address || '—' }}</span>
              <i class="mdi mdi-arrow-right"></i>
              <span class="to">{{ row.delivery_address || '—' }}</span>
            </div>
            <div class="route-meta">
              <i class="mdi mdi-city"></i>
              <span>{{ row.city || '—' }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column :label="$t('cargos.table.specs')" min-width="220">
          <template #default="{ row }">
            <div class="specs">
              <span class="chip"><i class="mdi mdi-weight-kilogram"></i> {{ row.weight_kg || 0 }} kg</span>
              <span class="chip"><i class="mdi mdi-cube-outline"></i> {{ row.volume_m3 || 0 }} m³</span>
              <span class="chip" v-if="row.partial_load"><i class="mdi mdi-package-variant"></i> {{ $t('forms.partialLoad') }}</span>
              <span class="chip" v-if="row.has_adr"><i class="mdi mdi-alert"></i> {{ $t('forms.adr') }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column :label="$t('cargos.table.dates')" min-width="180">
          <template #default="{ row }">
            <div class="dates">
              <span><i class="mdi mdi-calendar"></i> {{ formatDate(row.pickup_date) }}</span>
              <span class="muted"><i class="mdi mdi-calendar-end"></i> {{ formatDate(row.delivery_date) }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column :label="$t('cargos.table.rate')" min-width="160">
          <template #default="{ row }">
            <div class="rate">
              <span v-if="row.rate_cash">{{ row.rate_cash }} {{ row.rate_currency?.toUpperCase() }}</span>
              <span v-else class="muted">{{ $t('cargos.onRequest') }}</span>
              <span v-if="row.without_bargain" class="tag">{{ $t('forms.withoutBargain') }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column :label="$t('common.status')" width="120">
          <template #default="{ row }">
            <el-tag :type="statusType(row.status)">{{ statusLabel(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column v-if="!embedded" :label="$t('common.actions')" width="140" fixed="right">
          <template #default="{ row, $index }">
            <el-button text size="small" @click="editCargo(row, $index)"><i class="mdi mdi-pencil"></i></el-button>
            <el-button text size="small" type="danger" @click="removeCargo($index)"><i class="mdi mdi-delete"></i></el-button>
          </template>
        </el-table-column>
      </el-table>

      <div v-if="!embedded && !cargos.length" class="empty-state">
        <i class="mdi mdi-package-variant"></i>
        <p>{{ $t('cargos.noCargosYet') }}</p>
      </div>
    </el-card>

    <!-- Add/Edit Dialog with existing form -->
    <el-dialog v-if="!embedded" v-model="dialogVisible" :title="editingIndex === -1 ? ($t('cargos.addNew') as string) : ($t('cargos.editCargo') as string)" width="860px" class="cargo-dialog">
      <div class="vehicle-add-page">
        <el-card class="vehicle-card" shadow="never">
          <!-- 1️⃣ Груз и требования к кузову / загрузке -->
          <section class="form-section">
            <h2>{{ $t('forms.cargo') }}</h2>
            <div class="grid-2">
              <el-select v-model="form.cargo_type" placeholder="Тип груза">
                <el-option v-for="(label, value) in cargoTypes" :key="value" :label="label" :value="value" />
              </el-select>
              <el-input v-model="form.cargo_name" placeholder="Наименование груза" />
            </div>

            <div class="grid-3">
              <el-input-number v-model="form.weight_kg" :min="0" label="Вес (кг)" placeholder="кг" />
              <el-input-number v-model="form.volume_m3" :min="0" step="0.5" label="Объём (м³)" />
              <el-input-number v-model="form.quantity" :min="1" label="Кол-во мест" />
            </div>

            <h3>Требования к кузову и загрузке</h3>
            <div class="grid-2">
              <el-select v-model="form.body_type" placeholder="Тип кузова">
                <el-option v-for="(label, value) in bodyTypes" :key="value" :label="label" :value="value" />
              </el-select>
              <el-checkbox-group v-model="form.load_types">
                <el-checkbox v-for="(label, value) in loadTypes" :key="value" :label="value">{{ label }}</el-checkbox>
              </el-checkbox-group>
            </div>
          </section>

          <!-- 2️⃣ Характеристики -->
          <section class="form-section">
            <h2>{{ $t('forms.specs') }}</h2>
            <div class="grid-3">
              <el-input-number v-model="form.length_m" :min="0" step="0.1" label="Длина (м)" />
              <el-input-number v-model="form.width_m" :min="0" step="0.1" label="Ширина (м)" />
              <el-input-number v-model="form.height_m" :min="0" step="0.1" label="Высота (м)" />
            </div>

            <div class="extras">
              <el-checkbox v-model="form.has_adr">ADR</el-checkbox>
              <el-checkbox v-model="form.has_tir">TIR / EKMT</el-checkbox>
              <el-checkbox v-model="form.has_gps">GPS мониторинг</el-checkbox>
              <el-checkbox v-model="form.has_lift">Гидролифт</el-checkbox>
              <el-checkbox v-model="form.has_horses">Коники</el-checkbox>
              <el-checkbox v-model="form.partial_load">Догруз</el-checkbox>
            </div>
          </section>

          <!-- 3️⃣ Маршрут -->
          <section class="form-section">
            <h2>{{ $t('forms.route') }}</h2>
            <div class="grid-2">
              <el-input v-model="form.location_from" placeholder="Откуда (населённый пункт)" />
              <el-input v-model="form.possible_unload" placeholder="Куда (возможная разгрузка)" />
            </div>
            <div class="grid-2">
              <el-input-number v-model="form.location_from_radius_km" :min="0" placeholder="Радиус откуда (км)" />
              <el-input-number v-model="form.unload_radius_km" :min="0" placeholder="Радиус разгрузки (км)" />
            </div>

            <div class="grid-2">
              <el-date-picker v-model="form.available_from" type="date" placeholder="Готов к загрузке" style="width: 100%" />
              <el-input-number v-model="form.available_days" :min="1" placeholder="Количество дней" />
            </div>
          </section>

          <!-- 4️⃣ Ставка -->
          <section class="form-section">
            <h2>{{ $t('forms.rate') }}</h2>
            <el-radio-group v-model="form.rate_mode" class="rate-mode">
              <el-radio label="has_rate">{{ $t('forms.hasRate') }}</el-radio>
              <el-radio label="request_rate">{{ $t('forms.requestRate') }}</el-radio>
            </el-radio-group>

            <div class="grid-3">
              <el-input-number v-model="form.rate_with_vat" :min="0" placeholder="С НДС, безнал" />
              <el-input-number v-model="form.rate_without_vat" :min="0" placeholder="Без НДС, безнал" />
              <el-input-number v-model="form.rate_cash" :min="0" placeholder="Наличными" />
            </div>

            <div class="grid-2">
              <el-select v-model="form.rate_currency" placeholder="Валюта">
                <el-option label="TMT" value="tmt" />
                <el-option label="RUB" value="rub" />
                <el-option label="USD" value="usd" />
                <el-option label="EUR" value="eur" />
              </el-select>

              <div>
                <el-checkbox v-model="form.pay_to_card">на карту</el-checkbox>
                <el-checkbox v-model="form.without_bargain">без торга</el-checkbox>
              </div>
            </div>
          </section>

          <!-- 5️⃣ Данные компании -->
          <section class="form-section">
            <h2>{{ $t('forms.companyData') }}</h2>
            <el-checkbox v-model="form.is_private">Я — частное лицо</el-checkbox>

            <div class="grid-2">
              <el-select v-model="form.company_type" placeholder="Тип фирмы">
                <el-option label="ООО" value="ooo" />
                <el-option label="ИП" value="ip" />
                <el-option label="Физлицо" value="fl" />
                <el-option label="Самозанятый" value="self" />
              </el-select>
              <el-input v-model="form.company_name" placeholder="Название фирмы" />
            </div>

            <div class="grid-2">
              <el-input v-model="form.city" placeholder="Город" />
              <el-input v-model="form.contact_name" placeholder="Контактное лицо" />
            </div>
            <el-input v-model="form.contact_phone" placeholder="Телефон" />
            <el-input type="textarea" v-model="form.note" :rows="3" placeholder="Примечание" />
          </section>

          <!-- 6️⃣ Продвижение -->
          <section class="form-section">
            <h2>{{ $t('forms.promotion') }}</h2>
            <el-switch v-model="form.promote_top" active-text="TOP поиска" />
            <el-switch v-model="form.stealth_mode" active-text="Stealth режим" />
          </section>
        </el-card>
      </div>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">{{ $t('common.cancel') }}</el-button>
          <el-button type="primary" @click="submitForm">
            <i class="mdi mdi-package-check"></i>
            {{ editingIndex === -1 ? ($t('forms.publishCargo') as string) : ($t('common.update') as string) }}
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useI18n } from 'vue-i18n'
import { http } from '@/api/http'

const { embedded = false } = defineProps<{ embedded?: boolean }>()

// Local cargo list (demo). Replace with API calls when backend is ready.
interface CargoItem {
  // Legacy form fields (kept for local dialog)
  cargo_type: string
  cargo_name: string
  location_from: string
  location_from_radius_km: number
  possible_unload: string
  unload_radius_km: number
  available_from: any
  available_days: number | null

  // Cargo model aligned fields for table/API
  title?: string
  pickup_address?: string
  delivery_address?: string
  pickup_date?: any
  delivery_date?: any

  // Specs
  weight_kg: number | null
  volume_m3: number | null
  quantity: number
  body_type: string
  load_types: string[]
  length_m: number | null
  width_m: number | null
  height_m: number | null
  has_adr: boolean
  has_tir: boolean
  has_gps: boolean
  has_lift: boolean
  has_horses: boolean
  partial_load: boolean

  // Rate
  rate_mode: string
  rate_with_vat: number | null
  rate_without_vat: number | null
  rate_cash: number | null
  rate_currency: 'tmt'|'rub'|'usd'|'eur'
  pay_to_card: boolean
  without_bargain: boolean

  // Company/contact
  is_private: boolean
  company_type: 'ooo'|'ip'|'fl'|'self'
  company_name: string
  city: string
  contact_name: string
  contact_phone: string
  note: string

  // Promotion/status
  promote_top: boolean
  stealth_mode: boolean
  status?: 'open'|'in_progress'|'delivered'|'cancelled'
}

const cargos = ref<CargoItem[] | any[]>([])
const dialogVisible = ref(false)
const editingIndex = ref(-1)
const searchQuery = ref('')
const statusFilter = ref('')

// Prefill from marketplace (like vehicles)
const route = useRoute()
const { t } = useI18n()
const prefilterSummary = computed(() => {
  const from = (route.query.from as string) || ''
  const to = (route.query.to as string) || ''
  const date = (route.query.date as string) || ''
  const radius = route.query.radius as string | undefined
  if (!from && !to && !date && !radius) return ''
  const parts: string[] = []
  if (from) parts.push(`${t('cargos.prefillFrom')}: ${from}`)
  if (to) parts.push(`${t('cargos.prefillTo')}: ${to}`)
  if (date) parts.push(`${t('cargos.prefillWhen')}: ${date}`)
  if (radius) parts.push(`${t('cargos.prefillRadius')}: ${radius} ${t('home.distanceKm')}`)
  return `${t('cargos.prefilledFromSearch')} — ${parts.join(' • ')}`
})


function editCargo(row: CargoItem, index: number) {
  Object.assign(form, row)
  editingIndex.value = index
  dialogVisible.value = true
}

function removeCargo(index: number) {
  cargos.value.splice(index, 1)
  ElMessage.success(t('cargos.cargoDeleted') as string)
}

const totalWeight = computed(() => cargos.value.reduce((s, c) => s + (c.weight_kg || 0), 0))
const totalVolume = computed(() => cargos.value.reduce((s, c) => s + (c.volume_m3 || 0), 0))
const openCount = computed(() => cargos.value.filter(c => (c.status || 'open') === 'open').length)

const filteredCargos = computed(() => {
  let list = cargos.value
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(c =>
      (c.title || '').toLowerCase().includes(q) ||
      (c.pickup_address || '').toLowerCase().includes(q) ||
      (c.delivery_address || '').toLowerCase().includes(q)
    )
  }
  if (statusFilter.value) list = list.filter(c => (c.status || 'open') === statusFilter.value)
  return list
})

async function loadCargos() {
  try {
    const { data } = await http.get('/cargos/')
    const list = Array.isArray(data) ? data : (data?.results || [])
    if (list && list.length > 0) {
      cargos.value = list as any
    } else {
      cargos.value = generateMockCargos()
    }
  } catch (e) {
    console.warn('Failed to load cargos, using mock data', e)
    cargos.value = generateMockCargos()
  }
}

function generateMockCargos(): CargoItem[] {
  const from = (route.query.from as string) || ''
  const to = (route.query.to as string) || ''
  const fromRadius = Number(route.query.from_radius || route.query.radius || 0)
  const toRadius = Number(route.query.to_radius || 0)
  const weightMin = route.query.weight_min ? Number(route.query.weight_min) : undefined
  const weightMax = route.query.weight_max ? Number(route.query.weight_max) : undefined
  const volumeMin = route.query.volume_min ? Number(route.query.volume_min) : undefined
  const volumeMax = route.query.volume_max ? Number(route.query.volume_max) : undefined
  const bodyType = (route.query.body_type as string) || ''
  const loadType = (route.query.load_type as string) || ''
  const rateMin = route.query.rate_min ? Number(route.query.rate_min) : undefined
  const rateMax = route.query.rate_max ? Number(route.query.rate_max) : undefined
  const hasADR = route.query.has_adr === '1' || route.query.has_adr === 'true'
  const partialLoad = route.query.partial_load === '1' || route.query.partial_load === 'true'
  const withoutBargain = route.query.without_bargain === '1' || route.query.without_bargain === 'true'
  const cargoName = (route.query.cargo_name as string) || ''

  const today = new Date()
  const cities = [from, to].filter(Boolean) as string[]
  const fallbackCities = ['Ashgabat', 'Mary', 'Balkanabat', 'Turkmenabat', 'Dashoguz']
  const cityPool = cities.length ? cities : fallbackCities

  const bodyKeys = Object.keys(bodyTypes)
  const items: CargoItem[] = []
  const count = 18
  for (let i = 0; i < count; i++) {
    const pickup = cityPool[i % cityPool.length]
    const delivery = cityPool[(i + 1) % cityPool.length]
    const d1 = new Date(today)
    d1.setDate(today.getDate() + i)
    const d2 = new Date(d1)
    d2.setDate(d1.getDate() + 2)
    const weight = 500 + (i * 150)
    const volume = +(8 + (i % 6) * 1.2).toFixed(1)
    const rate = 1000 + i * 90

    items.push({
      // legacy form props (unused in table)
      cargo_type: 'general',
      cargo_name: cargoName || `Mock Cargo ${i + 1}`,
      location_from: pickup,
      location_from_radius_km: fromRadius || 0,
      possible_unload: delivery,
      unload_radius_km: toRadius || 0,
      available_from: d1.toISOString(),
      available_days: 2,

      // table/API aligned
      title: cargoName || `Mock Cargo ${i + 1}`,
      pickup_address: pickup,
      delivery_address: delivery,
      pickup_date: d1.toISOString(),
      delivery_date: d2.toISOString(),

      // specs
      weight_kg: weight,
      volume_m3: volume,
      quantity: 1 + (i % 4),
      body_type: bodyType || bodyKeys[i % bodyKeys.length],
      load_types: [loadType || 'top'].filter(Boolean) as string[],
      length_m: null,
      width_m: null,
      height_m: null,
      has_adr: hasADR ? true : (i % 7 === 0),
      has_tir: i % 5 === 0,
      has_gps: false,
      has_lift: i % 6 === 0,
      has_horses: false,
      partial_load: partialLoad ? true : (i % 3 === 0),

      // rate
      rate_mode: 'has_rate',
      rate_with_vat: null,
      rate_without_vat: null,
      rate_cash: rate,
      rate_currency: 'tmt',
      pay_to_card: false,
      without_bargain: withoutBargain ? true : (i % 4 === 0),

      // company/contact
      is_private: false,
      company_type: 'ooo',
      company_name: 'Demo LLC',
      city: pickup,
      contact_name: 'Dispatcher',
      contact_phone: '+99365000000',
      note: '',

      // meta
      promote_top: i % 5 === 0,
      stealth_mode: false,
      status: 'open'
    })
  }

  // Apply numeric filters
  let out = items
  if (weightMin != null) out = out.filter(i => (i.weight_kg || 0) >= weightMin)
  if (weightMax != null) out = out.filter(i => (i.weight_kg || 0) <= weightMax)
  if (volumeMin != null) out = out.filter(i => (i.volume_m3 || 0) >= volumeMin)
  if (volumeMax != null) out = out.filter(i => (i.volume_m3 || 0) <= volumeMax)
  if (rateMin != null) out = out.filter(i => (i.rate_cash || 0) >= rateMin)
  if (rateMax != null) out = out.filter(i => (i.rate_cash || 0) <= rateMax)

  return out
}

onMounted(() => loadCargos())

function refresh() {
  loadCargos()
}

function statusType(s?: string) {
  switch (s || 'open') {
    case 'open': return 'info'
    case 'in_progress': return 'warning'
    case 'delivered': return 'success'
    case 'cancelled': return 'danger'
    default: return ''
  }
}
function statusLabel(s?: string) {
  switch (s || 'open') {
    case 'open': return t('cargos.open') as string
    case 'in_progress': return t('cargos.inProgress') as string
    case 'delivered': return t('cargos.delivered') as string
    case 'cancelled': return t('cargos.cancelled') as string
    default: return t('cargos.open') as string
  }
}
function formatDate(d: any) {
  if (!d) return '—'
  try { return new Date(d).toISOString().slice(0,10) } catch { return String(d) }
}

const form = reactive<CargoItem>({
  cargo_type: '',
  cargo_name: '',
  weight_kg: null,
  volume_m3: null,
  quantity: 1,
  body_type: '',
  load_types: [],
  length_m: null,
  width_m: null,
  height_m: null,
  has_adr: false,
  has_tir: false,
  has_gps: false,
  has_lift: false,
  has_horses: false,
  partial_load: false,
  location_from: '',
  location_from_radius_km: 0,
  possible_unload: '',
  unload_radius_km: 0,
  available_from: '',
  available_days: null,
  rate_mode: 'has_rate',
  rate_with_vat: null,
  rate_without_vat: null,
  rate_cash: null,
  rate_currency: 'tmt',
  pay_to_card: false,
  without_bargain: false,
  is_private: false,
  company_type: 'ooo',
  company_name: '',
  city: '',
  contact_name: '',
  contact_phone: '',
  note: '',
  promote_top: false,
  stealth_mode: false,
  status: 'open'
})

const cargoTypes: Record<string, string> = {
  general: 'Общий груз',
  fragile: 'Хрупкий',
  hazardous: 'Опасный',
  refrigerated: 'Температурный',
  oversized: 'Негабарит',
  bulk: 'Навалочный',
  liquid: 'Жидкий'
}

const bodyTypes: Record<string, string> = {
  tent: 'Тентованный',
  refrigerator: 'Рефрижератор',
  open: 'Открытый',
  isotherm: 'Изотерм',
  tank: 'Цистерна',
  container: 'Контейнеровоз',
  car_transporter: 'Автовоз',
  other: 'Другое'
}

const loadTypes: Record<string, string> = {
  top: 'Верхняя',
  side: 'Боковая',
  rear: 'Задняя',
  full_open: 'Полное открытие',
  crossbar_remove: 'Съём перекладин',
  stand_remove: 'Съём стоек'
}


function submitForm() {
  // Minimal validation
  if (!form.cargo_name || !form.location_from) {
    ElMessage.error(t('messages.required'))
    return
  }
  // Map legacy form fields to cargo fields expected by the table
  const mapped: CargoItem = {
    ...form,
    title: form.cargo_name,
    pickup_address: form.location_from,
    delivery_address: form.possible_unload,
    pickup_date: form.available_from,
    delivery_date: form.available_from,
  }
  if (editingIndex.value === -1) {
    cargos.value.unshift({ ...mapped })
    ElMessage.success(t('cargos.cargoCreated'))
  } else {
    cargos.value.splice(editingIndex.value, 1, { ...mapped })
    ElMessage.success(t('cargos.cargoUpdated'))
  }
  dialogVisible.value = false
  // No server roundtrip required for local mock
}
</script>

<style scoped>
.cargos-page { padding: 16px; }

/* Header */
.page-header { margin-bottom: 12px; }
.header-content { display: flex; justify-content: space-between; align-items: center; gap: 12px; }
.page-title { display: flex; align-items: center; gap: 8px; margin: 0; }
.page-subtitle { margin: 4px 0 0; color: #64748b; font-size: 13px; }
.add-btn { box-shadow: 0 4px 10px rgba(59,130,246,.25); }

/* Filters */
.filters-card { margin-bottom: 12px; }
.filters-container { display: flex; gap: 12px; align-items: center; }
.search-input { max-width: 420px; flex: 1; }
.status-filter { width: 200px; }
.filter-btn { }
.prefilter-banner { margin: 8px 0 12px; }

/* Stats */
.stats-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin: 8px 0 16px; }
.stat-card { display: flex; align-items: center; gap: 12px; padding: 12px; background: #fff; border-radius: 12px; box-shadow: 0 1px 2px rgba(0,0,0,.04); }
.stat-icon { width: 40px; height: 40px; display: grid; place-items: center; border-radius: 10px; color: #111827; }
.stat-icon.total { background: #eef2ff; }
.stat-icon.weight { background: #fee2e2; }
.stat-icon.volume { background: #dcfce7; }
.stat-icon.open { background: #e0f2fe; }
.stat-content .stat-value { font-weight: 700; font-size: 18px; }
.stat-content .stat-label { color: #6b7280; font-size: 12px; }

/* Table */
.table-card { border-radius: 12px; }
.modern-table :deep(.el-table__row) { transition: background .15s ease; }
.modern-table :deep(.el-table__row:hover) { background: #f8fafc; }
.cargo-cell { display: flex; flex-direction: column; }
.cargo-title { font-weight: 600; }
.cargo-meta { color: #64748b; display: flex; gap: 6px; align-items: center; font-size: 12px; }
.route { display: flex; align-items: center; gap: 8px; }
.route-meta { color: #64748b; font-size: 12px; display: flex; align-items: center; gap: 6px; }
.specs { display: flex; flex-wrap: wrap; gap: 8px; }
.chip { background: #f1f5f9; border-radius: 999px; padding: 4px 10px; font-size: 12px; display: inline-flex; align-items: center; gap: 6px; }
.dates { display: flex; flex-direction: column; gap: 2px; }
.dates .muted, .rate .muted { color: #94a3b8; }
.rate .tag { margin-left: 8px; background: #fee2e2; color: #991b1b; border-radius: 999px; padding: 2px 8px; font-size: 11px; }
.empty-state { text-align: center; color: #64748b; padding: 24px 0; }

/* Dialog/form inner layout */
.vehicle-add-page { padding: 0; }
.vehicle-card { border-radius: 8px; }
.form-section { margin-top: 14px; }
.form-section h2 { font-size: 16px; margin: 0 0 10px; color: #334155; }
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; }
.extras { display: flex; flex-wrap: wrap; gap: 12px 16px; margin-top: 8px; }
.rate-mode { margin: 8px 0 12px; }
.dialog-footer { display: flex; justify-content: flex-end; gap: 8px; }

@media (max-width: 1024px) {
  .stats-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .grid-2, .grid-3 { grid-template-columns: 1fr; }
}
</style>
