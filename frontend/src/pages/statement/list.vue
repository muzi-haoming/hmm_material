<template>
  <view class="list-page">
    <view class="search-bar">
      <u-search
        v-model="keyword"
        placeholder="搜索对账单号"
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
              <text class="label">对账周期:</text>
              <text class="value">{{ item.period || '-' }}</text>
            </view>
            <view class="info-row">
              <text class="label">总金额:</text>
              <text class="value highlight">¥{{ item.total_amount || 0 }}</text>
            </view>
          </view>
        </view>

        <view v-if="items.length === 0 && loadStatus === 'nomore'" class="empty-tip">
          暂无信息
        </view>

        <u-loadmore v-if="items.length > 0" :status="loadStatus" />
      </view>
    </scroll-view>

    <view class="action-bar">
      <button class="add-button" @click="goCreate">
        <u-icon name="plus" color="#fff" size="32rpx" />
        <text>新增对账单</text>
      </button>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getStatementList } from '@/api/statement'

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
    const res = await getStatementList({
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
    '1': '待确认',
    '2': '已确认',
    '3': '已结算'
  }
  return statusMap[status] || status
}

const goDetail = (id) => {
  uni.navigateTo({ url: `/pages/statement/detail?id=${id}` })
}

const goCreate = () => {
  uni.navigateTo({ url: '/pages/statement/form' })
}
</script>

<style lang="scss" scoped>
.list-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f5f5;
  padding-bottom: calc(120rpx + env(safe-area-inset-bottom));
}

.search-bar {
  padding: 20rpx 24rpx;
  background-color: #fff;
}

.list-scroll {
  flex: 1;
  height: 0;
}

.list-content {
  padding: 24rpx;
  display: flex;
  flex-direction: column;
  min-height: 100%;
  background-color: #fff;
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
        background-color: #e6f7ff;
        color: #1890ff;
      }

      &.status-3 {
        background-color: #f6ffed;
        color: #52c41a;
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
          color: #f5222d;
          font-weight: 500;
        }
      }
    }
  }
}

.empty-tip {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-grow: 1;
  color: #999;
  font-size: 28rpx;
}

.action-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20rpx 24rpx;
  padding-bottom: calc(20rpx + env(safe-area-inset-bottom));
  background-color: #fff;
  border-top: 1rpx solid #eee;
}

.add-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 80rpx;
  font-size: 32rpx;
  color: #fff;
  background: linear-gradient(135deg, #BA55D3 0%, #9932CC 100%);
  border-radius: 40rpx;
  box-shadow: 0 4rpx 12rpx rgba(186, 85, 211, 0.3);

  text {
    margin-left: 10rpx;
  }
}
</style>
