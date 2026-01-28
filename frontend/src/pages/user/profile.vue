<template>
  <view class="page">
    <!-- 紫色渐变头部 -->
    <view class="header">
      <view class="status-bar"></view>
      <view class="header-content">
        <text class="header-title">HK 综合管理系统</text>
      </view>
    </view>

    <!-- 用户信息卡片 -->
    <view class="user-card">
      <view class="avatar">
        <view class="avatar-circle">
          <u-icon name="account-fill" size="60rpx" color="#999" />
        </view>
      </view>
      <view class="user-info">
        <text class="user-name">{{ userStore.userName || '未登录' }}</text>
        <text class="user-role">{{ userStore.userRoleName || '用户' }}</text>
      </view>
    </view>

    <!-- 菜单列表 -->
    <view class="menu-list">
      <view v-if="isAdmin" class="menu-item" @click="navigateTo('/pages/users/list')">
        <text class="menu-text">用户管理</text>
        <u-icon name="arrow-right" size="28rpx" color="#ccc" />
      </view>

      <view v-if="isAdmin" class="menu-item" @click="navigateTo('/pages/role/list')">
        <text class="menu-text">用户角色管理</text>
        <u-icon name="arrow-right" size="28rpx" color="#ccc" />
      </view>

      <view class="menu-item" @click="handleResetPassword">
        <text class="menu-text">重置密码</text>
        <u-icon name="arrow-right" size="28rpx" color="#ccc" />
      </view>

      <view class="menu-item" @click="handleLogout">
        <text class="menu-text">退出登陆</text>
        <u-icon name="arrow-right" size="28rpx" color="#ccc" />
      </view>
    </view>
  </view>
</template>

<script setup>
import { computed } from 'vue'
import { useUserStore } from '@/store/user'

const userStore = useUserStore()

const isAdmin = computed(() => {
  return userStore.userRole?.code === 'admin'
})

const navigateTo = (url) => {
  uni.navigateTo({ url })
}

const handleResetPassword = () => {
  uni.showToast({ title: '功能开发中', icon: 'none' })
}

const handleLogout = () => {
  uni.showModal({
    title: '确认退出',
    content: '确定要退出登录吗？',
    success: (res) => {
      if (res.confirm) {
        userStore.logout()
      }
    }
  })
}
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background-color: #fff;
  padding-bottom: 120rpx;
}

.header {
  background: linear-gradient(180deg, #BA55D3 0%, #9932CC 100%);
  padding-bottom: 40rpx;

  .status-bar {
    height: var(--status-bar-height, 44px);
  }

  .header-content {
    padding: 20rpx 32rpx;
  }

  .header-title {
    font-size: 36rpx;
    font-weight: bold;
    color: #fff;
  }
}

.user-card {
  display: flex;
  align-items: center;
  margin: 24rpx 32rpx;
  padding: 32rpx;
  background-color: #fff;
  border-radius: 16rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);

  .avatar {
    margin-right: 24rpx;

    .avatar-circle {
      width: 100rpx;
      height: 100rpx;
      border-radius: 50%;
      background-color: #f0f0f0;
      display: flex;
      align-items: center;
      justify-content: center;
    }
  }

  .user-info {
    flex: 1;

    .user-name {
      display: block;
      font-size: 36rpx;
      font-weight: bold;
      color: #333;
    }

    .user-role {
      display: block;
      font-size: 26rpx;
      color: #999;
      margin-top: 8rpx;
    }
  }
}

.menu-list {
  margin: 0 32rpx;
  background-color: #fff;
  border-radius: 16rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);
  overflow: hidden;

  .menu-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 32rpx 24rpx;
    border-bottom: 1rpx solid #f5f5f5;

    &:last-child {
      border-bottom: none;
    }

    &:active {
      background-color: #f9f9f9;
    }

    .menu-text {
      font-size: 30rpx;
      color: #333;
    }
  }
}
</style>
