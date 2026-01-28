<template>
  <view class="list-page">
    <view class="search-bar">
      <u-search
        v-model="keyword"
        placeholder="搜索产品名称"
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
            <text class="card-title">{{ item.product?.name || '-' }}</text>
            <view :class="['stock-badge', item.quantity > 0 ? 'in-stock' : 'out-stock']">
              {{ item.quantity > 0 ? '有库存' : '无库存' }}
            </view>
          </view>
          <view class="card-info">
            <view class="info-row">
              <text class="label">产品编号:</text>
              <text class="value">{{ item.product?.code || '-' }}</text>
            </view>
            <view class="info-row">
              <text class="label">库存数量:</text>
              <text class="value highlight">{{ item.quantity }} {{ item.product?.unit || '' }}</text>
            </view>
          </view>
        </view>

        <view v-if="items.length === 0 && loadStatus !== 'loading'" class="empty-state">
          <u-empty text="暂无库存数据" />
        </view>

        <u-loadmore v-if="items.length > 0" :status="loadStatus" />
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getStockList } from '@/api/stock'

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
    const res = await getStockList({
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

const goDetail = (id) => {
  uni.navigateTo({ url: `/pages/stock/detail?id=${id}` })
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

    .stock-badge {
      font-size: 22rpx;
      padding: 6rpx 16rpx;
      border-radius: 20rpx;

      &.in-stock {
        background-color: #f6ffed;
        color: #52c41a;
      }

      &.out-stock {
        background-color: #fff1f0;
        color: #f5222d;
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
        width: 140rpx;
      }

      .value {
        font-size: 26rpx;
        color: #666;
        flex: 1;

        &.highlight {
          color: #1890ff;
          font-weight: 500;
        }
      }
    }
  }
}

.empty-state {
  padding: 100rpx 0;
}
</style>
