<template>
  <div class="driver-request-page">
    <el-card class="request-card" shadow="hover">
      <h1 class="page-title"><i class="mdi mdi-clipboard-text-outline"></i> Заявка водителю на перевозку</h1>
      <p class="page-desc">Вы сможете отслеживать перевозку, местоположение груза и его статусы на карте. Данные из заявки увидит только водитель, которого вы выберете.</p>

      <!-- Driver and Vehicle -->
      <section class="form-section">
        <h2>Водитель и ТС</h2>
        <div class="grid-2">
          <el-input v-model="form.driver" placeholder="Введите фамилию или имя" />
          <el-input v-model="form.vehicle" placeholder="Выберите ТС" />
        </div>
      </section>

      <!-- Route and Cargo -->
      <section class="form-section">
        <h2>Маршрут и груз</h2>
        <div class="grid-2">
          <el-input v-model="form.load_city" placeholder="Населённый пункт загрузки" />
          <el-input v-model="form.load_address" placeholder="Адрес без города" />
        </div>

        <el-divider />

        <!-- Cargo items -->
        <div class="cargo-list">
          <div class="cargo-row" v-for="(c, idx) in form.cargos" :key="idx">
            <el-input v-model="c.name" placeholder="Наименование груза" />
            <el-input-number v-model="c.weight" :min="0" placeholder="Вес" />
            <el-select v-model="c.weightUnit" class="small">
              <el-option label="т" value="t" />
              <el-option label="кг" value="kg" />
            </el-select>
            <el-input-number v-model="c.volume" :min="0" step="0.1" placeholder="Объём" />
            <el-select v-model="c.volumeUnit" class="small">
              <el-option label="м³" value="m3" />
            </el-select>
            <el-button type="danger" text @click="removeCargo(idx)"><i class="mdi mdi-delete"></i></el-button>
          </div>
          <el-button type="primary" text @click="addCargo"><i class="mdi mdi-plus"></i> Ещё груз</el-button>
          <el-button type="default" text @click="togglePackages"><i class="mdi mdi-package-variant"></i> Упаковка и кол-во</el-button>
          <el-button type="default" text @click="toggleDims"><i class="mdi mdi-ruler"></i> Габариты</el-button>
        </div>
      </section>

      <!-- Unload -->
      <section class="form-section">
        <h2>Разгрузка</h2>
        <div class="grid-2">
          <el-input v-model="form.unload_city" placeholder="Населённый пункт разгрузки" />
          <el-input v-model="form.unload_address" placeholder="Адрес без города" />
        </div>
        <div class="grid-2">
          <el-button type="default" text @click="addWaypoint('load')"><i class="mdi mdi-plus-circle-outline"></i> Добавить точку маршрута: Загрузка</el-button>
          <el-button type="default" text @click="addWaypoint('unload')"><i class="mdi mdi-plus-circle-outline"></i> Добавить точку маршрута: Разгрузка</el-button>
        </div>
      </section>

      <!-- Additional -->
      <section class="form-section">
        <h2>Дополнительно</h2>
        <div class="chip-row">
          <el-button type="default" text @click="openDialog('contact')"><i class="mdi mdi-account-card-outline"></i> Контакт</el-button>
          <el-button type="default" text @click="openDialog('note')"><i class="mdi mdi-note-text-outline"></i> Примечание</el-button>
          <el-button type="default" text @click="openDialog('datetime')"><i class="mdi mdi-calendar-clock"></i> Дата и время загрузки</el-button>
          <el-button type="default" text @click="openDialog('unload_datetime')"><i class="mdi mdi-calendar-clock"></i> Дата и время разгрузки</el-button>
          <el-button type="default" text @click="openDialog('chain')"><i class="mdi mdi-link"></i> Ремней, шт.</el-button>
          <el-button type="default" text @click="openDialog('photos')"><i class="mdi mdi-file-image-outline"></i> Фото грузов и документы</el-button>
          <el-button type="default" text @click="openDialog('customs')"><i class="mdi mdi-shield-check-outline"></i> Таможня</el-button>
        </div>
      </section>

      <!-- Submit -->
      <div class="submit-wrapper">
        <el-button type="primary" size="large" @click="submit">
          <i class="mdi mdi-send"></i>
          Добавить заявку
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { reactive } from 'vue'
import { ElMessage } from 'element-plus'

interface CargoRow { name: string; weight: number | null; weightUnit: 't' | 'kg'; volume: number | null; volumeUnit: 'm3' }

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
  ElMessage.success('Заявка создана (демо)')
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
