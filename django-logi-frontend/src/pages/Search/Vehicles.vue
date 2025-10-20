<template>
  <div class="search-page">
    <div class="toolbar">
      <h1 class="title"><i class="mdi mdi-magnify"></i> {{ $t('nav.searchVehicles') }}</h1>
      <p class="subtitle">{{$t('marketplace.heroSubtitle')}}</p>
    </div>

    <!-- ATI-like search form for vehicles (only necessary fields) -->
    <el-card class="filters-card" shadow="never">
      <div class="filters-grid">
        <el-form :inline="true" @submit.prevent>
          <!-- Row 1: From/Radius/To/Date -->
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
            <el-form-item :label="$t('home.dateLabel') as string">
              <el-date-picker v-model="form.date" type="date" :placeholder="$t('home.datePlaceholder') as string" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="applyFilters"><i class="mdi mdi-magnify"></i> {{ $t('home.findVehicles') }}</el-button>
            </el-form-item>
          </div>

          <!-- Row 2: Body/load types and dimensions -->
          <div class="row">
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
            <el-form-item :label="$t('vehicles.capacity') as string">
              <div class="range">
                <el-input-number v-model="form.capacityMin" :min="0" :step="500" />
                <span class="dash">—</span>
                <el-input-number v-model="form.capacityMax" :min="0" :step="500" />
              </div>
            </el-form-item>
            <el-form-item :label="$t('vehicles.volume') as string">
              <div class="range">
                <el-input-number v-model="form.volumeMin" :min="0" :step="0.5" />
                <span class="dash">—</span>
                <el-input-number v-model="form.volumeMax" :min="0" :step="0.5" />
              </div>
            </el-form-item>
          </div>

          <!-- Row 3: Rates and toggles -->
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
              <el-checkbox v-model="form.hasADR">{{ $t('forms.adr') }}</el-checkbox>
              <el-checkbox v-model="form.hasLift">{{ $t('forms.hydrolift') }}</el-checkbox>
              <el-checkbox v-model="form.hasHorses">{{ $t('forms.stakes') }}</el-checkbox>
              <el-checkbox v-model="form.hasGPS">{{ $t('forms.gpsMonitoring') }}</el-checkbox>
              <el-checkbox v-model="form.partialLoad">{{ $t('forms.partialLoad') }}</el-checkbox>
              <el-checkbox v-model="form.withoutBargain">{{ $t('forms.withoutBargain') }}</el-checkbox>
              <el-checkbox v-model="form.payToCard">{{ $t('forms.payToCard') }}</el-checkbox>
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
    <VehiclesPage :key="listKey" :embedded="true" />
  </div>
</template>
<script lang="ts" setup>
import { reactive, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import VehiclesPage from '@/pages/Vehicles/index.vue'

const router = useRouter()
const route = useRoute()

const form = reactive({
  from: (route.query.from as string) || '',
  to: (route.query.to as string) || '',
  fromRadius: route.query.from_radius ? Number(route.query.from_radius) : 0,
  toRadius: route.query.to_radius ? Number(route.query.to_radius) : 0,
  date: (route.query.date as string) || '',

  bodyType: (route.query.body_type as string) || '',
  loadType: (route.query.load_type as string) || '',

  capacityMin: route.query.capacity_min ? Number(route.query.capacity_min) : undefined as number | undefined,
  capacityMax: route.query.capacity_max ? Number(route.query.capacity_max) : undefined as number | undefined,
  volumeMin: route.query.volume_min ? Number(route.query.volume_min) : undefined as number | undefined,
  volumeMax: route.query.volume_max ? Number(route.query.volume_max) : undefined as number | undefined,

  rateMin: route.query.rate_min ? Number(route.query.rate_min) : undefined as number | undefined,
  rateMax: route.query.rate_max ? Number(route.query.rate_max) : undefined as number | undefined,
  currency: (route.query.currency as string) || '',

  hasADR: route.query.has_adr === '1' || route.query.has_adr === 'true',
  hasLift: route.query.has_lift === '1' || route.query.has_lift === 'true',
  hasHorses: route.query.has_horses === '1' || route.query.has_horses === 'true',
  hasGPS: route.query.has_gps === '1' || route.query.has_gps === 'true',
  partialLoad: route.query.partial_load === '1' || route.query.partial_load === 'true',
  withoutBargain: route.query.without_bargain === '1' || route.query.without_bargain === 'true',
  payToCard: route.query.pay_to_card === '1' || route.query.pay_to_card === 'true',

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

  if (form.bodyType) q.body_type = form.bodyType
  if (form.loadType) q.load_type = form.loadType

  if (form.capacityMin != null) q.capacity_min = String(form.capacityMin)
  if (form.capacityMax != null) q.capacity_max = String(form.capacityMax)
  if (form.volumeMin != null) q.volume_min = String(form.volumeMin)
  if (form.volumeMax != null) q.volume_max = String(form.volumeMax)

  if (form.rateMin != null) q.rate_min = String(form.rateMin)
  if (form.rateMax != null) q.rate_max = String(form.rateMax)
  if (form.currency) q.currency = form.currency

  if (form.hasADR) q.has_adr = '1'
  if (form.hasLift) q.has_lift = '1'
  if (form.hasHorses) q.has_horses = '1'
  if (form.hasGPS) q.has_gps = '1'
  if (form.partialLoad) q.partial_load = '1'
  if (form.withoutBargain) q.without_bargain = '1'
  if (form.payToCard) q.pay_to_card = '1'

  if (form.addedWhen && form.addedWhen !== 'any') q.added = form.addedWhen

  router.push({ query: q })
  listKey.value += 1
}

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
