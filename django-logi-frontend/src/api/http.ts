// src/api/http.ts
import axios from 'axios'

// Django API bazowy URL
const http = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api',
  timeout: 10000
})

// Access tokeni awtomatik goşmak
http.interceptors.request.use((config) => {
  const token = localStorage.getItem('access')
  if (token) {
    config.headers = config.headers || {}
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export { http }
