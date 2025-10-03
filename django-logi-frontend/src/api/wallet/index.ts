import { http } from '../http'
import type { IWalletTx } from '@/types/models'
export const list = () => http.get<IWalletTx[]>('/wallet/')
export const balance = () => http.get<{balance:string}>('/topups/balance/')
