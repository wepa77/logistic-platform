<template>
  <div class="profile-page">
    <div class="profile-layout">
      <!-- Left rail: Ad + Menu -->
      <aside class="left-rail">
        <el-card class="rail-card pay-card" shadow="never">
          <div class="rail-pay-text">
            <div>
              <strong>{{ $t('wallet.title') }}</strong>
              <div class="muted">{{ $t('wallet.topUp') }}</div>
            </div>
            <el-button type="primary" size="small" @click="$router.push('/wallet')">
              <i class="mdi mdi-credit-card"></i>
              {{ $t('profile.topUp') }}
            </el-button>
          </div>
        </el-card>

        <nav class="rail-menu">
          <ul>
            <!-- Payment / history -->
            <li>
              <router-link to="/wallet">
                <i class="mdi mdi-bank-transfer"></i>
                <span>{{ $t('wallet.transactionHistory') }}</span>
              </router-link>
            </li>
            <li>
              <router-link to="/wallet">
                <i class="mdi mdi-history"></i>
                <span>История операций по счету</span>
              </router-link>
            </li>

            <li class="divider" aria-hidden="true"></li>

            <!-- Reference / subdivisions (static like screenshot) -->
            <li class="static">
              <span class="item">
                <i class="mdi mdi-book-open-page-variant"></i>
                <span>Справочники</span>
              </span>
            </li>
            <li class="static">
              <span class="item">
                <i class="mdi mdi-office-building"></i>
                <span>Подразделения</span>
                <i class="mdi mdi-help-circle-outline muted small"></i>
              </span>
            </li>

            <li class="divider" aria-hidden="true"></li>

            <!-- Cargos with add action -->
            <li>
              <router-link to="/cargos" class="with-action">
                <i class="mdi mdi-package-variant-closed"></i>
                <span>{{ $t('nav.cargos') }}</span>
                <el-button text class="icon-btn" @click.stop="$router.push('/cargos/add')" aria-label="add cargo">
                  <i class="mdi mdi-plus-circle-outline"></i>
                </el-button>
              </router-link>
            </li>
            <!-- Vehicles with add action -->
            <li>
              <router-link to="/vehicles" class="with-action">
                <i class="mdi mdi-truck"></i>
                <span>{{ $t('nav.vehicles') }}</span>
                <el-button text class="icon-btn" @click.stop="$router.push('/vehicles/add')" aria-label="add vehicle">
                  <i class="mdi mdi-plus-circle-outline"></i>
                </el-button>
              </router-link>
            </li>

            <li>
              <router-link to="/wallet">
                <i class="mdi mdi-receipt"></i>
                <span>Списания за размещение грузов</span>
              </router-link>
            </li>

            <li class="divider" aria-hidden="true"></li>

            <!-- Other services (static placeholders) -->
            <li class="static">
              <span class="item">
                <i class="mdi mdi-store-outline"></i>
                <span>Тракмаркет</span>
              </span>
            </li>
            <li class="static">
              <span class="item">
                <i class="mdi mdi-briefcase-outline"></i>
                <span>Тендеры</span>
              </span>
            </li>
            <li>
              <router-link to="/offers">
                <i class="mdi mdi-handshake-outline"></i>
                <span>{{ $t('nav.offers') }}</span>
              </router-link>
            </li>
            <li class="static">
              <span class="item">
                <i class="mdi mdi-shield-check-outline"></i>
                <span>Гарантии оплаты перевозки</span>
                <el-tag size="small" type="success" effect="plain" class="ml8">NEW</el-tag>
              </span>
            </li>
            <li class="static">
              <span class="item">
                <i class="mdi mdi-shield-outline"></i>
                <span>Страховки грузов</span>
              </span>
            </li>

            <li class="divider" aria-hidden="true"></li>

            <li>
              <router-link to="/shipments">
                <i class="mdi mdi-transit-connection-variant"></i>
                <span>{{ $t('nav.shipments') }}</span>
              </router-link>
            </li>
            <li>
              <router-link to="/reviews">
                <i class="mdi mdi-star-outline"></i>
                <span>{{ $t('nav.reviews') }}</span>
              </router-link>
            </li>
          </ul>
        </nav>
      </aside>

      <!-- Right: Main content -->
      <section class="main-content">
        <div class="page-header">
          <div class="title-wrap">
            <h1 class="title">{{ $t('profile.title') }}</h1>
            <p class="subtitle">{{ $t('profile.subtitle') }}</p>
          </div>
          <div class="actions">
            <el-button type="primary" @click="$router.push('/wallet')">
              <i class="mdi mdi-wallet-outline"></i>
              {{ $t('profile.topUp') }}
            </el-button>
          </div>
        </div>

        <!-- Verification notice -->
        <el-alert v-if="!user?.verified" type="warning" :closable="false" class="mb16">
          <template #title>
            <b>{{ $t('profile.verifyHeader') }}</b>
          </template>
          <div class="alert-content">
            <span>{{ $t('profile.verifyText') }}</span>
            <el-button text size="small" @click="goSettings">{{ $t('profile.goVerify') }}</el-button>
          </div>
        </el-alert>

        <div class="grid">
          <!-- Left: Account passport like ATI -->
          <el-card class="passport" shadow="never">
            <template #header>
              <div class="card-header">
                <span>{{ $t('profile.passport') }}</span>
                <el-tag type="info" v-if="user?.id">ID: {{ user?.id }}</el-tag>
              </div>
            </template>
            <div class="passport-row">
              <div class="label">{{ $t('profile.company') }}</div>
              <div class="value">{{ user?.company_name || '—' }}</div>
            </div>
            <div class="passport-row">
              <div class="label">{{ $t('profile.country') }}</div>
              <div class="value">{{ user?.address || '—' }}</div>
            </div>
            <div class="passport-row">
              <div class="label">{{ $t('profile.userType') }}</div>
              <div class="value">{{ formatUserType(user?.user_type) }}</div>
            </div>
          </el-card>

          <!-- Right: Balance -->
          <el-card class="balance" shadow="never">
            <template #header>
              <div class="card-header">
                <span>{{ $t('profile.balance') }}</span>
              </div>
            </template>
            <div class="balance-value">{{ formatBalance(user?.balance) }} TMT</div>
            <div class="balance-actions">
              <el-button type="primary" @click="$router.push('/wallet')">{{ $t('profile.topUp') }}</el-button>
            </div>
          </el-card>
        </div>

        <div class="grid two">
          <!-- Contact info -->
          <el-card shadow="never">
            <template #header>
              <div class="card-header">
                <span>{{ $t('profile.contactInfo') }}</span>
                <el-button text size="small" @click="goSettings">
                  <i class="mdi mdi-pencil-outline"></i> {{ $t('common.edit') }}
                </el-button>
              </div>
            </template>
            <div class="contact-grid">
              <div class="kv">
                <div class="row"><div class="k">{{ $t('profile.contactPerson') }}</div><div class="v">{{ user?.username }}</div></div>
                <div class="row"><div class="k">Email</div><div class="v">{{ user?.email || '—' }}</div></div>
                <div class="row"><div class="k">{{ $t('profile.mobile') }}</div><div class="v">{{ user?.phone || '—' }}</div></div>
                <div class="row"><div class="k">{{ $t('profile.department') }}</div><div class="v">—</div></div>
                <div class="row"><div class="k">{{ $t('profile.position') }}</div><div class="v">—</div></div>
              </div>
              <div class="logo-uploader">
                <el-upload class="avatar-uploader" list-type="picture-card" :auto-upload="false" :limit="1">
                  <template #default>
                    <div class="upload-placeholder">
                      <i class="mdi mdi-plus"></i>
                      <div>logo</div>
                    </div>
                  </template>
                </el-upload>
              </div>
            </div>
          </el-card>

          <!-- Company info -->
          <el-card shadow="never">
            <template #header>
              <div class="card-header">
                <span>{{ $t('profile.companyInfo') }}</span>
                <el-button text size="small" @click="goSettings">
                  <i class="mdi mdi-pencil-outline"></i> {{ $t('common.edit') }}
                </el-button>
              </div>
            </template>
            <div class="kv">
              <div class="row"><div class="k">{{ $t('profile.companyName') }}</div><div class="v">{{ user?.company_name || '—' }}</div></div>
              <div class="row"><div class="k">{{ $t('profile.country') }}</div><div class="v">{{ user?.address || '—' }}</div></div>
              <div class="row"><div class="k">{{ $t('forms.city') }}</div><div class="v">{{ extractCity(user?.address) }}</div></div>
              <div class="row"><div class="k">{{ $t('profile.userType') }}</div><div class="v">{{ formatUserType(user?.user_type) }}</div></div>
            </div>
          </el-card>
        </div>

        <!-- Related companies section -->
        <el-card class="mt12" shadow="never">
          <template #header>
            <div class="card-header">
              <span>{{ $t('profile.relatedCompanies') }}</span>
              <el-tooltip placement="top" :content="$t('common.info') as string">
                <i class="mdi mdi-information-outline"></i>
              </el-tooltip>
            </div>
          </template>
          <div class="muted small">{{ $t('profile.verifyText') }}</div>
        </el-card>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/store/auth'
