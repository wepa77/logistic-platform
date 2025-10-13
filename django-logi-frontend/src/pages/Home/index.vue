<template>
  <!-- Simple public Home page separate from authenticated dashboard -->
  <div class="home-page">
    <section class="hero">
      <div class="hero-inner">
        <div class="hero-text">
          <h1>Welcome to Logistic</h1>
          <p>Your gateway to cargos, vehicles, and trusted logistics partners.</p>
          <div class="cta-buttons">
            <router-link to="/market">
              <el-button type="primary" size="large">
                <i class="mdi mdi-storefront"></i>
                Go to Marketplace
              </el-button>
            </router-link>
            <router-link to="/login">
              <el-button size="large">
                <i class="mdi mdi-login"></i>
                Login
              </el-button>
            </router-link>
            <router-link to="/register">
              <el-button size="large" type="success">
                <i class="mdi mdi-account-plus"></i>
                Register
              </el-button>
            </router-link>
          </div>
        </div>
        <div class="hero-art" aria-hidden="true"></div>
      </div>
    </section>

    <section class="features">
      <el-row :gutter="16">
        <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="f in features" :key="f.title">
          <el-card shadow="hover" class="feature-card">
            <div class="icon" :class="f.kind"><i :class="f.icon"></i></div>
            <div class="content">
              <div class="title">{{ f.title }}</div>
              <div class="desc">{{ f.desc }}</div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </section>
  </div>
</template>

<script lang="ts" setup>
const features = [
  { title: 'Find Cargos', desc: 'Search thousands of loads daily', icon: 'mdi mdi-package-variant', kind: 'cargo' },
  { title: 'Find Vehicles', desc: 'Verified carriers across regions', icon: 'mdi mdi-truck', kind: 'vehicle' },
  { title: 'Orders & Offers', desc: 'Negotiate and track orders', icon: 'mdi mdi-handshake', kind: 'orders' },
  { title: 'Reputation', desc: 'Reviews and partner checks', icon: 'mdi mdi-shield-check', kind: 'check' }
]
</script>

<style scoped>
.home-page { padding: 24px; }
.hero { background: linear-gradient(180deg, #eef2ff, #ffffff); border-radius: 16px; margin-bottom: 20px; }
.hero-inner { display: flex; gap: 24px; padding: 32px; align-items: center; min-height: 220px; }
.hero-text h1 { margin: 0 0 8px; font-size: 28px; font-weight: 700; }
.hero-text p { margin: 0 0 16px; color: #475569; }
.hero-art { flex: 1; min-height: 160px; border-radius: 12px; background: radial-gradient(closest-side, #e0e7ff, transparent), repeating-linear-gradient(45deg, #eef2ff 0 10px, #ffffff 10px 20px); }
.cta-buttons { display: flex; gap: 12px; flex-wrap: wrap; }

.features { margin: 28px 0; }
.feature-card .icon { width: 40px; height: 40px; display: grid; place-items: center; border-radius: 8px; margin-bottom: 12px; }
.feature-card .icon.cargo { background: #fef3c7; color: #92400e; }
.feature-card .icon.vehicle { background: #dbeafe; color: #1e3a8a; }
.feature-card .icon.orders { background: #dcfce7; color: #166534; }
.feature-card .icon.check { background: #fee2e2; color: #991b1b; }
.feature-card .title { font-weight: 600; margin-bottom: 4px; }
.feature-card .desc { color: #6b7280; font-size: 13px; }

@media (max-width: 1024px) {
  .hero-inner { flex-direction: column; align-items: flex-start; }
}
</style>
