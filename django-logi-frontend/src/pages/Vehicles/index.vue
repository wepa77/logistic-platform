<template>
  <div class="vehicles-page">
    <!-- Header Section -->
    <div class="page-header" v-if="!embedded">
      <div class="header-content">
        <div class="header-left">
          <h1 class="page-title">
            <i class="mdi mdi-truck"></i>
            {{ $t('vehicles.title') }}
          </h1>
          <p class="page-subtitle">{{ $t('vehicles.subtitle') }}</p>
        </div>
        <div class="header-actions">
          <router-link to="/vehicles/add">
            <el-button type="primary" size="large" class="add-btn">
              <i class="mdi mdi-plus"></i>
              {{ $t('vehicles.addNew') }}
            </el-button>
          </router-link>
        </div>
      </div>
    </div>

    <!-- Route Prefilter Summary (from marketplace) -->
    <el-alert
      v-if="prefilterSummary"
      :title="prefilterSummary"
      type="info"
      class="prefilter-banner"
      show-icon
      :closable="false"
    />

    <!-- Filters & Search Section -->
    <el-card class="filters-card" shadow="never" v-if="!embedded">
      <div class="filters-container">
        <el-input
            v-model="searchQuery"
            :placeholder="$t('vehicles.searchPlaceholder') as string"
            class="search-input"
            clearable
        >
          <template #prefix>
            <i class="mdi mdi-magnify"></i>
          </template>
        </el-input>

        <el-select v-model="typeFilter" :placeholder="$t('vehicles.filterByType') as string" clearable class="type-filter">
          <el-option :label="$t('vehicles.allTypes') as string" value="" />
          <el-option :label="$t('vehicles.boxTruck') as string" value="box" />
          <el-option :label="$t('vehicles.flatbed') as string" value="flatbed" />
          <el-option :label="$t('vehicles.refrigerated') as string" value="refrigerated" />
          <el-option :label="$t('vehicles.tanker') as string" value="tanker" />
        </el-select>

        <el-select v-model="gpsFilter" :placeholder="$t('vehicles.gpsStatus') as string" clearable class="gps-filter">
          <el-option :label="$t('vehicles.allVehicles') as string" value="" />
          <el-option :label="$t('vehicles.gpsEnabled') as string" value="enabled" />
          <el-option :label="$t('vehicles.disabled') as string" value="disabled" />
        </el-select>

        <el-button class="filter-btn" @click="fetchVehicles">
          <i class="mdi mdi-refresh"></i>
        </el-button>
      </div>
    </el-card>

    <!-- Stats Cards -->
    <div class="stats-grid" v-if="!embedded">
      <div class="stat-card">
        <div class="stat-icon total">
          <i class="mdi mdi-truck-outline"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ vehicles.length }}</div>
          <div class="stat-label">{{ $t('vehicles.totalVehicles') }}</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon gps">
          <i class="mdi mdi-map-marker-check"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.gpsEnabled }}</div>
          <div class="stat-label">{{ $t('vehicles.gpsEnabledCount') }}</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon capacity">
          <i class="mdi mdi-weight-kilogram"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.totalCapacity.toFixed(0) }}</div>
          <div class="stat-label">{{ $t('vehicles.totalCapacity') }}</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon volume">
          <i class="mdi mdi-cube-outline"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.totalVolume.toFixed(1) }}</div>
          <div class="stat-label">{{ $t('vehicles.totalVolume') }}</div>
        </div>
      </div>
    </div>

    <!-- Vehicles Table -->
    <el-card v-if="!embedded" class="table-card" shadow="never">
      <el-table :data="filteredVehicles" :loading="loading" style="width: 100%" class="modern-table" @row-click="tryOpenDetails">
        <!-- New requested columns -->
        <el-table-column label="Направл." min-width="220">
          <template #default="{ row }">
            <div class="route">
              <span class="city">{{ fromCity(row) }}</span>
              <span class="arrow">→</span>
              <span class="city">{{ toCity(row) }}</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="Транспорт" min-width="200">
          <template #default="{ row }">
            <div class="transport">
              <strong>{{ transportLabel(row) }}</strong>
              <span v-if="row.capacity_kg">, {{ row.capacity_kg }} кг</span>
              <span v-if="row.volume_m3">, {{ row.volume_m3 }} м³</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="Откуда" min-width="160">
          <template #default="{ row }">
            <div class="from">
              <div class="city">{{ fromCity(row) }}</div>
              <div class="note" v-if="availableFrom(row)">с {{ availableFrom(row) }}</div>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="Куда" min-width="160">
          <template #default="{ row }">
            <div class="to">
              <div class="city">{{ toCity(row) }}</div>
              <div class="note" v-if="availableDays(row)">до {{ availableDays(row) }} дн</div>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="Ставка" min-width="200">
          <template #default="{ row }">
            <div class="rate" v-if="hasAnyRate(row)">
              <div v-if="row.rate_with_vat"><b>{{ row.rate_with_vat }}</b> {{ currencyCode(row) }} с НДС</div>
              <div v-if="row.rate_without_vat"><b>{{ row.rate_without_vat }}</b> {{ currencyCode(row) }} без НДС</div>
              <div v-if="row.rate_cash"><b>{{ row.rate_cash }}</b> {{ currencyCode(row) }} нал</div>
              <div v-if="!row.rate_with_vat && !row.rate_without_vat && !row.rate_cash && genericRate(row) != null"><b>{{ genericRate(row) }}</b> {{ currencyCode(row) }}</div>
            </div>
            <div class="rate request" v-else>торг</div>
          </template>
        </el-table-column>

        <el-table-column prop="plate_number" label="Plate Number" width="140">
          <template #default="scope">
            <div class="plate-number">
              <i class="mdi mdi-card-text"></i>
              <span>{{ scope.row.plate_number }}</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="Vehicle Info" min-width="220">
          <template #default="scope">
            <div class="vehicle-info">
              <div class="vehicle-name">{{ scope.row.brand }} {{ scope.row.model }}</div>
              <div class="vehicle-meta">
                <span class="year">
                  <i class="mdi mdi-calendar"></i>
                  {{ scope.row.year }}
                </span>
                <span class="type">
                  <i class="mdi mdi-truck-cargo-container"></i>
                  {{ scope.row.truck_type }}
                </span>
              </div>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="Specifications" min-width="200">
          <template #default="scope">
            <div class="specs">
              <div class="spec-item">
                <i class="mdi mdi-weight-kilogram"></i>
                <span>{{ scope.row.capacity_kg }} kg</span>
              </div>
              <div class="spec-item">
                <i class="mdi mdi-cube-outline"></i>
                <span>{{ scope.row.volume_m3 }} m³</span>
              </div>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="gps_enabled" label="GPS" width="120">
          <template #default="scope">
            <el-tag 
                :type="scope.row.gps_enabled ? 'success' : 'info'"
                :class="`gps-tag ${scope.row.gps_enabled ? 'enabled' : 'disabled'}`"
                effect="plain"
            >
              <i :class="scope.row.gps_enabled ? 'mdi mdi-map-marker-check' : 'mdi mdi-map-marker-off'"></i>
              {{ scope.row.gps_enabled ? 'Enabled' : 'Disabled' }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="Photo" width="100">
          <template #default="scope">
            <el-image
                v-if="scope.row.photo"
                :src="scope.row.photo"
                :preview-src-list="[scope.row.photo]"
                class="vehicle-photo"
                fit="cover"
            >
              <template #error>
                <div class="image-placeholder">
                  <i class="mdi mdi-image-off"></i>
                </div>
              </template>
            </el-image>
            <div v-else class="image-placeholder">
              <i class="mdi mdi-truck"></i>
            </div>
          </template>
        </el-table-column>

        <el-table-column v-if="!embedded" fixed="right" label="Actions" width="160">
          <template #default="scope">
            <div class="action-buttons">
              <el-tooltip content="Edit" placement="top">
                <el-button link type="primary" @click="openDialog(scope.row)">
                  <i class="mdi mdi-pencil"></i>
                </el-button>
              </el-tooltip>
              <el-tooltip content="View Details" placement="top">
                <el-button link type="info">
                  <i class="mdi mdi-eye"></i>
                </el-button>
              </el-tooltip>
              <el-popconfirm
                  title="Are you sure to delete this vehicle?"
                  @confirm="deleteVehicle(scope.row.id)"
              >
                <template #reference>
                  <el-tooltip content="Delete" placement="top">
                    <el-button link type="danger">
                      <i class="mdi mdi-delete"></i>
                    </el-button>
                  </el-tooltip>
                </template>
              </el-popconfirm>
            </div>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination-bar">
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @current-change="onPageChange"
          @size-change="onPageSizeChange"
        />
      </div>
    </el-card>

    <!-- Embedded search list redesigned to match screenshot -->
    <el-card v-else class="table-card" shadow="never">
      <div class="list-header">
        <div class="lh-left"></div>
        <div class="lh-col">Направл.</div>
        <div class="lh-col">Транспорт</div>
        <div class="lh-col">Откуда</div>
        <div class="lh-col">Куда</div>
        <div class="lh-col">Ставка</div>
        <div class="lh-right"></div>
      </div>
      <div class="results-list">
        <div
          v-for="item in filteredVehicles"
          :key="item.id || item.plate_number"
          class="result-row"
        >
          <div class="row-h">
            <!-- Left: checkbox + country badge -->
            <div class="col-left">
              <el-checkbox v-model="rowSelection[rowKey(item)]" @click.stop />
            </div>

            <!-- 5 columns content on gray background -->
            <div class="col-main" @click="tryOpenDetails(item)">
              <div class="cell dir">
                <span class="city">{{ fromCity(item) }}</span>
                <span class="arrow">→</span>
                <span class="city">{{ toCity(item) }}</span>
              </div>
              <div class="cell transport">
                <strong>{{ transportLabel(item) || 'Транспорт' }}</strong>
                <span v-if="item.capacity_kg">, {{ item.capacity_kg }} т</span>
                <span v-if="item.volume_m3">, {{ item.volume_m3 }} м³</span>
                <span v-if="item.length_m || item.width_m || item.height_m" class="dims">
                  • {{ item.length_m || '—' }}×{{ item.width_m || '—' }}×{{ item.height_m || '—' }} м
                </span>
              </div>
              <div class="cell from">
                <div class="city">{{ fromCity(item) }}</div>
                <div class="note" v-if="availableFrom(item)">постоянно ежедневно</div>
              </div>
              <div class="cell to">
                <div class="city">{{ toCity(item) }}</div>
                <div class="variants" v-if="getUnloadVariants(item).length">
                  <div class="variants-title">Возможные варианты разгрузки</div>
                  <div class="variants-list">
                    <template v-for="city in visibleUnloadVariants(item)" :key="city">
                      <div class="variant">{{ city }}</div>
                    </template>
                    <el-link
                      v-if="getUnloadVariants(item).length > maxVisibleUnloads"
                      type="primary"
                      :underline="false"
                      @click.stop="toggleUnloads(item)"
                      class="more-link-inline"
                    >{{ isUnloadsExpanded(item) ? 'Скрыть' : 'Еще' }}</el-link>
                  </div>
                </div>
              </div>
              <div class="cell rate">
                <div v-if="hasAnyRate(item)">
                  <div v-if="item.rate_with_vat"><b>{{ item.rate_with_vat }}</b> {{ currencyCode(item) }} с НДС</div>
                  <div v-if="item.rate_without_vat"><b>{{ item.rate_without_vat }}</b> {{ currencyCode(item) }} без НДС</div>
                  <div v-if="item.rate_cash"><b>{{ item.rate_cash }}</b> {{ currencyCode(item) }} нал</div>
                  <div v-if="!item.rate_with_vat && !item.rate_without_vat && !item.rate_cash && genericRate(item) != null"><b>{{ genericRate(item) }}</b> {{ currencyCode(item) }}</div>
                </div>
                <div v-else class="rate request">торг</div>
                <div class="rate-extra">
                  <el-link type="primary" :underline="false" @click.stop>Отправить предложение</el-link>
                  <div v-if="item.verified_ts || item.has_verified_ts" class="verified-badge">
                    <i class="mdi mdi-truck-check-outline"></i>
                    есть подтвержденные ТС
                  </div>
                </div>
              </div>
            </div>

            <!-- Right action icons -->
            <div class="col-right">
              <div class="col-right-inner">
                <div class="right-top">
                  <el-button circle size="small" type="primary" plain @click.stop="tryOpenDetails(item)">
                    <i class="mdi mdi-message-text-outline"></i>
                  </el-button>
                  <el-button circle size="small" type="warning" plain @click.stop>
                    <i class="mdi mdi-close"></i>
                  </el-button>
                </div>
                <el-link class="complaint-link" :underline="false" type="info" @click.stop>Жалоба</el-link>
              </div>
            </div>

            <!-- Side meta: timestamps like on screenshot -->
            <div class="col-meta">
              <div class="meta-time">
                <div class="time-line">изм <span class="time-strong">{{ formatTimeHM(item.updated_at) || '—' }}</span></div>
                <div class="time-line">доб <span class="time-strong">{{ formatDateDM(item.created_at) || '—' }}</span></div>
              </div>
            </div>
          </div>

          <!-- Bottom line with button and contact -->
          <div class="row-bottom">
            <div class="left-actions">
              <el-button size="small" type="primary" plain @click.stop="tryOpenDetails(item)">
                <i class="mdi mdi-phone"></i>
                ОТКРЫТЬ ПОЛНУЮ ИНФОРМАЦИЮ
              </el-button>
              <span class="hint">Доступно бесплатно после полной регистрации</span>
            </div>
            <div class="company" v-if="item.company_name || item.contact_phone">
              <div class="name">{{ item.company_name || '—' }}</div>
              <div class="contact" v-if="item.contact_phone"><i class="mdi mdi-phone"></i> {{ item.contact_phone }}</div>
            </div>
          </div>
        </div>

        <div class="pagination-bar">
          <el-pagination
            v-model:current-page="page"
            v-model:page-size="pageSize"
            :page-sizes="[10, 20, 50]"
            layout="total, sizes, prev, pager, next, jumper"
            :total="total"
            @current-change="onPageChange"
            @size-change="onPageSizeChange"
          />
        </div>
      </div>
    </el-card>

    <!-- Modern Dialog for create/update -->
    <el-dialog 
        v-if="!embedded"
        v-model="dialogVisible" 
        :title="form.id ? 'Edit Vehicle' : 'Add New Vehicle'" 
        width="700px"
        class="modern-dialog"
    >
      <el-form :model="form" label-position="top" class="vehicle-form">
        <div class="form-grid">
          <el-form-item label="Plate Number" class="form-item-full">
            <el-input v-model="form.plate_number" placeholder="Enter plate number">
              <template #prefix>
                <i class="mdi mdi-card-text"></i>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item label="Brand">
            <el-input v-model="form.brand" placeholder="e.g., Mercedes">
              <template #prefix>
                <i class="mdi mdi-factory"></i>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item label="Model">
            <el-input v-model="form.model" placeholder="e.g., Actros">
              <template #prefix>
                <i class="mdi mdi-truck"></i>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item label="Year">
            <el-input-number v-model="form.year" :min="1900" :max="2100" style="width: 100%" />
          </el-form-item>

          <el-form-item label="Truck Type">
            <el-select v-model="form.truck_type" placeholder="Select type" style="width: 100%">
              <el-option label="Box Truck" value="box" />
              <el-option label="Flatbed" value="flatbed" />
              <el-option label="Refrigerated" value="refrigerated" />
              <el-option label="Tanker" value="tanker" />
              <el-option label="Other" value="other" />
            </el-select>
          </el-form-item>

          <el-form-item label="Capacity (kg)">
            <el-input-number v-model="form.capacity_kg" :min="0" :step="100" style="width: 100%" />
          </el-form-item>

          <el-form-item label="Volume (m³)">
            <el-input-number v-model="form.volume_m3" :min="0" :step="0.5" style="width: 100%" />
          </el-form-item>

          <el-form-item label="GPS Tracking" class="gps-switch-item">
            <div class="switch-wrapper">
              <el-switch v-model="form.gps_enabled" size="large" />
              <span class="switch-label">{{ form.gps_enabled ? 'Enabled' : 'Disabled' }}</span>
            </div>
          </el-form-item>

          <el-form-item label="Vehicle Photo" class="form-item-full">
            <el-upload
                class="photo-uploader"
                :auto-upload="false"
                :show-file-list="false"
                :on-change="onFileChange"
                drag
            >
              <div class="upload-content">
                <i class="mdi mdi-cloud-upload"></i>
                <div class="upload-text">
                  <p>Drop file here or <em>click to upload</em></p>
                  <p class="upload-hint">Support: JPG, PNG (max 5MB)</p>
                </div>
              </div>
            </el-upload>
          </el-form-item>
        </div>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <el-button size="large" @click="dialogVisible = false">
            <i class="mdi mdi-close"></i>
            Cancel
          </el-button>
          <el-button type="primary" size="large" @click="saveVehicle">
            <i class="mdi mdi-check"></i>
            {{ form.id ? 'Update' : 'Create' }} Vehicle
          </el-button>
        </div>
      </template>
    </el-dialog>

    <!-- Access Guard Dialog (profile info) -->
    <el-dialog v-model="guardVisible" title="Укажите данные, чтобы продолжить" width="640px">
      <el-form label-position="top" class="guard-form">
        <div class="guard-grid">
          <el-form-item label="Город*">
            <el-input v-model="guardForm.city" placeholder="Например: Ашхабад" />
          </el-form-item>
          <el-form-item label="Вы">
            <el-radio-group v-model="guardForm.orgType" class="org-type">
              <el-radio-button label="ooo">ООО</el-radio-button>
              <el-radio-button label="ip">ИП</el-radio-button>
              <el-radio-button label="fl">Физлицо</el-radio-button>
              <el-radio-button label="self">Самозанятый</el-radio-button>
              <el-radio-button label="other">Другое</el-radio-button>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="Название фирмы">
            <el-input v-model="guardForm.companyName" placeholder="ООО Пример" />
          </el-form-item>
          <el-form-item label="Ф.И.О.*">
            <el-input v-model="guardForm.fullName" placeholder="Ваше имя и фамилия" />
          </el-form-item>
          <el-form-item label="Email">
            <el-input v-model="guardForm.email" placeholder="you@example.com" />
          </el-form-item>
          <el-form-item label="Моб. телефон*">
            <el-input v-model="guardForm.phone" placeholder="+993 6x xxx-xx-xx" />
          </el-form-item>
          <div class="guard-hint">Данные будут сохранены локально и использованы для связи по объявлениям.</div>
        </div>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="guardVisible = false">Отмена</el-button>
          <el-button type="primary" @click="submitGuard">Продолжить</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- Vehicle Details Drawer -->
    <el-drawer v-model="detailVisible" :with-header="true" title="Vehicle Details" size="40%">
      <div class="details" v-loading="detailLoading">
        <div class="details-row">
          <div class="details-label">Plate Number</div>
          <div class="details-value">{{ detailData?.plate_number || '—' }}</div>
        </div>
        <div class="details-row">
          <div class="details-label">Vehicle Info</div>
          <div class="details-value">{{ (detailData?.brand || '') + ' ' + (detailData?.model || '') }}<span v-if="detailData?.year"> • {{ detailData?.year }}</span><span v-if="detailData?.truck_type"> • {{ detailData?.truck_type }}</span></div>
        </div>
        <div class="details-row">
          <div class="details-label">Specifications</div>
          <div class="details-value">
            <div class="spec-line"><i class="mdi mdi-weight-kilogram"></i> {{ detailData?.capacity_kg ?? '—' }} kg</div>
            <div class="spec-line"><i class="mdi mdi-cube-outline"></i> {{ detailData?.volume_m3 ?? '—' }} m³</div>
            <div class="spec-line" v-if="detailData && (detailData.length_m || detailData.width_m || detailData.height_m)">
              <i class="mdi mdi-ruler"></i>
              {{ detailData.length_m ?? '—' }} × {{ detailData.width_m ?? '—' }} × {{ detailData.height_m ?? '—' }} m
            </div>
          </div>
        </div>
        <div class="details-row">
          <div class="details-label">GPS</div>
          <div class="details-value">
            <el-tag :type="detailData?.gps_enabled ? 'success' : 'info'">
              <i :class="detailData?.gps_enabled ? 'mdi mdi-map-marker-check' : 'mdi mdi-map-marker-off'"></i>
              {{ detailData?.gps_enabled ? 'Enabled' : 'Disabled' }}
            </el-tag>
          </div>
        </div>
        <div class="details-row">
          <div class="details-label">Photo</div>
          <div class="details-value">
            <el-image v-if="detailData?.photo" :src="detailData.photo" :preview-src-list="[detailData.photo]" style="width: 320px; height: 200px; object-fit: cover; border-radius: 8px" />
            <div v-else class="image-placeholder"><i class="mdi mdi-truck"></i></div>
          </div>
        </div>
        <div class="details-row" v-if="detailData?.location_from || detailData?.possible_unload">
          <div class="details-label">Route</div>
          <div class="details-value">
            <div class="spec-line"><i class="mdi mdi-map-marker"></i> {{ detailData?.location_from || '—' }} → {{ detailData?.possible_unload || '—' }}</div>
            <div class="spec-line" v-if="detailData?.location_from_radius_km || detailData?.unload_radius_km">
              <i class="mdi mdi-radar"></i>
              Radius: {{ detailData?.location_from_radius_km ?? '—' }} km / {{ detailData?.unload_radius_km ?? '—' }} km
            </div>
          </div>
        </div>
        <div class="details-row" v-if="detailData?.available_from || detailData?.available_days">
          <div class="details-label">Availability</div>
          <div class="details-value">
            <div class="spec-line"><i class="mdi mdi-calendar-clock"></i> From: {{ detailData?.available_from || '—' }}<span v-if="detailData?.available_days"> • Days: {{ detailData?.available_days }}</span></div>
          </div>
        </div>
        <div class="details-row" v-if="detailData?.rate_with_vat || detailData?.rate_without_vat || detailData?.rate_cash || detailData?.rate_currency">
          <div class="details-label">Rates & Payment</div>
          <div class="details-value">
            <div class="spec-line" v-if="detailData?.rate_with_vat"><i class="mdi mdi-cash-multiple"></i> With VAT: <b>{{ detailData.rate_with_vat }}</b> {{ (detailData.rate_currency && detailData.rate_currency.toUpperCase) ? detailData.rate_currency.toUpperCase() : (detailData.rate_currency || '') }}</div>
            <div class="spec-line" v-if="detailData?.rate_without_vat"><i class="mdi mdi-cash"></i> Without VAT: <b>{{ detailData.rate_without_vat }}</b> {{ (detailData.rate_currency && detailData.rate_currency.toUpperCase) ? detailData.rate_currency.toUpperCase() : (detailData.rate_currency || '') }}</div>
            <div class="spec-line" v-if="detailData?.rate_cash"><i class="mdi mdi-cash-fast"></i> Cash: <b>{{ detailData.rate_cash }}</b> {{ (detailData.rate_currency && detailData.rate_currency.toUpperCase) ? detailData.rate_currency.toUpperCase() : (detailData.rate_currency || '') }}</div>
            <div class="spec-line" v-if="detailData?.pay_to_card"><i class="mdi mdi-credit-card"></i> Pay to card</div>
            <div class="spec-line" v-if="detailData?.without_bargain"><i class="mdi mdi-lock"></i> Without bargain</div>
          </div>
        </div>
        <div class="details-row" v-if="detailData?.has_adr || detailData?.has_lift || detailData?.has_horses || detailData?.partial_load">
          <div class="details-label">Features</div>
          <div class="details-value">
            <el-tag v-if="detailData?.has_adr" type="warning" effect="plain"><i class="mdi mdi-biohazard"></i> ADR</el-tag>
            <el-tag v-if="detailData?.has_lift" type="info" effect="plain" style="margin-left:6px"><i class="mdi mdi-elevator-passenger-outline"></i> Lift</el-tag>
            <el-tag v-if="detailData?.has_horses" type="info" effect="plain" style="margin-left:6px"><i class="mdi mdi-fence"></i> Stakes</el-tag>
            <el-tag v-if="detailData?.partial_load" type="success" effect="plain" style="margin-left:6px"><i class="mdi mdi-truck-outline"></i> Partial load</el-tag>
          </div>
        </div>
        <div class="details-row" v-if="detailData?.company_name || detailData?.contact_phone || detailData?.city">
          <div class="details-label">Company</div>
          <div class="details-value">
            <div class="spec-line" v-if="detailData?.company_name"><i class="mdi mdi-domain"></i> {{ detailData.company_name }}</div>
            <div class="spec-line" v-if="detailData?.city"><i class="mdi mdi-city"></i> {{ detailData.city }}</div>
            <div class="spec-line" v-if="detailData?.contact_phone"><i class="mdi mdi-phone"></i> {{ detailData.contact_phone }}</div>
          </div>
        </div>
        <div class="details-row" v-if="detailData?.updated_at || detailData?.created_at">
          <div class="details-label">Meta</div>
          <div class="details-value">
            <div class="spec-line" v-if="detailData?.updated_at"><i class="mdi mdi-update"></i> Updated: {{ detailData.updated_at }}</div>
            <div class="spec-line" v-if="detailData?.created_at"><i class="mdi mdi-calendar-plus"></i> Created: {{ detailData.created_at }}</div>
          </div>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getVehicles, getVehicle, createVehicle, updateVehicle, deleteVehicleApi } from '@/api/api'

