<template>
  <view class="login-page">
    <view class="login-header">
      <image class="logo" src="/static/images/logo.png" mode="aspectFit" />
      <text class="title">HMM物料管理</text>
      <text class="subtitle">工地-厂家供应链管理平台</text>
    </view>

    <view class="login-form">
      <view class="input-group">
        <view class="input-wrapper">
          <u-icon name="account-fill" color="#909399" size="22"></u-icon>
          <input
            class="input-field"
            v-model="formData.username"
            placeholder="请输入用户名"
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
            placeholder="请输入密码"
            placeholder-class="placeholder-style"
          />
        </view>
      </view>

      <u-button
        type="primary"
        :loading="loading"
        @click="handleLogin"
        :customStyle="{ marginTop: '40rpx', height: '88rpx', borderRadius: '44rpx' }"
      >
        登 录
      </u-button>

      <view class="register-link" @click="goRegister">
        还没有账号？立即注册
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useUserStore } from '@/store/user'

const userStore = useUserStore()

const formData = reactive({
  username: '',
  password: ''
})

const loading = ref(false)

const handleLogin = async () => {
  if (!formData.username || !formData.password) {
    uni.showToast({ title: '请输入用户名和密码', icon: 'none' })
    return
  }

  loading.value = true

  try {
    await userStore.login(formData.username, formData.password)
    uni.showToast({ title: '登录成功', icon: 'success' })
    setTimeout(() => {
      uni.switchTab({ url: '/pages/index/index' })
    }, 500)
  } catch (error) {
    uni.showToast({ title: error.message || '登录失败', icon: 'none' })
  } finally {
    loading.value = false
  }
}

const goRegister = () => {
  uni.navigateTo({ url: '/pages/login/register' })
}
</script>

<style lang="scss" scoped>
.login-page {
  min-height: 100vh;
  padding: 100rpx 60rpx;
  background: linear-gradient(180deg, #f0f7ff 0%, #ffffff 100%);

  /* H5 大屏幕时限制宽度，居中显示 */
  @media screen and (min-width: 768px) {
    max-width: 450px;
    margin: 0 auto;
    padding-top: 150rpx;
  }
}

.login-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 80rpx;

  .logo {
    width: 160rpx;
    height: 160rpx;
    margin-bottom: 32rpx;
  }

  .title {
    font-size: 48rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 16rpx;
  }

  .subtitle {
    font-size: 28rpx;
    color: #999;
  }
}

.login-form {
  background-color: #fff;
  border-radius: 24rpx;
  padding: 48rpx;
  box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.08);
}

.input-group {
  margin-bottom: 32rpx;
}

.input-wrapper {
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

.placeholder-style {
  color: #c0c4cc;
}

.register-link {
  text-align: center;
  margin-top: 40rpx;
  font-size: 28rpx;
  color: $primary-color;
}
</style>
