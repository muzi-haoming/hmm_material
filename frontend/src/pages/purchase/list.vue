<template>
  <view class="list-page">
    <view class="search-bar">
      <u-search
        v-model="keyword"
        placeholder="搜索采购单号"
        @search="handleSearch"
        @clear="handleSearch"
        :showAction="false"
      />
    </view>

    <scroll-view
      scroll-y
      class="list-scroll"
      @scrolltolower="loadMore"
      :refresher-enabled="true"
      @refresherrefresh="onRefresh"
      :refresher-triggered="isRefreshing"
    >
      <view class="list-content">
        <view
          v-for="item in items"
          :key="item.id"
          class="list-card"
          @click="goDetail(item.id)"
        >
          <view class="card-header">
            <text class="card-title">{{ item.code || '-' }}</text>
            <view :class="['status-tag', `status-${item.status}`]">
              {{ getStatusText(item.status) }}
            </view>
          </view>
          <view class="card-info">
            <view class="info-row">
              <text class="label">产品:</text>
              <text class="value">{{ item.product?.name || '-' }}</text>
            </view>
            <view class="info-row">
              <text class="label">金额:</text>
              <text class="value highlight">¥{{ item.amount || 0 }}</text>
            </view>
          </view>
        </view>

        <view v-if="items.length === 0 && loadStatus !== 'loading'" class="empty-state">
          <u-empty text="暂无采购单数据" />
        </view>

        <u-loadmore v-if="items.length > 0" :status="loadStatus" />
      </view>
    </scroll-view>

    <view class="fab-btn" @click="goCreate">
      <u-icon name="plus" color="#fff" size="48rpx" />
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getPurchaseList } from '@/api/purchase'

const keyword = ref('')
const items = ref([])
const page = ref(1)
const loadStatus = ref('loadmore')
const isRefreshing = ref(false)

onMounted(() => {
  loadData()
})

const loadData = async (refresh = false) => {
  if (refresh) {
    page.value = 1
    items.value = []
  }

  loadStatus.value = 'loading'

  try {
    const res = await getPurchaseList({
      page: page.value,
      page_size: 20,
      keyword: keyword.value || undefined
    })

    items.value = refresh ? res.items : [...items.value, ...res.items]

    if (items.value.length >= res.total) {
      loadStatus.value = 'nomore'
    } else {
      loadStatus.value = 'loadmore'
    }
  } catch (error) {
    console.error('加载失败:', error)
    loadStatus.value = 'loadmore'
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

const getStatusText = (status) => {
  const statusMap = {
    '1': '待付款',
    '2': '已付款',
    '3': '已取消'
  }
  return statusMap[status] || status
}

const goDetail = (id) => {
  uni.navigateTo({ url: `/pages/purchase/detail?id=${id}` })
}

const goCreate = () => {
  uni.navigateTo({ url: '/pages/purchase/form' })
}
</script>

<style lang="scss" scoped>
.list-page {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.search-bar {
  padding: 20rpx 24rpx;
  background-color: #fff;
}

.list-scroll {
  height: calc(100vh - 100rpx);
}

.list-content {
  padding: 24rpx;
}

.list-card {
  background-color: #fff;
  border-radius: 16rpx;
  padding: 24rpx;
  margin-bottom: 20rpx;

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16rpx;

    .card-title {
      font-size: 32rpx;
      font-weight: bold;
      color: #333;
    }

    .status-tag {
      font-size: 22rpx;
      padding: 6rpx 16rpx;
      border-radius: 20rpx;

      &.status-1 {
        background-color: #fff7e6;
        color: #fa8c16;
      }

      &.status-2 {
        background-color: #f6ffed;
        color: #52c41a;
      }

      &.status-3 {
        background-color: #f5f5f5;
        color: #999;
      }
    }
  }

  .card-info {
    .info-row {
      display: flex;
      margin-top: 8rpx;

      .label {
        font-size: 26rpx;
        color: #999;
        width: 100rpx;
      }

      .value {
        font-size: 26rpx;
        color: #666;
        flex: 1;

        &.highlight {
          color: #f5222d;
          font-weight: 500;
        }
      }
    }
  }
}

.empty-state {
  padding: 100rpx 0;
}

.fab-btn {
  position: fixed;
  right: 32rpx;
  bottom: 140rpx;
  width: 96rpx;
  height: 96rpx;
  background: linear-gradient(135deg, #fa8c16 0%, #d46b08 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8rpx 24rpx rgba(250, 140, 22, 0.4);
}
</style>
