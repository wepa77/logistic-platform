// src/store/auth.ts
import { defineStore } from 'pinia'
import { http } from '@/api/http'
import type { IUser } from '@/types/models'
import { router } from '@/router'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    // Hydrate user from localStorage so role-based sidebar persists across refresh
    user: (() => {
      const raw = localStorage.getItem('user')
      try { return raw ? (JSON.parse(raw) as IUser) : null } catch { return null }
    })(),
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

      // fetch user profile (will also persist user)
      await this.fetchMe()

      // 🔥 redirect to dashboard
      router.push('/')
    },
    async fetchMe() {
      try {
        const { data } = await http.get<IUser>('/auth/me/')
        this.user = data
        // persist user so UI has immediate access on next load
        localStorage.setItem('user', JSON.stringify(data))
      } catch {
        this.logout()
      }
    },
    logout() {
      this.user = null
      this.access = ''
      this.refresh = ''
      localStorage.removeItem('user')
      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
      router.push('/login')
    },

    async updateUserType(userType: 'carrier' | 'shipper') {
      try {
        await http.patch('/auth/set-type/', { user_type: userType })
        await this.fetchMe()
        return true
      } catch (error) {
        console.error('Failed to update user type:', error)
        throw error
      }
    }
  }
})
