import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '../../api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  const isLoggedIn = computed(() => !!token.value)
  const userRole = computed(() => user.value?.role || '')

  function setToken(newToken) {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  function setUser(newUser) {
    user.value = newUser
    localStorage.setItem('user', JSON.stringify(newUser))
  }

  async function login(credentials) {
    try {
      const response = await authApi.login(credentials)
      if (response.data.code === 200) {
        const { token: newToken, userId, username, role } = response.data.data
        setToken(newToken)
        setUser({ userId, username, role })
        return true
      }
      return false
    } catch (error) {
      console.error('Login failed:', error)
      throw error
    }
  }

  async function register(userData) {
    try {
      const response = await authApi.register(userData)
      return response.data.code === 200
    } catch (error) {
      console.error('Registration failed:', error)
      throw error
    }
  }

  function logout() {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  return {
    token,
    user,
    isLoggedIn,
    userRole,
    setToken,
    setUser,
    login,
    register,
    logout
  }
})