import type { IUser } from '@/types/models'
const auth = useAuthStore()
const user = auth.user as IUser | null

function formatUserType(t?: string) {
  if (!t) return '—'
  return t === 'carrier' ? 'Carrier' : t === 'shipper' ? 'Shipper' : t
}
function formatBalance(b?: string) {
  if (!b) return '0.00'
  const n = Number(b)
  return isNaN(n) ? b : n.toFixed(2)
}
function goSettings(){
  // For now redirect to wallet/settings placeholder
  window.location.href = '/wallet'
}
function extractCity(address?: string){
  if (!address) return '—'
  // naive extraction: take first comma-separated token after potential country
  const parts = address.split(',').map(s=>s.trim()).filter(Boolean)
  if (parts.length >= 1) return parts[0]
  return address
}
</script>

<style scoped>
.profile-page { padding: 12px; }
.profile-layout { display: grid; grid-template-columns: 280px 1fr; gap: 16px; }
.left-rail { position: sticky; top: 12px; height: fit-content; }
.rail-card { margin-bottom: 12px; }
.rail-pay-text { display:flex; align-items:center; justify-content:space-between; gap: 8px; }
.muted { color:#6b7280; font-size:12px; }
.ad .ad-placeholder { height: 120px; background: #f1f5f9; border: 1px dashed #cbd5e1; border-radius: 6px; display:flex; align-items:center; justify-content:center; color:#64748b; }
.rail-menu ul { list-style:none; padding:0; margin:0; }
.rail-menu li { border-bottom: 1px solid #e5e7eb; }
.rail-menu li.divider { height: 10px; border: 0; }
.rail-menu .item,
.rail-menu a { display:flex; align-items:center; gap:10px; padding:12px 8px; color:#334155; text-decoration:none; }
.rail-menu a:hover { background:#f8fafc; }
.rail-menu .with-action { justify-content: space-between; }
.icon-btn { padding: 0 6px; height: 24px; }
.ml8 { margin-left: 8px; }
.small { font-size: 14px; }
.muted { color:#6b7280; }
.mt12{ margin-top:12px; }

.main-content {}
.page-header { display:flex; align-items:center; justify-content:space-between; margin-bottom:12px; }
.title { margin:0; font-size:22px; }
.subtitle { margin:2px 0 0; color:#64748b; font-size:13px; }
.mb16{ margin-bottom:16px; }
.grid{ display:grid; grid-template-columns: 1fr 300px; gap:12px; margin-bottom:12px; }
.grid.two{ grid-template-columns: 1fr 1fr; }
.card-header{ display:flex; align-items:center; justify-content:space-between; }
.passport-row{ display:flex; padding:8px 0; border-bottom:1px solid #f1f5f9; }
.passport-row .label{ width:40%; color:#64748b; }
.passport-row .value{ flex:1; }
.balance-value{ font-size:28px; font-weight:600; margin:8px 0 12px; }
.kv .row{ display:flex; padding:6px 0; border-bottom:1px dashed #eef2f7; }
.kv .k{ width:40%; color:#64748b; }
.kv .v{ flex:1; }
.contact-grid{ display:flex; gap:12px; align-items:flex-start; }
.logo-uploader{ min-width:120px; }
.avatar-uploader :deep(.el-upload--picture-card){ width: 100px; height: 100px; }
.upload-placeholder{ display:flex; flex-direction:column; align-items:center; justify-content:center; color:#64748b; }
@media (max-width: 1024px){
  .profile-layout{ grid-template-columns: 1fr; }
}
@media (max-width: 900px){
  .grid{ grid-template-columns:1fr; }
  .grid.two{ grid-template-columns:1fr; }
  .contact-grid{ flex-direction:column; }
}
</style>
