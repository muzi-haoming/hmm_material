<template>
  <view class="detail-page">
    <view class="detail-card" v-if="detail">
      <view class="card-header">
        <text class="title">出库单</text>
        <text class="code">{{ detail.code || '-' }}</text>
      </view>

      <view class="info-section">
        <view class="info-item">
          <text class="label">产品名称</text>
          <text class="value">{{ detail.product?.name || '-' }}</text>
        </view>
        <view class="info-item">
          <text class="label">出库数量</text>
          <text class="value highlight">-{{ detail.quantity }} {{ detail.product?.unit || '' }}</text>
        </view>
        <view class="info-item">
          <text class="label">关联订单</text>
          <text class="value">{{ detail.order?.code || '-' }}</text>
        </view>
        <view class="info-item">
          <text class="label">领用厂家</text>
          <text class="value">{{ detail.manufacturer?.name || '-' }}</text>
        </view>
        <view class="info-item">
          <text class="label">出库时间</text>
          <text class="value">{{ formatDate(detail.create_time) }}</text>
        </view>
      </view>
    </view>

    <view class="action-bar">
      <u-button type="error" @click="handleDelete">删除</u-button>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getStockOut, deleteStockOut } from '@/api/stock'

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
    detail.value = await getStockOut(id.value)
  } catch (error) {
    uni.showToast({ title: '加载失败', icon: 'none' })
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
}

const handleDelete = () => {
  uni.showModal({
    title: '确认删除',
    content: '确定要删除该出库记录吗？',
    success: async (res) => {
      if (res.confirm) {
        try {
          await deleteStockOut(id.value)
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
    background: linear-gradient(135deg, #f5222d 0%, #cf1322 100%);
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
  padding: 24rpx;
  background-color: #fff;
  box-shadow: 0 -4rpx 12rpx rgba(0, 0, 0, 0.05);
}
</style>