const { embedded = false } = defineProps<{ embedded?: boolean }>()

interface Vehicle {
  id?: number
  plate_number: string
  brand: string
  model: string
  year: number | null
  capacity_kg: number
  volume_m3: number
  truck_type: string
  gps_enabled: boolean
  photo?: string
  // Additional optional fields that may come from backend
  length_m?: number | null
  width_m?: number | null
  height_m?: number | null
  location_from?: string | null
  possible_unload?: string | null
  location_from_radius_km?: number | null
  unload_radius_km?: number | null
  available_from?: string | null
  available_days?: number | null
  rate_with_vat?: number | null
  rate_without_vat?: number | null
  rate_cash?: number | null
  rate_currency?: string | null
  pay_to_card?: boolean | null
  without_bargain?: boolean | null
  partial_load?: boolean | null
  has_adr?: boolean | null
  has_lift?: boolean | null
  has_horses?: boolean | null
  company_name?: string | null
  contact_phone?: string | null
  city?: string | null
  updated_at?: string | null
  created_at?: string | null
  // Optional enhanced destination variants
  unload_variants?: string[] | null
  possible_unload_variants?: string[] | null
  unload_variants_text?: string | null
  // UI badges/labels
  country_code?: string | null
  priority?: string | number | null
  // Verification
  verified_ts?: boolean | null
  has_verified_ts?: boolean | null
 }

