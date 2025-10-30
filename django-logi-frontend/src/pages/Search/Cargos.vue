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

              <!-- Col: Наименование груза (пример) -->
              <div class="section">
                <div class="sect-title">Наименование груза</div>
                <el-checkbox-group v-model="cargoNames" class="checklist two-cols">
                  <el-checkbox label="Вагонка" />
                  <el-checkbox label="Доски" />
                  <el-checkbox label="Продукты питания" />
                  <el-checkbox label="Стройматериалы" />
                  <el-checkbox label="ТНП" />
                </el-checkbox-group>
                <el-link type="primary" :underline="false" class="mt6">Все наименования</el-link>
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
                  <el-checkbox v-model="form.prepaid">С предоплатой</el-checkbox>
                  <el-checkbox v-model="form.cash">За наличную оплату</el-checkbox>
                  <el-checkbox v-model="form.cashlessNoVAT">Оплата б/н без НДС</el-checkbox>
                  <el-checkbox v-model="form.cashlessVAT">Оплата б/н с НДС</el-checkbox>
                  <el-checkbox>Со ставкой</el-checkbox>
                </div>
              </div>

              <!-- Col: Доп. параметры -->
              <div class="section">
                <div class="sect-title">Доп. параметры</div>
                <div class="checklist">
                  <el-checkbox>С кониками</el-checkbox>
                  <el-checkbox>Только курьерс.</el-checkbox>
                  <el-checkbox>Скрыть «постоянные»</el-checkbox>
                  <el-checkbox>Скрыть тендеры</el-checkbox>
                  <el-checkbox>Скрыть с экипажем</el-checkbox>
                  <el-checkbox v-model="form.hasADR">Опасные грузы (ADR)</el-checkbox>
                </div>
              </div>

              <!-- Col: Габариты и догруз -->
              <div class="section">
                <div class="sect-title">Габариты и догруз</div>
                <el-checkbox v-model="hideOversize">Скрыть без габаритов</el-checkbox>
                <div class="dims-grid">
                  <el-input-number v-model="lenFrom" :min="0" :step="0.1" placeholder="от" />
                  <el-input-number v-model="lenTo" :min="0" :step="0.1" placeholder="до" />
                  <el-input-number v-model="widFrom" :min="0" :step="0.1" placeholder="от" />
                  <el-input-number v-model="widTo" :min="0" :step="0.1" placeholder="до" />
                  <el-input-number v-model="heiFrom" :min="0" :step="0.1" placeholder="от" />
                  <el-input-number v-model="heiTo" :min="0" :step="0.1" placeholder="до" />
                </div>
                <div class="row mini mt6">
                  <el-form-item label="Догруз">
                    <el-select v-model="dogruz" size="small" style="width: 120px">
                      <el-option label="неважно" value="any" />
                      <el-option label="только догруз" value="partial" />
                      <el-option label="только отдельно" value="full" />
                    </el-select>
                  </el-form-item>
                </div>
                <div class="row mini">
                  <el-form-item label="Палеты">
                    <el-input-number v-model="pallets" :min="0" />
                  </el-form-item>
                </div>
              </div>

              <!-- Col: Площадки и торги -->
              <div class="section">
                <div class="sect-title">Площадки и торги</div>
                <div class="checklist">
                  <el-checkbox v-model="platformAti">Биржа ATI.SU</el-checkbox>
                  <el-checkbox>Только с торгами</el-checkbox>
                </div>
                <el-link type="primary" :underline="false" class="mt6">Подробнее о площадках</el-link>
              </div>

              <!-- Col: Поиск по фирмам -->
              <div class="section">
                <div class="sect-title">Поиск по фирмам</div>
                <div class="muted small">Данным фильтром могут пользоваться только платные Участники ATI.SU</div>
              </div>
            </div>
          </el-collapse-transition>
        </el-form>
      </div>
    </el-card>

    <!-- Modern Search Results -->
    <div class="search-results">
      <!-- Results Header -->
      <div class="results-header">
        <div class="results-summary">
          <h2>Найдено <span class="highlight">{{ filteredTotal }}</span> {{ declOfNum(filteredTotal, ['груз', 'груза', 'грузов']) }}</h2>
          <div class="sort-controls">
            <el-select v-model="sortBy" placeholder="Сортировка" size="medium" class="sort-select">
              <el-option label="По дате (новые)" value="new" />
              <el-option label="По дате (старые)" value="old" />
              <el-option label="По цене (убыв.)" value="price_desc" />
              <el-option label="По цене (возр.)" value="price_asc" />
              <el-option label="По весу" value="weight" />
              <el-option label="По объёму" value="volume" />
            </el-select>
            <el-select v-model="pageSize" size="medium" class="page-size-select">
              <el-option :label="`${pageSize} на странице`" :value="pageSize" disabled />
              <el-option :value="10">10 на странице</el-option>
              <el-option :value="20">20 на странице</el-option>
              <el-option :value="50">50 на странице</el-option>
            </el-select>
          </div>
        </div>
      </div>

      <!-- Results Grid -->
      <div class="cargo-grid">
        <el-card v-for="item in pagedCargos" :key="item.id" class="cargo-card" :class="{ 'is-expanded': isExpanded(item) }">
          <!-- Card Header -->
          <div class="cargo-header">
            <div class="cargo-id">#{{ item.id }}</div>
            <div class="cargo-date">
              <i class="mdi mdi-clock-outline"></i> {{ formatDateDM((item as any).created_at) }}
              <span class="time">в {{ formatTimeHM((item as any).created_at) }}</span>
            </div>
          </div>

          <!-- Main Content -->
          <div class="cargo-main">
            <!-- Route Info -->
            <div class="route-info">
              <div class="location from">
                <div class="location-icon"><i class="mdi mdi-map-marker"></i></div>
                <div class="location-details">
                  <div class="city">{{ fromCity(item) }}</div>
                  <div class="date" v-if="item.pickup_date">
                    <i class="mdi mdi-calendar"></i> {{ formatDateDM(item.pickup_date) }}
                  </div>
                </div>
              </div>
              
              <div class="route-arrow">
                <i class="mdi mdi-arrow-right"></i>
              </div>
              
              <div class="location to">
                <div class="location-icon"><i class="mdi mdi-map-marker"></i></div>
                <div class="location-details">
                  <div class="city">{{ toCity(item) }}</div>
                  <div class="distance" v-if="(item as any).distance">
                    <i class="mdi mdi-map-marker-distance"></i> {{ (item as any).distance }} км
                  </div>
                </div>
              </div>
            </div>

            <!-- Cargo Details -->
            <div class="cargo-details">
              <div class="cargo-type">
                <span class="type-badge">{{ displayBodyType(item) }}</span>
                <div class="cargo-specs">
                  <span><i class="mdi mdi-weight-kilogram"></i> {{ fmt(item.weight_kg) }} кг</span>
                  <span><i class="mdi mdi-cube-scan"></i> {{ fmt(item.volume_m3) }} м³</span>
                  <span v-if="(item as any).length || (item as any).width || (item as any).height">
                    <i class="mdi mdi-ruler"></i> {{ (item as any).length || '—' }}×{{ (item as any).width || '—' }}×{{ (item as any).height || '—' }} м
                  </span>
                </div>
              </div>
              
              <div class="cargo-flags">
                <el-tag v-if="(item as any).has_adr" size="small" type="warning" effect="dark" class="flag-tag">
                  <i class="mdi mdi-alert"></i> ADR
                </el-tag>
                <el-tag v-if="(item as any).partial_load" size="small" type="success" effect="dark" class="flag-tag">
                  <i class="mdi mdi-package-variant"></i> Догруз
                </el-tag>
                <el-tag v-if="(item as any).without_bargain" size="small" type="danger" effect="dark" class="flag-tag">
                  <i class="mdi mdi-hand-back-right"></i> Без торга
                </el-tag>
                <el-tag v-if="(item as any).pay_to_card" size="small" type="success" effect="dark" class="flag-tag">
                  <i class="mdi mdi-credit-card"></i> Оплата на карту
                </el-tag>
              </div>
            </div>

            <!-- Price and Actions -->
            <div class="cargo-actions">
              <div class="price" v-if="hasAnyRate(item)">
                <div class="amount">{{ formatPrice(item.price_offer) }}</div>
                <div class="price-note">Предложенная ставка</div>
              </div>
              <div class="no-price" v-else>
                <span>Цена не указана</span>
              </div>
              
              <div class="action-buttons">
                <el-button 
                  size="medium" 
                  :type="isExpanded(item) ? 'primary' : 'default'" 
                  @click="toggleContacts(item)"
                  class="action-btn"
                >
                  <i :class="isExpanded(item) ? 'mdi mdi-eye-off' : 'mdi mdi-eye'"></i>
                  {{ isExpanded(item) ? 'Скрыть контакты' : 'Показать контакты' }}
                </el-button>
                
                <el-button 
                  size="medium" 
                  type="primary" 
                  plain 
                  class="action-btn"
                  @click="makeOffer(item)"
                >
                  <i class="mdi mdi-gavel"></i>
                  Сделать предложение
                </el-button>
              </div>
            </div>
          </div>

          <!-- Expanded Details -->
          <el-collapse-transition>
            <div v-if="isExpanded(item)" class="expanded-details">
              <div class="details-section">
                <h4><i class="mdi mdi-information-outline"></i> Контактная информация</h4>
                <div class="contact-info">
                  <div class="contact-item" v-if="companyName(item)">
                    <i class="mdi mdi-domain"></i>
                    <span>{{ companyName(item) }}</span>
                  </div>
                  <div class="contact-item" v-if="contactPhone(item)">
                    <i class="mdi mdi-phone"></i>
                    <a :href="'tel:' + contactPhone(item)" class="phone-link">{{ contactPhone(item) }}</a>
                  </div>
                  <div class="contact-item" v-if="(item as any).contact_name">
                    <i class="mdi mdi-account"></i>
                    <span>{{ (item as any).contact_name }}</span>
                  </div>
                  <div class="contact-item" v-if="(item as any).email">
                    <i class="mdi mdi-email"></i>
                    <a :href="'mailto:' + (item as any).email">{{ (item as any).email }}</a>
                  </div>
                </div>
              </div>

              <div class="details-section" v-if="(item as any).note || (item as any).description">
                <h4><i class="mdi mdi-note-text-outline"></i> Примечание</h4>
                <div class="note-content">
                  {{ String((item as any).note || (item as any).description) }}
                </div>
              </div>

              <div class="action-buttons">
                <el-button type="primary" size="medium" class="action-btn">
                  <i class="mdi mdi-phone"></i> Позвонить
                </el-button>
                <el-button type="success" size="medium" class="action-btn">
                  <i class="mdi mdi-message-text"></i> Написать сообщение
                </el-button>
                <el-button type="warning" size="medium" class="action-btn">
                  <i class="mdi mdi-file-document-edit"></i> Создать заявку
                </el-button>
              </div>
            </div>
          </el-collapse-transition>
        </el-card>
      </div>

      <!-- Pagination -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="page"
          :page-size="pageSize"
          :total="filteredTotal"
          layout="prev, pager, next, sizes, total"
          :page-sizes="[10, 20, 50]"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          background
        />
      </div>
    </div>
  </div>
