<template>
  <view class="list-page">
    <view class="filter-tabs">
      <scroll-view scroll-x class="tabs-scroll">
        <view v-for="tab in typeTabs" :key="tab.value" :class="['tab-item', { active: currentType === tab.value }]" @click="changeType(tab.value)">{{ tab.label }}</view>
      </scroll-view>
    </view>
    <scroll-view scroll-y class="list-scroll" @scrolltolower="loadMore" :refresher-enabled="true" @refresherrefresh="onRefresh" :refresher-triggered="isRefreshing">
      <view class="list-content">
        <view v-for="item in items" :key="item.id" class="item-card" @click="goDetail(item.id)">
          <view class="item-header">
            <text class="item-no">{{ item.delegation_no }}</text>
            <view :class="['status-tag', `status-${item.status}`]">{{ getStatusText(item.status) }}</view>
          </view>
          <view class="item-type">
            <u-icon :name="item.type === 'supply' ? 'share' : 'setting'" size="28rpx" />
            <text>{{ item.type === 'supply' ? '委托供货' : '委托加工' }}</text>
          </view>
          <view class="item-info">
            <text class="amount">¥{{ item.amount }}</text>
            <text class="date">{{ formatDate(item.delegation_date) }}</text>
          </view>
        </view>
        <u-loadmore :status="loadStatus" />
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getDelegationList } from '@/api/delegation'

const currentType = ref('')
const items = ref([])
const page = ref(1)
const loadStatus = ref('loadmore')
const isRefreshing = ref(false)

const typeTabs = [
  { label: '全部', value: '' },
  { label: '委托供货', value: 'supply' },
  { label: '委托加工', value: 'process' }
]

const getStatusText = (status) => {
  const map = { draft: '草稿', pending: '待确认', accepted: '已接受', in_progress: '执行中', completed: '已完成', rejected: '已拒绝', cancelled: '已取消' }
  return map[status] || status
}
const formatDate = (dateStr) => dateStr ? dateStr.split('T')[0] : ''

onMounted(() => { loadData() })

const loadData = async (refresh = false) => {
  if (refresh) { page.value = 1; items.value = [] }
  loadStatus.value = 'loading'
  try {
    const res = await getDelegationList({ page: page.value, page_size: 20, type: currentType.value || undefined })
    items.value = refresh ? res.items : [...items.value, ...res.items]
    loadStatus.value = items.value.length >= res.total ? 'nomore' : 'loadmore'
  } catch (error) { loadStatus.value = 'loadmore' }
}

const changeType = (type) => { currentType.value = type; loadData(true) }
const loadMore = () => { if (loadStatus.value !== 'loadmore') return; page.value++; loadData() }
const onRefresh = async () => { isRefreshing.value = true; await loadData(true); isRefreshing.value = false }
const goDetail = (id) => { uni.navigateTo({ url: `/pages/delegation/detail?id=${id}` }) }
</script>

<style lang="scss" scoped>
.list-page { min-height: 100vh; background-color: #f5f5f5; }
.filter-tabs { background-color: #fff; border-bottom: 1rpx solid #f0f0f0; }
.tabs-scroll { white-space: nowrap; padding: 0 24rpx; }
.tab-item { display: inline-block; padding: 24rpx 32rpx; font-size: 28rpx; color: #666; &.active { color: $primary-color; font-weight: bold; } }
.list-scroll { height: calc(100vh - 100rpx); }
.list-content { padding: 24rpx; }
.item-card { background-color: #fff; border-radius: 16rpx; padding: 24rpx; margin-bottom: 20rpx; }
.item-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12rpx; }
.item-no { font-size: 28rpx; font-weight: bold; color: #333; }
.item-type { display: flex; align-items: center; margin-bottom: 12rpx; text { margin-left: 8rpx; font-size: 26rpx; color: #666; } }
.item-info { display: flex; justify-content: space-between; }
.amount { font-size: 28rpx; font-weight: bold; color: #f5222d; }
.date { font-size: 24rpx; color: #999; }
</style>
