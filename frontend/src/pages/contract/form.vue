<template>
  <view class="form-page">
    <view class="form-card">
      <view class="form-item">
        <text class="label required">合同编号</text>
        <input class="input" v-model="formData.code" placeholder="请输入合同编号" :disabled="isEdit" />
      </view>

      <view class="form-item">
        <text class="label required">合同名称</text>
        <input class="input" v-model="formData.name" placeholder="请输入合同名称" />
      </view>

      <view class="form-item">
        <text class="label required">关联工地</text>
        <picker mode="selector" :range="sites" range-key="name" @change="onSiteChange">
          <view class="picker-field">
            <text :class="{ placeholder: !formData.site_id }">{{ selectedSiteName || '请选择工地' }}</text>
            <u-icon name="arrow-down" color="#999" size="28rpx" />
          </view>
        </picker>
      </view>

      <view class="form-item">
        <text class="label required">厂家组</text>
        <picker mode="selector" :range="manufacturerGroups" range-key="name" @change="onGroupChange">
          <view class="picker-field">
            <text :class="{ placeholder: !formData.manufacturer_group_id }">{{ selectedGroupName || '请选择厂家组' }}</text>
            <u-icon name="arrow-down" color="#999" size="28rpx" />
          </view>
        </picker>
      </view>

      <view class="form-item">
        <text class="label required">负责人</text>
        <picker mode="selector" :range="users" range-key="name" @change="onAgentChange">
          <view class="picker-field">
            <text :class="{ placeholder: !formData.agent_id }">{{ selectedAgentName || '请选择负责人' }}</text>
            <u-icon name="arrow-down" color="#999" size="28rpx" />
          </view>
        </picker>
      </view>

      <view class="form-item">
        <text class="label">状态</text>
        <picker mode="selector" :range="statusOptions" range-key="label" @change="onStatusChange">
          <view class="picker-field">
            <text>{{ selectedStatusLabel || '请选择状态' }}</text>
            <u-icon name="arrow-down" color="#999" size="28rpx" />
          </view>
        </picker>
      </view>
    </view>

    <view class="action-bar">
      <u-button type="primary" :loading="loading" @click="handleSubmit">
        {{ isEdit ? '保存修改' : '创建合同' }}
      </u-button>
    </view>
  </view>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { getContract, createContract, updateContract } from '@/api/contract'
import { getSiteList } from '@/api/site'
import { getManufacturerGroupList } from '@/api/manufacturer'
import { getUserList } from '@/api/user'

const id = ref('')
const loading = ref(false)
const sites = ref([])
const manufacturerGroups = ref([])
const users = ref([])

const statusOptions = [
  { label: '草稿', value: '0' },
  { label: '生效', value: '1' },
  { label: '终止', value: '2' }
]

const formData = reactive({
  code: '',
  name: '',
  site_id: '',
  manufacturer_group_id: '',
  agent_id: '',
  status: '1'
})

const isEdit = computed(() => !!id.value)
const selectedSiteName = computed(() => sites.value.find(s => s.id === formData.site_id)?.name || '')
const selectedGroupName = computed(() => manufacturerGroups.value.find(g => g.id === formData.manufacturer_group_id)?.name || '')
const selectedAgentName = computed(() => users.value.find(u => u.id === formData.agent_id)?.name || '')
const selectedStatusLabel = computed(() => statusOptions.find(s => s.value === formData.status)?.label || '')

onMounted(() => {
  const pages = getCurrentPages()
  const currentPage = pages[pages.length - 1]
  id.value = currentPage.options.id || ''
  loadOptions()
  if (id.value) loadDetail()
})

const loadOptions = async () => {
  try {
    const [siteRes, groupRes, userRes] = await Promise.all([
      getSiteList({ page: 1, page_size: 100 }),
      getManufacturerGroupList({ page: 1, page_size: 100 }),
      getUserList({ page: 1, page_size: 100 })
    ])
    sites.value = siteRes.items || []
    manufacturerGroups.value = groupRes.items || []
    users.value = userRes.items || []
  } catch (error) {
    console.error('加载选项失败:', error)
  }
}

const loadDetail = async () => {
  try {
    const detail = await getContract(id.value)
    Object.assign(formData, {
      code: detail.code || '',
      name: detail.name || '',
      site_id: detail.site_id || '',
      manufacturer_group_id: detail.manufacturer_group_id || '',
      agent_id: detail.agent_id || '',
      status: detail.status || '1'
    })
  } catch (error) {
    uni.showToast({ title: '加载失败', icon: 'none' })
  }
}

const onSiteChange = (e) => { formData.site_id = sites.value[e.detail.value].id }
const onGroupChange = (e) => { formData.manufacturer_group_id = manufacturerGroups.value[e.detail.value].id }
const onAgentChange = (e) => { formData.agent_id = users.value[e.detail.value].id }
const onStatusChange = (e) => { formData.status = statusOptions[e.detail.value].value }

const handleSubmit = async () => {
  if (!formData.code) { uni.showToast({ title: '请输入合同编号', icon: 'none' }); return }
  if (!formData.name) { uni.showToast({ title: '请输入合同名称', icon: 'none' }); return }
  if (!formData.site_id) { uni.showToast({ title: '请选择工地', icon: 'none' }); return }
  if (!formData.manufacturer_group_id) { uni.showToast({ title: '请选择厂家组', icon: 'none' }); return }
  if (!formData.agent_id) { uni.showToast({ title: '请选择负责人', icon: 'none' }); return }

  loading.value = true
  try {
    if (isEdit.value) {
      await updateContract(id.value, formData)
      uni.showToast({ title: '修改成功', icon: 'success' })
    } else {
      await createContract(formData)
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
