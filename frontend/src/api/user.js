/**
 * 用户相关 API
 */
import { get, put, del } from '@/utils/request'

/**
 * 获取当前用户信息
 */
export const getCurrentUser = () => {
  return get('/users/me')
}

/**
 * 更新当前用户信息
 */
export const updateCurrentUser = (data) => {
  return put('/users/me', data)
}

/**
 * 获取用户列表（管理员）
 */
export const getUserList = (params = {}) => {
  return get('/users', params)
}

/**
 * 获取用户详情
 */
export const getUser = (id) => {
  return get(`/users/${id}`)
}

/**
 * 更新用户
 */
export const updateUser = (id, data) => {
  return put(`/users/${id}`, data)
}

/**
 * 删除用户
 */
export const deleteUser = (id) => {
  return del(`/users/${id}`)
}
