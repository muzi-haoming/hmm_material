<template>
  <view class="register-page">
    <view class="register-header">
      <text class="title">HMM物料管理</text>
      <text class="subtitle">用户注册</text>
    </view>

    <view class="register-form">
      <view class="input-group">
        <view class="input-wrapper">
          <u-icon name="account-fill" color="#909399" size="22"></u-icon>
          <input
            class="input-field"
            v-model="formData.username"
            placeholder="请输入用户名（3-50字符）"
            placeholder-class="placeholder-style"
          />
        </view>
      </view>

      <view class="input-group">
        <view class="input-wrapper">
          <u-icon name="email-fill" color="#909399" size="22"></u-icon>
          <input
            class="input-field"
            v-model="formData.email"
            type="text"
            placeholder="请输入邮箱"
            placeholder-class="placeholder-style"
          />
        </view>
      </view>

      <view class="input-group">
        <view class="input-wrapper">
          <u-icon name="account" color="#909399" size="22"></u-icon>
          <input
            class="input-field"
            v-model="formData.full_name"
            placeholder="请输入姓名"
            placeholder-class="placeholder-style"
          />
        </view>
      </view>

      <view class="input-group">
        <view class="input-wrapper">
          <u-icon name="phone-fill" color="#909399" size="22"></u-icon>
          <input
            class="input-field"
            v-model="formData.phone"
            type="tel"
            placeholder="请输入手机号（选填）"
            placeholder-class="placeholder-style"
          />
        </view>
      </view>

      <view class="input-group">
        <view class="input-wrapper">
          <u-icon name="lock-fill" color="#909399" size="22"></u-icon>
          <input
            class="input-field"
            v-model="formData.password"
            type="password"
            placeholder="请输入密码（至少6位）"
            placeholder-class="placeholder-style"
          />
        </view>
      </view>

      <view class="input-group">
        <view class="input-wrapper">
          <u-icon name="lock-fill" color="#909399" size="22"></u-icon>
          <input
            class="input-field"
            v-model="formData.confirmPassword"
            type="password"
            placeholder="请确认密码"
            placeholder-class="placeholder-style"
          />
        </view>
      </view>

      <view class="input-group">
        <view class="picker-wrapper" @click="showRolePicker = true">
          <u-icon name="integral-fill" color="#909399" size="22"></u-icon>
          <text class="picker-text" :class="{ placeholder: !formData.role }">
            {{ formData.role ? getRoleText(formData.role) : '请选择角色' }}
          </text>
          <u-icon name="arrow-down" color="#909399" size="18"></u-icon>
        </view>
      </view>

      <u-button
        type="primary"
        :loading="loading"
        @click="handleRegister"
        :customStyle="{ marginTop: '40rpx', height: '88rpx', borderRadius: '44rpx' }"
      >
        注 册
      </u-button>

      <view class="login-link" @click="goLogin">
        已有账号？立即登录
      </view>
    </view>

    <!-- 角色选择器 -->
    <u-picker
      :show="showRolePicker"
      :columns="roleColumns"
      @confirm="onRoleConfirm"
      @cancel="showRolePicker = false"
      keyName="label"
    ></u-picker>
  </view>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { register } from '@/api'

const formData = reactive({
  username: '',
  email: '',
  full_name: '',
  phone: '',
  password: '',
  confirmPassword: '',
  role: ''
})

const loading = ref(false)
const showRolePicker = ref(false)

const roleColumns = [
  [
    { label: '工地员工', value: 'SITE_STAFF' },
    { label: '工地管理员', value: 'SITE_MANAGER' },
    { label: '厂家代理人', value: 'AGENT' },
    { label: '厂家员工', value: 'MANUFACTURER' }
  ]
]

const getRoleText = (role) => {
  const roleMap = {
    ADMIN: '系统管理员',
    SITE_MANAGER: '工地管理员',
    SITE_STAFF: '工地员工',
    AGENT: '厂家代理人',
    MANUFACTURER: '厂家员工'
  }
  return roleMap[role] || '未知角色'
}

const onRoleConfirm = (e) => {
  formData.role = e.value[0].value
  showRolePicker.value = false
}

const handleRegister = async () => {
  // 表单验证
  if (!formData.username || formData.username.length < 3) {
    uni.showToast({ title: '用户名至少3个字符', icon: 'none' })
    return
  }
  if (!formData.email || !formData.email.includes('@')) {
    uni.showToast({ title: '请输入有效的邮箱', icon: 'none' })
    return
  }
  if (!formData.full_name) {
    uni.showToast({ title: '请输入姓名', icon: 'none' })
    return
  }
  if (!formData.password || formData.password.length < 6) {
    uni.showToast({ title: '密码至少6位', icon: 'none' })
    return
  }
  if (formData.password !== formData.confirmPassword) {
    uni.showToast({ title: '两次密码输入不一致', icon: 'none' })
    return
  }
  if (!formData.role) {
    uni.showToast({ title: '请选择角色', icon: 'none' })
    return
  }

  loading.value = true

  try {
    await register({
      username: formData.username,
      email: formData.email,
      full_name: formData.full_name,
      phone: formData.phone || null,
      password: formData.password,
      role: formData.role
    })
    uni.showToast({ title: '注册成功', icon: 'success' })
    setTimeout(() => {
      uni.navigateTo({ url: '/pages/login/login' })
    }, 1500)
  } catch (error) {
    uni.showToast({ title: error.message || '注册失败', icon: 'none' })
  } finally {
    loading.value = false
  }
}

const goLogin = () => {
  uni.navigateTo({ url: '/pages/login/login' })
}
</script>

<style lang="scss" scoped>
.register-page {
  min-height: 100vh;
  padding: 60rpx 60rpx;
  background: linear-gradient(180deg, #f0f7ff 0%, #ffffff 100%);

  @media screen and (min-width: 768px) {
    max-width: 450px;
    margin: 0 auto;
    padding-top: 80rpx;
  }
}

.register-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 60rpx;

  .title {
    font-size: 44rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 16rpx;
  }

  .subtitle {
    font-size: 28rpx;
    color: #999;
  }
}

.register-form {
  background-color: #fff;
  border-radius: 24rpx;
  padding: 48rpx;
  box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.08);
}

.input-group {
  margin-bottom: 24rpx;
}

.input-wrapper,
.picker-wrapper {
  display: flex;
  align-items: center;
  padding: 24rpx 32rpx;
  background-color: #f5f5f5;
  border-radius: 44rpx;
  border: 1px solid #e8e8e8;
}

.input-field {
  flex: 1;
  margin-left: 20rpx;
  font-size: 28rpx;
  color: #333;
  background: transparent;
  border: none;
  outline: none;
}

.picker-wrapper {
  .picker-text {
    flex: 1;
    margin-left: 20rpx;
    font-size: 28rpx;
    color: #333;

    &.placeholder {
      color: #c0c4cc;
    }
  }
}

.placeholder-style {
  color: #c0c4cc;
}

.login-link {
  text-align: center;
  margin-top: 40rpx;
  font-size: 28rpx;
  color: $primary-color;
}
</style>
