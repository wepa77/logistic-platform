<template>
  <div class="vehicle-add-page">
    <el-card class="vehicle-card" shadow="hover">
      <h1 class="page-title">
        <i class="mdi mdi-truck"></i>
        {{ $t('forms.addVehicle') }}
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

      <!-- 1) Тип кузова и загрузка -->
      <section class="form-section">
        <h2>{{ $t('forms.requirements') }}</h2>
        <div class="grid-2">
          <el-select v-model="form.body_type" :placeholder="$t('forms.bodyType') as string">
            <el-option v-for="item in vehicleBodyTypes" :key="item.code" :label="dictLabel(item)" :value="item.code" />
          </el-select>
          <el-checkbox-group v-model="form.load_types">
            <el-checkbox v-for="item in vehicleLoadTypes" :key="item.code" :label="item.code">{{ dictLabel(item) }}</el-checkbox>
          </el-checkbox-group>
        </div>

        <el-select v-model="form.truck_category" placeholder="Тип транспорта">
            <el-option v-for="item in vehicleTruckCategories" :key="item.code" :label="dictLabel(item)" :value="item.code" />
          </el-select>

        <el-select v-model="form.body_load_requirements" multiple placeholder="Требования к кузову и загрузке" style="margin-top: 12px;">
          <el-option v-for="item in bodyLoadRequirements" :key="item.code" :label="dictLabel(item)" :value="item.code" />
        </el-select>

        <div class="extras">
          <el-checkbox v-model="form.has_lift">{{ $t('forms.hydrolift') }}</el-checkbox>
          <el-checkbox v-model="form.has_gps">{{ $t('forms.gpsMonitoring') }}</el-checkbox>
          <el-checkbox v-model="form.has_adr">{{ $t('forms.adr') }}</el-checkbox>
          <el-checkbox v-model="form.has_tir">{{ $t('forms.tir') }}</el-checkbox>
          <el-checkbox v-model="form.has_horses">{{ $t('forms.stakes') }}</el-checkbox>
          <el-checkbox v-model="form.partial_load">{{ $t('forms.partialLoad') }}</el-checkbox>
        </div>
      </section>

      <!-- 2) Грузоподъемность, объем, габариты -->
      <section class="form-section">
        <h2>Характеристики</h2>
        <div class="grid-3">
          <el-input-number v-model="form.capacity_kg" :min="0" label="Грузоподъёмность (кг)" placeholder="кг" />
          <el-input-number v-model="form.volume_m3" :min="0" step="0.5" label="Объём кузова (м³)" />
          <div />
        </div>
        <div class="grid-3">
          <el-input-number v-model="form.length_m" :min="0" step="0.1" label="Длина (м)" />
          <el-input-number v-model="form.width_m" :min="0" step="0.1" label="Ширина (м)" />
          <el-input-number v-model="form.height_m" :min="0" step="0.1" label="Высота (м)" />
        </div>
      </section>

      <!-- 3) Когда, откуда/разгрузка -->
      <section class="form-section">
        <h2>Маршрут и даты</h2>
        <div class="grid-2">
          <el-date-picker v-model="form.available_from" type="date" placeholder="Готов к загрузке" style="width: 100%" />
          <el-input-number v-model="form.available_days" :min="1" placeholder="Сколько дней" />
        </div>
        <div class="grid-2">
          <el-input v-model="form.location_from" :placeholder="$t('forms.locationFrom') as string" />
          <el-input v-model="form.possible_unload" placeholder="Возможная разгрузка" />
        </div>
        <div class="grid-2">
          <el-input-number v-model="form.location_from_radius_km" :min="0" placeholder="Радиус откуда (км)" />
          <el-input-number v-model="form.unload_radius_km" :min="0" placeholder="Радиус разгрузки (км)" />
        </div>
      </section>

      <!-- 4) Ставка -->
      <section class="form-section">
        <h2>Ставка</h2>
        <el-radio-group v-model="form.rate_mode" class="rate-mode">
          <el-radio label="has_rate">Есть ставка</el-radio>
          <el-radio label="request_rate">Запросить ставку</el-radio>
        </el-radio-group>
        <div class="grid-3">
          <el-input-number v-model="form.rate_with_vat" :min="0" placeholder="С НДС, безнал" />
          <el-input-number v-model="form.rate_without_vat" :min="0" placeholder="Без НДС, безнал" />
          <el-input-number v-model="form.rate_cash" :min="0" placeholder="Наличными" />
        </div>
        <div class="grid-2">
          <el-select v-model="form.rate_currency" placeholder="Валюта">
            <el-option v-for="item in currencies" :key="item.code" :label="dictLabel(item)" :value="item.code" />
          </el-select>
          <div>
            <el-checkbox v-model="form.pay_to_card">на карту</el-checkbox>
            <el-checkbox v-model="form.without_bargain">без торга</el-checkbox>
          </div>
        </div>
      </section>

      <!-- 5) Данные компании -->
      <section class="form-section">
        <h2>Данные компании</h2>
        <el-checkbox v-model="form.is_private">Я — частное лицо</el-checkbox>
        <div class="grid-2">
          <el-select v-model="form.company_type" placeholder="Тип фирмы">
            <el-option v-for="item in companyTypes" :key="item.code" :label="dictLabel(item)" :value="item.code" />
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

      <!-- 6) Продвижение -->
      <section class="form-section">
        <h2>Продвижение</h2>
        <el-switch v-model="form.promote_top" active-text="Поднять в ТОП" />
        <el-switch v-model="form.stealth_mode" active-text="Stealth режим" />
      </section>

      <!-- Submit -->
      <div class="submit-wrapper">
        <el-button type="primary" size="large" @click="submitForm">
          <i class="mdi mdi-truck-check"></i>
          {{ $t('forms.publishVehicle') }}
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { reactive, computed, ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useI18n } from 'vue-i18n'
import { getVehicleBodyTypes, getVehicleLoadTypes, getCurrencies, getCompanyTypes, getVehicleTruckCategories, getBodyLoadRequirements } from '@/api/dicts'
import type { DictItem } from '@/api/dicts'

