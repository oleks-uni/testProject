import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const BASE_URL = 'http://localhost:8000/api'

// Main API instance with interceptors
const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Separate instance for refresh requests - NO interceptors, NO auth header
const refreshApi = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

let isRefreshing = false
let failedQueue = []

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(token)
    }
  })
  failedQueue = []
}

// Request interceptor - add auth header (skip for public endpoints)
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.accessToken) {
      config.headers.Authorization = `Bearer ${authStore.accessToken}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor - handle auth errors
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    const status = error.response?.status
    const errorCode = error.response?.data?.error || error.response?.data?.code
    
    // Handle refresh token expired - logout immediately
    if (errorCode === 'token_refresh_expired_error') {
      const authStore = useAuthStore()
      authStore.clearTokens()
      router.push('/login')
      return Promise.reject(error)
    }

    if (originalRequest.url.includes('/auth/token/refresh/')) {
  return Promise.reject(error)
}
    
    // Handle access token expired (401) - try refresh
    const shouldRefresh = status === 401 || errorCode === 'token_expired_error'
    
    if (shouldRefresh && !originalRequest._retry) {
      if (isRefreshing) {
        // Queue requests while refreshing
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject })
        }).then(token => {
          originalRequest.headers.Authorization = `Bearer ${token}`
          return api(originalRequest)
        }).catch(err => Promise.reject(err))
      }
      
      originalRequest._retry = true
      isRefreshing = true
      
      const authStore = useAuthStore()
      
      try {
        // Use refreshApi - no auth header attached
        const response = await refreshApi.post('/auth/token/refresh/', {
          refresh: authStore.refreshToken
        })
        
        const newAccessToken = response.data.access
        authStore.accessToken = newAccessToken
        localStorage.setItem('access_token', newAccessToken)
        
        // Process queued requests with new token
        processQueue(null, newAccessToken)
        
        // Retry original request
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`
        return api(originalRequest)
        
      } catch (refreshError) {
        // Refresh failed - logout user
        processQueue(refreshError, null)
        authStore.clearTokens()
        router.push('/login')
        return Promise.reject(refreshError)
        
      } finally {
        isRefreshing = false
      }
    }
    
    return Promise.reject(error)
  }
)

export default api
