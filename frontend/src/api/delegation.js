/**
 * 委托函相关 API
 */
import { get, post, put } from '@/utils/request'

/**
 * 获取委托函列表
 */
export const getDelegationList = (params = {}) => {
  return get('/delegations', params)
}

/**
 * 获取委托函详情
 */
export const getDelegation = (id) => {
  return get(`/delegations/${id}`)
}

/**
 * 创建委托函
 */
export const createDelegation = (data) => {
  return post('/delegations', data)
}

/**
 * 更新委托函
 */
export const updateDelegation = (id, data) => {
  return put(`/delegations/${id}`, data)
}

/**
 * 接受委托
 */
export const acceptDelegation = (id) => {
  return post(`/delegations/${id}/accept`)
}

/**
 * 拒绝委托
 */
export const rejectDelegation = (id) => {
  return post(`/delegations/${id}/reject`)
}

/**
 * 完成委托
 */
export const completeDelegation = (id) => {
  return post(`/delegations/${id}/complete`)
}
