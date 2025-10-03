import { http } from '../http'
import type { IVehicle } from '@/types/models'
export const list = (params?: any) => http.get<IVehicle[]>('/vehicles/', { params })
export const create = (payload: Partial<IVehicle>) => http.post<IVehicle>('/vehicles/', payload)
export const update = (id:number, payload: Partial<IVehicle>) => http.patch<IVehicle>(`/vehicles/${id}/`, payload)
export const remove = (id:number) => http.delete(`/vehicles/${id}/`)
