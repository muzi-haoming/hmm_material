<template>
  <view class="detail-page">
    <view v-if="item" class="detail-content">
      <view class="status-section">
        <view :class="['status-icon', `status-${item.status}`]">
          <u-icon :name="item.type === 'supply' ? 'share' : 'setting'" size="48rpx" color="#fff" />
        </view>
        <text class="type-text">{{ item.type === 'supply' ? '委托供货' : '委托加工' }}</text>
        <text class="status-text">{{ getStatusText(item.status) }}</text>
      </view>

      <view class="card">
        <view class="card-title">委托信息</view>
        <view class="info-row"><text class="label">委托函编号</text><text class="value">{{ item.delegation_no }}</text></view>
        <view class="info-row"><text class="label">委托金额</text><text class="value price">¥{{ item.amount }}</text></view>
        <view class="info-row"><text class="label">委托日期</text><text class="value">{{ formatDate(item.delegation_date) }}</text></view>
        <view v-if="item.expected_completion_date" class="info-row"><text class="label">预计完成</text><text class="value">{{ formatDate(item.expected_completion_date) }}</text></view>
      </view>

      <view class="card">
        <view class="card-title">委托内容</view>
        <text class="content-text">{{ item.content }}</text>
      </view>

      <view v-if="item.raw_material_info" class="card">
        <view class="card-title">原材料信息</view>
        <text class="content-text">{{ item.raw_material_info }}</text>
      </view>

      <view v-if="item.remark" class="card">
        <view class="card-title">备注</view>
        <text class="content-text">{{ item.remark }}</text>
      </view>
    </view>

    <view class="action-bar" v-if="item && item.status === 'pending'">
      <u-button type="default" @click="handleReject">拒绝</u-button>
      <u-button type="primary" @click="handleAccept">接受委托</u-button>
    </view>

    <u-loading-page :loading="loading" />
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getDelegation, acceptDelegation, rejectDelegation } from '@/api/delegation'

const item = ref(null)
const loading = ref(true)
const delegationId = ref(null)

const getStatusText = (status) => {
  const map = { draft: '草稿', pending: '待确认', accepted: '已接受', in_progress: '执行中', completed: '已完成', rejected: '已拒绝', cancelled: '已取消' }
  return map[status] || status
}
const formatDate = (dateStr) => dateStr ? dateStr.split('T')[0] + ' ' + (dateStr.split('T')[1]?.substring(0, 5) || '') : ''

onMounted(() => {
  const pages = getCurrentPages()
  delegationId.value = pages[pages.length - 1]?.options?.id
  if (delegationId.value) loadDetail()
})

const loadDetail = async () => {
  loading.value = true
  try { item.value = await getDelegation(delegationId.value) }
  catch (error) { uni.showToast({ title: '加载失败', icon: 'none' }) }
  finally { loading.value = false }
}

const handleAccept = async () => {
  try {
    await acceptDelegation(delegationId.value)
    uni.showToast({ title: '已接受', icon: 'success' })
    loadDetail()
  } catch (error) { uni.showToast({ title: error.message || '操作失败', icon: 'none' }) }
}

const handleReject = async () => {
  uni.showModal({
    title: '确认拒绝',
    content: '确定要拒绝此委托吗？',
    success: async (res) => {
      if (res.confirm) {
        try {
          await rejectDelegation(delegationId.value)
          uni.showToast({ title: '已拒绝', icon: 'success' })
          loadDetail()
        } catch (error) { uni.showToast({ title: error.message || '操作失败', icon: 'none' }) }
      }
    }
  })
}
</script>

<style lang="scss" scoped>
.detail-page { min-height: 100vh; background-color: #f5f5f5; padding-bottom: 140rpx; }
.status-section { background: linear-gradient(135deg, #722ed1 0%, #531dab 100%); padding: 48rpx; display: flex; flex-direction: column; align-items: center; }
.status-icon { width: 96rpx; height: 96rpx; border-radius: 50%; background-color: rgba(255, 255, 255, 0.2); display: flex; align-items: center; justify-content: center; }
.type-text { margin-top: 16rpx; font-size: 32rpx; font-weight: bold; color: #fff; }
.status-text { margin-top: 8rpx; font-size: 28rpx; color: rgba(255, 255, 255, 0.8); }
.card { margin: 24rpx; background-color: #fff; border-radius: 16rpx; padding: 24rpx; }
.card-title { font-size: 30rpx; font-weight: bold; color: #333; margin-bottom: 20rpx; padding-bottom: 16rpx; border-bottom: 1rpx solid #f0f0f0; }
.info-row { display: flex; justify-content: space-between; padding: 16rpx 0; }
.label { font-size: 28rpx; color: #999; }
.value { font-size: 28rpx; color: #333; &.price { color: #f5222d; font-weight: bold; } }
.content-text { font-size: 28rpx; color: #666; line-height: 1.6; }
.action-bar { position: fixed; bottom: 0; left: 0; right: 0; background-color: #fff; padding: 24rpx 32rpx; padding-bottom: calc(24rpx + env(safe-area-inset-bottom)); display: flex; gap: 24rpx; box-shadow: 0 -4rpx 16rpx rgba(0, 0, 0, 0.05); }
</style>
