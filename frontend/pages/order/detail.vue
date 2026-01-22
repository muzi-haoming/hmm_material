<template>
  <view class="order-detail-page">
    <view v-if="order" class="detail-content">
      <!-- 订单状态 -->
      <view class="status-section">
        <view :class="['status-icon', `status-${order.status}`]">
          <u-icon :name="getStatusIcon(order.status)" size="48rpx" color="#fff" />
        </view>
        <text class="status-text">{{ getStatusText(order.status) }}</text>
      </view>

      <!-- 基本信息 -->
      <view class="card">
        <view class="card-title">订单信息</view>
        <view class="info-row">
          <text class="label">订单编号</text>
          <text class="value">{{ order.order_no }}</text>
        </view>
        <view class="info-row">
          <text class="label">订单类型</text>
          <text class="value">{{ getTypeText(order.order_type) }}</text>
        </view>
        <view class="info-row">
          <text class="label">订单金额</text>
          <text class="value price">¥{{ order.total_amount }}</text>
        </view>
        <view class="info-row">
          <text class="label">下单时间</text>
          <text class="value">{{ formatDate(order.order_date) }}</text>
        </view>
        <view v-if="order.expected_delivery_date" class="info-row">
          <text class="label">期望交付</text>
          <text class="value">{{ formatDate(order.expected_delivery_date) }}</text>
        </view>
      </view>

      <!-- 收货信息 -->
      <view class="card">
        <view class="card-title">收货信息</view>
        <view class="info-row">
          <text class="label">收货地址</text>
          <text class="value">{{ order.delivery_address }}</text>
        </view>
        <view class="info-row">
          <text class="label">联系人</text>
          <text class="value">{{ order.delivery_contact }}</text>
        </view>
        <view class="info-row">
          <text class="label">联系电话</text>
          <text class="value phone" @click="callPhone(order.delivery_phone)">
            {{ order.delivery_phone }}
          </text>
        </view>
      </view>

      <!-- 商品明细 -->
      <view class="card">
        <view class="card-title">商品明细</view>
        <view
          v-for="item in order.items"
          :key="item.id"
          class="product-item"
        >
          <view class="product-info">
            <text class="product-name">产品ID: {{ item.product_id }}</text>
            <text v-if="item.specification" class="product-spec">
              规格: {{ item.specification }}
            </text>
          </view>
          <view class="product-price">
            <text class="unit-price">¥{{ item.unit_price }}</text>
            <text class="quantity">x{{ item.quantity }}</text>
            <text class="amount">¥{{ item.amount }}</text>
          </view>
        </view>
      </view>

      <!-- 备注 -->
      <view v-if="order.remark" class="card">
        <view class="card-title">备注</view>
        <text class="remark-text">{{ order.remark }}</text>
      </view>
    </view>

    <!-- 底部操作按钮 -->
    <view class="action-bar" v-if="order">
      <template v-if="order.status === 'pending'">
        <u-button type="default" @click="handleCancel">取消订单</u-button>
        <u-button type="primary" @click="handleConfirm">确认订单</u-button>
      </template>
      <template v-else-if="order.status === 'confirmed'">
        <u-button type="primary" @click="handleShip">发货</u-button>
      </template>
      <template v-else-if="order.status === 'shipped'">
        <u-button type="primary" @click="handleComplete">确认收货</u-button>
      </template>
    </view>

    <u-loading-page :loading="loading" />
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import {
  getOrder,
  confirmOrder,
  shipOrder,
  completeOrder,
  cancelOrder
} from '@/api/order'

const order = ref(null)
const loading = ref(true)
const orderId = ref(null)

onMounted(() => {
  const pages = getCurrentPages()
  const currentPage = pages[pages.length - 1]
  orderId.value = currentPage?.options?.id

  if (orderId.value) {
    loadDetail()
  }
})

const loadDetail = async () => {
  loading.value = true
  try {
    order.value = await getOrder(orderId.value)
  } catch (error) {
    uni.showToast({ title: '加载失败', icon: 'none' })
  } finally {
    loading.value = false
  }
}

const getStatusText = (status) => {
  const map = {
    pending: '待处理',
    confirmed: '已确认',
    processing: '处理中',
    shipped: '已发货',
    delivered: '已送达',
    completed: '已完成',
    cancelled: '已取消'
  }
  return map[status] || status
}

