<template>
  <view class="list-page">
    <view class="search-bar">
      <u-search v-model="keyword" placeholder="搜索合同编号/名称" @search="handleSearch" :showAction="false" />
    </view>
    <scroll-view scroll-y class="list-scroll" @scrolltolower="loadMore" :refresher-enabled="true" @refresherrefresh="onRefresh" :refresher-triggered="isRefreshing">
      <view class="list-content">
        <view v-for="item in items" :key="item.id" class="item-card" @click="goDetail(item.id)">
          <view class="item-header">
            <text class="item-name">{{ item.name }}</text>
            <view :class="['status-tag', `status-${item.status}`]">{{ getStatusText(item.status) }}</view>
          </view>
          <view class="item-info">
            <text class="contract-no">{{ item.contract_no }}</text>
            <text class="amount">¥{{ item.total_amount }}</text>
          </view>
          <view class="date-range">
            {{ formatDate(item.start_date) }} ~ {{ formatDate(item.end_date) }}
          </view>
        </view>
        <u-loadmore :status="loadStatus" />
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getContractList } from '@/api/contract'

const keyword = ref('')
const items = ref([])
const page = ref(1)
const loadStatus = ref('loadmore')
const isRefreshing = ref(false)

const getStatusText = (status) => {
  const map = { draft: '草稿', active: '生效中', completed: '已完成', cancelled: '已取消', expired: '已过期' }
  return map[status] || status
}
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return dateStr.split('T')[0]
}

onMounted(() => { loadData() })

const loadData = async (refresh = false) => {
  if (refresh) { page.value = 1; items.value = [] }
  loadStatus.value = 'loading'
  try {
    const res = await getContractList({ page: page.value, page_size: 20, keyword: keyword.value || undefined })
    items.value = refresh ? res.items : [...items.value, ...res.items]
    loadStatus.value = items.value.length >= res.total ? 'nomore' : 'loadmore'
  } catch (error) { loadStatus.value = 'loadmore' }
}

const loadMore = () => { if (loadStatus.value !== 'loadmore') return; page.value++; loadData() }
const onRefresh = async () => { isRefreshing.value = true; await loadData(true); isRefreshing.value = false }
const handleSearch = () => { loadData(true) }
const goDetail = (id) => { uni.navigateTo({ url: `/pages/contract/detail?id=${id}` }) }
</script>

<style lang="scss" scoped>
.list-page { min-height: 100vh; background-color: #f5f5f5; }
.search-bar { padding: 20rpx 24rpx; background-color: #fff; }
.list-scroll { height: calc(100vh - 100rpx); }
.list-content { padding: 24rpx; }
.item-card { background-color: #fff; border-radius: 16rpx; padding: 24rpx; margin-bottom: 20rpx; }
.item-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12rpx; }
.item-name { font-size: 30rpx; font-weight: bold; color: #333; flex: 1; }
.item-info { display: flex; justify-content: space-between; margin-bottom: 12rpx; }
.contract-no { font-size: 26rpx; color: #666; }
.amount { font-size: 28rpx; font-weight: bold; color: #f5222d; }
.date-range { font-size: 24rpx; color: #999; }
</style>
