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

        <view v-if="items.length === 0 && loadStatus === 'nomore'" class="empty-tip">
          暂无信息
        </view>
      </view>
    </scroll-view>

    <view class="action-bar">
      <button class="add-button" @click="goCreate">
        <u-icon name="plus" color="#fff" size="32rpx" />
        <text>新增角色</text>
      </button>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getRoleList } from '@/api/user'

const items = ref([])
const isRefreshing = ref(false)
const loadStatus = ref('loadmore')

onMounted(() => loadData())

const loadData = async () => {
  loadStatus.value = 'loading'
  try {
    const res = await getRoleList()
    items.value = res || []
    loadStatus.value = 'nomore'
  } catch (error) {
    console.error('加载失败:', error)
    loadStatus.value = 'loadmore'
  }
}

const onRefresh = async () => {
  isRefreshing.value = true
  await loadData()
  isRefreshing.value = false
}

const goDetail = (id) => uni.navigateTo({ url: `/pages/role/detail?id=${id}` })
const goCreate = () => uni.navigateTo({ url: '/pages/role/form' })
</script>

<style lang="scss" scoped>
.list-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f5f5;
  padding-bottom: calc(120rpx + env(safe-area-inset-bottom));
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
  background-color: #fff; border-radius: 16rpx; padding: 24rpx; margin-bottom: 20rpx;
  .card-header { display: flex; justify-content: space-between; align-items: center;
    .card-title { font-size: 32rpx; font-weight: bold; color: #333; }
    .card-code { font-size: 24rpx; color: #999; background-color: #f5f5f5; padding: 4rpx 12rpx; border-radius: 8rpx; }
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
