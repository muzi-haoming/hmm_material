/**
 * 采购单相关 API
 */
import { get, post, put, del } from '@/utils/request'

/**
 * 获取采购单列表
 */
export const getPurchaseList = (params = {}) => {
  return get('/purchases', params)
}

/**
 * 获取采购单详情
 */
export const getPurchase = (id) => {
  return get(`/purchases/${id}`)
}

/**
 * 创建采购单
 */
export const createPurchase = (data) => {
  return post('/purchases', data)
}

/**
 * 更新采购单
 */
export const updatePurchase = (id, data) => {
  return put(`/purchases/${id}`, data)
}

/**
 * 删除采购单
 */
export const deletePurchase = (id) => {
  return del(`/purchases/${id}`)
}
