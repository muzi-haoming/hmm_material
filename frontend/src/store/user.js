/**
 * 用户状态管理
 */
import { defineStore } from 'pinia'
import { login as loginApi, getCurrentUser } from '@/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: uni.getStorageSync('token') || '',
    user: uni.getStorageSync('user') || null,
    isLoggedIn: !!uni.getStorageSync('token')
  }),

  getters: {
    isAdmin: (state) => state.user?.role?.code === 'admin',
    userRole: (state) => state.user?.role?.code || '',
    userRoleName: (state) => state.user?.role?.name || '未知角色',
    userName: (state) => state.user?.name || state.user?.username || ''
  },

  actions: {
    /**
     * 登录
     */
    async login(username, password) {
      try {
        const res = await loginApi(username, password)
        this.token = res.access_token
        this.user = res.user
        this.isLoggedIn = true

        // 保存到本地
        uni.setStorageSync('token', res.access_token)
        uni.setStorageSync('user', res.user)

        return res
      } catch (error) {
        throw error
      }
    },

    /**
     * 登出
     */
    logout() {
      this.token = ''
      this.user = null
      this.isLoggedIn = false

      uni.removeStorageSync('token')
      uni.removeStorageSync('user')

      uni.reLaunch({ url: '/pages/login/login' })
    },

    /**
     * 检查登录状态
     */
    async checkAuth() {
      if (!this.token) {
        return false
      }

      try {
        const user = await getCurrentUser()
        this.user = user
        uni.setStorageSync('user', user)
        return true
      } catch (error) {
        this.logout()
        return false
      }
    },

    /**
     * 更新用户信息
     */
    updateUser(userData) {
      this.user = { ...this.user, ...userData }
      uni.setStorageSync('user', this.user)
    }
  }
})
