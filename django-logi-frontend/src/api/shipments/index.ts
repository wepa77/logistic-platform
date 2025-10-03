import { http } from '../http'
import type { IShipment } from '@/types/models'
export const list = (p?: any)=> http.get<IShipment[]>('/shipments/', { params:p })
export const create = (payload: Partial<IShipment>) => http.post<IShipment>('/shipments/', payload)
export const update = (id:number, payload: Partial<IShipment>) => http.patch<IShipment>(`/shipments/${id}/`, payload)
