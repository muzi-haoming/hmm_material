/**
 * 封装 uni.request 请求
 */

// API 基础地址
const BASE_URL = process.env.NODE_ENV === 'development'
  ? 'http://localhost:8000/api/v1'
  : '/api/v1'

// 请求拦截器
const requestInterceptor = (config) => {
  // 获取 token
  const token = uni.getStorageSync('token')
  if (token) {
    config.header = {
      ...config.header,
      'Authorization': `Bearer ${token}`
    }
  }
  return config
}

// 响应拦截器
const responseInterceptor = (response) => {
  const { statusCode, data } = response

  if (statusCode >= 200 && statusCode < 300) {
    return data
  }

  // 处理错误
  if (statusCode === 401) {
    // 未授权，跳转登录
    uni.removeStorageSync('token')
    uni.removeStorageSync('user')
    uni.reLaunch({ url: '/pages/login/login' })
    return Promise.reject(new Error('请先登录'))
  }

  if (statusCode === 403) {
    uni.showToast({ title: '权限不足', icon: 'none' })
    return Promise.reject(new Error('权限不足'))
  }

  if (statusCode === 404) {
    return Promise.reject(new Error('资源不存在'))
  }

  // 其他错误
  const message = data?.detail || '请求失败'
  uni.showToast({ title: message, icon: 'none' })
  return Promise.reject(new Error(message))
}

/**
 * 通用请求方法
 */
const request = (options) => {
  // 应用请求拦截器
  const config = requestInterceptor({
    url: `${BASE_URL}${options.url}`,
    method: options.method || 'GET',
    data: options.data,
    header: {
      'Content-Type': 'application/json',
      ...options.header
    },
    timeout: options.timeout || 30000
  })

  return new Promise((resolve, reject) => {
    uni.request({
      ...config,
      success: (res) => {
        try {
          const result = responseInterceptor(res)
          resolve(result)
        } catch (error) {
          reject(error)
        }
      },
      fail: (err) => {
        uni.showToast({ title: '网络错误', icon: 'none' })
        reject(err)
      }
    })
  })
}

/**
 * GET 请求
 */
export const get = (url, params = {}) => {
  // 将参数拼接到 URL
  const queryString = Object.keys(params)
    .filter(key => params[key] !== undefined && params[key] !== null)
    .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
    .join('&')

  const fullUrl = queryString ? `${url}?${queryString}` : url

  return request({
    url: fullUrl,
    method: 'GET'
  })
}

/**
 * POST 请求
 */
export const post = (url, data = {}) => {
  return request({
    url,
    method: 'POST',
    data
  })
}

/**
 * PUT 请求
 */
export const put = (url, data = {}) => {
  return request({
    url,
    method: 'PUT',
    data
  })
}

/**
 * DELETE 请求
 */
export const del = (url) => {
  return request({
    url,
    method: 'DELETE'
  })
}

export default request
