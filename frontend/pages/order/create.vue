<template>
  <view class="create-order-page">
    <u-form :model="formData" ref="formRef">
      <!-- 选择合同 -->
      <view class="section">
        <view class="section-title">选择合同</view>
        <u-form-item prop="contract_id">
          <u-input
            v-model="contractName"
            placeholder="请选择合同"
            :disabled="true"
            @click="showContractPicker = true"
            suffixIcon="arrow-right"
          />
        </u-form-item>
      </view>

      <!-- 选择厂家 -->
      <view class="section">
        <view class="section-title">选择厂家</view>
        <u-form-item prop="manufacturer_id">
          <u-input
            v-model="manufacturerName"
            placeholder="请选择厂家"
            :disabled="true"
            @click="showManufacturerPicker = true"
            suffixIcon="arrow-right"
          />
        </u-form-item>
      </view>

      <!-- 商品列表 -->
      <view class="section">
        <view class="section-header">
          <text class="section-title">商品明细</text>
          <text class="add-btn" @click="addItem">+ 添加商品</text>
        </view>

        <view
          v-for="(item, index) in formData.items"
          :key="index"
          class="item-card"
        >
          <view class="item-header">
            <text class="item-title">商品 {{ index + 1 }}</text>
            <u-icon name="trash" size="36rpx" color="#f5222d" @click="removeItem(index)" />
          </view>

          <u-form-item label="产品ID" :prop="`items[${index}].product_id`">
            <u-input
              v-model.number="item.product_id"
              type="number"
              placeholder="请输入产品ID"
            />
          </u-form-item>

          <u-form-item label="数量" :prop="`items[${index}].quantity`">
            <u-input
              v-model.number="item.quantity"
              type="digit"
              placeholder="请输入数量"
            />
          </u-form-item>

          <u-form-item label="单价" :prop="`items[${index}].unit_price`">
            <u-input
              v-model.number="item.unit_price"
              type="digit"
              placeholder="请输入单价"
            />
          </u-form-item>

          <u-form-item label="规格说明">
            <u-input v-model="item.specification" placeholder="选填" />
          </u-form-item>
        </view>
      </view>

      <!-- 收货信息 -->
      <view class="section">
        <view class="section-title">收货信息</view>

        <u-form-item label="收货地址" prop="delivery_address">
          <u-input v-model="formData.delivery_address" placeholder="请输入收货地址" />
        </u-form-item>

        <u-form-item label="联系人" prop="delivery_contact">
          <u-input v-model="formData.delivery_contact" placeholder="请输入联系人" />
        </u-form-item>

        <u-form-item label="联系电话" prop="delivery_phone">
          <u-input v-model="formData.delivery_phone" placeholder="请输入联系电话" />
        </u-form-item>

        <u-form-item label="备注">
          <u-textarea v-model="formData.remark" placeholder="选填" />
        </u-form-item>
      </view>
    </u-form>

    <!-- 提交按钮 -->
    <view class="submit-bar">
      <view class="total">
        <text class="label">合计：</text>
        <text class="amount">¥{{ totalAmount }}</text>
      </view>
      <u-button type="primary" :loading="submitting" @click="handleSubmit">
        提交订单
      </u-button>
    </view>

    <!-- 合同选择器 -->
    <u-picker
      :show="showContractPicker"
      :columns="contractColumns"
      @confirm="onContractSelect"
      @cancel="showContractPicker = false"
    />

    <!-- 厂家选择器 -->
    <u-picker
      :show="showManufacturerPicker"
      :columns="manufacturerColumns"
      @confirm="onManufacturerSelect"
      @cancel="showManufacturerPicker = false"
    />
  </view>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { getContractList } from '@/api/contract'
import { getManufacturerList } from '@/api/manufacturer'
import { createOrder } from '@/api/order'

const formRef = ref(null)
const submitting = ref(false)

const formData = reactive({
  contract_id: null,
  manufacturer_id: null,
  order_type: 'direct',
  delivery_address: '',
  delivery_contact: '',
  delivery_phone: '',
  remark: '',
  items: [
    { product_id: null, quantity: 1, unit_price: 0, specification: '' }
  ]
})

