<template>
  <view class="list-page">
    <scroll-view scroll-y class="list-scroll" :refresher-enabled="true" @refresherrefresh="onRefresh" :refresher-triggered="isRefreshing">
      <view class="list-content">
        <view v-for="item in items" :key="item.id" class="list-card" @click="goDetail(item.id)">
          <view class="card-header">
            <text class="card-title">{{ item.name }}</text>
            <text class="card-code">{{ item.code }}</text>
          </view>
        </view>

        <view v-if="items.length === 0 && !isRefreshing" class="empty-state">
          <u-empty text="暂无角色数据" />
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getRoleList } from '@/api/user'

const items = ref([])
const isRefreshing = ref(false)

onMounted(() => loadData())

const loadData = async () => {
  try {
    const res = await getRoleList()
    items.value = res || []
  } catch (error) {
    console.error('加载失败:', error)
  }
}

const onRefresh = async () => {
  isRefreshing.value = true
  await loadData()
  isRefreshing.value = false
}

const goDetail = (id) => uni.navigateTo({ url: `/pages/role/detail?id=${id}` })
</script>

<style lang="scss" scoped>
.list-page { min-height: 100vh; background-color: #f5f5f5; }
.list-scroll { height: 100vh; }
.list-content { padding: 24rpx; }
.list-card {
  background-color: #fff; border-radius: 16rpx; padding: 24rpx; margin-bottom: 20rpx;
  .card-header { display: flex; justify-content: space-between; align-items: center;
    .card-title { font-size: 32rpx; font-weight: bold; color: #333; }
    .card-code { font-size: 24rpx; color: #999; background-color: #f5f5f5; padding: 4rpx 12rpx; border-radius: 8rpx; }
  }
}
.empty-state { padding: 100rpx 0; }
</style>
