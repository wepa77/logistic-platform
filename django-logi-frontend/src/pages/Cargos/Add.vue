<template>
  <div class="cargo-add-page">
    <el-card class="cargo-card" shadow="hover">
      <h1 class="page-title">
        <i class="mdi mdi-package-variant"></i>
        {{ $t('forms.addCargo') }}
      </h1>

      <!-- Prefilter banner (from marketplace) -->
      <el-alert
        v-if="prefilterSummary"
        :title="prefilterSummary"
        type="info"
        class="prefilter-banner"
        show-icon
        :closable="false"
      />

      <!-- 1) Груз и требования к кузову / загрузке -->
      <section class="form-section">
        <h2>{{ $t('forms.cargo') }}</h2>
        <div class="grid-2">
          <el-select v-model="form.cargo_type" :placeholder="$t('forms.cargoType') as string">
            <el-option v-for="item in cargoTypes" :key="item.code" :label="dictLabel(item)" :value="item.code" />
          </el-select>
          <el-input v-model="form.cargo_name" :placeholder="$t('forms.cargoName') as string" />
        </div>

        <div class="grid-3">
          <el-input-number v-model="form.weight_kg" :min="0" label="Вес (кг)" placeholder="кг" />
          <el-input-number v-model="form.volume_m3" :min="0" step="0.5" label="Объём (м³)" />
          <el-input-number v-model="form.quantity" :min="1" label="Кол-во мест" />
        </div>
        <el-input v-model="form.packing_type" :placeholder="$t('forms.packingType') as string" />

        <h3>{{ $t('forms.requirements') }}</h3>
        <div class="grid-2">
          <el-select v-model="form.body_type" :placeholder="$t('forms.bodyType') as string">
            <el-option v-for="item in cargoBodyTypes" :key="item.code" :label="dictLabel(item)" :value="item.code" />
          </el-select>
          <el-checkbox-group v-model="form.load_types">
            <el-checkbox v-for="item in cargoLoadTypes" :key="item.code" :label="item.code">{{ dictLabel(item) }}</el-checkbox>
          </el-checkbox-group>
        </div>
      </section>

      <!-- 2) Характеристики -->
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
          <el-checkbox v-model="form.has_pneumatic">{{ $t('forms.pneumatic') }}</el-checkbox>
          <el-checkbox v-model="form.has_straps">{{ $t('forms.straps') }}</el-checkbox>
          <el-checkbox v-model="form.partial_load">Догруз</el-checkbox>
        </div>
      </section>

      <!-- 3) Маршрут -->
      <section class="form-section">
        <h2>{{ $t('forms.route') }}</h2>
        <!-- Ready status and dates -->
        <div class="grid-3">
          <el-select v-model="form.ready_status" :placeholder="$t('forms.readyStatus') as string">
            <el-option v-for="item in readyStatuses" :key="item.code" :label="dictLabel(item)" :value="item.code" />
          </el-select>
          <el-date-picker v-model="form.pickup_date" type="date" :placeholder="$t('cargos.pickupDate') as string" />
          <el-date-picker v-model="form.delivery_date" type="date" :placeholder="$t('cargos.deliveryDate') as string" />
        </div>

        <!-- Pickup and delivery addresses -->
        <div class="grid-2">
          <el-input v-model="form.pickup_address" :placeholder="$t('cargos.pickupAddress') as string" />
          <el-input v-model="form.delivery_address" :placeholder="$t('cargos.deliveryAddress') as string" />
        </div>

        <!-- Time ranges -->
        <div class="grid-2">
          <el-time-picker v-model="form.pickup_time" is-range range-separator="-" :start-placeholder="$t('forms.pickupTimeFrom') as string" :end-placeholder="$t('forms.pickupTimeTo') as string" />
          <el-time-picker v-model="form.delivery_time" is-range range-separator="-" :start-placeholder="$t('forms.deliveryTimeFrom') as string" :end-placeholder="$t('forms.deliveryTimeTo') as string" />
        </div>

        <!-- Load/unload types -->
        <div class="grid-2">
          <el-select v-model="form.load_type" :placeholder="$t('forms.loadTypes') as string">
            <el-option v-for="item in cargoLoadTypes" :key="item.code" :label="dictLabel(item)" :value="item.code" />
          </el-select>
          <el-select v-model="form.unload_type" :placeholder="$t('forms.unloadType') as string">
            <el-option v-for="item in cargoLoadTypes" :key="item.code" :label="dictLabel(item)" :value="item.code" />
          </el-select>
        </div>

        <!-- Extra flags -->
        <div class="extras">
          <el-checkbox v-model="form.full_truck">{{ $t('forms.fullTruck') }}</el-checkbox>
          <el-checkbox v-model="form.partial_load">{{ $t('forms.partialLoad') }}</el-checkbox>
          <el-checkbox v-model="form.gps_required">{{ $t('forms.gpsMonitoring') }}</el-checkbox>
          <el-checkbox v-model="form.customs_required">{{ $t('forms.customsRequired') }}</el-checkbox>
        </div>

        <el-input type="textarea" v-model="form.route_info" :rows="2" :placeholder="$t('forms.routeInfo') as string" />
      </section>

      <!-- 4) Ставка -->
      <section class="form-section">
        <h2>{{ $t('forms.rate') }}</h2>
        <el-radio-group v-model="form.rate_mode" class="rate-mode">
          <el-radio label="has_rate">{{ $t('forms.hasRate') }}</el-radio>
          <el-radio label="request_rate">{{ $t('forms.requestRate') }}</el-radio>
        </el-radio-group>

        <div class="grid-3">
          <el-input-number v-model="form.rate_with_vat" :min="0" :placeholder="$t('forms.rateWithVat') as string" />
          <el-input-number v-model="form.rate_without_vat" :min="0" :placeholder="$t('forms.rateWithoutVat') as string" />
          <el-input-number v-model="form.rate_cash" :min="0" :placeholder="$t('forms.rateCash') as string" />
        </div>

        <div class="grid-2">
          <el-select v-model="form.rate_currency" :placeholder="$t('forms.currency') as string">
            <el-option v-for="item in currencies" :key="item.code" :label="dictLabel(item)" :value="item.code" />
          </el-select>

          <div>
            <el-checkbox v-model="form.pay_to_card">{{ $t('forms.payToCard') }}</el-checkbox>
            <el-checkbox v-model="form.without_bargain">{{ $t('forms.withoutBargain') }}</el-checkbox>
            <el-checkbox v-model="form.mutual_offers_only">{{ $t('forms.mutualOffersOnly') }}</el-checkbox>
          </div>
        </div>
      </section>

      <!-- 5) Payment terms -->
      <section class="form-section">
        <h2>{{ $t('forms.paymentTerms') }}</h2>
        <div class="grid-3">
          <el-input-number v-model="form.prepayment_percent" :min="0" :max="100" :placeholder="$t('forms.prepaymentPercent') as string" />
          <el-select v-model="form.payment_method" :placeholder="$t('forms.paymentMethod') as string">
            <el-option v-for="item in cargoPaymentMethods" :key="item.code" :label="dictLabel(item)" :value="item.code" />
          </el-select>
          <el-input-number v-model="form.payment_days" :min="0" :placeholder="$t('forms.paymentDays') as string" />
        </div>
        <div class="extras">
          <el-checkbox v-model="form.payment_on_unload">{{ $t('forms.paymentOnUnload') }}</el-checkbox>
          <el-checkbox v-model="form.direct_contract">{{ $t('forms.directContract') }}</el-checkbox>
        </div>
      </section>

      <!-- 6) Данные компании -->
      <section class="form-section">
        <h2>{{ $t('forms.companyData') }}</h2>
        <el-checkbox v-model="form.is_private">{{ $t('forms.isPrivate') }}</el-checkbox>

        <div class="grid-2">
          <el-select v-model="form.company_type" :placeholder="$t('forms.companyType') as string">
            <el-option v-for="item in companyTypes" :key="item.code" :label="dictLabel(item)" :value="item.code" />
          </el-select>
          <el-input v-model="form.company_name" :placeholder="$t('forms.companyName') as string" />
        </div>

        <div class="grid-2">
          <el-input v-model="form.city" :placeholder="$t('forms.city') as string" />
          <el-input v-model="form.contact_name" :placeholder="$t('forms.contactName') as string" />
        </div>
        <el-input v-model="form.contact_phone" :placeholder="$t('forms.contactPhone') as string" />
        <el-input type="textarea" v-model="form.note" :rows="3" :placeholder="$t('forms.note') as string" />
      </section>

      <!-- 6) Продвижение -->
      <section class="form-section">
        <h2>{{ $t('forms.promotion') }}</h2>
        <el-switch v-model="form.promote_top" :active-text="$t('forms.promoteTop') as string" />
        <el-switch v-model="form.stealth_mode" :active-text="$t('forms.stealthMode') as string" />
      </section>

      <!-- Submit -->
      <div class="submit-wrapper">
        <el-button type="primary" size="large" @click="submitForm">
          <i class="mdi mdi-package-check"></i>
          {{ $t('forms.publishCargo') }}
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { reactive, computed, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useI18n } from 'vue-i18n'
import { getCargoBodyTypes, getCargoLoadTypes, getCurrencies, getCargoPaymentMethods, getCompanyTypes, getCargoTypes, getReadyStatuses } from '@/api/dicts'
import { create as createCargo } from '@/api/cargos'

