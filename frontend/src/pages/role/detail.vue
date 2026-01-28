<template>
  <view class="detail-page">
    <view class="detail-card" v-if="detail">
      <view class="card-header">
        <text class="title">{{ detail.name }}</text>
        <text class="code">{{ detail.code }}</text>
      </view>

      <view class="info-section">
        <view class="info-item">
          <text class="label">角色编号</text>
          <text class="value">{{ detail.code }}</text>
        </view>
        <view class="info-item">
          <text class="label">角色名称</text>
          <text class="value">{{ detail.name }}</text>
        </view>
      </view>
    </view>

    <view class="action-bar">
      <u-button type="primary" @click="goEdit">编辑</u-button>
      <u-button type="error" @click="handleDelete">删除</u-button>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getRole, deleteRole } from '@/api/user'

const detail = ref(null)
const id = ref('')

onMounted(() => {
  const pages = getCurrentPages()
  const currentPage = pages[pages.length - 1]
  id.value = currentPage.options.id
  loadDetail()
})

const loadDetail = async () => {
  try { detail.value = await getRole(id.value) }
  catch (error) { uni.showToast({ title: '加载失败', icon: 'none' }) }
}

const goEdit = () => uni.navigateTo({ url: `/pages/role/form?id=${id.value}` })

const handleDelete = () => {
  uni.showModal({
    title: '确认删除', content: '确定要删除该角色吗？',
    success: async (res) => {
      if (res.confirm) {
        try {
          await deleteRole(id.value)
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
  .card-header { background: linear-gradient(135deg, #faad14 0%, #d48806 100%); padding: 32rpx 24rpx;
    .title { display: block; font-size: 36rpx; font-weight: bold; color: #fff; margin-bottom: 8rpx; }
    .code { font-size: 26rpx; color: rgba(255,255,255,0.8); }
  }
  .info-section { padding: 24rpx;
    .info-item { display: flex; justify-content: space-between; padding: 20rpx 0; border-bottom: 1rpx solid #f0f0f0;
      &:last-child { border-bottom: none; }
      .label { font-size: 28rpx; color: #999; }
      .value { font-size: 28rpx; color: #333; }
    }
  }
}
.action-bar { position: fixed; bottom: 0; left: 0; right: 0; display: flex; gap: 24rpx; padding: 24rpx; background-color: #fff; box-shadow: 0 -4rpx 12rpx rgba(0, 0, 0, 0.05); }
</style>
