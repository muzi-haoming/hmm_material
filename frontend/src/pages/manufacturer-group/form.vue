<template>
  <view class="form-page">
    <view class="form-card">
      <view class="form-item">
        <text class="label required">编号</text>
        <input class="input" v-model="formData.code" placeholder="请输入编号" :disabled="isEdit" />
      </view>
      <view class="form-item">
        <text class="label required">名称</text>
        <input class="input" v-model="formData.name" placeholder="请输入名称" />
      </view>
    </view>

    <view class="form-card">
      <view class="section-header">
        <text class="section-title">选择厂家</text>
      </view>
      <view class="checkbox-list">
        <view v-for="mfr in manufacturers" :key="mfr.id" class="checkbox-item" @click="toggleManufacturer(mfr.id)">
          <view :class="['checkbox', { checked: formData.manufacturer_ids.includes(mfr.id) }]">
            <u-icon v-if="formData.manufacturer_ids.includes(mfr.id)" name="checkmark" color="#fff" size="24rpx" />
          </view>
          <text class="checkbox-label">{{ mfr.name }}</text>
        </view>
      </view>
    </view>

    <view class="action-bar">
      <u-button type="primary" :loading="loading" @click="handleSubmit">
        {{ isEdit ? '保存修改' : '创建厂家组' }}
      </u-button>
    </view>
  </view>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { getManufacturerGroup, createManufacturerGroup, updateManufacturerGroup, getManufacturerList } from '@/api/manufacturer'

const id = ref('')
const loading = ref(false)
const manufacturers = ref([])
const formData = reactive({ code: '', name: '', manufacturer_ids: [] })
const isEdit = computed(() => !!id.value)

onMounted(() => {
  const pages = getCurrentPages()
  const currentPage = pages[pages.length - 1]
  id.value = currentPage.options.id || ''
  loadManufacturers()
  if (id.value) loadDetail()
})

const loadManufacturers = async () => {
  try {
    const res = await getManufacturerList({ page: 1, page_size: 100 })
    manufacturers.value = res.items || []
  } catch (error) { console.error('加载厂家失败:', error) }
}

const loadDetail = async () => {
  try {
    const detail = await getManufacturerGroup(id.value)
    formData.code = detail.code || ''
    formData.name = detail.name || ''
    formData.manufacturer_ids = detail.manufacturers?.map(m => m.id) || []
  } catch (error) { uni.showToast({ title: '加载失败', icon: 'none' }) }
}

const toggleManufacturer = (mfrId) => {
  const index = formData.manufacturer_ids.indexOf(mfrId)
  if (index > -1) formData.manufacturer_ids.splice(index, 1)
  else formData.manufacturer_ids.push(mfrId)
}

const handleSubmit = async () => {
  if (!formData.code) { uni.showToast({ title: '请输入编号', icon: 'none' }); return }
  if (!formData.name) { uni.showToast({ title: '请输入名称', icon: 'none' }); return }

  loading.value = true
  try {
    if (isEdit.value) {
      await updateManufacturerGroup(id.value, formData)
      uni.showToast({ title: '修改成功', icon: 'success' })
    } else {
      await createManufacturerGroup(formData)
      uni.showToast({ title: '创建成功', icon: 'success' })
    }
    setTimeout(() => uni.navigateBack(), 1500)
  } catch (error) { uni.showToast({ title: error.message || '操作失败', icon: 'none' }) }
  finally { loading.value = false }
}
</script>

<style lang="scss" scoped>
.form-page { min-height: 100vh; background-color: #f5f5f5; padding: 24rpx; padding-bottom: 160rpx; }
.form-card { background-color: #fff; border-radius: 16rpx; padding: 24rpx; margin-bottom: 24rpx; }
.form-item {
  margin-bottom: 24rpx;
  .label { display: block; font-size: 28rpx; color: #333; margin-bottom: 12rpx; &.required::before { content: '*'; color: #f5222d; margin-right: 8rpx; } }
  .input { width: 100%; height: 80rpx; padding: 0 24rpx; background-color: #f5f5f5; border-radius: 12rpx; font-size: 28rpx; }
}
.section-header { margin-bottom: 16rpx; }
.section-title { font-size: 28rpx; font-weight: bold; color: #333; }
.checkbox-list { max-height: 600rpx; overflow-y: auto; }
.checkbox-item { display: flex; align-items: center; padding: 16rpx 0; border-bottom: 1rpx solid #f0f0f0;
  .checkbox { width: 40rpx; height: 40rpx; border: 2rpx solid #ddd; border-radius: 8rpx; display: flex; align-items: center; justify-content: center; margin-right: 16rpx;
    &.checked { background-color: #007AFF; border-color: #007AFF; }
  }
  .checkbox-label { font-size: 28rpx; color: #333; }
}
.action-bar { position: fixed; bottom: 0; left: 0; right: 0; padding: 24rpx; background-color: #fff; box-shadow: 0 -4rpx 12rpx rgba(0, 0, 0, 0.05); }
</style>
