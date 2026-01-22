<template>
  <view class="detail-page">
    <view v-if="item" class="detail-content">
      <view class="card">
        <view class="card-title">合同信息</view>
        <view class="info-row"><text class="label">合同名称</text><text class="value">{{ item.name }}</text></view>
        <view class="info-row"><text class="label">合同编号</text><text class="value">{{ item.contract_no }}</text></view>
        <view class="info-row"><text class="label">合同状态</text><view :class="['status-tag', `status-${item.status}`]">{{ getStatusText(item.status) }}</view></view>
        <view class="info-row"><text class="label">合同金额</text><text class="value price">¥{{ item.total_amount }}</text></view>
        <view class="info-row"><text class="label">开始日期</text><text class="value">{{ formatDate(item.start_date) }}</text></view>
        <view class="info-row"><text class="label">结束日期</text><text class="value">{{ formatDate(item.end_date) }}</text></view>
      </view>
      <view v-if="item.content" class="card">
        <view class="card-title">合同内容</view>
        <text class="content-text">{{ item.content }}</text>
      </view>
      <view v-if="item.manufacturer_relations && item.manufacturer_relations.length" class="card">
        <view class="card-title">关联厂家</view>
        <view v-for="mfr in item.manufacturer_relations" :key="mfr.id" class="mfr-item">
          <text>厂家ID: {{ mfr.manufacturer_id }}</text>
          <u-tag v-if="mfr.is_primary" text="主供应商" size="mini" type="primary" />
        </view>
      </view>
    </view>
    <u-loading-page :loading="loading" />
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getContract } from '@/api/contract'

const item = ref(null)
const loading = ref(true)

const getStatusText = (status) => {
  const map = { draft: '草稿', active: '生效中', completed: '已完成', cancelled: '已取消', expired: '已过期' }
  return map[status] || status
}
const formatDate = (dateStr) => dateStr ? dateStr.split('T')[0] : ''

onMounted(() => {
  const pages = getCurrentPages()
  const id = pages[pages.length - 1]?.options?.id
  if (id) loadDetail(id)
})

const loadDetail = async (id) => {
  loading.value = true
  try { item.value = await getContract(id) }
  catch (error) { uni.showToast({ title: '加载失败', icon: 'none' }) }
  finally { loading.value = false }
}
</script>

<style lang="scss" scoped>
.detail-page { min-height: 100vh; background-color: #f5f5f5; padding: 24rpx; }
.card { background-color: #fff; border-radius: 16rpx; padding: 24rpx; margin-bottom: 24rpx; }
.card-title { font-size: 30rpx; font-weight: bold; color: #333; margin-bottom: 20rpx; padding-bottom: 16rpx; border-bottom: 1rpx solid #f0f0f0; }
.info-row { display: flex; justify-content: space-between; align-items: center; padding: 16rpx 0; }
.label { font-size: 28rpx; color: #999; }
.value { font-size: 28rpx; color: #333; &.price { color: #f5222d; font-weight: bold; } }
.content-text { font-size: 28rpx; color: #666; line-height: 1.6; }
.mfr-item { display: flex; justify-content: space-between; align-items: center; padding: 16rpx 0; border-bottom: 1rpx solid #f0f0f0; &:last-child { border-bottom: none; } }
</style>