const form = reactive({
  // Body + loading
  body_type: '',
  load_types: [] as string[],
  truck_category: 'truck',
  body_load_requirements: [] as string[],
  has_lift: false,
  has_gps: false,
  has_adr: false,
  has_tir: false,
  has_horses: false,
  partial_load: false,
  // Specs
  capacity_kg: null as number | null,
  volume_m3: null as number | null,
  length_m: null as number | null,
  width_m: null as number | null,
  height_m: null as number | null,
  // Route + availability
  available_from: '',
  available_days: null as number | null,
  location_from: '',
  location_from_radius_km: 0,
  possible_unload: '',
  unload_radius_km: 0,
  // Rates
  rate_mode: 'has_rate',
  rate_with_vat: null as number | null,
  rate_without_vat: null as number | null,
  rate_cash: null as number | null,
  rate_currency: 'tmt',
  pay_to_card: false,
  without_bargain: false,
  // Company
  is_private: false,
  company_type: 'ooo',
  company_name: '',
  city: '',
  contact_name: '',
  contact_phone: '',
  note: '',
  // Promotion
  promote_top: false,
  stealth_mode: false,
})

const { locale } = useI18n()
const vehicleBodyTypes = ref<DictItem[]>([])
const vehicleLoadTypes = ref<DictItem[]>([])
const vehicleTruckCategories = ref<DictItem[]>([])
const currencies = ref<DictItem[]>([])
const companyTypes = ref<DictItem[]>([])
const bodyLoadRequirements = ref<DictItem[]>([])

function dictLabel(item: DictItem) {
  const loc = String(locale.value)
  if (loc.startsWith('ru') && item.name_ru) return item.name_ru
  if ((loc.startsWith('en') || loc.startsWith('us')) && item.name_en) return item.name_en
  return item.name_tk
}

