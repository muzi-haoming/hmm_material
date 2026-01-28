<template>
  <view class="form-page">
    <view class="form-card">
      <view class="form-item">
        <text class="label required">对账单号</text>
        <input class="input" v-model="formData.code" placeholder="请输入对账单号" :disabled="isEdit" />
      </view>

      <view class="form-item">
        <text class="label required">对账周期</text>
        <input class="input" v-model="formData.period" placeholder="如: 2024年1月" />
      </view>

      <view class="form-item">
        <text class="label required">总金额</text>
        <input class="input" v-model="formData.total_amount" type="digit" placeholder="请输入总金额" />
      </view>

      <view class="form-item">
        <text class="label required">状态</text>
        <picker mode="selector" :range="statusOptions" range-key="label" @change="onStatusChange">
          <view class="picker-field">
            <text :class="{ placeholder: !formData.status }">{{ selectedStatusLabel || '请选择状态' }}</text>
            <u-icon name="arrow-down" color="#999" size="28rpx" />
          </view>
        </picker>
      </view>
    </view>

    <view class="action-bar">
      <u-button type="primary" :loading="loading" @click="handleSubmit">
        {{ isEdit ? '保存修改' : '创建对账单' }}
      </u-button>
    </view>
  </view>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { getStatement, createStatement, updateStatement } from '@/api/statement'

const id = ref('')
const loading = ref(false)

const statusOptions = [
  { label: '待确认', value: '1' },
  { label: '已确认', value: '2' },
  { label: '已结算', value: '3' }
]

const formData = reactive({ code: '', period: '', total_amount: '', status: '1' })

const isEdit = computed(() => !!id.value)
const selectedStatusLabel = computed(() => statusOptions.find(s => s.value === formData.status)?.label || '')

onMounted(() => {
  const pages = getCurrentPages()
  const currentPage = pages[pages.length - 1]
  id.value = currentPage.options.id || ''
  if (id.value) loadDetail()
})

const loadDetail = async () => {
  try {
    const detail = await getStatement(id.value)
    Object.assign(formData, {
      code: detail.code || '',
      period: detail.period || '',
      total_amount: detail.total_amount?.toString() || '',
      status: detail.status || '1'
    })
  } catch (error) {
    uni.showToast({ title: '加载失败', icon: 'none' })
  }
}

const onStatusChange = (e) => {
  formData.status = statusOptions[e.detail.value].value
}

const handleSubmit = async () => {
  if (!formData.code) { uni.showToast({ title: '请输入对账单号', icon: 'none' }); return }
  if (!formData.period) { uni.showToast({ title: '请输入对账周期', icon: 'none' }); return }
  if (!formData.total_amount) { uni.showToast({ title: '请输入总金额', icon: 'none' }); return }

  loading.value = true
  try {
    const data = { ...formData, total_amount: parseFloat(formData.total_amount) }
    if (isEdit.value) {
      await updateStatement(id.value, data)
      uni.showToast({ title: '修改成功', icon: 'success' })
    } else {
      await createStatement(data)
      uni.showToast({ title: '创建成功', icon: 'success' })
    }
    setTimeout(() => uni.navigateBack(), 1500)
  } catch (error) {
    uni.showToast({ title: error.message || '操作失败', icon: 'none' })
  } finally {
    loading.value = false
  }
}
</script>

<style lang="scss" scoped>
.form-page { min-height: 100vh; background-color: #f5f5f5; padding: 24rpx; padding-bottom: 160rpx; }
.form-card { background-color: #fff; border-radius: 16rpx; padding: 24rpx; }
.form-item {
  margin-bottom: 24rpx;
  .label { display: block; font-size: 28rpx; color: #333; margin-bottom: 12rpx; &.required::before { content: '*'; color: #f5222d; margin-right: 8rpx; } }
  .input { width: 100%; height: 80rpx; padding: 0 24rpx; background-color: #f5f5f5; border-radius: 12rpx; font-size: 28rpx; }
  .picker-field { display: flex; align-items: center; justify-content: space-between; height: 80rpx; padding: 0 24rpx; background-color: #f5f5f5; border-radius: 12rpx; font-size: 28rpx; .placeholder { color: #c0c4cc; } }
}
.action-bar { position: fixed; bottom: 0; left: 0; right: 0; padding: 24rpx; background-color: #fff; box-shadow: 0 -4rpx 12rpx rgba(0, 0, 0, 0.05); }
</style>
