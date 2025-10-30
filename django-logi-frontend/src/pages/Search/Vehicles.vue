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
            <el-form-item>
              <el-button text type="primary" class="toggle-adv" @click="showAdvanced = !showAdvanced">
                <i :class="showAdvanced ? 'mdi mdi-chevron-up' : 'mdi mdi-chevron-down'"></i>
                <span>Фильтры</span>
              </el-button>
            </el-form-item>
          </div>

          <el-collapse-transition>
            <div v-show="showAdvanced" class="adv-grid">
              <!-- Col: Дата погрузки -->
              <div class="section">
                <div class="sect-title">Дата погрузки</div>
                <el-select v-model="form.addedWhen" size="small" style="width: 180px">
                  <el-option :label="$t('filters.anytime') as string" value="any" />
                  <el-option :label="$t('filters.today') as string" value="today" />
                  <el-option :label="$t('filters.last3Days') as string" value="3d" />
                  <el-option :label="$t('filters.last7Days') as string" value="7d" />
                </el-select>
                <el-link type="primary" :underline="false" class="mt6">Указать точные даты</el-link>
              </div>

              <!-- Col: Тип кузова -->
              <div class="section">
                <div class="sect-title">Тип кузова</div>
                <el-checkbox-group v-model="bodyTypeGroup" class="checklist">
                  <el-checkbox v-for="(label, value) in bodyTypes" :key="value" :label="value">{{ label }}</el-checkbox>
                </el-checkbox-group>
                <el-link type="primary" :underline="false" class="mt6">Все типы</el-link>
              </div>

              <!-- Col: Тип загрузки -->
              <div class="section">
                <div class="sect-title">Тип загрузки</div>
                <el-checkbox-group v-model="loadTypeGroup" class="checklist">
                  <el-checkbox v-for="(label, value) in loadTypes" :key="value" :label="value">{{ label }}</el-checkbox>
                </el-checkbox-group>
                <el-link type="primary" :underline="false" class="mt6">Все типы</el-link>
              </div>

              <!-- Col: Оплата -->
              <div class="section">
                <div class="sect-title">Оплата</div>
                <div class="row mini">
                  <el-form-item>
                    <el-input-number v-model="form.rateMin" :min="0" :step="50" placeholder="от" />
                    <span class="dash">—</span>
                    <el-input-number v-model="form.rateMax" :min="0" :step="50" placeholder="до" />
                  </el-form-item>
                </div>
                <el-select v-model="form.currency" size="small" style="width: 120px">
                  <el-option label="TMT" value="tmt" />
                  <el-option label="RUB" value="rub" />
                  <el-option label="USD" value="usd" />
                  <el-option label="EUR" value="eur" />
                </el-select>
                <div class="checklist mt6">
                  <el-checkbox v-model="form.payToCard">{{ $t('forms.payToCard') }}</el-checkbox>
                  <el-checkbox v-model="form.withoutBargain">{{ $t('forms.withoutBargain') }}</el-checkbox>
                </div>
              </div>

              <!-- Col: Доп. параметры -->
              <div class="section">
                <div class="sect-title">Доп. параметры</div>
                <div class="checklist">
                  <el-checkbox v-model="form.hasLift">{{ $t('forms.hydrolift') }}</el-checkbox>
                  <el-checkbox v-model="form.hasHorses">{{ $t('forms.stakes') }}</el-checkbox>
                  <el-checkbox v-model="form.hasGPS">{{ $t('forms.gpsMonitoring') }}</el-checkbox>
                  <el-checkbox v-model="form.partialLoad">{{ $t('forms.partialLoad') }}</el-checkbox>
                  <el-checkbox v-model="form.hasADR">Опасные грузы (ADR)</el-checkbox>
                </div>
              </div>

              <!-- Col: Габариты и догруз -->
              <div class="section">
                <div class="sect-title">Габариты и догруз</div>
                <div class="dims-grid">
                  <el-form-item :label="$t('forms.lengthM') as string">
                    <div class="range">
                      <el-input-number v-model="form.lengthMin" :min="0" :step="0.1" />
                      <span class="dash">—</span>
                      <el-input-number v-model="form.lengthMax" :min="0" :step="0.1" />
                    </div>
                  </el-form-item>
                  <el-form-item :label="$t('forms.widthM') as string">
                    <div class="range">
                      <el-input-number v-model="form.widthMin" :min="0" :step="0.1" />
                      <span class="dash">—</span>
                      <el-input-number v-model="form.widthMax" :min="0" :step="0.1" />
                    </div>
                  </el-form-item>
                  <el-form-item :label="$t('forms.heightM') as string">
                    <div class="range">
                      <el-input-number v-model="form.heightMin" :min="0" :step="0.1" />
                      <span class="dash">—</span>
                      <el-input-number v-model="form.heightMax" :min="0" :step="0.1" />
                    </div>
                  </el-form-item>
                </div>
              </div>

              <!-- Col: ADR level -->
              <div class="section">
                <div class="sect-title">Опасные грузы, ADR</div>
                <el-select size="small" disabled style="width: 180px">
                  <el-option label="неважно" value="any" />
                </el-select>
              </div>

              <!-- Col: Добавлены -->
              <div class="section">
                <div class="sect-title">Добавлены</div>
                <el-select v-model="form.addedWhen" size="small" style="width: 180px">
                  <el-option :label="$t('filters.anytime') as string" value="any" />
                  <el-option :label="$t('filters.today') as string" value="today" />
                  <el-option :label="$t('filters.last3Days') as string" value="3d" />
                  <el-option :label="$t('filters.last7Days') as string" value="7d" />
                </el-select>
              </div>

              <!-- Col: Поиск по фирмам (инфо) -->
              <div class="section">
                <div class="sect-title">Поиск по фирмам</div>
                <div class="muted small">Доступно только платным участникам ATI</div>
              </div>
            </div>
          </el-collapse-transition>
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

