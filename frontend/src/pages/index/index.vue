<template>
  <view class="index-page">
    <!-- 顶部用户信息 -->
    <view class="header-section">
      <view class="user-info">
        <view class="avatar">
          <u-avatar :text="userStore.userName?.charAt(0) || 'U'" size="80rpx" />
        </view>
        <view class="user-text">
          <text class="name">{{ userStore.userName || '未登录' }}</text>
          <text class="role">{{ getRoleText(userStore.userRole) }}</text>
        </view>
      </view>
    </view>

    <!-- 数据统计 -->
    <view class="stats-section">
      <view class="stats-grid">
        <view class="stat-item" @click="navigateTo('/pages/order/list?status=pending')">
          <text class="stat-value">{{ stats.pendingOrders }}</text>
          <text class="stat-label">待处理订单</text>
        </view>
        <view class="stat-item" @click="navigateTo('/pages/order/list?status=processing')">
          <text class="stat-value">{{ stats.processingOrders }}</text>
          <text class="stat-label">处理中</text>
        </view>
        <view class="stat-item" @click="navigateTo('/pages/contract/list')">
          <text class="stat-value">{{ stats.activeContracts }}</text>
          <text class="stat-label">生效合同</text>
        </view>
        <view class="stat-item" @click="navigateTo('/pages/delegation/list')">
          <text class="stat-value">{{ stats.pendingDelegations }}</text>
          <text class="stat-label">待处理委托</text>
        </view>
      </view>
    </view>

    <!-- 快捷入口 -->
    <view class="section">
      <view class="section-title">快捷入口</view>
      <view class="quick-grid">
        <view class="quick-item" @click="navigateTo('/pages/order/create')">
          <u-icon name="plus-circle" size="48rpx" color="#007AFF" />
          <text>创建订单</text>
        </view>
        <view class="quick-item" @click="navigateTo('/pages/site/list')">
          <u-icon name="home" size="48rpx" color="#52c41a" />
          <text>工地管理</text>
        </view>
        <view class="quick-item" @click="navigateTo('/pages/manufacturer/list')">
          <u-icon name="grid" size="48rpx" color="#fa8c16" />
          <text>厂家管理</text>
        </view>
        <view class="quick-item" @click="navigateTo('/pages/contract/list')">
          <u-icon name="file-text" size="48rpx" color="#1890ff" />
          <text>合同管理</text>
        </view>
      </view>
    </view>

    <!-- 最近订单 -->
    <view class="section">
      <view class="section-header">
        <text class="section-title">最近订单</text>
        <text class="view-more" @click="navigateTo('/pages/order/list')">查看全部</text>
      </view>
      <view class="order-list">
        <view
          v-for="order in recentOrders"
          :key="order.id"
          class="order-item"
          @click="navigateTo(`/pages/order/detail?id=${order.id}`)"
        >
          <view class="order-info">
            <text class="order-no">{{ order.order_no }}</text>
            <text class="order-amount">¥{{ order.total_amount }}</text>
          </view>
          <view class="order-meta">
            <text class="order-date">{{ formatDate(order.order_date) }}</text>
            <view :class="['status-tag', `status-${order.status}`]">
              {{ getStatusText(order.status) }}
            </view>
          </view>
        </view>
        <view v-if="recentOrders.length === 0" class="empty-tip">
          暂无订单数据
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/store/user'
import { getOrderList } from '@/api/order'

const userStore = useUserStore()

const stats = ref({
  pendingOrders: 0,
  processingOrders: 0,
  activeContracts: 0,
  pendingDelegations: 0
})

const recentOrders = ref([])

onMounted(() => {
  loadData()
})

const loadData = async () => {
  try {
    // 加载最近订单
    const res = await getOrderList({ page: 1, page_size: 5 })
    recentOrders.value = res.items || []

    // TODO: 加载统计数据
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

const getRoleText = (role) => {
  const roleMap = {
    admin: '系统管理员',
    site_manager: '工地管理员',
    site_staff: '工地员工',
    agent: '厂家代理人',
    manufacturer: '厂家员工'
  }
  return roleMap[role] || '未知角色'
}

const getStatusText = (status) => {
  const statusMap = {
    pending: '待处理',
    confirmed: '已确认',
    processing: '处理中',
    shipped: '已发货',
    delivered: '已送达',
    completed: '已完成',
    cancelled: '已取消'
  }
  return statusMap[status] || status
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getMonth() + 1}/${date.getDate()} ${date.getHours()}:${date.getMinutes().toString().padStart(2, '0')}`
}

const navigateTo = (url) => {
  uni.navigateTo({ url })
}
</script>

<style lang="scss" scoped>
.index-page {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding-bottom: 120rpx;
}

.header-section {
  background: linear-gradient(135deg, #007AFF 0%, #0056b3 100%);
  padding: 60rpx 32rpx 80rpx;

  .user-info {
    display: flex;
    align-items: center;

    .avatar {
      margin-right: 24rpx;
    }

    .user-text {
      display: flex;
      flex-direction: column;

      .name {
        font-size: 36rpx;
        font-weight: bold;
        color: #fff;
      }

      .role {
        font-size: 26rpx;
        color: rgba(255, 255, 255, 0.8);
        margin-top: 8rpx;
      }
    }
  }
}

.stats-section {
  margin: -40rpx 24rpx 24rpx;
  background-color: #fff;
  border-radius: 16rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.08);

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    padding: 32rpx 0;

    .stat-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      border-right: 1rpx solid #f0f0f0;

      &:last-child {
        border-right: none;
      }

      .stat-value {
        font-size: 44rpx;
        font-weight: bold;
        color: #333;
      }

      .stat-label {
        font-size: 24rpx;
        color: #999;
        margin-top: 8rpx;
      }
    }
  }
}

.section {
  margin: 24rpx;
  background-color: #fff;
  border-radius: 16rpx;
  padding: 24rpx;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.view-more {
  font-size: 26rpx;
  color: #999;
}

.quick-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24rpx;
  margin-top: 24rpx;

  .quick-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 24rpx 0;

    text {
      font-size: 26rpx;
      color: #666;
      margin-top: 16rpx;
    }
  }
}

.order-list {
  .order-item {
    padding: 24rpx 0;
    border-bottom: 1rpx solid #f0f0f0;

    &:last-child {
      border-bottom: none;
    }

    .order-info {
      display: flex;
      justify-content: space-between;
      margin-bottom: 12rpx;

      .order-no {
        font-size: 28rpx;
        color: #333;
      }

      .order-amount {
        font-size: 28rpx;
        font-weight: bold;
        color: #f5222d;
      }
    }

    .order-meta {
      display: flex;
      justify-content: space-between;
      align-items: center;

      .order-date {
        font-size: 24rpx;
        color: #999;
      }
    }
  }
}

.empty-tip {
  text-align: center;
  padding: 48rpx 0;
  color: #999;
  font-size: 28rpx;
}
</style>
