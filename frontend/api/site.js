/**
 * 工地相关 API
 */
import { get, post, put, del } from '@/utils/request'

/**
 * 获取工地列表
 */
export const getSiteList = (params = {}) => {
  return get('/sites', params)
}

/**
 * 获取工地详情
 */
export const getSite = (id) => {
  return get(`/sites/${id}`)
}

/**
 * 创建工地
 */
export const createSite = (data) => {
  return post('/sites', data)
}

/**
 * 更新工地
 */
export const updateSite = (id, data) => {
  return put(`/sites/${id}`, data)
}

/**
 * 删除工地
 */
export const deleteSite = (id) => {
  return del(`/sites/${id}`)
}