</template>
<script lang="ts" setup>
import { reactive, ref, watch, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { http } from '@/api/http'
import type { ICargo } from '@/types/models'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()
const { t } = useI18n()

const showAdvanced = ref(false)

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

// UI state for expanded filter sections (to mimic ATI screenshot)
const bodyTypeGroup = ref<string[]>(form.bodyType ? [form.bodyType] : [])
const loadTypeGroup = ref<string[]>(form.loadType ? [form.loadType] : [])
const cargoNames = ref<string[]>([])
const hideOversize = ref(false)
const lenFrom = ref<number | undefined>(undefined)
const lenTo = ref<number | undefined>(undefined)
const widFrom = ref<number | undefined>(undefined)
const widTo = ref<number | undefined>(undefined)
const heiFrom = ref<number | undefined>(undefined)
const heiTo = ref<number | undefined>(undefined)
const dogruz = ref<'any'|'partial'|'full'>('any')
const pallets = ref<number | undefined>(undefined)
const platformAti = ref(true)

// Keep original single-select fields in sync with checkbox groups
watch(bodyTypeGroup, (v)=> { form.bodyType = v[0] || '' })
watch(loadTypeGroup, (v)=> { form.loadType = v[0] || '' })

const cargos = ref<ICargo[]>([])
const loading = ref(false)
const page = ref(1)
const pageSize = ref(10)
const sortBy = ref<'new'|'old'|'weight'|'volume'|'price_desc'|'price_asc'>('new')

async function fetchCargos(){
  loading.value = true
  try{
    const { data } = await http.get('/cargos/')
    cargos.value = Array.isArray(data) ? data : (data?.results || [])
  } finally {
    loading.value = false
  }
}

onMounted(fetchCargos)

// Expanded contacts state keyed per cargo
const expanded = ref<Record<string, boolean>>({})
function rowKey(item: any): string { return String((item && (item.id || item.title)) || Math.random()) }
function toggleContacts(item: any) { const k = rowKey(item); expanded.value[k] = !expanded.value[k] }
function isExpanded(item: any): boolean { return !!expanded.value[rowKey(item)] }

const filtered = computed(() => {
  // Apply minimal client-side filtering for demo purpose
  let list = [...cargos.value]
  if (form.weightMin != null) list = list.filter(c => (Number(c.weight_kg)||0) >= (form.weightMin as number))
  if (form.weightMax != null) list = list.filter(c => (Number(c.weight_kg)||0) <= (form.weightMax as number))
  if (form.volumeMin != null) list = list.filter(c => (Number(c.volume_m3)||0) >= (form.volumeMin as number))
  if (form.volumeMax != null) list = list.filter(c => (Number(c.volume_m3)||0) <= (form.volumeMax as number))
  if (form.bodyType) list = list.filter(c => (c as any).body_type === form.bodyType)
  if (form.from) list = list.filter(c => (c.pickup_address||'').toLowerCase().includes(form.from.toLowerCase()))
  if (form.to) list = list.filter(c => (c.delivery_address||'').toLowerCase().includes(form.to.toLowerCase()))

  switch (sortBy.value){
    case 'weight':
      list.sort((a,b)=> (Number(b.weight_kg)||0)-(Number(a.weight_kg)||0));
      break
    case 'volume':
      list.sort((a,b)=> (Number(b.volume_m3)||0)-(Number(a.volume_m3)||0));
      break
    case 'price_desc':
      list.sort((a,b)=> num(b.price_offer)-num(a.price_offer));
      break
    case 'price_asc':
      list.sort((a,b)=> num(a.price_offer)-num(b.price_offer));
      break
    case 'old':
      list.sort((a,b)=> new Date(a.created_at||a.pickup_date||'').getTime() - new Date(b.created_at||b.pickup_date||'').getTime());
      break
    default:
      list.sort((a,b)=> new Date(b.created_at||b.pickup_date||'').getTime() - new Date(a.created_at||a.pickup_date||'').getTime());
  }
  return list
})

const filteredTotal = computed(()=> filtered.value.length)
const pagedCargos = computed(()=>{
  const start = (page.value-1)*pageSize.value
  return filtered.value.slice(start, start+pageSize.value)
})

function num(v:any){
  const n = Number(v)
  return isNaN(n) ? 0 : n
}

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
  page.value = 1
}