interface CargoForm {
  // Cargo basics
  cargo_type: string
  cargo_name: string
  weight_kg: number | null
  volume_m3: number | null
  quantity: number
  packing_type: string
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
  has_pneumatic: boolean
  has_straps: boolean
  partial_load: boolean

  // Route and schedule (aligned with Cargo model)
  ready_status: string
  pickup_date: any
  delivery_date: any
  pickup_address: string
  delivery_address: string
  pickup_time: [any, any] | null
  delivery_time: [any, any] | null
  load_type: string
  unload_type: string
  full_truck: boolean
  gps_required: boolean
  customs_required: boolean
  route_info: string

  // Legacy marketplace radius (optional)
  location_from_radius_km: number
  unload_radius_km: number

  // Rate and payment
  rate_mode: string
  rate_with_vat: number | null
  rate_without_vat: number | null
  rate_cash: number | null
  rate_currency: 'tmt'|'rub'|'usd'|'eur'
  pay_to_card: boolean
  without_bargain: boolean
  mutual_offers_only: boolean
  prepayment_percent: number | null
  payment_method: 'cash'|'bank'|'stripe' | ''
  payment_days: number | null
  payment_on_unload: boolean
  direct_contract: boolean

  // Company/contact
  is_private: boolean
  company_type: 'ooo'|'ip'|'fl'|'self'
  company_name: string
  city: string
  contact_name: string
  contact_phone: string
  note: string

