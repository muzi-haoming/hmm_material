<template>
  <view class="detail-page">
    <view v-if="site" class="detail-content">
      <view class="card">
        <view class="card-title">基本信息</view>
        <view class="info-row">
          <text class="label">工地名称</text>
          <text class="value">{{ site.name }}</text>
        </view>
        <view class="info-row">
          <text class="label">工地编号</text>
          <text class="value">{{ site.code }}</text>
        </view>
        <view class="info-row">
          <text class="label">省份</text>
          <text class="value">{{ site.province }}</text>
        </view>
        <view class="info-row">
          <text class="label">城市</text>
          <text class="value">{{ site.city }}</text>
        </view>
        <view class="info-row">
          <text class="label">详细地址</text>
          <text class="value">{{ site.address }}</text>
        </view>
      </view>

      <view class="card">
        <view class="card-title">联系信息</view>
        <view class="info-row">
          <text class="label">联系人</text>
          <text class="value">{{ site.contact_name }}</text>
        </view>
        <view class="info-row">
          <text class="label">联系电话</text>
          <text class="value phone" @click="callPhone(site.contact_phone)">
            {{ site.contact_phone }}
          </text>
        </view>
      </view>

      <view v-if="site.description" class="card">
        <view class="card-title">描述</view>
        <text class="description">{{ site.description }}</text>
      </view>
    </view>

    <view class="action-bar">
      <u-button type="primary" @click="goEdit">编辑</u-button>
      <u-button type="error" @click="handleDelete">删除</u-button>
    </view>

    <u-loading-page :loading="loading" />
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getSite, deleteSite } from '@/api/site'

const site = ref(null)
const loading = ref(true)
const id = ref('')

onMounted(() => {
  const pages = getCurrentPages()
  const currentPage = pages[pages.length - 1]
  id.value = currentPage?.options?.id || ''

  if (id.value) {
    loadDetail()
  }
})

const loadDetail = async () => {
  loading.value = true
  try {
    site.value = await getSite(id.value)
  } catch (error) {
    uni.showToast({ title: '加载失败', icon: 'none' })
  } finally {
    loading.value = false
  }
}

const callPhone = (phone) => {
  uni.makePhoneCall({ phoneNumber: phone })
}

const goEdit = () => {
  uni.navigateTo({ url: `/pages/site/form?id=${id.value}` })
}

const handleDelete = () => {
  uni.showModal({
    title: '确认删除',
    content: '确定要删除该工地吗？',
    success: async (res) => {
      if (res.confirm) {
        try {
          await deleteSite(id.value)
          uni.showToast({ title: '删除成功', icon: 'success' })
          setTimeout(() => uni.navigateBack(), 1500)
        } catch (error) {
          uni.showToast({ title: '删除失败', icon: 'none' })
        }
      }
    }
  })
}
</script>

<style lang="scss" scoped>
.detail-page {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 24rpx;
  padding-bottom: 160rpx;
}

.card {
  background-color: #fff;
  border-radius: 16rpx;
  padding: 24rpx;
  margin-bottom: 24rpx;
}

.card-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
  padding-bottom: 16rpx;
  border-bottom: 1rpx solid #f0f0f0;
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

    &.phone {
      color: $primary-color;
    }
  }
}

.description {
  font-size: 28rpx;
  color: #666;
  line-height: 1.6;
}

.action-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  gap: 24rpx;
  padding: 24rpx;
  background-color: #fff;
  box-shadow: 0 -4rpx 12rpx rgba(0, 0, 0, 0.05);
}
</style>
