/**
 * 对账单相关 API
 */
import { get, post, put, del } from '@/utils/request'

/**
 * 获取对账单列表
 */
export const getStatementList = (params = {}) => {
  return get('/statements', params)
}

/**
 * 获取对账单详情
 */
export const getStatement = (id) => {
  return get(`/statements/${id}`)
}

/**
 * 创建对账单
 */
export const createStatement = (data) => {
  return post('/statements', data)
}

/**
 * 更新对账单
 */
export const updateStatement = (id, data) => {
  return put(`/statements/${id}`, data)
}

/**
 * 删除对账单
 */
export const deleteStatement = (id) => {
  return del(`/statements/${id}`)
}