  // Promo
  promote_top: boolean
  stealth_mode: boolean
}

const form = reactive<CargoForm>({
  // Cargo basics
  cargo_type: '',
  cargo_name: '',
  weight_kg: null,
  volume_m3: null,
  quantity: 1,
  packing_type: '',
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
  has_pneumatic: false,
  has_straps: false,
  partial_load: false,

  // Route and schedule
  ready_status: 'ready',
  pickup_date: '',
  delivery_date: '',
  pickup_address: '',
  delivery_address: '',
  pickup_time: null,
  delivery_time: null,
  load_type: '',
  unload_type: '',
  full_truck: true,
  gps_required: false,
  customs_required: false,
  route_info: '',

  // Legacy optional radiuses from marketplace
  location_from_radius_km: 0,
  unload_radius_km: 0,

  // Rate and payment
  rate_mode: 'has_rate',
  rate_with_vat: null,
  rate_without_vat: null,
  rate_cash: null,
  rate_currency: 'tmt',
  pay_to_card: false,
  without_bargain: false,
  mutual_offers_only: false,
  prepayment_percent: null,
  payment_method: '',
  payment_days: null,
  payment_on_unload: false,
  direct_contract: false,

  // Company/contact
  is_private: false,
  company_type: 'ooo',
  company_name: '',
  city: '',
  contact_name: '',
  contact_phone: '',
  note: '',

  // Promo
  promote_top: false,
  stealth_mode: false,
})

const cargoTypes = ref<DictItem[]>([])
const readyStatuses = ref<DictItem[]>([])

// Dictionaries from backend
import type { DictItem } from '@/api/dicts'
const { locale } = useI18n()
const router = useRouter()
const cargoBodyTypes = ref<DictItem[]>([])
const cargoLoadTypes = ref<DictItem[]>([])
const currencies = ref<DictItem[]>([])
const cargoPaymentMethods = ref<DictItem[]>([])
const companyTypes = ref<DictItem[]>([])

function dictLabel(item: DictItem) {
  const loc = String(locale.value)
  if (loc.startsWith('ru') && item.name_ru) return item.name_ru
  if ((loc.startsWith('en') || loc.startsWith('us')) && item.name_en) return item.name_en
  return item.name_tk
}

onMounted(async () => {
  try {
    const [bt, lt, cur, pm, ct, cTypes, rStatuses] = await Promise.all([
      getCargoBodyTypes(),
      getCargoLoadTypes(),
      getCurrencies(),
      getCargoPaymentMethods(),
      getCompanyTypes(),
      getCargoTypes(),
      getReadyStatuses(),
    ])
    cargoBodyTypes.value = bt
    cargoLoadTypes.value = lt
    currencies.value = cur
    cargoPaymentMethods.value = pm
    companyTypes.value = ct
    cargoTypes.value = cTypes
    readyStatuses.value = rStatuses
  } catch (e) {
    // Non-blocking: keep selects empty on failure
    console.error('Failed to load dictionaries', e)
  }
})

