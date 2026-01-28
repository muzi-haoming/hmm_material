<template>
  <view class="site-list-page">
    <view class="search-bar">
      <u-search
        v-model="keyword"
        placeholder="搜索工地名称/编号"
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
          v-for="site in sites"
          :key="site.id"
          class="site-card"
          @click="goDetail(site.id)"
        >
          <view class="site-header">
            <text class="site-name">{{ site.name }}</text>
            <text class="site-code">{{ site.code }}</text>
          </view>
          <view class="site-info">
            <view class="info-item">
              <u-icon name="map" size="28rpx" color="#999" />
              <text>{{ site.province }} {{ site.city }}</text>
            </view>
            <view class="info-item">
              <u-icon name="account" size="28rpx" color="#999" />
              <text>{{ site.contact_name }} {{ site.contact_phone }}</text>
            </view>
          </view>
        </view>

        <u-loadmore :status="loadStatus" />
      </view>
    </scroll-view>

    <view class="fab-btn" @click="goCreate">
      <u-icon name="plus" color="#fff" size="48rpx" />
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getSiteList } from '@/api/site'

const keyword = ref('')
const sites = ref([])
const page = ref(1)
const loadStatus = ref('loadmore')
const isRefreshing = ref(false)

onMounted(() => {
  loadData()
})

const loadData = async (refresh = false) => {
  if (refresh) {
    page.value = 1
    sites.value = []
  }

  loadStatus.value = 'loading'

  try {
    const res = await getSiteList({
      page: page.value,
      page_size: 20,
      keyword: keyword.value || undefined
    })

    sites.value = refresh ? res.items : [...sites.value, ...res.items]

    if (sites.value.length >= res.total) {
      loadStatus.value = 'nomore'
    } else {
      loadStatus.value = 'loadmore'
    }
  } catch (error) {
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
  uni.navigateTo({ url: `/pages/site/detail?id=${id}` })
}

const goCreate = () => {
  uni.navigateTo({ url: '/pages/site/form' })
}
</script>

<style lang="scss" scoped>
.site-list-page {
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

.site-card {
  background-color: #fff;
  border-radius: 16rpx;
  padding: 24rpx;
  margin-bottom: 20rpx;

  .site-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16rpx;

    .site-name {
      font-size: 32rpx;
      font-weight: bold;
      color: #333;
    }

    .site-code {
      font-size: 24rpx;
      color: #999;
      background-color: #f5f5f5;
      padding: 4rpx 12rpx;
      border-radius: 8rpx;
    }
  }

  .site-info {
    .info-item {
      display: flex;
      align-items: center;
      margin-top: 12rpx;

      text {
        margin-left: 8rpx;
        font-size: 26rpx;
        color: #666;
      }
    }
  }
}

.fab-btn {
  position: fixed;
  right: 32rpx;
  bottom: 140rpx;
  width: 96rpx;
  height: 96rpx;
  background: linear-gradient(135deg, #BA55D3 0%, #9932CC 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8rpx 24rpx rgba(186, 85, 211, 0.4);
}
</style>