const vehicles = ref<Vehicle[]>([])
const dialogVisible = ref(false)
const searchQuery = ref('')
const typeFilter = ref('')
const gpsFilter = ref('')

// Pagination & loading
const loading = ref(false)
const page = ref(Number((useRoute().query.page as string) || 1))
const pageSize = ref(Number((useRoute().query.page_size as string) || 10))
const total = ref(0)

// Prefilter summary from marketplace route query
const route = useRoute()
const prefilterSummary = computed(() => {
  const from = (route.query.from as string) || ''
  const to = (route.query.to as string) || ''
  const date = (route.query.date as string) || ''
  const radius = route.query.radius as string | undefined
  if (!from && !to && !date && !radius) return ''
  const parts: string[] = []
  if (from) parts.push(`From: ${from}`)
  if (to) parts.push(`To: ${to}`)
  if (date) parts.push(`Date: ${date}`)
  if (radius) parts.push(`Radius: ${radius} km`)
  return `Searching vehicles — ${parts.join(' • ')}`
})

const form = ref<Vehicle>({
  plate_number: '',
  brand: '',
  model: '',
  year: null,
  capacity_kg: 0,
  volume_m3: 0,
  truck_type: '',
  gps_enabled: false
})
let file: File | null = null

// Computed stats
const stats = computed(() => {
  return {
    gpsEnabled: vehicles.value.filter(v => v.gps_enabled).length,
    totalCapacity: vehicles.value.reduce((sum, v) => sum + v.capacity_kg, 0),
    totalVolume: vehicles.value.reduce((sum, v) => sum + v.volume_m3, 0),
  }
})