// React to query changes (back/forward) and refetch once (lightweight)
watch(() => route.query, () => { fetchCargos() })

function fmt(v:any){
  if (v==null || v==='') return '—'
  const n = Number(v)
  return isNaN(n) ? String(v) : n.toString()
}
function formatPrice(v:any){
  const n = Number(v)
  if (!n) return t('cargos.onRequest') as string
  return `${n} TMT`
}

function displayBodyType(item: ICargo){
  const key = (item as any).body_type as string | undefined
  if (!key) return t('cargos.general') as string
  return bodyTypes[key] || key
}
function formatDate(v:any){
  if (!v) return '—'
  const d = new Date(v)
  if (isNaN(d.getTime())) return String(v)
  return d.toLocaleDateString()
}
// Helpers for new list UI
function fromCity(item: any): string { return String(item?.pickup_address || item?.from || '') || '—' }
function toCity(item: any): string { return String(item?.delivery_address || item?.to || '') || '—' }
function hasAnyRate(item: any): boolean { return !!(item?.price_offer || item?.price || item?.rate) }
function formatTimeHM(v?: any): string {
  if (!v) return ''
  try { const d = new Date(v); return d.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' }) } catch { return '' }
}
function formatDateDM(v?: any): string {
  if (!v) return ''
  try { const d = new Date(v); const day = d.toLocaleDateString('ru-RU',{day:'2-digit'}); const mon = d.toLocaleDateString('ru-RU',{month:'short'}).replace('.',''); return `${day} ${mon}` } catch { return '' }
}

// Contact/helpers similar to Vehicles list to keep parity
function pick(row: any, keys: string[], fallback: string = ''): any {
  if (!row) return fallback
  for (const k of keys) {
    try {
      const v = k.includes('?.') ? k.split('?.').reduce((o:any, p)=> o?.[p], row) : row[k]
      if (v !== undefined && v !== null && String(v).toString().trim() !== '') return v
    } catch { /* ignore */ }
  }
  return fallback
}
function companyName(row: any): string {
  const v = pick(row, ['company_name','shipper?.company_name','owner?.company_name'])
  return typeof v === 'string' ? v : ''
}
function contactPhone(row: any): string {
  const v = pick(row, ['contact_phone','shipper?.phone','owner?.phone'])
  return typeof v === 'string' ? v : ''
}

// Pluralization helper
function declOfNum(n: number, titles: string[]) {
  const cases = [2, 0, 1, 1, 1, 2];
  return titles[(n % 100 > 4 && n % 100 < 20) ? 2 : cases[(n % 10 < 5) ? n % 10 : 5]];
}

// Pagination handlers
const handleSizeChange = (val: number) => {
  pageSize.value = val;
  page.value = 1;
};

const handleCurrentChange = (val: number) => {
  page.value = val;
};

// Make offer function
const makeOffer = (item: any) => {
  console.log('Make offer for:', item);
  ElMessage.info('Функционал предложения в разработке');
};

</script>

<style scoped lang="scss">
/* ================================
   ✅ VARIABLES & MIXINS
   ================================ */
:deep(.el-card) {
  border-radius: 12px;
  border: 1px solid #e4e7ed;
  transition: all 0.3s ease;
  margin-bottom: 16px;
  
  &:hover {
    box-shadow: 0 6px 16px -8px rgba(0, 0, 0, 0.08), 0 9px 28px 0 rgba(0, 0, 0, 0.05), 0 12px 48px 16px rgba(0, 0, 0, 0.03);
  }
}

:deep(.el-tag) {
  margin-right: 8px;
  margin-bottom: 8px;
  
  .mdi {
    font-size: 14px;
    margin-right: 4px;
  }
}

:deep(.el-button) {
  .mdi {
    font-size: 16px;
    margin-right: 6px;
  }
}

/* ================================
   ✅ SEARCH RESULTS LAYOUT
   ================================ */
.search-results {
  margin-top: 24px;
}

.results-header {
  margin-bottom: 24px;
  
  .results-summary {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 16px;
    
    h2 {
      font-size: 20px;
      font-weight: 600;
      margin: 0;
      
      .highlight {
        color: var(--el-color-primary);
      }
    }
  }
  
  .sort-controls {
    display: flex;
    gap: 12px;
    
    .sort-select {
      width: 220px;
    }
    
    .page-size-select {
      width: 180px;
    }
  }
}

.cargo-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
  margin-bottom: 24px;
}

