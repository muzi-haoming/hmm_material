<template>
  <view class="form-page">
    <view class="form-card">
      <view class="form-item">
        <text class="label required">用户名</text>
        <input class="input" v-model="formData.username" placeholder="请输入用户名" :disabled="isEdit" />
      </view>

      <view class="form-item">
        <text class="label required">姓名</text>
        <input class="input" v-model="formData.name" placeholder="请输入姓名" />
      </view>

      <view class="form-item" v-if="!isEdit">
        <text class="label required">密码</text>
        <input class="input" v-model="formData.password" type="password" placeholder="请输入密码" />
      </view>

      <view class="form-item">
        <text class="label required">角色</text>
        <picker mode="selector" :range="roles" range-key="name" @change="onRoleChange">
          <view class="picker-field">
            <text :class="{ placeholder: !formData.role_id }">{{ selectedRoleName || '请选择角色' }}</text>
            <u-icon name="arrow-down" color="#999" size="28rpx" />
          </view>
        </picker>
      </view>
    </view>

    <view class="action-bar">
      <u-button type="primary" :loading="loading" @click="handleSubmit">
        {{ isEdit ? '保存修改' : '创建用户' }}
      </u-button>
    </view>
  </view>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { getUser, createUser, updateUser, getRoleList } from '@/api/user'

const id = ref('')
const loading = ref(false)
const roles = ref([])

const formData = reactive({
  username: '',
  name: '',
  password: '',
  role_id: ''
})

const isEdit = computed(() => !!id.value)
const selectedRoleName = computed(() => roles.value.find(r => r.id === formData.role_id)?.name || '')

onMounted(() => {
  const pages = getCurrentPages()
  const currentPage = pages[pages.length - 1]
  id.value = currentPage.options.id || ''
  loadRoles()
  if (id.value) loadDetail()
})

const loadRoles = async () => {
  try {
    const res = await getRoleList()
    roles.value = res || []
  } catch (error) {
    console.error('加载角色失败:', error)
  }
}

const loadDetail = async () => {
  try {
    const detail = await getUser(id.value)
    formData.username = detail.username || ''
    formData.name = detail.name || ''
    formData.role_id = detail.role_id || ''
  } catch (error) {
    uni.showToast({ title: '加载失败', icon: 'none' })
  }
}

const onRoleChange = (e) => {
  formData.role_id = roles.value[e.detail.value].id
}

const handleSubmit = async () => {
  if (!formData.username) { uni.showToast({ title: '请输入用户名', icon: 'none' }); return }
  if (!formData.name) { uni.showToast({ title: '请输入姓名', icon: 'none' }); return }
  if (!isEdit.value && !formData.password) { uni.showToast({ title: '请输入密码', icon: 'none' }); return }
  if (!formData.role_id) { uni.showToast({ title: '请选择角色', icon: 'none' }); return }

  loading.value = true
  try {
    const submitData = {
      username: formData.username,
      name: formData.name,
      role_id: formData.role_id
    }
    if (!isEdit.value) {
      submitData.password = formData.password
    }

    if (isEdit.value) {
      await updateUser(id.value, submitData)
      uni.showToast({ title: '修改成功', icon: 'success' })
    } else {
      await createUser(submitData)
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