// Filtered vehicles
const filteredVehicles = computed(() => {
  let filtered = vehicles.value

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(vehicle =>
        vehicle.plate_number.toLowerCase().includes(query) ||
        vehicle.brand.toLowerCase().includes(query) ||
        vehicle.model.toLowerCase().includes(query) ||
        vehicle.truck_type.toLowerCase().includes(query)
    )
  }

  // Filter by type
  if (typeFilter.value) {
    filtered = filtered.filter(vehicle => vehicle.truck_type === typeFilter.value)
  }

  // Filter by GPS status
  if (gpsFilter.value) {
    const isEnabled = gpsFilter.value === 'enabled'
    filtered = filtered.filter(vehicle => vehicle.gps_enabled === isEnabled)
  }

  return filtered
})

// ---- Unload variants helpers (embedded list) ----
const maxVisibleUnloads = 2
const expandedUnloads = ref<Record<string, boolean>>({})
const rowSelection = ref<Record<string, boolean>>({})

function rowKey(item: any): string {
  return String(item?.id ?? item?.plate_number ?? Math.random())
}

function getUnloadVariants(item: any): string[] {
  if (!item) return []
  const arr = (item.unload_variants || item.possible_unload_variants) as any
  if (Array.isArray(arr)) return arr.filter(Boolean)
  const text = (item.unload_variants_text || '') as string
  if (typeof text === 'string' && text.trim()) {
    return text.split(/[,;\n]/).map(s => s.trim()).filter(Boolean)
  }
  return []
}