.cargo-card {
  transition: all 0.3s ease;
  
  &.is-expanded {
    border-color: var(--el-color-primary-light-5);
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  }
  
  .cargo-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 12px;
    border-bottom: 1px solid #f0f2f5;
    margin-bottom: 16px;
    
    .cargo-id {
      font-size: 13px;
      color: #909399;
    }
    
    .cargo-date {
      font-size: 13px;
      color: #909399;
      
      .time {
        margin-left: 4px;
        color: #c0c4cc;
      }
      
      .mdi {
        margin-right: 4px;
      }
    }
  }
  
  .cargo-main {
    .route-info {
      display: flex;
      align-items: flex-start;
      gap: 16px;
      margin-bottom: 16px;
      
      .location {
        flex: 1;
        display: flex;
        gap: 12px;
        
        .location-icon {
          color: var(--el-color-primary);
          font-size: 20px;
          margin-top: 2px;
        }
        
        .location-details {
          .city {
            font-weight: 600;
            margin-bottom: 4px;
          }
          
          .date, .distance {
            font-size: 13px;
            color: #606266;
            
            .mdi {
              margin-right: 4px;
            }
          }
        }
        
        &.to .city {
          color: var(--el-color-success);
        }
      }
      
      .route-arrow {
        color: #c0c4cc;
        padding: 8px 0;
        
        .mdi {
          font-size: 20px;
        }
      }
    }
    
    .cargo-details {
      background-color: #f8f9fa;
      border-radius: 8px;
      padding: 16px;
      margin-bottom: 16px;
      
      .cargo-type {
        margin-bottom: 12px;
        
        .type-badge {
          display: inline-block;
          background-color: var(--el-color-primary-light-9);
          color: var(--el-color-primary);
          padding: 4px 10px;
          border-radius: 4px;
          font-weight: 600;
          margin-right: 8px;
          margin-bottom: 8px;
        }
        
        .cargo-specs {
          display: flex;
          flex-wrap: wrap;
          gap: 12px;
          margin-top: 8px;
          color: #606266;
          font-size: 14px;
          
          .mdi {
            margin-right: 4px;
            color: #909399;
          }
        }
      }
      
      .cargo-flags {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
      }
    }
    
    .cargo-actions {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
      
      .price {
        .amount {
          font-size: 20px;
          font-weight: 600;
          color: var(--el-color-primary);
          line-height: 1.2;
        }
        
        .price-note {
          font-size: 12px;
          color: #909399;
        }
      }
      
      .no-price {
        color: #909399;
        font-style: italic;
      }
      
      .action-buttons {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
        
        .action-btn {
          .mdi {
            margin-right: 6px;
          }
        }
      }
    }
  }
  
  .expanded-details {
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid #f0f2f5;
    
    .details-section {
      margin-bottom: 20px;
      
      &:last-child {
        margin-bottom: 0;
      }
      
      h4 {
        font-size: 15px;
        margin: 0 0 12px 0;
        color: #303133;
        display: flex;
        align-items: center;
        
        .mdi {
          margin-right: 8px;
          color: var(--el-color-primary);
        }
      }
      
      .contact-info {
        .contact-item {
          display: flex;
          align-items: center;
          margin-bottom: 8px;
          font-size: 14px;
          
          .mdi {
            margin-right: 8px;
            color: #909399;
            width: 20px;
            text-align: center;
          }
          
          a {
            color: var(--el-color-primary);
            text-decoration: none;
            
            &:hover {
              text-decoration: underline;
            }
          }
          
          .phone-link {
            font-weight: 500;
          }
        }
      }
      
      .note-content {
        background-color: #f8f9fa;
        border-radius: 4px;
        padding: 12px;
        font-size: 14px;
        line-height: 1.6;
        color: #606266;
        white-space: pre-line;
      }
    }
  }
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 24px;
  
  :deep(.el-pagination) {
    .btn-prev,
    .btn-next,
    .el-pager li {
      border-radius: 8px;
      margin: 0 4px;
    }
    
    .el-pager li:not(.is-disabled).is-active {
      background-color: var(--el-color-primary);
    }
  }
}

