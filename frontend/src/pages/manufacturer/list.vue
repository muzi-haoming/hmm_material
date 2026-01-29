<template>
  <view class="list-page">
    <view class="search-bar">
      <u-search v-model="keyword" placeholder="搜索厂家名称/编号" @search="handleSearch" :showAction="false" />
    </view>

    <scroll-view scroll-y class="list-scroll" @scrolltolower="loadMore" :refresher-enabled="true" @refresherrefresh="onRefresh" :refresher-triggered="isRefreshing">
      <view class="list-content">
        <view v-for="item in items" :key="item.id" class="item-card" @click="goDetail(item.id)">
          <view class="item-header">
            <text class="item-name">{{ item.name }}</text>
            <view :class="['type-tag', `type-${item.type}`]">{{ getTypeText(item.type) }}</view>
          </view>
          <view class="item-info">
            <view class="info-item">
              <u-icon name="map" size="28rpx" color="#999" />
              <text>{{ item.province }} {{ item.city }}</text>
            </view>
            <view class="info-item">
              <u-icon name="account" size="28rpx" color="#999" />
              <text>{{ item.contact_name }} {{ item.contact_phone }}</text>
            </view>
          </view>
        </view>
        <view v-if="items.length === 0 && loadStatus === 'nomore'" class="empty-tip">
          暂无信息
        </view>
        <u-loadmore :status="loadStatus" />
      </view>
    </scroll-view>

    <view class="action-bar">
      <button class="add-button" @click="goCreate">
        <u-icon name="plus" color="#fff" size="32rpx" />
        <text>新增厂家</text>
      </button>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getManufacturerList } from '@/api/manufacturer'

const keyword = ref('')
const items = ref([])
const page = ref(1)
const loadStatus = ref('loadmore')
const isRefreshing = ref(false)

const getTypeText = (type) => {
  const map = { supplier: '供应商', processor: '加工厂', both: '综合' }
  return map[type] || type
}

onMounted(() => { loadData() })

const loadData = async (refresh = false) => {
  if (refresh) { page.value = 1; items.value = [] }
  loadStatus.value = 'loading'
  try {
    const res = await getManufacturerList({ page: page.value, page_size: 20, keyword: keyword.value || undefined })
    items.value = refresh ? res.items : [...items.value, ...res.items]
    loadStatus.value = items.value.length >= res.total ? 'nomore' : 'loadmore'
  } catch (error) { loadStatus.value = 'loadmore' }
}

const loadMore = () => { if (loadStatus.value !== 'loadmore') return; page.value++; loadData() }
const onRefresh = async () => { isRefreshing.value = true; await loadData(true); isRefreshing.value = false }
const handleSearch = () => { loadData(true) }
const goDetail = (id) => { uni.navigateTo({ url: `/pages/manufacturer/detail?id=${id}` }) }
const goCreate = () => { uni.navigateTo({ url: '/pages/manufacturer/form' }) }
</script>

<style lang="scss" scoped>
.list-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f5f5;
  padding-bottom: calc(120rpx + env(safe-area-inset-bottom));
}
.search-bar { padding: 20rpx 24rpx; background-color: #fff; }
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
.item-card { background-color: #fff; border-radius: 16rpx; padding: 24rpx; margin-bottom: 20rpx; }
.item-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16rpx; }
.item-name { font-size: 32rpx; font-weight: bold; color: #333; }
.type-tag { font-size: 24rpx; padding: 4rpx 12rpx; border-radius: 8rpx; background-color: #e6f7ff; color: #1890ff; }
.type-processor { background-color: #fff7e6; color: #fa8c16; }
.type-both { background-color: #f6ffed; color: #52c41a; }
.item-info .info-item { display: flex; align-items: center; margin-top: 12rpx; text { margin-left: 8rpx; font-size: 26rpx; color: #666; } }
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