function isUnloadsExpanded(item: any): boolean {
  return !!expandedUnloads.value[rowKey(item)]
}

function visibleUnloadVariants(item: any): string[] {
  const list = getUnloadVariants(item)
  if (!list.length) return []
  return isUnloadsExpanded(item) ? list : list.slice(0, maxVisibleUnloads)
}

function toggleUnloads(item: any) {
  const key = rowKey(item)
  expandedUnloads.value[key] = !expandedUnloads.value[key]
}

// ---- Display helpers to normalize backend field names ----
function pick(row: any, keys: string[], fallback: string = '—'): any {
  if (!row) return fallback
  for (const k of keys) {
    const v = row[k]
    if (v !== undefined && v !== null && String(v).toString().trim() !== '') return v
  }
  return fallback
}

function fromCity(row: any): string {
  return String(pick(row, ['location_from','from','from_city','pickup_address','load_city','city']))
}
function toCity(row: any): string {
  return String(pick(row, ['possible_unload','to','to_city','delivery_address','unload_city','unload']))
}
function transportLabel(row: any): string {
  const val = pick(row, ['truck_type','truck_category','body_type','vehicle_type','type'], '—')
  return String(val)
}
function availableFrom(row: any): string | '' {
  const v = pick(row, ['available_from','ready_from','ready_date','availableDate','available'], '')
  return String(v || '')
}
function availableDays(row: any): number | '' {
  const v = pick(row, ['available_days','days_available','available_for_days'], '')
  return v === '' ? '' : Number(v)
}
function currencyCode(row: any): string {
  const c = pick(row, ['rate_currency','currency'], '')
  return c ? String(c).toUpperCase() : ''
}
function hasAnyRate(row: any): boolean {
  return !!(row?.rate_with_vat || row?.rate_without_vat || row?.rate_cash || row?.rate || row?.price)
}
function genericRate(row: any): number | null {
  const v = row?.rate ?? row?.price ?? null
  return v != null ? Number(v) : null
}

