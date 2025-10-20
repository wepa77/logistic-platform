<template>
  <div class="search-page">
    <div class="toolbar">
      <h1 class="title"><i class="mdi mdi-magnify"></i> {{ $t('nav.searchCargos') }}</h1>
      <p class="subtitle">{{$t('marketplace.heroSubtitle')}}</p>
    </div>

    <!-- Search form (compact, inspired by ATI) -->
    <el-card class="filters-card" shadow="never">
      <div class="filters-grid">
        <!-- Row 1: From / Radius / To / Radius -->
        <el-form :inline="true" @submit.prevent>
          <div class="row">
            <el-form-item :label="$t('home.fromLabel') as string">
              <el-input v-model="form.from" :placeholder="$t('home.fromPlaceholder') as string" clearable />
            </el-form-item>
            <el-form-item :label="$t('home.radiusLabel') as string">
              <el-input-number v-model="form.fromRadius" :min="0" :max="1000" :step="10" />
            </el-form-item>
            <el-form-item :label="$t('home.toLabel') as string">
              <el-input v-model="form.to" :placeholder="$t('home.toPlaceholder') as string" clearable />
            </el-form-item>
            <el-form-item :label="$t('home.radiusLabel') as string">
              <el-input-number v-model="form.toRadius" :min="0" :max="1000" :step="10" />
            </el-form-item>
            <el-form-item :label="$t('home.dateLabel') as string">
              <el-date-picker v-model="form.date" type="date" :placeholder="$t('home.datePlaceholder') as string" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="applyFilters"><i class="mdi mdi-magnify"></i> {{ $t('home.findCargos') }}</el-button>
            </el-form-item>
          </div>

          <!-- Row 2: Weight/Volume ranges -->
          <div class="row">
            <el-form-item :label="$t('forms.weightKg') as string">
              <div class="range">
                <el-input-number v-model="form.weightMin" :min="0" :step="0.5" />
                <span class="dash">—</span>
                <el-input-number v-model="form.weightMax" :min="0" :step="0.5" />
              </div>
            </el-form-item>
            <el-form-item :label="$t('forms.volumeM3') as string">
              <div class="range">
                <el-input-number v-model="form.volumeMin" :min="0" :step="0.5" />
                <span class="dash">—</span>
                <el-input-number v-model="form.volumeMax" :min="0" :step="0.5" />
              </div>
            </el-form-item>
            <el-form-item :label="$t('forms.bodyType') as string">
              <el-select v-model="form.bodyType" clearable filterable style="min-width: 180px">
                <el-option v-for="(label, value) in bodyTypes" :key="value" :label="label" :value="value" />
              </el-select>
            </el-form-item>
            <el-form-item :label="$t('forms.loadTypes') as string">
              <el-select v-model="form.loadType" clearable filterable style="min-width: 180px">
                <el-option v-for="(label, value) in loadTypes" :key="value" :label="label" :value="value" />
              </el-select>
            </el-form-item>
          </div>

          <!-- Row 3: Payment and additional toggles -->
          <div class="row">
            <el-form-item :label="$t('offers.price') as string">
              <el-input-number v-model="form.rateMin" :min="0" :step="50" placeholder="min" />
              <span class="dash">—</span>
              <el-input-number v-model="form.rateMax" :min="0" :step="50" placeholder="max" />
            </el-form-item>
            <el-form-item :label="$t('forms.currency') as string">
              <el-select v-model="form.currency" clearable style="width: 120px">
                <el-option label="TMT" value="tmt" />
                <el-option label="RUB" value="rub" />
                <el-option label="USD" value="usd" />
                <el-option label="EUR" value="eur" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-checkbox v-model="form.hasADR">ADR</el-checkbox>
              <el-checkbox v-model="form.partialLoad">{{ $t('forms.partialLoad') }}</el-checkbox>
              <el-checkbox v-model="form.withoutBargain">{{ $t('forms.withoutBargain') }}</el-checkbox>
            </el-form-item>
            <el-form-item :label="$t('common.date') as string">
              <el-select v-model="form.addedWhen" style="min-width: 180px">
                <el-option :label="$t('filters.anytime') as string" value="any" />
                <el-option :label="$t('filters.today') as string" value="today" />
                <el-option :label="$t('filters.last3Days') as string" value="3d" />
                <el-option :label="$t('filters.last7Days') as string" value="7d" />
              </el-select>
            </el-form-item>
          </div>
        </el-form>
      </div>
    </el-card>

    <!-- Results list -->
    <CargosPage :key="listKey" :embedded="true" />
  </div>
