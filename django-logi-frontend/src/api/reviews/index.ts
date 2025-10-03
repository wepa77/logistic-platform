import { http } from '../http'
import type { IReview } from '@/types/models'
export const list = (p?: any)=> http.get<IReview[]>('/reviews/', { params:p })
export const create = (payload: Partial<IReview>) => http.post<IReview>('/reviews/', payload)
export const update = (id:number, payload: Partial<IReview>) => http.patch<IReview>(`/reviews/${id}/`, payload)
export const remove = (id:number) => http.delete(`/reviews/${id}/`)
