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
            <el-option v-for="(label, value) in bodyTypes" :key="value" :label="label" :value="value" />
          </el-select>
          <el-checkbox-group v-model="form.load_types">
            <el-checkbox v-for="(label, value) in loadTypes" :key="value" :label="value">{{ label }}</el-checkbox>
          </el-checkbox-group>
        </div>

        <div class="extras">
          <el-checkbox v-model="form.half_trailer">Полуприцеп</el-checkbox>
          <el-checkbox v-model="form.is_truck">Грузовик</el-checkbox>
          <el-checkbox v-model="form.is_scene">Сцепка</el-checkbox>
        </div>

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
          <el-input v-model="form.location_from" placeholder="Откуда (населённый пункт)" />
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

      <!-- 5) Данные компании -->
      <section class="form-section">
        <h2>Данные компании</h2>
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
          Опубликовать машину
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { reactive, computed } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'

const form = reactive({
  // Body + loading
  body_type: '',
  load_types: [] as string[],
  half_trailer: true,
  is_truck: false,
  is_scene: false,
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

const bodyTypes: Record<string, string> = {
  tent: 'Тентованный',
  refrigerator: 'Рефрижератор',
  open: 'Открытый',
  isotherm: 'Изотерм',
  tank: 'Цистерна',
  container: 'Контейнеровоз',
  car_transporter: 'Автовоз',
  other: 'Другое',
}

const loadTypes: Record<string, string> = {
  back: 'задняя',
  side: 'боковая',
  top: 'верхняя',
  removable_racks: 'со съемными стойками',
  removable_crossbars: 'со снятием поперечных перекладин',
  removable_racks_and_crossbars: 'со снятием стоек',
}

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
    body_type: '', load_types: [], half_trailer: true, is_truck: false, is_scene: false,
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
  if (!form.body_type || !form.location_from) {
    ElMessage.error('Заполните обязательные поля: Тип кузова и Откуда')
    return
  }
  // Here you can call your API to create vehicle offer
  ElMessage.success('Машина опубликована (демо)')
  resetForm()
}
</script>

<style scoped>
.vehicle-add-page { padding: 16px; }
.vehicle-card { border-radius: 12px; }
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
