/**
 * 厂家相关 API
 */
import { get, post, put, del } from '@/utils/request'

/**
 * 获取厂家列表
 */
export const getManufacturerList = (params = {}) => {
  return get('/manufacturers', params)
}

/**
 * 获取厂家详情
 */
export const getManufacturer = (id) => {
  return get(`/manufacturers/${id}`)
}

/**
 * 创建厂家
 */
export const createManufacturer = (data) => {
  return post('/manufacturers', data)
}

/**
 * 更新厂家
 */
export const updateManufacturer = (id, data) => {
  return put(`/manufacturers/${id}`, data)
}

/**
 * 删除厂家
 */
export const deleteManufacturer = (id) => {
  return del(`/manufacturers/${id}`)
}

/**
 * 获取厂家组列表
 */
export const getManufacturerGroupList = (params = {}) => {
  return get('/manufacturers/groups', params)
}

/**
 * 获取厂家组详情
 */
export const getManufacturerGroup = (id) => {
  return get(`/manufacturers/groups/${id}`)
}

/**
 * 创建厂家组
 */
export const createManufacturerGroup = (data) => {
  return post('/manufacturers/groups', data)
}
