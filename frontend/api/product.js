/**
 * 产品相关 API
 */
import { get, post, put, del } from '@/utils/request'

/**
 * 获取产品列表
 */
export const getProductList = (params = {}) => {
  return get('/products', params)
}

/**
 * 获取产品详情
 */
export const getProduct = (id) => {
  return get(`/products/${id}`)
}

/**
 * 创建产品
 */
export const createProduct = (data) => {
  return post('/products', data)
}

/**
 * 更新产品
 */
export const updateProduct = (id, data) => {
  return put(`/products/${id}`, data)
}

/**
 * 删除产品
 */
export const deleteProduct = (id) => {
  return del(`/products/${id}`)
}

/**
 * 获取厂家可供应的产品
 */
export const getManufacturerProducts = (manufacturerId) => {
  return get(`/products/manufacturer/${manufacturerId}/products`)
}

/**
 * 创建厂家-产品关联
 */
export const createManufacturerProduct = (data) => {
  return post('/products/manufacturer-products', data)
}
