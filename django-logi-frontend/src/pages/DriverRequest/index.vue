<template>
  <div class="driver-request-page">
    <el-card class="request-card" shadow="hover">
      <h1 class="page-title"><i class="mdi mdi-clipboard-text-outline"></i> {{ $t('driverRequest.title') }}</h1>
      <p class="page-desc">{{ $t('driverRequest.description') }}</p>

      <!-- Driver and Vehicle -->
      <section class="form-section">
        <h2>{{ $t('driverRequest.sections.driverVehicle') }}</h2>
        <div class="grid-2">
          <el-input v-model="form.driver" :placeholder="$t('driverRequest.placeholders.driver')" />
          <el-input v-model="form.vehicle" :placeholder="$t('driverRequest.placeholders.vehicle')" />
        </div>
      </section>

      <!-- Route and Cargo -->
      <section class="form-section">
        <h2>{{ $t('driverRequest.sections.routeCargo') }}</h2>
        <div class="grid-2">
          <el-input v-model="form.load_city" :placeholder="$t('driverRequest.placeholders.loadCity')" />
          <el-input v-model="form.load_address" :placeholder="$t('driverRequest.placeholders.loadAddress')" />
        </div>

        <el-divider />

        <!-- Cargo items -->
        <div class="cargo-list">
          <div class="cargo-row" v-for="(c, idx) in form.cargos" :key="idx">
            <el-input v-model="c.name" :placeholder="$t('driverRequest.placeholders.cargoName')" />
            <el-input-number v-model="c.weight" :min="0" :placeholder="$t('driverRequest.placeholders.weight')" />
            <el-select v-model="c.weightUnit" class="small">
              <el-option :label="$t('driverRequest.units.t')" value="t" />
              <el-option :label="$t('driverRequest.units.kg')" value="kg" />
            </el-select>
            <el-input-number v-model="c.volume" :min="0" step="0.1" :placeholder="$t('driverRequest.placeholders.volume')" />
            <el-select v-model="c.volumeUnit" class="small">
              <el-option :label="$t('driverRequest.units.m3')" value="m3" />
            </el-select>
            <el-button type="danger" text @click="removeCargo(idx)"><i class="mdi mdi-delete"></i></el-button>
          </div>
          <el-button type="primary" text @click="addCargo"><i class="mdi mdi-plus"></i> {{ $t('driverRequest.actions.addMoreCargo') }}</el-button>
          <el-button type="default" text @click="togglePackages"><i class="mdi mdi-package-variant"></i> {{ $t('driverRequest.actions.packages') }}</el-button>
          <el-button type="default" text @click="toggleDims"><i class="mdi mdi-ruler"></i> {{ $t('driverRequest.actions.dimensions') }}</el-button>
        </div>
      </section>

      <!-- Unload -->
      <section class="form-section">
        <h2>{{ $t('driverRequest.sections.unload') }}</h2>
        <div class="grid-2">
          <el-input v-model="form.unload_city" :placeholder="$t('driverRequest.placeholders.unloadCity')" />
          <el-input v-model="form.unload_address" :placeholder="$t('driverRequest.placeholders.unloadAddress')" />
        </div>
        <div class="grid-2">
          <el-button type="default" text @click="addWaypoint('load')"><i class="mdi mdi-plus-circle-outline"></i> {{ $t('driverRequest.actions.addWaypointLoad') }}</el-button>
          <el-button type="default" text @click="addWaypoint('unload')"><i class="mdi mdi-plus-circle-outline"></i> {{ $t('driverRequest.actions.addWaypointUnload') }}</el-button>
        </div>
      </section>

      <!-- Additional -->
      <section class="form-section">
        <h2>{{ $t('driverRequest.sections.additional') }}</h2>
        <div class="chip-row">
          <el-button type="default" text @click="openDialog('contact')"><i class="mdi mdi-account-card-outline"></i> {{ $t('driverRequest.additional.contact') }}</el-button>
          <el-button type="default" text @click="openDialog('note')"><i class="mdi mdi-note-text-outline"></i> {{ $t('driverRequest.additional.note') }}</el-button>
          <el-button type="default" text @click="openDialog('datetime')"><i class="mdi mdi-calendar-clock"></i> {{ $t('driverRequest.additional.loadDateTime') }}</el-button>
          <el-button type="default" text @click="openDialog('unload_datetime')"><i class="mdi mdi-calendar-clock"></i> {{ $t('driverRequest.additional.unloadDateTime') }}</el-button>
          <el-button type="default" text @click="openDialog('chain')"><i class="mdi mdi-link"></i> {{ $t('driverRequest.additional.strapsCount') }}</el-button>
          <el-button type="default" text @click="openDialog('photos')"><i class="mdi mdi-file-image-outline"></i> {{ $t('driverRequest.additional.photosDocs') }}</el-button>
          <el-button type="default" text @click="openDialog('customs')"><i class="mdi mdi-shield-check-outline"></i> {{ $t('driverRequest.additional.customs') }}</el-button>
        </div>
      </section>

      <!-- Submit -->
      <div class="submit-wrapper">
        <el-button type="primary" size="large" @click="submit">
          <i class="mdi mdi-send"></i>
          {{ $t('driverRequest.submit') }}
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { useI18n } from 'vue-i18n'

interface CargoRow { name: string; weight: number | null; weightUnit: 't' | 'kg'; volume: number | null; volumeUnit: 'm3' }

const { t } = useI18n()

const form = reactive({
  driver: '',
  vehicle: '',
  load_city: '',
  load_address: '',
  unload_city: '',
  unload_address: '',
  cargos: [{ name: '', weight: null, weightUnit: 't', volume: null, volumeUnit: 'm3' }] as CargoRow[],
})

function addCargo() { form.cargos.push({ name: '', weight: null, weightUnit: 't', volume: null, volumeUnit: 'm3' }) }
function removeCargo(i: number) { form.cargos.splice(i, 1) }
function togglePackages() { /* UI stub */ }
function toggleDims() { /* UI stub */ }
function addWaypoint(_type: 'load'|'unload') { /* UI stub for extra waypoints */ }
function openDialog(_kind: string) { /* open corresponding dialog - left as stub */ }

function submit() {
  // Demo only: just show toast and reset
  ElMessage.success(t('driverRequest.createdDemo'))
}
</script>

<style scoped>
.driver-request-page { padding: 16px; }
.request-card { border-radius: 12px; }
.page-title { display: flex; align-items: center; gap: 8px; margin: 0 0 4px; }
.page-desc { color: #64748b; margin: 0 0 16px; }
.form-section { margin-top: 18px; }
.form-section h2 { font-size: 16px; margin: 0 0 12px; color: #111827; }
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.cargo-list { display: flex; flex-direction: column; gap: 8px; }
.cargo-row { display: grid; grid-template-columns: 1fr 160px 100px 160px 100px 40px; gap: 8px; align-items: center; }
.cargo-row .small { width: 100%; }
.chip-row { display: flex; flex-wrap: wrap; gap: 8px; }
.submit-wrapper { display: flex; justify-content: flex-start; margin-top: 16px; }
@media (max-width: 900px) {
  .grid-2 { grid-template-columns: 1fr; }
  .cargo-row { grid-template-columns: 1fr 1fr 100px 1fr 100px 40px; }
}
</style>