onMounted(async () => {
  try {
    const [bt, lt, cats, cur, ct, blr] = await Promise.all([
      getVehicleBodyTypes(),
      getVehicleLoadTypes(),
      getVehicleTruckCategories(),
      getCurrencies(),
      getCompanyTypes(),
      getBodyLoadRequirements(),
    ])
    vehicleBodyTypes.value = bt
    vehicleLoadTypes.value = lt
    vehicleTruckCategories.value = cats
    currencies.value = cur
    companyTypes.value = ct
    bodyLoadRequirements.value = blr
  } catch (e) {
    console.error('Failed to load vehicle dictionaries', e)
  }
})

// Prefill from marketplace
const route = useRoute()
if (route.query.from) form.location_from = String(route.query.from)
if (route.query.to) form.possible_unload = String(route.query.to)
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
    body_type: '', load_types: [], truck_category: 'truck', body_load_requirements: [],
    has_lift: false, has_gps: false, has_adr: false, has_tir: false, has_horses: false, partial_load: false,
    capacity_kg: null, volume_m3: null, length_m: null, width_m: null, height_m: null,
    available_from: '', available_days: null,
    location_from: '', location_from_radius_km: 0, possible_unload: '', unload_radius_km: 0,
    rate_mode: 'has_rate', rate_with_vat: null, rate_without_vat: null, rate_cash: null, rate_currency: 'tmt', pay_to_card: false, without_bargain: false,
    is_private: false, company_type: 'ooo', company_name: '', city: '', contact_name: '', contact_phone: '', note: '',
    promote_top: false, stealth_mode: false,
  })
}

function submitForm() {
  // Minimal validation
  if (!form.location_from) {
    ElMessage.error('Заполните обязательные поля: Откуда')
    return
  }
  // Here you can call your API to create vehicle offer
  ElMessage.success('Машина опубликована (демо)')
  resetForm()
}
</script>

<style scoped>/* ============================================
 ✅ Global Layout
============================================ */
.vehicle-add-page {
  padding: 16px;
  max-width: 1100px;
  margin: 0 auto;
}

.vehicle-card {
  border-radius: 16px;
  padding: 20px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 24px;
  margin-bottom: 14px;
}

/* ============================================
 ✅ Base Grids
============================================ */
.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
}

.extras {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-top: 12px;
}

/* ============================================
 ✅ Responsive Behavior
============================================ */

/* ---------- Large Tablets/Laptops: 1024px ↓ ---------- */
@media (max-width: 1024px) {
  .grid-2 {
    grid-template-columns: 1fr;
  }

  .grid-3 {
    grid-template-columns: 1fr 1fr;
  }
}

/* ---------- Tablets: 768px ↓ ---------- */
@media (max-width: 768px) {
  .page-title {
    font-size: 20px;
  }

  .vehicle-card {
    padding: 16px;
  }

  .grid-3 {
    grid-template-columns: 1fr;
  }

  .extras {
    gap: 12px;
  }

  /* Input groups full-width */
  .el-select,
  .el-input,
  .el-input-number,
  .el-date-picker {
    width: 100% !important;
  }

  .submit-wrapper {
    justify-content: center;
  }
}

/* ---------- Phones: 480px ↓ ---------- */
@media (max-width: 480px) {

  .page-title {
    font-size: 18px;
    gap: 6px;
  }

  .form-section h2 {
    font-size: 14px;
  }

  .grid-2,
  .grid-3 {
    grid-template-columns: 1fr;
    gap: 12px;
  }

  .rate-mode {
    flex-direction: column;
  }

  .extras {
    gap: 10px;
  }

  .submit-wrapper {
    margin-top: 20px;
  }

  .submit-wrapper .el-button {
    width: 100%;
    padding: 14px 0;
    font-size: 16px;
  }
}

/* ---------- Smallest Phones: 360px ↓ ---------- */
@media (max-width: 360px) {

  .page-title {
    font-size: 16px;
  }

  .vehicle-card {
    padding: 12px;
  }

  .extras {
    gap: 8px;
  }

  .form-section h2 {
    font-size: 13px;
  }

  .submit-wrapper .el-button {
    font-size: 15px;
  }
}

</style>