function formatTimeHM(v?: any): string {
  if (!v) return ''
  try {
    const d = new Date(v)
    return d.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
  } catch {
    return ''
  }
}
function formatDateDM(v?: any): string {
  if (!v) return ''
  try {
    const d = new Date(v)
    // e.g., "11 авг"
    const day = d.toLocaleDateString('ru-RU', { day: '2-digit' })
    const mon = d.toLocaleDateString('ru-RU', { month: 'short' }).replace('.', '')
    return `${day} ${mon}`
  } catch {
    return ''
  }
}

async function fetchVehicles() {
  loading.value = true
  try {
    // Build params from route.query + pagination
    const q = route.query as Record<string, any>
    const params: Record<string, any> = { ...q }
    params.page = page.value
    params.page_size = pageSize.value

    // Normalize booleans that may come as '1' from Search page
    ;['has_adr','has_lift','has_horses','has_gps','partial_load','without_bargain','pay_to_card'].forEach(k => {
      if (params[k] === '1' || params[k] === 'true') params[k] = 1
    })

    const { data } = await getVehicles(params)
    if (Array.isArray(data)) {
      vehicles.value = data as any
      total.value = data.length
    } else if (data && typeof data === 'object' && 'results' in data) {
      vehicles.value = (data as any).results
      total.value = Number((data as any).count || 0)
    } else {
      vehicles.value = []
      total.value = 0
    }
  } finally {
    loading.value = false
  }
}

function openDialog(vehicle?: Vehicle) {
  if (vehicle) {
    form.value = { ...vehicle }
  } else {
    form.value = { 
      plate_number: '',
      brand: '',
      model: '',
      year: null,
      capacity_kg: 0,
      volume_m3: 0,
      truck_type: '',
      gps_enabled: false 
    }
  }
  file = null
  dialogVisible.value = true
}

function onFileChange(uploadFile: any) {
  file = uploadFile.raw
}

async function saveVehicle() {
  const formData = new FormData()
  Object.entries(form.value).forEach(([key, val]) => {
    if (val !== null && val !== undefined) formData.append(key, String(val))
  })
  if (file) formData.append('photo', file)

  if (form.value.id) {
    await updateVehicle(form.value.id, formData)
    ElMessage.success('Vehicle updated successfully')
  } else {
    await createVehicle(formData)
    ElMessage.success('Vehicle created successfully')
  }
  dialogVisible.value = false
  await fetchVehicles()
}

