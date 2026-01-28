<template>
  <view class="detail-page">
    <view class="detail-card" v-if="detail">
      <view class="card-header">
        <view class="user-avatar">
          <text>{{ detail.name?.charAt(0) || 'U' }}</text>
        </view>
        <text class="user-name">{{ detail.name }}</text>
        <text class="user-username">@{{ detail.username }}</text>
      </view>

      <view class="info-section">
        <view class="info-item">
          <text class="label">用户名</text>
          <text class="value">{{ detail.username }}</text>
        </view>
        <view class="info-item">
          <text class="label">姓名</text>
          <text class="value">{{ detail.name }}</text>
        </view>
        <view class="info-item">
          <text class="label">角色</text>
          <text class="value">{{ detail.role?.name || '-' }}</text>
        </view>
        <view class="info-item">
          <text class="label">创建时间</text>
          <text class="value">{{ formatDate(detail.create_time) }}</text>
        </view>
      </view>
    </view>

    <view class="action-bar">
      <u-button type="error" @click="handleDelete">删除用户</u-button>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getUser, deleteUser } from '@/api/user'

const detail = ref(null)
const id = ref('')

onMounted(() => {
  const pages = getCurrentPages()
  const currentPage = pages[pages.length - 1]
  id.value = currentPage.options.id
  loadDetail()
})

const loadDetail = async () => {
  try { detail.value = await getUser(id.value) }
  catch (error) { uni.showToast({ title: '加载失败', icon: 'none' }) }
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`
}

const handleDelete = () => {
  uni.showModal({
    title: '确认删除', content: '确定要删除该用户吗？',
    success: async (res) => {
      if (res.confirm) {
        try {
          await deleteUser(id.value)
          uni.showToast({ title: '删除成功', icon: 'success' })
          setTimeout(() => uni.navigateBack(), 1500)
        } catch (error) { uni.showToast({ title: error.message || '删除失败', icon: 'none' }) }
      }
    }
  })
}
</script>

<style lang="scss" scoped>
.detail-page { min-height: 100vh; background-color: #f5f5f5; padding: 24rpx; padding-bottom: 160rpx; }
.detail-card {
  background-color: #fff; border-radius: 16rpx; overflow: hidden;
  .card-header { background: linear-gradient(135deg, #007AFF 0%, #0056b3 100%); padding: 48rpx 24rpx; display: flex; flex-direction: column; align-items: center;
    .user-avatar { width: 120rpx; height: 120rpx; border-radius: 50%; background-color: rgba(255,255,255,0.2); display: flex; align-items: center; justify-content: center; margin-bottom: 16rpx;
      text { font-size: 48rpx; color: #fff; font-weight: bold; }
    }
    .user-name { font-size: 36rpx; font-weight: bold; color: #fff; margin-bottom: 8rpx; }
    .user-username { font-size: 26rpx; color: rgba(255,255,255,0.8); }
  }
  .info-section { padding: 24rpx;
    .info-item { display: flex; justify-content: space-between; padding: 20rpx 0; border-bottom: 1rpx solid #f0f0f0;
      &:last-child { border-bottom: none; }
      .label { font-size: 28rpx; color: #999; }
      .value { font-size: 28rpx; color: #333; }
    }
  }
}
.action-bar { position: fixed; bottom: 0; left: 0; right: 0; padding: 24rpx; background-color: #fff; box-shadow: 0 -4rpx 12rpx rgba(0, 0, 0, 0.05); }
</style>
