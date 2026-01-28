<template>
  <view class="page">
    <!-- 紫色渐变头部 -->
    <view class="header">
      <view class="status-bar"></view>
      <view class="header-content">
        <text class="header-title">HK 综合管理系统</text>
      </view>
    </view>

    <!-- 统计卡片 -->
    <view class="stats-card">
      <view class="stat-item" @click="navigateTo('/pages/order/list?status=1')">
        <text class="stat-value">{{ stats.pending }}</text>
        <text class="stat-label">待处理</text>
      </view>
      <view class="stat-item" @click="navigateTo('/pages/order/list?status=2')">
        <text class="stat-value">{{ stats.processing }}</text>
        <text class="stat-label">处理中</text>
      </view>
      <view class="stat-item" @click="navigateTo('/pages/order/list?status=3')">
        <text class="stat-value">{{ stats.completed }}</text>
        <text class="stat-label">已完成</text>
      </view>
    </view>

    <!-- 内容区域 -->
    <view class="content">
      <!-- 空白区域，保持简洁设计 -->
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/store/user'

const userStore = useUserStore()

const stats = ref({
  pending: 0,
  processing: 0,
  completed: 0
})

onMounted(() => {
  // TODO: 从API加载统计数据
})

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
  padding-bottom: 80rpx;

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

.stats-card {
  display: flex;
  justify-content: space-around;
  margin: -60rpx 32rpx 0;
  padding: 40rpx 0;
  background-color: #fff;
  border-radius: 16rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);

  .stat-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 160rpx;

    &:active {
      opacity: 0.7;
    }

    .stat-value {
      font-size: 56rpx;
      font-weight: 300;
      color: #333;
    }

    .stat-label {
      font-size: 24rpx;
      color: #999;
      margin-top: 8rpx;
    }
  }
}

.content {
  padding: 32rpx;
  min-height: 400rpx;
}
</style>
