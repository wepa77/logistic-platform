<template>
  <div class="vehicle-add-page">
    <el-card class="vehicle-card" shadow="hover">
      <h1 class="page-title">
        <i class="mdi mdi-truck-plus-outline"></i>
        Добавить машину
      </h1>

      <!-- 1️⃣ Тип кузова и загрузка -->
      <section class="form-section">
        <h2>Тип кузова</h2>
        <div class="grid-2">
          <el-select v-model="form.body_type" placeholder="Выберите тип кузова">
            <el-option v-for="(label, value) in bodyTypes" :key="value" :label="label" :value="value" />
          </el-select>

          <div class="truck-category">
            <el-radio-group v-model="form.truck_category">
              <el-radio label="semi_trailer">Полуприцеп</el-radio>
              <el-radio label="truck">Грузовик</el-radio>
              <el-radio label="coupling">Сцепка</el-radio>
            </el-radio-group>
          </div>
        </div>

        <h3>Загрузка</h3>
        <el-checkbox-group v-model="form.load_types">
          <el-checkbox v-for="(label, value) in loadTypes" :key="value" :label="value">{{ label }}</el-checkbox>
        </el-checkbox-group>
      </section>

      <!-- 2️⃣ Грузоподъёмность и размеры -->
      <section class="form-section">
        <h2>Характеристики</h2>
        <div class="grid-3">
          <el-input-number v-model="form.capacity_kg" :min="0" label="Грузоподъёмность (кг)" placeholder="т" />
          <el-input-number v-model="form.volume_m3" :min="0" step="0.5" label="Объём (м³)" />
        </div>
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

      <!-- 3️⃣ Откуда / разгрузка -->
      <section class="form-section">
        <h2>Маршрут</h2>
        <div class="grid-2">
          <el-input v-model="form.location_from" placeholder="Откуда (населённый пункт)" />
          <el-input v-model="form.possible_unload" placeholder="Куда (возможная разгрузка)" />
        </div>
        <div class="grid-2">
          <el-input-number v-model="form.location_from_radius_km" :min="0" placeholder="Радиус откуда (км)" />
          <el-input-number v-model="form.unload_radius_km" :min="0" placeholder="Радиус разгрузки (км)" />
        </div>

        <div class="grid-2">
          <el-date-picker v-model="form.available_from" type="date" placeholder="Готов к загрузке" style="width: 100%" />
          <el-input-number v-model="form.available_days" :min="1" placeholder="Количество дней" />
        </div>
      </section>

      <!-- 4️⃣ Ставка -->
      <section class="form-section">
        <h2>Ставка</h2>
        <el-radio-group v-model="form.rate_mode" class="rate-mode">
          <el-radio label="has_rate">Есть ставка</el-radio>
          <el-radio label="request_rate">Запросить ставку</el-radio>
        </el-radio-group>

        <div class="grid-3">
          <el-input-number v-model="form.rate_with_vat" :min="0" placeholder="С НДС, безнал" />
          <el-input-number v-model="form.rate_without_vat" :min="0" placeholder="Без НДС, безнал" />
          <el-input-number v-model="form.rate_cash" :min="0" placeholder="Наличными" />
        </div>

        <div class="grid-2">
          <el-select v-model="form.rate_currency" placeholder="Валюта">
            <el-option label="TMT" value="tmt" />
            <el-option label="RUB" value="rub" />
            <el-option label="USD" value="usd" />
            <el-option label="EUR" value="eur" />
          </el-select>

          <div>
            <el-checkbox v-model="form.pay_to_card">на карту</el-checkbox>
            <el-checkbox v-model="form.without_bargain">без торга</el-checkbox>
          </div>
        </div>
      </section>

      <!-- 5️⃣ Данные компании -->
      <section class="form-section">
        <h2>Данные компании</h2>
        <el-checkbox v-model="form.is_private">Я — частное лицо</el-checkbox>

        <div class="grid-2">
          <el-select v-model="form.company_type" placeholder="Тип фирмы">
            <el-option label="ООО" value="ooo" />
            <el-option label="ИП" value="ip" />
            <el-option label="Физлицо" value="fl" />
            <el-option label="Самозанятый" value="self" />
          </el-select>
          <el-input v-model="form.company_name" placeholder="Название фирмы" />
        </div>

        <div class="grid-2">
          <el-input v-model="form.city" placeholder="Город" />
          <el-input v-model="form.contact_name" placeholder="Контактное лицо" />
        </div>
        <el-input v-model="form.contact_phone" placeholder="Телефон" />
        <el-input type="textarea" v-model="form.note" :rows="3" placeholder="Примечание" />
      </section>

      <!-- 6️⃣ Продвижение -->
      <section class="form-section">
        <h2>Продвижение</h2>
        <el-switch v-model="form.promote_top" active-text="TOP поиска" />
        <el-switch v-model="form.stealth_mode" active-text="Stealth режим" />
      </section>

      <!-- Submit -->
      <div class="submit-wrapper">
        <el-button type="primary" size="large" @click="submitForm">
          <i class="mdi mdi-truck-check-outline"></i>
          Опубликовать машину
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { reactive } from 'vue'
import { ElMessage } from 'element-plus'

const form = reactive({
  body_type: '',
  truck_category: 'semi_trailer',
  load_types: [],
  capacity_kg: null,
  volume_m3: null,
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
  location_from_radius_km: null,
  possible_unload: '',
  unload_radius_km: null,
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

const bodyTypes = {
  tent: 'Тентованный',
  refrigerator: 'Рефрижератор',
  open: 'Открытый',
  isotherm: 'Изотерм',
  tank: 'Цистерна',
  container: 'Контейнеровоз',
  car_transporter: 'Автовоз',
  other: 'Другое'
}

const loadTypes = {
  top: 'Верхняя',
  side: 'Боковая',
  rear: 'Задняя',
  full_open: 'Полное открытие',
  crossbar_remove: 'Съём перекладин',
  stand_remove: 'Съём стоек'
}

function submitForm() {
  console.log('✅ Vehicle form data:', form)
  ElMessage.success('Машина успешно опубликована!')
}
</script>

<style scoped>
.vehicle-card {
  max-width: 1100px;
  margin: 30px auto;
  padding: 30px;
  border-radius: 14px;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 24px;
  color: #1e293b;
  display: flex;
  align-items: center;
  gap: 10px;
}

.form-section {
  margin-bottom: 32px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e2e8f0;
}

.form-section h2 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 16px;
  color: #334155;
}

.grid-2 {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.extras {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px 20px;
}

.rate-mode {
  margin-bottom: 16px;
}

.submit-wrapper {
  text-align: right;
  margin-top: 30px;
}

.submit-wrapper .el-button {
  padding: 14px 26px;
  font-weight: 600;
  border-radius: 10px;
  font-size: 16px;
}
</style>
