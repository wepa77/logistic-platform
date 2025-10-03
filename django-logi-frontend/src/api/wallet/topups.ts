import { http } from '../http'
import type { ITopUp } from '@/types/models'
export const list = () => http.get<ITopUp[]>('/topups/')
export const create = (amount:number) => http.post<ITopUp>('/topups/', { amount })
