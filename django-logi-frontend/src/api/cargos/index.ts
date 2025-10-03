import { http } from '../http'
import type { ICargo } from '@/types/models'
export const list = (p?: any)=> http.get<ICargo[]>('/cargos/', { params:p })
export const create = (payload: Partial<ICargo>) => http.post<ICargo>('/cargos/', payload)
export const update = (id:number, payload: Partial<ICargo>) => http.patch<ICargo>(`/cargos/${id}/`, payload)
export const remove = (id:number) => http.delete(`/cargos/${id}/`)
