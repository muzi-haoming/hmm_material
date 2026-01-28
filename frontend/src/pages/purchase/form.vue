<template>
  <view class="form-page">
    <view class="form-card">
      <view class="form-item">
        <text class="label required">关联订单</text>
        <picker mode="selector" :range="orders" range-key="code" @change="onOrderChange">
          <view class="picker-field">
            <text :class="{ placeholder: !formData.order_id }">
              {{ selectedOrderCode || '请选择订单' }}
            </text>
            <u-icon name="arrow-down" color="#999" size="28rpx" />
          </view>
        </picker>
      </view>

      <view class="form-item">
        <text class="label required">产品</text>
        <picker mode="selector" :range="products" range-key="name" @change="onProductChange">
          <view class="picker-field">
            <text :class="{ placeholder: !formData.product_id }">
              {{ selectedProductName || '请选择产品' }}
            </text>
            <u-icon name="arrow-down" color="#999" size="28rpx" />
          </view>
        </picker>
      </view>

      <view class="form-item">
        <text class="label required">采购金额</text>
        <input
          class="input"
          v-model="formData.amount"
          type="digit"
          placeholder="请输入采购金额"
        />
      </view>

      <view class="form-item">
        <text class="label required">状态</text>
        <picker mode="selector" :range="statusOptions" range-key="label" @change="onStatusChange">
          <view class="picker-field">
            <text :class="{ placeholder: !formData.status }">
              {{ selectedStatusLabel || '请选择状态' }}
            </text>
            <u-icon name="arrow-down" color="#999" size="28rpx" />
          </view>
        </picker>
      </view>
    </view>

    <view class="action-bar">
      <u-button type="primary" :loading="loading" @click="handleSubmit">
        {{ isEdit ? '保存修改' : '创建采购单' }}
      </u-button>
    </view>
  </view>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { getPurchase, createPurchase, updatePurchase } from '@/api/purchase'
import { getOrderList } from '@/api/order'
import { getProductList } from '@/api/product'

const id = ref('')
const loading = ref(false)
const orders = ref([])
const products = ref([])

const statusOptions = [
  { label: '待付款', value: '1' },
  { label: '已付款', value: '2' },
  { label: '已取消', value: '3' }
]

const formData = reactive({
  order_id: '',
  product_id: '',
  amount: '',
  status: '1'
})

const isEdit = computed(() => !!id.value)

const selectedOrderCode = computed(() => {
  const order = orders.value.find(o => o.id === formData.order_id)
  return order?.code || ''
})

const selectedProductName = computed(() => {
  const product = products.value.find(p => p.id === formData.product_id)
  return product?.name || ''
})

const selectedStatusLabel = computed(() => {
  const status = statusOptions.find(s => s.value === formData.status)
  return status?.label || ''
})

onMounted(() => {
  const pages = getCurrentPages()
  const currentPage = pages[pages.length - 1]
  id.value = currentPage.options.id || ''

  loadOrders()
  loadProducts()

  if (id.value) {
    loadDetail()
  }
})

const loadOrders = async () => {
  try {
    const res = await getOrderList({ page: 1, page_size: 100 })
    orders.value = res.items || []
  } catch (error) {
    console.error('加载订单失败:', error)
  }
}

const loadProducts = async () => {
  try {
    const res = await getProductList({ page: 1, page_size: 100 })
    products.value = res.items || []
  } catch (error) {
    console.error('加载产品失败:', error)
  }
}

const loadDetail = async () => {
  try {
    const detail = await getPurchase(id.value)
    Object.assign(formData, {
      order_id: detail.order_id || '',
      product_id: detail.product_id || '',
      amount: detail.amount?.toString() || '',
      status: detail.status || '1'
    })
  } catch (error) {
    uni.showToast({ title: '加载失败', icon: 'none' })
  }
}

const onOrderChange = (e) => {
  const index = e.detail.value
  formData.order_id = orders.value[index].id
}

const onProductChange = (e) => {
  const index = e.detail.value
  formData.product_id = products.value[index].id
}

const onStatusChange = (e) => {
  const index = e.detail.value
  formData.status = statusOptions[index].value
}

const handleSubmit = async () => {
  if (!formData.order_id) {
    uni.showToast({ title: '请选择订单', icon: 'none' })
    return
  }
  if (!formData.product_id) {
    uni.showToast({ title: '请选择产品', icon: 'none' })
    return
  }
  if (!formData.amount || parseFloat(formData.amount) <= 0) {
    uni.showToast({ title: '请输入有效的金额', icon: 'none' })
    return
  }

  loading.value = true

  try {
    const data = {
      order_id: formData.order_id,
      product_id: formData.product_id,
      amount: parseFloat(formData.amount),
      status: formData.status
    }

    if (isEdit.value) {
      await updatePurchase(id.value, data)
      uni.showToast({ title: '修改成功', icon: 'success' })
    } else {
      await createPurchase(data)
      uni.showToast({ title: '创建成功', icon: 'success' })
    }

    setTimeout(() => {
      uni.navigateBack()
    }, 1500)
  } catch (error) {
    uni.showToast({ title: error.message || '操作失败', icon: 'none' })
  } finally {
    loading.value = false
  }
}
</script>

<style lang="scss" scoped>
.form-page {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 24rpx;
  padding-bottom: 160rpx;
}

.form-card {
  background-color: #fff;
  border-radius: 16rpx;
  padding: 24rpx;
}

.form-item {
  margin-bottom: 24rpx;

  .label {
    display: block;
    font-size: 28rpx;
    color: #333;
    margin-bottom: 12rpx;

    &.required::before {
      content: '*';
      color: #f5222d;
      margin-right: 8rpx;
    }
  }

  .input {
    width: 100%;
    height: 80rpx;
    padding: 0 24rpx;
    background-color: #f5f5f5;
    border-radius: 12rpx;
    font-size: 28rpx;
  }

  .picker-field {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 80rpx;
    padding: 0 24rpx;
    background-color: #f5f5f5;
    border-radius: 12rpx;
    font-size: 28rpx;

    .placeholder {
      color: #c0c4cc;
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
