import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || null)
  const isLoggedIn = computed(() => !!token.value && !!user.value)

  async function login(username, password) {
    try {
      const response = await axios.post('/api/auth/login', {
        username,
        password
      })
      if (response.data.success) {
        token.value = response.data.data.access_token
        user.value = response.data.data.user
        localStorage.setItem('token', token.value)
        axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
        return true
      }
      return false
    } catch (error) {
      console.error('登录失败:', error)
      return false
    }
  }

  async function register(username, password) {
    try {
      const response = await axios.post('/api/auth/register', {
        username,
        password
      })
      return response.data.success
    } catch (error) {
      console.error('注册失败:', error)
      return false
    }
  }

  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
    delete axios.defaults.headers.common['Authorization']
  }

  function initAuth() {
    if (token.value) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
    }
  }

  return {
    user,
    token,
    isLoggedIn,
    login,
    register,
    logout,
    initAuth
  }
})