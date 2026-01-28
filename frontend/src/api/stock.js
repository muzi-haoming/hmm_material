/**
 * 库存相关 API
 */
import { get, post, del } from '@/utils/request'

// ==================== 库存 ====================

/**
 * 获取库存列表
 */
export const getStockList = (params = {}) => {
  return get('/stocks', params)
}

/**
 * 获取库存详情
 */
export const getStock = (id) => {
  return get(`/stocks/${id}`)
}

// ==================== 入库 ====================

/**
 * 获取入库列表
 */
export const getStockInList = (params = {}) => {
  return get('/stock-in', params)
}

/**
 * 获取入库详情
 */
export const getStockIn = (id) => {
  return get(`/stock-in/${id}`)
}

/**
 * 创建入库记录
 */
export const createStockIn = (data) => {
  return post('/stock-in', data)
}

/**
 * 删除入库记录
 */
export const deleteStockIn = (id) => {
  return del(`/stock-in/${id}`)
}

// ==================== 出库 ====================

/**
 * 获取出库列表
 */
export const getStockOutList = (params = {}) => {
  return get('/stock-out', params)
}

/**
 * 获取出库详情
 */
export const getStockOut = (id) => {
  return get(`/stock-out/${id}`)
}

/**
 * 创建出库记录
 */
export const createStockOut = (data) => {
  return post('/stock-out', data)
}

/**
 * 删除出库记录
 */
export const deleteStockOut = (id) => {
  return del(`/stock-out/${id}`)
}
