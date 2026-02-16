import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref(localStorage.getItem('access_token') || null)
  const refreshToken = ref(localStorage.getItem('refresh_token') || null)
  const user = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => !!accessToken.value)

  const setTokens = (access, refresh) => {
    accessToken.value = access
    refreshToken.value = refresh
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)
  }

  const clearTokens = () => {
    accessToken.value = null
    refreshToken.value = null
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  const login = async (email, password) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.post('/auth/token/', { email, password })
      setTokens(response.data.access, response.data.refresh)
      return true
    } catch (err) {
      error.value = err.response?.data?.detail || 'Login failed'
      return false
    } finally {
      loading.value = false
    }
  }

  const register = async (email, password, password2) => {
    loading.value = true
    error.value = null
    
    try {
      await api.post('/auth/register/', { email, password, password2 })
      return true
    } catch (err) {
      error.value = err.response?.data?.email?.[0] || err.response?.data?.password?.[0] || err.response?.data?.detail || 'Registration failed'
      return false
    } finally {
      loading.value = false
    }
  }

  const logout = async () => {
    try {
      if (refreshToken.value) {
        await api.post('/auth/logout/', { refresh: refreshToken.value })
      }
    } catch (err) {
      console.error('Logout error:', err)
    } finally {
      clearTokens()
    }
  }

  const refreshAccessToken = async () => {
    try {
      const response = await api.post('/auth/token/refresh/', {
        refresh: refreshToken.value
      })
      accessToken.value = response.data.access
      localStorage.setItem('access_token', response.data.access)
      return true
    } catch (err) {
      clearTokens()
      return false
    }
  }

  return {
    accessToken,
    refreshToken,
    user,
    loading,
    error,
    isAuthenticated,
    login,
    register,
    logout,
    refreshAccessToken,
    clearTokens
  }
})