const showAdvanced = ref(false)

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

  // Dimensions (UI only for now)
  lengthMin: undefined as number | undefined,
  lengthMax: undefined as number | undefined,
  widthMin: undefined as number | undefined,
  widthMax: undefined as number | undefined,
  heightMin: undefined as number | undefined,
  heightMax: undefined as number | undefined,

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

// Checklist sync (как на грузах): чек-листы управляют одиночными полями
const bodyTypeGroup = ref<string[]>(form.bodyType ? [form.bodyType] : [])
const loadTypeGroup = ref<string[]>(form.loadType ? [form.loadType] : [])
watch(bodyTypeGroup, v => { form.bodyType = v[0] || '' })
watch(loadTypeGroup, v => { form.loadType = v[0] || '' })

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
/* =======================================
 ✅ RESPONSIVE BREAKPOINTS — VEHICLES SEARCH
======================================= */

/* ✅ 1280px ↓ wider tablets */
@media (max-width: 1280px) {
  .adv-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* ✅ 1024px ↓ tablets */
@media (max-width: 1024px) {
  .row {
    flex-wrap: wrap;
    gap: 10px;
  }

  .filters-grid {
    gap: 16px;
  }

  .adv-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* ✅ 768px ↓ mobile landscape / small tablets */
@media (max-width: 768px) {

  .title {
    font-size: 20px;
  }

  /* 🔹 form rows become vertical */
  .row {
    flex-direction: column;
    align-items: stretch;
  }

  .filters-card {
    padding: 12px;
  }

  /* 🔹 advanced filter section → 1 col */
  .adv-grid {
    grid-template-columns: 1fr;
  }

  .section {
    padding: 10px;
  }

  .dims-grid {
    grid-template-columns: 1fr;
  }

  .search-page {
    padding: 10px;
  }
}

/* ✅ 600px ↓ mobile */
@media (max-width: 600px) {

  .title {
    font-size: 18px;
  }

  .subtitle {
    font-size: 13px;
  }

  .row {
    gap: 8px;
  }

  .filters-card {
    padding: 10px;
  }

  .sect-title {
    font-size: 14px;
  }

  .checklist {
    gap: 4px;
  }

  .range {
    gap: 4px;
  }

  .dash {
    font-size: 12px;
  }
}

/* ✅ 480px ↓ small phones */
@media (max-width: 480px) {

  .title {
    font-size: 17px;
  }

  .filters-card {
    padding: 8px;
  }

  .section {
    padding: 8px;
  }

  .row {
    gap: 6px;
  }

  .adv-grid {
    gap: 8px;
  }

  .sect-title {
    font-size: 13px;
  }
}

/* ✅ 360px ↓ ultra small */
@media (max-width: 360px) {

  .title {
    font-size: 15px;
  }

  .subtitle {
    font-size: 12px;
  }

  .filters-card {
    padding: 6px;
  }

  .section {
    padding: 6px;
  }

  .sect-title {
    font-size: 12px;
  }

  .range {
    flex-direction: column;
    align-items: flex-start;
  }
}

</style>


