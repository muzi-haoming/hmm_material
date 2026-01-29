<template>
  <view class="list-page">
    <view class="search-bar">
      <u-search v-model="keyword" placeholder="搜索用户" @search="handleSearch" @clear="handleSearch" :showAction="false" />
    </view>

    <scroll-view scroll-y class="list-scroll" @scrolltolower="loadMore" :refresher-enabled="true" @refresherrefresh="onRefresh" :refresher-triggered="isRefreshing">
      <view class="list-content">
        <view v-for="item in items" :key="item.id" class="list-card" @click="goDetail(item.id)">
          <view class="card-header">
            <view class="user-avatar">
              <text>{{ item.name?.charAt(0) || 'U' }}</text>
            </view>
            <view class="user-info">
              <text class="user-name">{{ item.name }}</text>
              <text class="user-username">@{{ item.username }}</text>
            </view>
            <view class="role-tag">{{ item.role?.name || '未知角色' }}</view>
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
        <text>新增用户</text>
      </button>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getUserList } from '@/api/user'

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
    const res = await getUserList({ page: page.value, page_size: 20 })
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
const goDetail = (id) => uni.navigateTo({ url: `/pages/users/detail?id=${id}` })
const goCreate = () => uni.navigateTo({ url: '/pages/users/form' })
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
.list-card {
  background-color: #fff; border-radius: 16rpx; padding: 24rpx; margin-bottom: 20rpx;
  .card-header { display: flex; align-items: center;
    .user-avatar { width: 80rpx; height: 80rpx; border-radius: 50%; background: linear-gradient(135deg, #007AFF 0%, #0056b3 100%); display: flex; align-items: center; justify-content: center; margin-right: 20rpx;
      text { font-size: 32rpx; color: #fff; font-weight: bold; }
    }
    .user-info { flex: 1;
      .user-name { display: block; font-size: 30rpx; font-weight: bold; color: #333; margin-bottom: 4rpx; }
      .user-username { font-size: 24rpx; color: #999; }
    }
    .role-tag { font-size: 22rpx; padding: 6rpx 16rpx; background-color: #e6f7ff; color: #1890ff; border-radius: 20rpx; }
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
