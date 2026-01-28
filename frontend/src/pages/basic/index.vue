<template>
  <view class="page-container">
    <view class="page-header">
      <text class="page-title">基础数据</text>
      <text class="page-subtitle">管理合同、工地、厂家等基础信息</text>
    </view>

    <view class="menu-section">
      <view class="menu-group">
        <view class="group-title">业务基础</view>
        <view class="menu-list">
          <view class="menu-item" @click="navigateTo('/pages/contract/list')">
            <view class="menu-icon" style="background-color: #e6f7ff;">
              <u-icon name="file-text" color="#1890ff" size="40rpx" />
            </view>
            <view class="menu-content">
              <text class="menu-name">合同管理</text>
              <text class="menu-desc">管理项目合同信息</text>
            </view>
            <u-icon name="arrow-right" color="#999" size="28rpx" />
          </view>

          <view class="menu-item" @click="navigateTo('/pages/site/list')">
            <view class="menu-icon" style="background-color: #f6ffed;">
              <u-icon name="map" color="#52c41a" size="40rpx" />
            </view>
            <view class="menu-content">
              <text class="menu-name">工地管理</text>
              <text class="menu-desc">管理施工工地信息</text>
            </view>
            <u-icon name="arrow-right" color="#999" size="28rpx" />
          </view>

          <view class="menu-item" @click="navigateTo('/pages/product/list')">
            <view class="menu-icon" style="background-color: #fff7e6;">
              <u-icon name="gift" color="#fa8c16" size="40rpx" />
            </view>
            <view class="menu-content">
              <text class="menu-name">产品管理</text>
              <text class="menu-desc">管理物料产品信息</text>
            </view>
            <u-icon name="arrow-right" color="#999" size="28rpx" />
          </view>
        </view>
      </view>

      <view class="menu-group">
        <view class="group-title">厂家信息</view>
        <view class="menu-list">
          <view class="menu-item" @click="navigateTo('/pages/manufacturer/list')">
            <view class="menu-icon" style="background-color: #f9f0ff;">
              <u-icon name="home" color="#722ed1" size="40rpx" />
            </view>
            <view class="menu-content">
              <text class="menu-name">厂家管理</text>
              <text class="menu-desc">管理供应商和厂家</text>
            </view>
            <u-icon name="arrow-right" color="#999" size="28rpx" />
          </view>

          <view class="menu-item" @click="navigateTo('/pages/manufacturer-group/list')">
            <view class="menu-icon" style="background-color: #e6fffb;">
              <u-icon name="grid" color="#13c2c2" size="40rpx" />
            </view>
            <view class="menu-content">
              <text class="menu-name">厂家组管理</text>
              <text class="menu-desc">管理厂家分组</text>
            </view>
            <u-icon name="arrow-right" color="#999" size="28rpx" />
          </view>
        </view>
      </view>

      <view class="menu-group" v-if="isAdmin">
        <view class="group-title">系统管理</view>
        <view class="menu-list">
          <view class="menu-item" @click="navigateTo('/pages/users/list')">
            <view class="menu-icon" style="background-color: #fff1f0;">
              <u-icon name="account" color="#f5222d" size="40rpx" />
            </view>
            <view class="menu-content">
              <text class="menu-name">用户管理</text>
              <text class="menu-desc">管理系统用户</text>
            </view>
            <u-icon name="arrow-right" color="#999" size="28rpx" />
          </view>

          <view class="menu-item" @click="navigateTo('/pages/role/list')">
            <view class="menu-icon" style="background-color: #fffbe6;">
              <u-icon name="integral" color="#faad14" size="40rpx" />
            </view>
            <view class="menu-content">
              <text class="menu-name">角色管理</text>
              <text class="menu-desc">管理用户角色权限</text>
            </view>
            <u-icon name="arrow-right" color="#999" size="28rpx" />
          </view>
        </view>
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
</script>

<style lang="scss" scoped>
.page-container {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding-bottom: 120rpx;
}

.page-header {
  background: linear-gradient(135deg, #52c41a 0%, #389e0d 100%);
  padding: 48rpx 32rpx;

  .page-title {
    display: block;
    font-size: 40rpx;
    font-weight: bold;
    color: #fff;
    margin-bottom: 12rpx;
  }

  .page-subtitle {
    font-size: 26rpx;
    color: rgba(255, 255, 255, 0.8);
  }
}

.menu-section {
  padding: 24rpx;
}

.menu-group {
  margin-bottom: 24rpx;

  .group-title {
    font-size: 28rpx;
    font-weight: 500;
    color: #666;
    padding: 16rpx 8rpx;
  }
}

.menu-list {
  background-color: #fff;
  border-radius: 16rpx;
  overflow: hidden;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 28rpx 24rpx;
  border-bottom: 1rpx solid #f0f0f0;

  &:last-child {
    border-bottom: none;
  }

  &:active {
    background-color: #f5f5f5;
  }
}

.menu-icon {
  width: 80rpx;
  height: 80rpx;
  border-radius: 16rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 24rpx;
}

.menu-content {
  flex: 1;

  .menu-name {
    display: block;
    font-size: 30rpx;
    color: #333;
    margin-bottom: 8rpx;
  }

  .menu-desc {
    font-size: 24rpx;
    color: #999;
  }
}
</style>