const getStatusIcon = (status) => {
  const map = {
    pending: 'clock',
    confirmed: 'checkmark',
    processing: 'setting',
    shipped: 'car',
    delivered: 'checkmark-circle',
    completed: 'checkmark-circle-fill',
    cancelled: 'close-circle'
  }
  return map[status] || 'info-circle'
}

const getTypeText = (type) => {
  const map = {
    direct: '直接发货',
    delegated: '委托发货',
    processed: '加工发货'
  }
  return map[type] || type
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
}

const callPhone = (phone) => {
  uni.makePhoneCall({ phoneNumber: phone })
}

const handleConfirm = async () => {
  try {
    await confirmOrder(orderId.value)
    uni.showToast({ title: '确认成功', icon: 'success' })
    loadDetail()
  } catch (error) {
    uni.showToast({ title: error.message || '操作失败', icon: 'none' })
  }
}

const handleShip = async () => {
  try {
    await shipOrder(orderId.value)
    uni.showToast({ title: '发货成功', icon: 'success' })
    loadDetail()
  } catch (error) {
    uni.showToast({ title: error.message || '操作失败', icon: 'none' })
  }
}

const handleComplete = async () => {
  try {
    await completeOrder(orderId.value)
    uni.showToast({ title: '已完成', icon: 'success' })
    loadDetail()
  } catch (error) {
    uni.showToast({ title: error.message || '操作失败', icon: 'none' })
  }
}

const handleCancel = async () => {
  uni.showModal({
    title: '确认取消',
    content: '确定要取消此订单吗？',
    success: async (res) => {
      if (res.confirm) {
        try {
          await cancelOrder(orderId.value)
          uni.showToast({ title: '已取消', icon: 'success' })
          loadDetail()
        } catch (error) {
          uni.showToast({ title: error.message || '操作失败', icon: 'none' })
        }
      }
    }
  })
}
</script>

<style lang="scss" scoped>
.order-detail-page {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding-bottom: 140rpx;
}

.status-section {
  background: linear-gradient(135deg, #007AFF 0%, #0056b3 100%);
  padding: 48rpx;
  display: flex;
  flex-direction: column;
  align-items: center;

  .status-icon {
    width: 96rpx;
    height: 96rpx;
    border-radius: 50%;
    background-color: rgba(255, 255, 255, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .status-text {
    margin-top: 20rpx;
    font-size: 36rpx;
    font-weight: bold;
    color: #fff;
  }
}

.card {
  margin: 24rpx;
  background-color: #fff;
  border-radius: 16rpx;
  padding: 24rpx;

  .card-title {
    font-size: 30rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 20rpx;
    padding-bottom: 16rpx;
    border-bottom: 1rpx solid #f0f0f0;
  }
}

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 16rpx 0;

  .label {
    font-size: 28rpx;
    color: #999;
  }

  .value {
    font-size: 28rpx;
    color: #333;

    &.price {
      color: #f5222d;
      font-weight: bold;
    }

    &.phone {
      color: $primary-color;
    }
  }
}

.product-item {
  display: flex;
  justify-content: space-between;
  padding: 20rpx 0;
  border-bottom: 1rpx solid #f0f0f0;

  &:last-child {
    border-bottom: none;
  }

  .product-info {
    .product-name {
      font-size: 28rpx;
      color: #333;
      display: block;
    }

    .product-spec {
      font-size: 24rpx;
      color: #999;
      margin-top: 8rpx;
      display: block;
    }
  }

  .product-price {
    text-align: right;

    .unit-price {
      font-size: 26rpx;
      color: #666;
      display: block;
    }

    .quantity {
      font-size: 24rpx;
      color: #999;
      display: block;
    }

    .amount {
      font-size: 28rpx;
      font-weight: bold;
      color: #f5222d;
      display: block;
      margin-top: 8rpx;
    }
  }
}

.remark-text {
  font-size: 28rpx;
  color: #666;
  line-height: 1.6;
}

.action-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: #fff;
  padding: 24rpx 32rpx;
  padding-bottom: calc(24rpx + env(safe-area-inset-bottom));
  display: flex;
  gap: 24rpx;
  box-shadow: 0 -4rpx 16rpx rgba(0, 0, 0, 0.05);
}
</style>
