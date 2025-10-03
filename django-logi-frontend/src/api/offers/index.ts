import { http } from '../http'
import type { IOffer } from '@/types/models'
export const list = (p?: any)=> http.get<IOffer[]>('/offers/', { params:p })
export const create = (payload: Partial<IOffer>) => http.post<IOffer>('/offers/', payload)
export const update = (id:number, payload: Partial<IOffer>) => http.patch<IOffer>(`/offers/${id}/`, payload)
export const remove = (id:number) => http.delete(`/offers/${id}/`)
