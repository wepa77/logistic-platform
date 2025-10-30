<template>
  <!-- Home page redesigned to match the provided screenshot style -->
  <div class="home-page">
    <!-- Hero with quick stats and subtle background illustration -->
    <section class="hero">
      <div class="hero-inner">
        <div class="hero-text">
          <h1>{{ $t('home.heroTitle') }}</h1>
          <p>{{ $t('home.heroSubtitle') }}</p>
          <QuickStats />
        </div>
        <div class="hero-art" aria-hidden="true"></div>
      </div>
    </section>

    <!-- Search panel like in the screenshot -->
    <el-card class="search-card" shadow="always">
      <div class="search-grid">
        <div class="field">
          <label>{{ $t('home.fromLabel') }}</label>
          <el-input v-model="search.from" :placeholder="$t('home.fromPlaceholder')" />
        </div>
        <div class="field">
          <label>{{ $t('home.toLabel') }}</label>
          <el-input v-model="search.to" :placeholder="$t('home.toPlaceholder')" />
        </div>
        <div class="field small">
          <label>{{ $t('home.radiusLabel') }}</label>
          <el-input-number v-model="search.radius" :min="0" :max="1000" :step="10" controls-position="right" />
        </div>
        <div class="field small">
          <label>{{ $t('home.dateLabel') }}</label>
          <el-date-picker v-model="search.date" type="date" :placeholder="$t('home.datePlaceholder')" style="width: 100%" />
        </div>
        <div class="actions">
          <el-button type="success" size="large" @click="goFind('cargos')">
            <i class="mdi mdi-package-variant"></i> {{ $t('home.findCargos') }}
          </el-button>
          <el-button type="warning" size="large" @click="goFind('vehicles')">
            <i class="mdi mdi-truck"></i> {{ $t('home.findVehicles') }}
          </el-button>
          <el-button size="large" @click="calcDistance">
            <i class="mdi mdi-ruler"></i> {{ $t('home.calcDistance') }}
          </el-button>
        </div>
      </div>
      <div v-if="distanceKm !== null" class="distance-result">
        <i class="mdi mdi-map-marker-distance"></i>
        <span>{{ $t('home.distance') }}: {{ distanceKm.toFixed(0) }} {{ $t('home.distanceKm') }}</span>
      </div>
    </el-card>

    <!-- Services shortcuts -->
    <section class="services">
      <el-row :gutter="16">
        <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="s in services" :key="s.title">
          <el-card shadow="hover" class="service-card" @click="navigate(s.to)">
            <div class="icon" :class="s.kind"><i :class="s.icon"></i></div>
            <div class="content">
              <div class="title">{{ s.title }}</div>
              <div class="desc">{{ s.desc }}</div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </section>

    <!-- CTA for auth -->
    <section class="cta">
      <el-card class="cta-card" shadow="never">
        <div class="cta-inner">
          <div>
            <h3>{{ $t('home.ctaTitle') }}</h3>
            <p>{{ $t('home.ctaDesc') }}</p>
          </div>
          <div class="cta-actions">
            <router-link to="/login"><el-button type="primary">{{ $t('home.login') }}</el-button></router-link>
            <router-link to="/register"><el-button>{{ $t('home.register') }}</el-button></router-link>
          </div>
        </div>
      </el-card>
    </section>
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'

const { t, locale } = useI18n()

// Haversine distance (km)
function haversineKm(lat1: number, lon1: number, lat2: number, lon2: number) {
  const toRad = (d: number) => (d * Math.PI) / 180
  const R = 6371
  const dLat = toRad(lat2 - lat1)
  const dLon = toRad(lon2 - lon1)
  const a = Math.sin(dLat / 2) ** 2 + Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon / 2) ** 2
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
  return R * c
}