async function deleteVehicle(id: number) {
  await deleteVehicleApi(id)
  ElMessage.success('Vehicle deleted successfully')
  await fetchVehicles()
}

// Details drawer state and handler
const detailVisible = ref(false)
const detailLoading = ref(false)
const detailData = ref<any | null>(null)

async function onRowClick(row: any) {
  detailVisible.value = true
  detailData.value = row
  if (row && row.id) {
    detailLoading.value = true
    try {
      const { data } = await getVehicle(row.id)
      // Merge to preserve any client-only fields
      detailData.value = { ...row, ...data }
    } catch (e) {
      // Non-blocking: show what we have
    } finally {
      detailLoading.value = false
    }
  }
}

const router = useRouter()

// Sync when route.query changes (filters or page)
watch(() => route.query, () => {
  page.value = Number((route.query.page as string) || 1)
  pageSize.value = Number((route.query.page_size as string) || pageSize.value)
  fetchVehicles()
})

function onPageChange(p: number) {
  router.push({ query: { ...route.query, page: String(p) } })
}
function onPageSizeChange(ps: number) {
  router.push({ query: { ...route.query, page: '1', page_size: String(ps) } })
}

onMounted(fetchVehicles)

// -------- Guard dialog logic --------
const guardVisible = ref(false)
const guardForm = ref({
  city: '',
  orgType: 'ooo',
  companyName: '',
  fullName: '',
  email: '',
  phone: ''
})
const pendingRow = ref<any | null>(null)

function isProfileCompleted(): boolean {
  return localStorage.getItem('profileCompleted') === '1'
}

async function tryOpenDetails(row: any) {
  if (!isProfileCompleted()) {
    pendingRow.value = row
    guardVisible.value = true
  } else {
    await onRowClick(row)
  }
}

function submitGuard() {
  // minimal validation
  if (!guardForm.value.city || !guardForm.value.fullName || !guardForm.value.phone) {
    ElMessage.error('Заполните обязательные поля: Город, Ф.И.О. и телефон')
    return
  }
  try {
    const data = {
      city: guardForm.value.city,
      orgType: guardForm.value.orgType,
      companyName: guardForm.value.companyName,
      fullName: guardForm.value.fullName,
      email: guardForm.value.email,
      phone: guardForm.value.phone,
    }
    localStorage.setItem('profileData', JSON.stringify(data))
    localStorage.setItem('profileCompleted', '1')
  } catch (e) {
    // ignore storage errors
  }
  guardVisible.value = false
  if (pendingRow.value) {
    const row = pendingRow.value
    pendingRow.value = null
    tryOpenDetails(row) // now it will pass
  }
}
</script>

<style scoped>
.vehicles-page {
  max-width: 1400px;
  margin: 0 auto;
}

/* Page Header */
.page-header {
  margin-bottom: 24px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
}