// 选择器
const showContractPicker = ref(false)
const showManufacturerPicker = ref(false)
const contractColumns = ref([])
const manufacturerColumns = ref([])
const contractName = ref('')
const manufacturerName = ref('')

// 原始数据
const contracts = ref([])
const manufacturers = ref([])

// 计算总金额
const totalAmount = computed(() => {
  return formData.items.reduce((sum, item) => {
    return sum + (item.quantity || 0) * (item.unit_price || 0)
  }, 0).toFixed(2)
})

onMounted(() => {
  loadContracts()
  loadManufacturers()
})

const loadContracts = async () => {
  try {
    const res = await getContractList({ page: 1, page_size: 100, status: 'active' })
    contracts.value = res.items || []
    contractColumns.value = [
      contracts.value.map(c => ({ label: c.name, value: c.id }))
    ]
  } catch (error) {
    console.error('加载合同失败:', error)
  }
}

const loadManufacturers = async () => {
  try {
    const res = await getManufacturerList({ page: 1, page_size: 100 })
    manufacturers.value = res.items || []
    manufacturerColumns.value = [
      manufacturers.value.map(m => ({ label: m.name, value: m.id }))
    ]
  } catch (error) {
    console.error('加载厂家失败:', error)
  }
}

const onContractSelect = (e) => {
  const selected = e.value[0]
  formData.contract_id = selected.value
  contractName.value = selected.label
  showContractPicker.value = false
}

const onManufacturerSelect = (e) => {
  const selected = e.value[0]
  formData.manufacturer_id = selected.value
  manufacturerName.value = selected.label
  showManufacturerPicker.value = false
}

const addItem = () => {
  formData.items.push({
    product_id: null,
    quantity: 1,
    unit_price: 0,
    specification: ''
  })
}

const removeItem = (index) => {
  if (formData.items.length > 1) {
    formData.items.splice(index, 1)
  } else {
    uni.showToast({ title: '至少保留一个商品', icon: 'none' })
  }
}

const handleSubmit = async () => {
  // 验证
  if (!formData.contract_id) {
    uni.showToast({ title: '请选择合同', icon: 'none' })
    return
  }
  if (!formData.manufacturer_id) {
    uni.showToast({ title: '请选择厂家', icon: 'none' })
    return
  }
  if (!formData.delivery_address || !formData.delivery_contact || !formData.delivery_phone) {
    uni.showToast({ title: '请填写完整收货信息', icon: 'none' })
    return
  }

  const hasValidItem = formData.items.some(
    item => item.product_id && item.quantity > 0 && item.unit_price > 0
  )
  if (!hasValidItem) {
    uni.showToast({ title: '请添加有效的商品', icon: 'none' })
    return
  }

  submitting.value = true

  try {
    await createOrder({
      ...formData,
      items: formData.items.filter(item => item.product_id)
    })
    uni.showToast({ title: '创建成功', icon: 'success' })
    setTimeout(() => {
      uni.navigateBack()
    }, 1500)
  } catch (error) {
    uni.showToast({ title: error.message || '创建失败', icon: 'none' })
  } finally {
    submitting.value = false
  }
}
</script>

<style lang="scss" scoped>
.create-order-page {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding-bottom: 180rpx;
}

.section {
  margin: 24rpx;
  background-color: #fff;
  border-radius: 16rpx;
  padding: 24rpx;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16rpx;
}

.section-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 16rpx;
}

.add-btn {
  font-size: 28rpx;
  color: $primary-color;
}

.item-card {
  background-color: #f9f9f9;
  border-radius: 12rpx;
  padding: 20rpx;
  margin-bottom: 20rpx;

  .item-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16rpx;

    .item-title {
      font-size: 28rpx;
      font-weight: bold;
      color: #333;
    }
  }
}

.submit-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: #fff;
  padding: 24rpx 32rpx;
  padding-bottom: calc(24rpx + env(safe-area-inset-bottom));
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 -4rpx 16rpx rgba(0, 0, 0, 0.05);

  .total {
    .label {
      font-size: 28rpx;
      color: #666;
    }

    .amount {
      font-size: 40rpx;
      font-weight: bold;
      color: #f5222d;
    }
  }
}
</style>
