import api from './api'

export interface DictItem {
  id: number
  code: string
  name_tk: string
  name_ru: string | null
  name_en: string | null
  is_active: boolean
  ordering: number
}

// Generic fetcher
const list = (path: string) => api.get<DictItem[]>(path).then(res => res.data)

// Vehicles
export const getVehicleBodyTypes = () => list('/dicts/vehicle-body-types/')
export const getVehicleLoadTypes = () => list('/dicts/vehicle-load-types/')
export const getVehicleTruckCategories = () => list('/dicts/vehicle-truck-categories/')
export const getVehicleRateTypes = () => list('/dicts/vehicle-rate-types/')

// Shared
export const getCurrencies = () => list('/dicts/currencies/')
export const getCompanyTypes = () => list('/dicts/company-types/')

// Cargos
export const getCargoBodyTypes = () => list('/dicts/cargo-body-types/')
export const getCargoLoadTypes = () => list('/dicts/cargo-load-types/')
export const getCargoRateTypes = () => list('/dicts/cargo-rate-types/')
export const getCargoPaymentMethods = () => list('/dicts/cargo-payment-methods/')

// New dictionaries
export const getCargoTypes = () => list('/dicts/cargo-types/')
export const getReadyStatuses = () => list('/dicts/ready-statuses/')
export const getVehicleTruckTypes = () => list('/dicts/vehicle-truck-types/')