// Public Nominatim geocoder (demo)
async function geocode(q: string): Promise<{ lat: number; lon: number } | null> {
  if (!q) return null
  const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(q)}`
  const res = await fetch(url, { headers: { 'Accept-Language': locale.value } })
  const json = (await res.json()) as Array<{ lat: string; lon: string }> | undefined
  if (!json || !json.length) return null
  const first = json[0] as { lat: string; lon: string }
  return { lat: Number(first.lat), lon: Number(first.lon) }
}

const router = useRouter()
const search = reactive({ from: '', to: '', radius: 0, date: '' as any })
const distanceKm = ref<number | null>(null)

function goFind(kind: 'cargos' | 'vehicles') {
  router.push({ name: kind, query: { from: search.from || undefined, to: search.to || undefined, radius: search.radius || undefined, date: search.date ? new Date(search.date).toISOString().slice(0, 10) : undefined } })
}

async function calcDistance() {
  distanceKm.value = null
  const [a, b] = await Promise.all([geocode(search.from), geocode(search.to)])
  if (a && b) distanceKm.value = haversineKm(a.lat, a.lon, b.lat, b.lon)
}

const services = computed(() => [
  { title: t('home.services.addCargoTitle'), desc: t('home.services.addCargoDesc'), icon: 'mdi mdi-package-variant', kind: 'cargo', to: { name: 'cargos' } },
  { title: t('home.services.addVehicleTitle'), desc: t('home.services.addVehicleDesc'), icon: 'mdi mdi-truck', kind: 'vehicle', to: { name: 'vehicles' } },
  { title: t('home.services.guaranteeTitle'), desc: t('home.services.guaranteeDesc'), icon: 'mdi mdi-shield-check', kind: 'check', to: { name: 'reviews' } },
  { title: t('home.services.platformsTitle'), desc: t('home.services.platformsDesc'), icon: 'mdi mdi-handshake', kind: 'orders', to: { name: 'offers' } }
])

function navigate(to: any) { router.push(to) }
</script>

<style scoped>
.home-page {
  padding: 24px;
}

/* HERO SECTION */
.hero {
  background: linear-gradient(180deg, #eef5ff, #ffffff);
  border-radius: 16px;
  margin-bottom: 20px;
}

.hero-inner {
  display: flex;
  gap: 24px;
  padding: 32px;
  align-items: center;
  min-height: 220px;
}

.hero-text h1 {
  margin: 0 0 8px;
  font-size: 28px;
  font-weight: 700;
}

.hero-text p {
  margin: 0 0 16px;
  color: #475569;
}

.hero-art {
  flex: 1;
  min-height: 160px;
  border-radius: 12px;
  background: radial-gradient(closest-side, #dbeafe, transparent),
  repeating-linear-gradient(45deg, #eff6ff 0 10px, #ffffff 10px 20px);
}

/* SEARCH SECTION */
.search-card {
  margin-bottom: 24px;
}

.search-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 160px 220px;
  gap: 16px;
  align-items: end;
}

.field label {
  display: block;
  font-size: 12px;
  color: #64748b;
  margin-bottom: 6px;
}

.field.small {
  min-width: 140px;
}

.actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.distance-result {
  margin-top: 12px;
  color: #334155;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* SERVICE CARDS */
.services {
  margin: 28px 0;
}

.service-card {
  cursor: pointer;
  transition: transform 0.15s ease;
}

.service-card:hover {
  transform: translateY(-2px);
}

.service-card .icon {
  width: 40px;
  height: 40px;
  display: grid;
  place-items: center;
  border-radius: 8px;
  margin-bottom: 12px;
}

.service-card .icon.cargo {
  background: #fef3c7;
  color: #92400e;
}

.service-card .icon.vehicle {
  background: #dbeafe;
  color: #1e3a8a;
}

.service-card .icon.orders {
  background: #dcfce7;
  color: #166534;
}

.service-card .icon.check {
  background: #fee2e2;
  color: #991b1b;
}

.service-card .title {
  font-weight: 600;
  margin-bottom: 4px;
}

.service-card .desc {
  color: #6b7280;
  font-size: 13px;
}

/* CTA */
.cta-card {
  border-radius: 12px;
}

.cta-inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 10px 4px;
}

.cta-actions {
  display: flex;
  gap: 10px;
}

/* ✅ RESPONSIVE FIXES */
@media (max-width: 1024px) {
  .hero-inner {
    flex-direction: column;
    text-align: center;
  }

  .search-grid {
    grid-template-columns: 1fr 1fr;
  }

  .actions {
    grid-column: 1 / -1;
    justify-content: center;
    flex-wrap: wrap;
  }
}

@media (max-width: 768px) {
  .hero-inner {
    padding: 20px;
  }

  .search-grid {
    grid-template-columns: 1fr;
  }

  .actions {
    flex-direction: column;
    width: 100%;
  }

  .actions button {
    width: 100%;
  }

  .cta-inner {
    flex-direction: column;
    text-align: center;
  }
}

@media (max-width: 480px) {
  .hero-text h1 {
    font-size: 22px;
  }

  .hero-inner {
    padding: 16px;
  }

  .service-card .desc {
    font-size: 12px;
  }
}

</style>
