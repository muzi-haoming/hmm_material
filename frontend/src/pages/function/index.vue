<template>
  <view class="page">
    <!-- 紫色渐变头部 -->
    <view class="header">
      <view class="status-bar"></view>
      <view class="header-content">
        <text class="header-title">HK 综合管理系统</text>
      </view>
    </view>

    <!-- Tab 切换卡片 -->
    <view class="tab-card">
      <view class="tabs">
        <view
          :class="['tab-item', { active: activeTab === 'basic' }]"
          @click="activeTab = 'basic'"
        >
          <view class="tab-icon">
            <text class="icon-text">📋</text>
          </view>
          <text class="tab-label">基础信息</text>
        </view>
        <view
          :class="['tab-item', { active: activeTab === 'business' }]"
          @click="activeTab = 'business'"
        >
          <view class="tab-icon">
            <text class="icon-text">📊</text>
          </view>
          <text class="tab-label">业务数据</text>
        </view>
      </view>

      <!-- 基础信息菜单 -->
      <view v-if="activeTab === 'basic'" class="menu-grid">
        <view class="menu-item" @click="navigateTo('/pages/site/list')">
          <view class="menu-icon" style="background-color: #E8E8E8;">
            <text class="icon-letter">G</text>
          </view>
          <text class="menu-label">工地信息</text>
        </view>
        <view class="menu-item" @click="navigateTo('/pages/manufacturer/list')">
          <view class="menu-icon" style="background-color: #E8E8E8;">
            <text class="icon-letter">C</text>
          </view>
          <text class="menu-label">厂家信息</text>
        </view>
        <view class="menu-item" @click="navigateTo('/pages/manufacturer-group/list')">
          <view class="menu-icon" style="background-color: #E8E8E8;">
            <text class="icon-letter">C</text>
          </view>
          <text class="menu-label">厂家组</text>
        </view>
        <view class="menu-item" @click="navigateTo('/pages/product/list')">
          <view class="menu-icon" style="background-color: #E8E8E8;">
            <text class="icon-letter">C</text>
          </view>
          <text class="menu-label">产品信息</text>
        </view>
      </view>

      <!-- 业务数据菜单 -->
      <view v-if="activeTab === 'business'" class="menu-grid">
        <view class="menu-item" @click="navigateTo('/pages/order/list')">
          <view class="menu-icon" style="background-color: #E8E8E8;">
            <text class="icon-letter">G</text>
          </view>
          <text class="menu-label">工地订单</text>
        </view>
        <view class="menu-item" @click="navigateTo('/pages/purchase/list')">
          <view class="menu-icon" style="background-color: #E8E8E8;">
            <text class="icon-letter">C</text>
          </view>
          <text class="menu-label">采购单</text>
        </view>
        <view class="menu-item" @click="navigateTo('/pages/statement/list')">
          <view class="menu-icon" style="background-color: #E8E8E8;">
            <text class="icon-letter">D</text>
          </view>
          <text class="menu-label">对账单</text>
        </view>
        <view class="menu-item" @click="navigateTo('/pages/stock/list')">
          <view class="menu-icon" style="background-color: #E8E8E8;">
            <text class="icon-letter">K</text>
          </view>
          <text class="menu-label">库存信息</text>
        </view>
        <view class="menu-item" @click="navigateTo('/pages/stock-out/list')">
          <view class="menu-icon" style="background-color: #E8E8E8;">
            <text class="icon-letter">C</text>
          </view>
          <text class="menu-label">出库单</text>
        </view>
        <view class="menu-item" @click="navigateTo('/pages/stock-in/list')">
          <view class="menu-icon" style="background-color: #E8E8E8;">
            <text class="icon-letter">R</text>
          </view>
          <text class="menu-label">入库单</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'

const activeTab = ref('basic')

const navigateTo = (url) => {
  uni.navigateTo({ url })
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

.tab-card {
  margin: 24rpx 32rpx;
  background-color: #fff;
  border-radius: 16rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.tabs {
  display: flex;
  border-bottom: 1rpx solid #f0f0f0;

  .tab-item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 24rpx;
    position: relative;

    &.active {
      &::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 80rpx;
        height: 4rpx;
        background-color: #BA55D3;
        border-radius: 2rpx;
      }

      .tab-label {
        color: #BA55D3;
        font-weight: 500;
      }
    }

    .tab-icon {
      width: 60rpx;
      height: 60rpx;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 8rpx;

      .icon-text {
        font-size: 40rpx;
      }
    }

    .tab-label {
      font-size: 26rpx;
      color: #666;
    }
  }
}

.menu-grid {
  display: flex;
  flex-wrap: wrap;
  padding: 24rpx;

  .menu-item {
    width: 25%;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20rpx 0;

    &:active {
      opacity: 0.7;
    }

    .menu-icon {
      width: 80rpx;
      height: 80rpx;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 12rpx;

      .icon-letter {
        font-size: 32rpx;
        font-weight: bold;
        color: #666;
      }
    }

    .menu-label {
      font-size: 24rpx;
      color: #333;
    }
  }
}
</style>
