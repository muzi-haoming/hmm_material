<template>
  <view class="order-list-page">
    <!-- 搜索和筛选 -->
    <view class="search-bar">
      <u-search
        v-model="keyword"
        placeholder="搜索订单编号"
        @search="handleSearch"
        @clear="handleSearch"
        :showAction="false"
      />
    </view>

    <!-- 状态筛选 -->
    <view class="filter-tabs">
      <scroll-view scroll-x class="tabs-scroll">
        <view
          v-for="tab in statusTabs"
          :key="tab.value"
          :class="['tab-item', { active: currentStatus === tab.value }]"
          @click="changeStatus(tab.value)"
        >
          {{ tab.label }}
        </view>
      </scroll-view>
    </view>

    <!-- 订单列表 -->
    <scroll-view
      scroll-y
      class="order-scroll"
      @scrolltolower="loadMore"
      :refresher-enabled="true"
      @refresherrefresh="onRefresh"
      :refresher-triggered="isRefreshing"
    >
      <view class="order-list">
        <view
          v-for="order in orders"
          :key="order.id"
          class="order-card"
          @click="goDetail(order.id)"
        >
          <view class="order-header">
            <text class="order-no">{{ order.order_no }}</text>
            <view :class="['status-tag', `status-${order.status}`]">
              {{ getStatusText(order.status) }}
            </view>
          </view>

          <view class="order-body">
            <view class="order-type">
              <u-icon :name="getTypeIcon(order.order_type)" size="32rpx" />
              <text>{{ getTypeText(order.order_type) }}</text>
            </view>
            <view class="order-amount">
              <text class="label">订单金额：</text>
              <text class="value">¥{{ order.total_amount }}</text>
            </view>
          </view>

          <view class="order-footer">
            <text class="time">{{ formatDate(order.order_date) }}</text>
            <view class="actions">
              <u-button
                v-if="order.status === 'pending'"
                type="primary"
                size="mini"
                @click.stop="confirmOrder(order.id)"
              >
                确认
              </u-button>
              <u-button
                v-if="order.status === 'confirmed'"
                type="primary"
                size="mini"
                @click.stop="shipOrder(order.id)"
              >
                发货
              </u-button>
            </view>
          </view>
        </view>

        <u-loadmore :status="loadStatus" />
      </view>
    </scroll-view>

    <!-- 新建订单按钮 -->
    <view class="fab-button" @click="goCreate">
      <u-icon name="plus" size="48rpx" color="#fff" />
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getOrderList, confirmOrder as confirmOrderApi, shipOrder as shipOrderApi } from '@/api/order'

const keyword = ref('')
const currentStatus = ref('')
const orders = ref([])
const page = ref(1)
const pageSize = 10
const total = ref(0)
const loadStatus = ref('loadmore')
const isRefreshing = ref(false)

const statusTabs = [
  { label: '全部', value: '' },
  { label: '待处理', value: 'pending' },
  { label: '已确认', value: 'confirmed' },
  { label: '处理中', value: 'processing' },
  { label: '已发货', value: 'shipped' },
  { label: '已完成', value: 'completed' }
]

onMounted(() => {
  // 获取URL参数中的状态
  const pages = getCurrentPages()
  const currentPage = pages[pages.length - 1]
  if (currentPage?.options?.status) {
    currentStatus.value = currentPage.options.status
  }
  loadData()
})

const loadData = async (refresh = false) => {
  if (refresh) {
    page.value = 1
    orders.value = []
  }

  loadStatus.value = 'loading'

  try {
    const params = {
      page: page.value,
      page_size: pageSize,
      keyword: keyword.value || undefined,
      status: currentStatus.value || undefined
    }

    const res = await getOrderList(params)
    orders.value = refresh ? res.items : [...orders.value, ...res.items]
    total.value = res.total

    if (orders.value.length >= total.value) {
      loadStatus.value = 'nomore'
    } else {
      loadStatus.value = 'loadmore'
    }
  } catch (error) {
    loadStatus.value = 'loadmore'
    uni.showToast({ title: '加载失败', icon: 'none' })
  }
}

