/**
 * 认证相关 API
 */
import { get, post } from '@/utils/request'

/**
 * 用户登录
 */
export const login = (username, password) => {
  // OAuth2 表单格式
  const formData = `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`

  return new Promise((resolve, reject) => {
    uni.request({
      url: `${process.env.NODE_ENV === 'development' ? 'http://localhost:8000' : ''}/api/v1/auth/login`,
      method: 'POST',
      header: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      data: formData,
      success: (res) => {
        if (res.statusCode === 200) {
          resolve(res.data)
        } else {
          reject(new Error(res.data?.detail || '登录失败'))
        }
      },
      fail: (err) => {
        reject(err)
      }
    })
  })
}

/**
 * 用户注册
 */
export const register = (userData) => {
  return post('/auth/register', userData)
}

/**
 * 获取可用角色列表
 */
export const getRoles = () => {
  return get('/auth/roles')
}
