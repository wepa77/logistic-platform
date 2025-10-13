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
            <el-option v-for="(label, value) in cargoTypes" :key="value" :label="label" :value="value" />
          </el-select>
          <el-input v-model="form.cargo_name" :placeholder="$t('forms.cargoName') as string" />
        </div>

        <div class="grid-3">
          <el-input-number v-model="form.weight_kg" :min="0" label="Вес (кг)" placeholder="кг" />
          <el-input-number v-model="form.volume_m3" :min="0" step="0.5" label="Объём (м³)" />
          <el-input-number v-model="form.quantity" :min="1" label="Кол-во мест" />
        </div>

        <h3>{{ $t('forms.requirements') }}</h3>
        <div class="grid-2">
          <el-select v-model="form.body_type" :placeholder="$t('forms.bodyType') as string">
            <el-option v-for="(label, value) in bodyTypes" :key="value" :label="label" :value="value" />
          </el-select>
          <el-checkbox-group v-model="form.load_types">
            <el-checkbox v-for="(label, value) in loadTypes" :key="value" :label="value">{{ label }}</el-checkbox>
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
          <el-checkbox v-model="form.partial_load">Догруз</el-checkbox>
        </div>
      </section>

      <!-- 3) Маршрут -->
      <section class="form-section">
        <h2>{{ $t('forms.route') }}</h2>
        <div class="grid-2">
          <el-input v-model="form.location_from" :placeholder="$t('forms.locationFrom') as string" />
          <el-input v-model="form.possible_unload" :placeholder="$t('forms.possibleUnload') as string" />
        </div>
        <div class="grid-2">
          <el-input-number v-model="form.location_from_radius_km" :min="0" :placeholder="$t('forms.fromRadiusKm') as string" />
          <el-input-number v-model="form.unload_radius_km" :min="0" :placeholder="$t('forms.unloadRadiusKm') as string" />
        </div>

        <div class="grid-2">
          <el-date-picker v-model="form.available_from" type="date" :placeholder="$t('forms.availableFrom') as string" style="width: 100%" />
          <el-input-number v-model="form.available_days" :min="1" :placeholder="$t('forms.availableDays') as string" />
        </div>
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
            <el-option label="TMT" value="tmt" />
            <el-option label="RUB" value="rub" />
            <el-option label="USD" value="usd" />
            <el-option label="EUR" value="eur" />
          </el-select>

          <div>
            <el-checkbox v-model="form.pay_to_card">{{ $t('forms.payToCard') }}</el-checkbox>
            <el-checkbox v-model="form.without_bargain">{{ $t('forms.withoutBargain') }}</el-checkbox>
          </div>
        </div>
      </section>

      <!-- 5) Данные компании -->
      <section class="form-section">
        <h2>{{ $t('forms.companyData') }}</h2>
        <el-checkbox v-model="form.is_private">{{ $t('forms.isPrivate') }}</el-checkbox>

        <div class="grid-2">
          <el-select v-model="form.company_type" :placeholder="$t('forms.companyType') as string">
            <el-option label="ООО" value="ooo" />
            <el-option label="ИП" value="ip" />
            <el-option label="Физлицо" value="fl" />
            <el-option label="Самозанятый" value="self" />
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
import { reactive, computed } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'

interface CargoForm {
  cargo_type: string
  cargo_name: string
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
  location_from: string
  location_from_radius_km: number
  possible_unload: string
  unload_radius_km: number
  available_from: any
  available_days: number | null
  rate_mode: string
  rate_with_vat: number | null
  rate_without_vat: number | null
  rate_cash: number | null
  rate_currency: 'tmt'|'rub'|'usd'|'eur'
  pay_to_card: boolean
  without_bargain: boolean
  is_private: boolean
  company_type: 'ooo'|'ip'|'fl'|'self'
  company_name: string
  city: string
  contact_name: string
  contact_phone: string
  note: string
  promote_top: boolean
  stealth_mode: boolean
}

const form = reactive<CargoForm>({
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
})

const cargoTypes: Record<string, string> = {
  general: 'Общий груз',
  fragile: 'Хрупкий',
  hazardous: 'Опасный',
  refrigerated: 'Температурный',
  oversized: 'Негабарит',
  bulk: 'Навалочный',
  liquid: 'Жидкий',
}

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
  top: 'Верхняя',
  side: 'Боковая',
  rear: 'Задняя',
  full_open: 'Полное открытие',
  crossbar_remove: 'Съём перекладин',
  stand_remove: 'Съём стоек',
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
    cargo_type: '', cargo_name: '', weight_kg: null, volume_m3: null, quantity: 1,
    body_type: '', load_types: [], length_m: null, width_m: null, height_m: null,
    has_adr: false, has_tir: false, has_gps: false, has_lift: false, has_horses: false, partial_load: false,
    location_from: '', location_from_radius_km: 0, possible_unload: '', unload_radius_km: 0,
    available_from: '', available_days: null,
    rate_mode: 'has_rate', rate_with_vat: null, rate_without_vat: null, rate_cash: null, rate_currency: 'tmt',
    pay_to_card: false, without_bargain: false,
    is_private: false, company_type: 'ooo', company_name: '', city: '', contact_name: '', contact_phone: '', note: '',
    promote_top: false, stealth_mode: false,
  })
}

function submitForm() {
  if (!form.cargo_name || !form.location_from) {
    ElMessage.error('Заполните обязательные поля: Наименование груза и Откуда')
    return
  }
  // Here you would call backend API to create cargo
  ElMessage.success('Груз опубликован (демо)')
  resetForm()
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
