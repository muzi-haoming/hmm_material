<template>
  <view class="list-page">
    <view class="search-bar">
      <u-search v-model="keyword" placeholder="搜索厂家组" @search="handleSearch" @clear="handleSearch" :showAction="false" />
    </view>

    <scroll-view scroll-y class="list-scroll" @scrolltolower="loadMore" :refresher-enabled="true" @refresherrefresh="onRefresh" :refresher-triggered="isRefreshing">
      <view class="list-content">
        <view v-for="item in items" :key="item.id" class="list-card" @click="goDetail(item.id)">
          <view class="card-header">
            <text class="card-title">{{ item.name }}</text>
            <text class="card-code">{{ item.code }}</text>
          </view>
          <view class="card-info">
            <view class="info-row">
              <text class="label">包含厂家:</text>
              <text class="value">{{ item.manufacturers?.length || 0 }} 个</text>
            </view>
          </view>
        </view>

        <view v-if="items.length === 0 && loadStatus !== 'loading'" class="empty-state">
          <u-empty text="暂无厂家组数据" />
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
import { getManufacturerGroupList } from '@/api/manufacturer'

const keyword = ref('')
const items = ref([])
const page = ref(1)
const loadStatus = ref('loadmore')
const isRefreshing = ref(false)

onMounted(() => loadData())

const loadData = async (refresh = false) => {
  if (refresh) { page.value = 1; items.value = [] }
  loadStatus.value = 'loading'
  try {
    const res = await getManufacturerGroupList({ page: page.value, page_size: 20, keyword: keyword.value || undefined })
    items.value = refresh ? res.items : [...items.value, ...res.items]
    loadStatus.value = items.value.length >= res.total ? 'nomore' : 'loadmore'
  } catch (error) {
    console.error('加载失败:', error)
    loadStatus.value = 'loadmore'
  }
}

const loadMore = () => { if (loadStatus.value !== 'loadmore') return; page.value++; loadData() }
const onRefresh = async () => { isRefreshing.value = true; await loadData(true); isRefreshing.value = false }
const handleSearch = () => loadData(true)
const goDetail = (id) => uni.navigateTo({ url: `/pages/manufacturer-group/detail?id=${id}` })
const goCreate = () => uni.navigateTo({ url: '/pages/manufacturer-group/form' })
</script>

<style lang="scss" scoped>
.list-page { min-height: 100vh; background-color: #f5f5f5; }
.search-bar { padding: 20rpx 24rpx; background-color: #fff; }
.list-scroll { height: calc(100vh - 100rpx); }
.list-content { padding: 24rpx; }
.list-card {
  background-color: #fff; border-radius: 16rpx; padding: 24rpx; margin-bottom: 20rpx;
  .card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16rpx;
    .card-title { font-size: 32rpx; font-weight: bold; color: #333; }
    .card-code { font-size: 24rpx; color: #999; background-color: #f5f5f5; padding: 4rpx 12rpx; border-radius: 8rpx; }
  }
  .card-info .info-row { display: flex; margin-top: 8rpx;
    .label { font-size: 26rpx; color: #999; width: 140rpx; }
    .value { font-size: 26rpx; color: #666; flex: 1; }
  }
}
.empty-state { padding: 100rpx 0; }
.fab-btn { position: fixed; right: 32rpx; bottom: 140rpx; width: 96rpx; height: 96rpx; background: linear-gradient(135deg, #13c2c2 0%, #08979c 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 8rpx 24rpx rgba(19, 194, 194, 0.4); }
</style>
