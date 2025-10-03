import { http } from '../http'
import type { IUser } from '@/types/models'
export const me = () => http.get<IUser>('/auth/me/')