const loadMore = () => {
  if (loadStatus.value !== 'loadmore') return
  page.value++
  loadData()
}

const onRefresh = async () => {
  isRefreshing.value = true
  await loadData(true)
  isRefreshing.value = false
}

const handleSearch = () => {
  loadData(true)
}

const changeStatus = (status) => {
  currentStatus.value = status
  loadData(true)
}

const getStatusText = (status) => {
  const map = {
    pending: '待处理',
    confirmed: '已确认',
    processing: '处理中',
    shipped: '已发货',
    delivered: '已送达',
    completed: '已完成',
    cancelled: '已取消'
  }
  return map[status] || status
}

const getTypeText = (type) => {
  const map = {
    direct: '直接发货',
    delegated: '委托发货',
    processed: '加工发货'
  }
  return map[type] || type
}

const getTypeIcon = (type) => {
  const map = {
    direct: 'car',
    delegated: 'share',
    processed: 'setting'
  }
  return map[type] || 'order'
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
}

const goDetail = (id) => {
  uni.navigateTo({ url: `/pages/order/detail?id=${id}` })
}

const goCreate = () => {
  uni.navigateTo({ url: '/pages/order/form' })
}

const confirmOrder = async (id) => {
  try {
    await confirmOrderApi(id)
    uni.showToast({ title: '确认成功', icon: 'success' })
    loadData(true)
  } catch (error) {
    uni.showToast({ title: error.message || '操作失败', icon: 'none' })
  }
}

const shipOrder = async (id) => {
  try {
    await shipOrderApi(id)
    uni.showToast({ title: '发货成功', icon: 'success' })
    loadData(true)
  } catch (error) {
    uni.showToast({ title: error.message || '操作失败', icon: 'none' })
  }
}
</script>

<style lang="scss" scoped>
.order-list-page {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.search-bar {
  padding: 20rpx 24rpx;
  background-color: #fff;
}

.filter-tabs {
  background-color: #fff;
  border-bottom: 1rpx solid #f0f0f0;

  .tabs-scroll {
    white-space: nowrap;
    padding: 0 24rpx;

    .tab-item {
      display: inline-block;
      padding: 24rpx 32rpx;
      font-size: 28rpx;
      color: #666;

      &.active {
        color: $primary-color;
        font-weight: bold;
        position: relative;

        &::after {
          content: '';
          position: absolute;
          bottom: 0;
          left: 50%;
          transform: translateX(-50%);
          width: 48rpx;
          height: 4rpx;
          background-color: $primary-color;
          border-radius: 2rpx;
        }
      }
    }
  }
}

.order-scroll {
  height: calc(100vh - 200rpx);
}

.order-list {
  padding: 24rpx;
}

.order-card {
  background-color: #fff;
  border-radius: 16rpx;
  padding: 24rpx;
  margin-bottom: 24rpx;

  .order-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20rpx;

    .order-no {
      font-size: 30rpx;
      font-weight: bold;
      color: #333;
    }
  }

  .order-body {
    .order-type {
      display: flex;
      align-items: center;
      margin-bottom: 12rpx;

      text {
        margin-left: 8rpx;
        font-size: 26rpx;
        color: #666;
      }
    }

    .order-amount {
      .label {
        font-size: 26rpx;
        color: #999;
      }

      .value {
        font-size: 32rpx;
        font-weight: bold;
        color: #f5222d;
      }
    }
  }

  .order-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 20rpx;
    padding-top: 20rpx;
    border-top: 1rpx solid #f0f0f0;

    .time {
      font-size: 24rpx;
      color: #999;
    }
  }
}

.fab-button {
  position: fixed;
  right: 32rpx;
  bottom: 180rpx;
  width: 100rpx;
  height: 100rpx;
  background-color: $primary-color;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8rpx 24rpx rgba(0, 122, 255, 0.4);
}
</style>
