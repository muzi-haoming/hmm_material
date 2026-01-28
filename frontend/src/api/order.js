/**
 * 订单相关 API
 */
import { get, post, put, del } from '@/utils/request'

/**
 * 获取订单列表
 */
export const getOrderList = (params = {}) => {
  return get('/orders', params)
}

/**
 * 获取订单详情
 */
export const getOrder = (id) => {
  return get(`/orders/${id}`)
}

/**
 * 创建订单
 */
export const createOrder = (data) => {
  return post('/orders', data)
}

/**
 * 更新订单
 */
export const updateOrder = (id, data) => {
  return put(`/orders/${id}`, data)
}

/**
 * 确认订单
 */
export const confirmOrder = (id) => {
  return post(`/orders/${id}/confirm`)
}

/**
 * 发货
 */
export const shipOrder = (id) => {
  return post(`/orders/${id}/ship`)
}

/**
 * 完成订单
 */
export const completeOrder = (id) => {
  return post(`/orders/${id}/complete`)
}

/**
 * 取消订单
 */
export const cancelOrder = (id) => {
  return post(`/orders/${id}/cancel`)
}

/**
 * 删除订单
 */
export const deleteOrder = (id) => {
  return del(`/orders/${id}`)
}