</template>
<script lang="ts" setup>
import { reactive, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import CargosPage from '@/pages/Cargos/index.vue'

const router = useRouter()
const route = useRoute()

const form = reactive({
  from: (route.query.from as string) || '',
  to: (route.query.to as string) || '',
  fromRadius: route.query.from_radius ? Number(route.query.from_radius) : 0,
  toRadius: route.query.to_radius ? Number(route.query.to_radius) : 0,
  date: (route.query.date as string) || '',
  weightMin: route.query.weight_min ? Number(route.query.weight_min) : undefined as number | undefined,
  weightMax: route.query.weight_max ? Number(route.query.weight_max) : undefined as number | undefined,
  volumeMin: route.query.volume_min ? Number(route.query.volume_min) : undefined as number | undefined,
  volumeMax: route.query.volume_max ? Number(route.query.volume_max) : undefined as number | undefined,
  bodyType: (route.query.body_type as string) || '',
  loadType: (route.query.load_type as string) || '',
  rateMin: route.query.rate_min ? Number(route.query.rate_min) : undefined as number | undefined,
  rateMax: route.query.rate_max ? Number(route.query.rate_max) : undefined as number | undefined,
  currency: (route.query.currency as string) || '',
  hasADR: route.query.has_adr === '1' || route.query.has_adr === 'true',
  partialLoad: route.query.partial_load === '1' || route.query.partial_load === 'true',
  withoutBargain: route.query.without_bargain === '1' || route.query.without_bargain === 'true',
  prepaid: route.query.prepaid === '1' || route.query.prepaid === 'true',
  cash: route.query.pay_cash === '1' || route.query.pay_cash === 'true',
  cashlessVAT: route.query.pay_cashless_vat === '1' || route.query.pay_cashless_vat === 'true',
  cashlessNoVAT: route.query.pay_cashless_no_vat === '1' || route.query.pay_cashless_no_vat === 'true',
  paymentOnUnload: route.query.payment_on_unload === '1' || route.query.payment_on_unload === 'true',
  cargoName: (route.query.cargo_name as string) || '',
  addedWhen: (route.query.added as string) || 'any'
})

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

const listKey = ref(0)

function applyFilters() {
  const q: Record<string, any> = {}
  if (form.from) q.from = form.from
  if (form.to) q.to = form.to
  if (form.fromRadius) q.from_radius = String(form.fromRadius)
  if (form.toRadius) q.to_radius = String(form.toRadius)
  if (form.date) q.date = typeof form.date === 'string' ? form.date : new Date(form.date as any).toISOString().slice(0,10)
  if (form.weightMin != null) q.weight_min = String(form.weightMin)
  if (form.weightMax != null) q.weight_max = String(form.weightMax)
  if (form.volumeMin != null) q.volume_min = String(form.volumeMin)
  if (form.volumeMax != null) q.volume_max = String(form.volumeMax)
  if (form.bodyType) q.body_type = form.bodyType
  if (form.loadType) q.load_type = form.loadType
  if (form.rateMin != null) q.rate_min = String(form.rateMin)
  if (form.rateMax != null) q.rate_max = String(form.rateMax)
  if (form.currency) q.currency = form.currency
  if (form.hasADR) q.has_adr = '1'
  if (form.partialLoad) q.partial_load = '1'
  if (form.withoutBargain) q.without_bargain = '1'
  if (form.prepaid) q.prepaid = '1'
  if (form.cash) q.pay_cash = '1'
  if (form.cashlessVAT) q.pay_cashless_vat = '1'
  if (form.cashlessNoVAT) q.pay_cashless_no_vat = '1'
  if (form.paymentOnUnload) q.payment_on_unload = '1'
  if (form.cargoName) q.cargo_name = form.cargoName
  if (form.addedWhen && form.addedWhen !== 'any') q.added = form.addedWhen

  router.push({ query: q })
  // Force results to refresh (CargosPage reads route.query on mount)
  listKey.value += 1
}

// If user navigates with back/forward, refresh results
watch(() => route.query, () => { listKey.value += 1 })
</script>
<style scoped>
.search-page{padding:12px}
.title{display:flex;align-items:center;gap:8px;margin:0}
.subtitle{color:#64748b;margin:4px 0 12px}

.filters-card{margin-bottom:12px}
.filters-grid{display:flex;flex-direction:column;gap:10px}
.row{display:flex;flex-wrap:wrap;gap:12px;align-items:center}
.range{display:flex;align-items:center;gap:6px}
.dash{color:#94a3b8}
</style>
