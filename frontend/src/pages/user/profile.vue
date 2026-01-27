<template>
  <view class="profile-page">
    <!-- 用户信息卡片 -->
    <view class="user-card">
      <view class="avatar-section">
        <u-avatar :text="userStore.userName?.charAt(0) || 'U'" size="120rpx" />
        <view class="user-info">
          <text class="name">{{ userStore.userName || '未登录' }}</text>
          <text class="role">{{ userStore.userRoleName }}</text>
        </view>
      </view>
    </view>

    <!-- 菜单列表 -->
    <view class="menu-section">
      <view class="menu-group">
        <view class="menu-item" @click="navigateTo('/pages/site/list')">
          <u-icon name="home" size="40rpx" color="#52c41a" />
          <text class="menu-text">工地管理</text>
          <u-icon name="arrow-right" size="28rpx" color="#999" />
        </view>

        <view class="menu-item" @click="navigateTo('/pages/manufacturer/list')">
          <u-icon name="grid" size="40rpx" color="#fa8c16" />
          <text class="menu-text">厂家管理</text>
          <u-icon name="arrow-right" size="28rpx" color="#999" />
        </view>

        <view class="menu-item" @click="navigateTo('/pages/contract/list')">
          <u-icon name="file-text" size="40rpx" color="#1890ff" />
          <text class="menu-text">合同管理</text>
          <u-icon name="arrow-right" size="28rpx" color="#999" />
        </view>
      </view>

      <view class="menu-group">
        <view class="menu-item">
          <u-icon name="setting" size="40rpx" color="#666" />
          <text class="menu-text">设置</text>
          <u-icon name="arrow-right" size="28rpx" color="#999" />
        </view>

        <view class="menu-item">
          <u-icon name="info-circle" size="40rpx" color="#666" />
          <text class="menu-text">关于</text>
          <u-icon name="arrow-right" size="28rpx" color="#999" />
        </view>
      </view>
    </view>

    <!-- 退出登录 -->
    <view class="logout-section">
      <u-button type="error" :plain="true" @click="handleLogout">
        退出登录
      </u-button>
    </view>
  </view>
</template>

<script setup>
import { useUserStore } from '@/store/user'

const userStore = useUserStore()

const navigateTo = (url) => {
  uni.navigateTo({ url })
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
.profile-page {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.user-card {
  background: linear-gradient(135deg, #007AFF 0%, #0056b3 100%);
  padding: 60rpx 32rpx;

  .avatar-section {
    display: flex;
    align-items: center;

    .user-info {
      margin-left: 24rpx;

      .name {
        display: block;
        font-size: 36rpx;
        font-weight: bold;
        color: #fff;
      }

      .role {
        display: block;
        font-size: 26rpx;
        color: rgba(255, 255, 255, 0.8);
        margin-top: 8rpx;
      }
    }
  }
}

.menu-section {
  padding: 24rpx;
}

.menu-group {
  background-color: #fff;
  border-radius: 16rpx;
  margin-bottom: 24rpx;
  overflow: hidden;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 32rpx 24rpx;
  border-bottom: 1rpx solid #f0f0f0;

  &:last-child {
    border-bottom: none;
  }

  .menu-text {
    flex: 1;
    margin-left: 24rpx;
    font-size: 30rpx;
    color: #333;
  }
}

.logout-section {
  padding: 48rpx 24rpx;
}
</style>
