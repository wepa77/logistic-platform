// src/store/auth.ts
import { defineStore } from 'pinia'
import { http } from '@/api/http'
import type { IUser } from '@/types/models'
import { router } from '@/router'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as IUser | null,
    access: localStorage.getItem('access') || '',
    refresh: localStorage.getItem('refresh') || ''
  }),
  getters: {
    isAuthed: (s) => !!s.access,
    isCarrier: (s) => s.user?.user_type === 'carrier',
    isShipper: (s) => s.user?.user_type === 'shipper'
  },
  actions: {
    async login(username: string, password: string) {
      const { data } = await http.post<{ access: string; refresh: string }>(
        '/auth/token/',
        { username, password }
      )
      // ✅ save tokens
      this.access = data.access
      this.refresh = data.refresh
      localStorage.setItem('access', data.access)
      localStorage.setItem('refresh', data.refresh)

      // fetch user profile
      await this.fetchMe()

      // 🔥 redirect to dashboard
      router.push('/')
    },
    async fetchMe() {
      try {
        const { data } = await http.get<IUser>('/auth/me/')
        this.user = data
      } catch {
        // token expired or invalid
        this.logout()
      }
    },
    logout() {
      this.user = null
      this.access = ''
      this.refresh = ''
      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
      router.push('/login')
    }
  }
})