.header-left {
  flex: 1;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 8px 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-title i {
  color: #3b82f6;
  font-size: 32px;
}

.page-subtitle {
  font-size: 15px;
  color: #64748b;
  margin: 0;
}

.add-btn {
  padding: 12px 24px;
  font-weight: 600;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

.add-btn i {
  margin-right: 6px;
  font-size: 18px;
}

/* Filters Card */
.filters-card {
  margin-bottom: 20px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.filters-container {
  display: flex;
  gap: 12px;
  align-items: center;
}

.search-input {
  flex: 1;
  max-width: 400px;
}

.type-filter,
.gps-filter {
  width: 180px;
}

.filter-btn {
  padding: 12px;
  font-size: 20px;
  border-radius: 8px;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: white;
}

.stat-icon.total {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.stat-icon.gps {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.stat-icon.capacity {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.stat-icon.volume {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #0f172a;
  line-height: 1;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #64748b;
  font-weight: 500;
}

/* Table Card */
.table-card {
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.modern-table {
  border-radius: 8px;
  overflow: hidden;
}

.modern-table :deep(.el-table__header) {
  background: #f8fafc;
}

.modern-table :deep(th) {
  background: #f8fafc !important;
  color: #475569;
  font-weight: 600;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.modern-table :deep(.el-table__row:hover) {
  background: #f8fafc;
}

.plate-number {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 700;
  color: #0f172a;
  font-family: monospace;
  font-size: 15px;
}

.plate-number i {
  color: #3b82f6;
  font-size: 18px;
}

.vehicle-info {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.vehicle-name {
  font-weight: 600;
  color: #0f172a;
  font-size: 15px;
}

.vehicle-meta {
  display: flex;
  gap: 12px;
  font-size: 13px;
  color: #64748b;
}

.vehicle-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.vehicle-meta i {
  color: #94a3b8;
  font-size: 14px;
}

.specs {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.spec-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #64748b;
}

.spec-item i {
  color: #94a3b8;
  font-size: 16px;
}

.gps-tag {
  font-weight: 600;
  font-size: 12px;
  padding: 6px 12px;
  border-radius: 6px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.gps-tag i {
  font-size: 14px;
}

.vehicle-photo {
  width: 64px;
  height: 64px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.vehicle-photo:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.image-placeholder {
  width: 64px;
  height: 64px;
  border-radius: 8px;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #cbd5e1;
  font-size: 24px;
}

.action-buttons {
  display: flex;
  gap: 4px;
  align-items: center;
}

.action-buttons :deep(.el-button) {
  font-size: 18px;
  padding: 8px;
  transition: all 0.3s ease;
}

.action-buttons :deep(.el-button:hover) {
  transform: scale(1.1);
}

/* Dialog Styles */
.modern-dialog :deep(.el-dialog) {
  border-radius: 16px;
  overflow: hidden;
}

.modern-dialog :deep(.el-dialog__header) {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  padding: 20px 24px;
  margin: 0;
}

.modern-dialog :deep(.el-dialog__title) {
  color: white;
  font-weight: 600;
  font-size: 18px;
}

.modern-dialog :deep(.el-dialog__headerbtn .el-dialog__close) {
  color: white;
  font-size: 20px;
}

.modern-dialog :deep(.el-dialog__body) {
  padding: 24px;
}

.vehicle-form {
  margin-top: 8px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.form-item-full {
  grid-column: 1 / -1;
}

.vehicle-form :deep(.el-form-item__label) {
  font-weight: 600;
  color: #334155;
  margin-bottom: 8px;
}

.vehicle-form :deep(.el-input__wrapper) {
  border-radius: 8px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.gps-switch-item {
  display: flex;
  align-items: center;
}

.switch-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
}

.switch-label {
  font-size: 14px;
  font-weight: 600;
  color: #64748b;
}

.photo-uploader :deep(.el-upload-dragger) {
  border-radius: 8px;
  border: 2px dashed #cbd5e1;
  background: #f8fafc;
  padding: 30px;
  transition: all 0.3s ease;
}

.photo-uploader :deep(.el-upload-dragger:hover) {
  border-color: #3b82f6;
  background: #eff6ff;
}

.upload-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.upload-content i {
  font-size: 48px;
  color: #3b82f6;
}

.upload-text {
  text-align: center;
}

.upload-text p {
  margin: 0;
  color: #64748b;
  font-size: 14px;
}

.upload-text em {
  color: #3b82f6;
  font-style: normal;
  font-weight: 600;
}

.upload-hint {
  font-size: 12px !important;
  color: #94a3b8 !important;
  margin-top: 4px !important;
}

.dialog-footer {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.dialog-footer .el-button {
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
}

.dialog-footer .el-button i {
  margin-right: 6px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
  }

  .filters-container {
    flex-direction: column;
  }

  .search-input,
  .type-filter,
  .gps-filter {
    width: 100%;
    max-width: none;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .form-grid {
    grid-template-columns: 1fr;
  }
}
/* Embedded results list styles */
.list-header {
  display: grid;
  grid-template-columns: 80px repeat(5, 1fr) 80px 160px;
  gap: 8px;
  padding: 6px 12px;
  color: #6b7280;
  font-size: 12px;
  border: 1px solid #e5e7eb;
  border-bottom: none;
  border-radius: 10px 10px 0 0;
  background: #fff;
}
.lh-col { text-transform: none; }
.results-list { display: flex; flex-direction: column; gap: 10px; }
.result-row { border: 1px solid #e5e7eb; border-radius: 10px; overflow: hidden; background: #fff; }
.result-row:hover { box-shadow: 0 4px 12px rgba(0,0,0,.06); }

/* Horizontal row layout to match screenshot */
.row-h { display: grid; grid-template-columns: 80px 1fr 100px 160px; align-items: stretch; gap: 0; }
.col-left { display: flex; align-items: center; gap: 8px; padding: 12px; }
.country-badge { font-size: 12px; background: #f3f4f6; border: 1px solid #e5e7eb; color: #111827; padding: 2px 6px; border-radius: 4px; }
.col-main { background: #f6f7f9; display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; padding: 10px 12px; }
.col-right { display: flex; align-items: center; justify-content: center; gap: 8px; padding: 10px; }
.col-meta { display: flex; flex-direction: column; justify-content: center; align-items: flex-end; padding: 10px 12px; color: #6b7280; font-size: 12px; }
.meta-title { margin-bottom: 4px; }
.meta-value { color: #64748b; }
.meta-time { display: flex; flex-direction: column; align-items: flex-end; gap: 2px; }
.meta-time .time-line { color: #6b7280; }
.meta-time .time-strong { color: #111827; font-weight: 600; }

.cell { color: #111827; font-size: 14px; }
.cell .city { font-weight: 600; }
.cell .note { font-size: 12px; color: #64748b; }
.transport strong { font-weight: 700; }
.transport .dims { color: #64748b; margin-left: 6px; }
.features { display: inline-flex; gap: 6px; margin-left: 8px; color: #94a3b8; }
.feature.success { color: #10b981; }
.arrow { text-align: center; color: #64748b; margin: 0 6px; }
.rate { font-size: 14px; color: #111827; }
.rate.request { color: #f59e0b; font-weight: 700; }
.rate-extra { margin-top: 6px; display: flex; flex-direction: column; gap: 4px; }
.verified-badge { display: inline-flex; align-items: center; gap: 6px; color: #10b981; font-size: 12px; }
.verified-badge i { font-size: 16px; }
.col-right-inner { display: flex; flex-direction: column; align-items: center; gap: 6px; }
.right-top { display: flex; gap: 8px; }
.complaint-link { font-size: 12px; color: #6b7280; }

.row-bottom { display: flex; justify-content: space-between; align-items: center; padding: 10px 12px; }
.left-actions { display: flex; align-items: center; gap: 10px; }
.left-actions .hint { color: #9ca3af; font-size: 12px; }
.company .name { font-weight: 600; }
.company .contact { color: #64748b; font-size: 13px; }
.time { font-size: 12px; color: #64748b; }

/* Unload variants block */
.variants { margin-top: 6px; }
.variants-title { color: #6b7280; font-size: 12px; }
.variants-list { display: flex; flex-direction: column; gap: 2px; }
.variant { color: #111827; font-size: 13px; }
.more-link-inline { padding-left: 0; }

/* Details Drawer tweaks */
.details { display: flex; flex-direction: column; gap: 12px; }
.details-row { display: flex; gap: 16px; align-items: flex-start; }
.details-label { width: 140px; font-weight: 600; color: #334155; }
.details-value { flex: 1; color: #0f172a; }
.spec-line { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; color: #475569; }

@media (max-width: 1024px) {
  .row-h { grid-template-columns: 60px 1fr; }
  .col-right, .col-meta { display: none; }
  .col-main { grid-template-columns: 1fr; }
}

</style>
