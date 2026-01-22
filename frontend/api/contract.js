/**
 * 合同相关 API
 */
import { get, post, put, del } from '@/utils/request'

/**
 * 获取合同列表
 */
export const getContractList = (params = {}) => {
  return get('/contracts', params)
}

/**
 * 获取合同详情
 */
export const getContract = (id) => {
  return get(`/contracts/${id}`)
}

/**
 * 创建合同
 */
export const createContract = (data) => {
  return post('/contracts', data)
}

/**
 * 更新合同
 */
export const updateContract = (id, data) => {
  return put(`/contracts/${id}`, data)
}

/**
 * 删除合同
 */
export const deleteContract = (id) => {
  return del(`/contracts/${id}`)
}