/* ================================
   ✅ RESPONSIVE ADJUSTMENTS
   ================================ */
@media (max-width: 992px) {
  .cargo-actions {
    flex-direction: column;
    align-items: flex-start !important;
  }
  
  .action-buttons {
    width: 100%;
    
    .el-button {
      flex: 1;
      justify-content: center;
    }
  }
}

@media (max-width: 768px) {
  .results-summary {
    flex-direction: column;
    align-items: flex-start !important;
  }
  
  .sort-controls {
    width: 100%;
    flex-direction: column;
    
    .el-select {
      width: 100% !important;
    }
  }
  
  .route-info {
    flex-direction: column !important;
    gap: 12px !important;
    
    .route-arrow {
      display: none;
    }
  }
  
  .action-buttons {
    .el-button {
      width: 100%;
    }
  }
}

/* ================================
   ✅ ANIMATIONS & TRANSITIONS
   ================================ */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* ================================
   ✅ RESPONSIVE BREAKPOINTS
   ================================ */

/* ✅ 1400px ↓ — Large screens */
@media (max-width: 1400px) {
  .row-h {
    grid-template-columns: 60px 1fr 80px 140px;
  }
}

/* ✅ 1200px ↓ — Reduce main columns */
@media (max-width: 1200px) {
  .col-main {
    grid-template-columns: repeat(4, 1fr);
  }
  .col-main .cell.rate {
    grid-column: span 1;
  }

  .adv-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* ✅ 1024px ↓ — Tablet landscape */
@media (max-width: 1024px) {
  .c-list-header {
    display: none; /* Hide desktop header */
  }

  .row-h {
    grid-template-columns: 50px 1fr 70px;
  }

  .col-right,
  .col-meta {
    display: none; /* hide tiny side columns */
  }

  .col-main {
    grid-template-columns: repeat(3, 1fr);
    padding: 12px;
  }

  .adv-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* ✅ 900px ↓ — Tablet portrait */
@media (max-width: 900px) {

  .filters-grid {
    gap: 16px;
  }

  .row {
    flex-direction: column;
    align-items: stretch;
  }

  .adv-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .c-results-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .col-main {
    grid-template-columns: 1fr 1fr;
  }
}

/* ✅ 768px ↓ — Mobile */
@media (max-width: 768px) {
  .title {
    font-size: 20px;
  }

  .filters-card {
    padding: 12px;
  }

  .adv-grid {
    grid-template-columns: 1fr;
  }

  .c-result-row {
    border-radius: 12px;
  }

  /* ✅ Mobile cargo row layout (ATI mobile style) */
  .row-h {
    display: flex;
    flex-direction: column;
    padding: 10px;
    gap: 12px;
  }

  .col-left {
    order: 1;
    padding: 0;
  }

  .col-main {
    order: 2;
    background: #f6f7f9;
    padding: 10px;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .col-right,
  .col-meta {
    display: none;
  }

  .cell {
    font-size: 14px;
  }

  .rate .value {
    font-size: 15px;
  }

  .row-bottom {
    flex-direction: column;
    align-items: flex-start;
    gap: 6px;
  }
}

/* ✅ 600px ↓ — Smaller mobile */
@media (max-width: 600px) {

  .title {
    font-size: 18px;
  }

  .c-results-header {
    gap: 6px;
  }

  .left-actions .hint {
    font-size: 11px;
  }

  .contacts-panel {
    flex-direction: column;
    gap: 10px;
  }

  .cp-right {
    justify-content: flex-start;
  }

  .filters-card {
    padding: 10px;
  }

  .row-h {
    padding: 8px;
  }

  .cell .city {
    font-size: 14px;
  }
}

/* ✅ 480px ↓ — Compact phones */
@media (max-width: 480px) {

  .title i {
    font-size: 20px;
  }

  .cell {
    font-size: 13px;
  }

  .rate .value {
    font-size: 14px;
  }

  .c-result-row {
    padding: 0;
  }

  .col-main {
    padding: 8px;
  }

  .contacts-panel {
    padding: 8px;
  }
}

/* ✅ 360px ↓ — Ultra small */
@media (max-width: 360px) {

  .title {
    font-size: 16px;
  }

  .filters-grid {
    gap: 8px;
  }

  .adv-grid {
    grid-template-columns: 1fr;
  }

  .c-result-row {
    border-radius: 8px;
  }

  .cell {
    font-size: 12px;
  }

  .rate .value {
    font-size: 13px;
  }
}

</style>
