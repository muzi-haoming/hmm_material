<template>
  <view class="detail-page">
    <view class="detail-card" v-if="detail">
      <view class="card-header">
        <text class="title">采购单</text>
        <text class="code">{{ detail.code || '-' }}</text>
      </view>

      <view class="info-section">
        <view class="info-item">
          <text class="label">采购单号</text>
          <text class="value">{{ detail.code || '-' }}</text>
        </view>
        <view class="info-item">
          <text class="label">产品名称</text>
          <text class="value">{{ detail.product?.name || '-' }}</text>
        </view>
        <view class="info-item">
          <text class="label">采购金额</text>
          <text class="value highlight">¥{{ detail.amount || 0 }}</text>
        </view>
        <view class="info-item">
          <text class="label">状态</text>
          <text class="value">{{ getStatusText(detail.status) }}</text>
        </view>
        <view class="info-item">
          <text class="label">创建时间</text>
          <text class="value">{{ formatDate(detail.create_time) }}</text>
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
import { getPurchase, deletePurchase } from '@/api/purchase'

const detail = ref(null)
const id = ref('')

onMounted(() => {
  const pages = getCurrentPages()
  const currentPage = pages[pages.length - 1]
  id.value = currentPage.options.id
  loadDetail()
})

const loadDetail = async () => {
  try {
    detail.value = await getPurchase(id.value)
  } catch (error) {
    uni.showToast({ title: '加载失败', icon: 'none' })
  }
}

const getStatusText = (status) => {
  const statusMap = {
    '1': '待付款',
    '2': '已付款',
    '3': '已取消'
  }
  return statusMap[status] || status
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
}

const goEdit = () => {
  uni.navigateTo({ url: `/pages/purchase/form?id=${id.value}` })
}

const handleDelete = () => {
  uni.showModal({
    title: '确认删除',
    content: '确定要删除该采购单吗？',
    success: async (res) => {
      if (res.confirm) {
        try {
          await deletePurchase(id.value)
          uni.showToast({ title: '删除成功', icon: 'success' })
          setTimeout(() => {
            uni.navigateBack()
          }, 1500)
        } catch (error) {
          uni.showToast({ title: '删除失败', icon: 'none' })
        }
      }
    }
  })
}
</script>

<style lang="scss" scoped>
.detail-page {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 24rpx;
  padding-bottom: 160rpx;
}

.detail-card {
  background-color: #fff;
  border-radius: 16rpx;
  overflow: hidden;

  .card-header {
    background: linear-gradient(135deg, #fa8c16 0%, #d46b08 100%);
    padding: 32rpx 24rpx;

    .title {
      display: block;
      font-size: 36rpx;
      font-weight: bold;
      color: #fff;
      margin-bottom: 8rpx;
    }

    .code {
      font-size: 26rpx;
      color: rgba(255, 255, 255, 0.8);
    }
  }

  .info-section {
    padding: 24rpx;

    .info-item {
      display: flex;
      justify-content: space-between;
      padding: 20rpx 0;
      border-bottom: 1rpx solid #f0f0f0;

      &:last-child {
        border-bottom: none;
      }

      .label {
        font-size: 28rpx;
        color: #999;
      }

      .value {
        font-size: 28rpx;
        color: #333;

        &.highlight {
          color: #f5222d;
          font-weight: bold;
        }
      }
    }
  }
}

.action-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  gap: 24rpx;
  padding: 24rpx;
  background-color: #fff;
  box-shadow: 0 -4rpx 12rpx rgba(0, 0, 0, 0.05);
}
</style>