// Prefill from marketplace
const route = useRoute()
if (route.query.from) form.pickup_address = String(route.query.from)
if (route.query.to) form.delivery_address = String(route.query.to)
if (route.query.date) form.pickup_date = String(route.query.date)
if (route.query.radius) form.location_from_radius_km = Number(route.query.radius)

const prefilterSummary = computed(() => {
  const from = (route.query.from as string) || ''
  const to = (route.query.to as string) || ''
  const date = (route.query.date as string) || ''
  const radius = route.query.radius as string | undefined
  if (!from && !to && !date && !radius) return ''
  const parts: string[] = []
  if (from) parts.push(`Откуда: ${from}`)
  if (to) parts.push(`Куда: ${to}`)
  if (date) parts.push(`Когда: ${date}`)
  if (radius) parts.push(`Радиус: ${radius} км`)
  return `Предзаполнено из поиска — ${parts.join(' • ')}`
})

function resetForm() {
  Object.assign(form, {
    cargo_type: '', cargo_name: '', weight_kg: null, volume_m3: null, quantity: 1,
    packing_type: '',
    body_type: '', load_types: [], length_m: null, width_m: null, height_m: null,
    has_adr: false, has_tir: false, has_gps: false, has_lift: false, has_horses: false,
    has_pneumatic: false, has_straps: false, partial_load: false,
    ready_status: 'ready', pickup_date: '', delivery_date: '', pickup_address: '', delivery_address: '',
    pickup_time: null, delivery_time: null, load_type: '', unload_type: '', full_truck: true,
    gps_required: false, customs_required: false, route_info: '',
    location_from_radius_km: 0, unload_radius_km: 0,
    rate_mode: 'has_rate', rate_with_vat: null, rate_without_vat: null, rate_cash: null, rate_currency: 'tmt',
    pay_to_card: false, without_bargain: false, mutual_offers_only: false, prepayment_percent: null, payment_method: '', payment_days: null,
    payment_on_unload: false, direct_contract: false,
    is_private: false, company_type: 'ooo', company_name: '', city: '', contact_name: '', contact_phone: '', note: '',
    promote_top: false, stealth_mode: false,
  })
}

async function submitForm() {
  if (!form.cargo_name || !form.pickup_address || !form.delivery_address) {
    ElMessage.error('Заполните обязательные поля: Наименование и адреса')
    return
  }
  
  try {
    // Map form data to ICargo structure
    const payload = {
      title: form.cargo_name,
      description: form.note || `${form.cargo_type} - ${form.packing_type}`,
      weight_kg: form.weight_kg || 0,
      volume_m3: form.volume_m3?.toString() || '0',
      pickup_address: form.pickup_address,
      delivery_address: form.delivery_address,
      pickup_date: form.pickup_date || new Date().toISOString().split('T')[0],
      delivery_date: form.delivery_date || undefined,
      price_offer: form.rate_with_vat?.toString() || form.rate_without_vat?.toString() || form.rate_cash?.toString() || undefined,
      status: 'open' as const
    }
    
    const result = await createCargo(payload)
    ElMessage.success(`Груз "${result.title}" успешно опубликован!`)
    resetForm()
    // Optionally redirect to cargo list
    setTimeout(() => router.push('/cargos'), 1500)
  } catch (error: any) {
    console.error('Failed to create cargo:', error)
    ElMessage.error(error?.response?.data?.detail || 'Ошибка при публикации груза. Проверьте подключение к API.')
  }
}
</script>

<style scoped>
.cargo-add-page { padding: 16px; }
.cargo-card { border-radius: 12px; }
.page-title { display: flex; align-items: center; gap: 8px; margin: 0 0 12px; }
.prefilter-banner { margin-bottom: 12px; }
.form-section { margin-top: 18px; }
.form-section h2 { font-size: 16px; margin: 0 0 12px; color: #334155; }
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; }
.extras { display: flex; flex-wrap: wrap; gap: 16px; margin-top: 10px; color: #334155; }
.rate-mode { margin: 8px 0 12px; }
.submit-wrapper { margin-top: 16px; display: flex; justify-content: flex-end; }
@media (max-width: 1024px) { .grid-2, .grid-3 { grid-template-columns: 1fr; } }
</style>
