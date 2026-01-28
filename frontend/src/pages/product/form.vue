<template>
  <view class="form-page">
    <view class="form-card">
      <view class="form-item">
        <text class="label required">产品编号</text>
        <input
          class="input"
          v-model="formData.code"
          placeholder="请输入产品编号"
          :disabled="isEdit"
        />
      </view>

      <view class="form-item">
        <text class="label required">产品名称</text>
        <input
          class="input"
          v-model="formData.name"
          placeholder="请输入产品名称"
        />
      </view>

      <view class="form-item">
        <text class="label">规格型号</text>
        <input
          class="input"
          v-model="formData.spec"
          placeholder="请输入规格型号"
        />
      </view>

      <view class="form-item">
        <text class="label">计量单位</text>
        <input
          class="input"
          v-model="formData.unit"
          placeholder="请输入计量单位"
        />
      </view>
    </view>

    <view class="action-bar">
      <u-button type="primary" :loading="loading" @click="handleSubmit">
        {{ isEdit ? '保存修改' : '创建产品' }}
      </u-button>
    </view>
  </view>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { getProduct, createProduct, updateProduct } from '@/api/product'

const id = ref('')
const loading = ref(false)

const formData = reactive({
  code: '',
  name: '',
  spec: '',
  unit: ''
})

const isEdit = computed(() => !!id.value)

onMounted(() => {
  const pages = getCurrentPages()
  const currentPage = pages[pages.length - 1]
  id.value = currentPage.options.id || ''

  if (id.value) {
    loadDetail()
  }
})

const loadDetail = async () => {
  try {
    const detail = await getProduct(id.value)
    Object.assign(formData, {
      code: detail.code,
      name: detail.name,
      spec: detail.spec || '',
      unit: detail.unit || ''
    })
  } catch (error) {
    uni.showToast({ title: '加载失败', icon: 'none' })
  }
}

const handleSubmit = async () => {
  if (!formData.code) {
    uni.showToast({ title: '请输入产品编号', icon: 'none' })
    return
  }
  if (!formData.name) {
    uni.showToast({ title: '请输入产品名称', icon: 'none' })
    return
  }

  loading.value = true

  try {
    if (isEdit.value) {
      await updateProduct(id.value, formData)
      uni.showToast({ title: '修改成功', icon: 'success' })
    } else {
      await createProduct(formData)
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
