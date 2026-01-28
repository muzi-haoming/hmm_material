<template>
  <view class="page-container">
    <view class="page-header">
      <text class="page-title">业务管理</text>
      <text class="page-subtitle">管理订单、采购、库存等业务数据</text>
    </view>

    <view class="menu-section">
      <view class="menu-group">
        <view class="group-title">订单与采购</view>
        <view class="menu-list">
          <view class="menu-item" @click="navigateTo('/pages/order/list')">
            <view class="menu-icon" style="background-color: #e6f7ff;">
              <u-icon name="list" color="#1890ff" size="40rpx" />
            </view>
            <view class="menu-content">
              <text class="menu-name">订单管理</text>
              <text class="menu-desc">查看和管理所有订单</text>
            </view>
            <u-icon name="arrow-right" color="#999" size="28rpx" />
          </view>

          <view class="menu-item" @click="navigateTo('/pages/purchase/list')">
            <view class="menu-icon" style="background-color: #fff7e6;">
              <u-icon name="shopping-cart" color="#fa8c16" size="40rpx" />
            </view>
            <view class="menu-content">
              <text class="menu-name">采购单管理</text>
              <text class="menu-desc">管理采购订单和付款</text>
            </view>
            <u-icon name="arrow-right" color="#999" size="28rpx" />
          </view>

          <view class="menu-item" @click="navigateTo('/pages/statement/list')">
            <view class="menu-icon" style="background-color: #f6ffed;">
              <u-icon name="file-text" color="#52c41a" size="40rpx" />
            </view>
            <view class="menu-content">
              <text class="menu-name">对账单管理</text>
              <text class="menu-desc">财务对账和结算</text>
            </view>
            <u-icon name="arrow-right" color="#999" size="28rpx" />
          </view>
        </view>
      </view>

      <view class="menu-group">
        <view class="group-title">库存管理</view>
        <view class="menu-list">
          <view class="menu-item" @click="navigateTo('/pages/stock/list')">
            <view class="menu-icon" style="background-color: #f9f0ff;">
              <u-icon name="bag" color="#722ed1" size="40rpx" />
            </view>
            <view class="menu-content">
              <text class="menu-name">库存查询</text>
              <text class="menu-desc">查看当前库存情况</text>
            </view>
            <u-icon name="arrow-right" color="#999" size="28rpx" />
          </view>

          <view class="menu-item" @click="navigateTo('/pages/stock-in/list')">
            <view class="menu-icon" style="background-color: #e6fffb;">
              <u-icon name="plus-circle" color="#13c2c2" size="40rpx" />
            </view>
            <view class="menu-content">
              <text class="menu-name">入库管理</text>
              <text class="menu-desc">管理物料入库记录</text>
            </view>
            <u-icon name="arrow-right" color="#999" size="28rpx" />
          </view>

          <view class="menu-item" @click="navigateTo('/pages/stock-out/list')">
            <view class="menu-icon" style="background-color: #fff1f0;">
              <u-icon name="minus-circle" color="#f5222d" size="40rpx" />
            </view>
            <view class="menu-content">
              <text class="menu-name">出库管理</text>
              <text class="menu-desc">管理物料出库记录</text>
            </view>
            <u-icon name="arrow-right" color="#999" size="28rpx" />
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
const navigateTo = (url) => {
  uni.navigateTo({ url })
}
</script>

<style lang="scss" scoped>
.page-container {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding-bottom: 120rpx;
}

.page-header {
  background: linear-gradient(135deg, #1890ff 0%, #096dd9 100%);
  padding: 48rpx 32rpx;

  .page-title {
    display: block;
    font-size: 40rpx;
    font-weight: bold;
    color: #fff;
    margin-bottom: 12rpx;
  }

  .page-subtitle {
    font-size: 26rpx;
    color: rgba(255, 255, 255, 0.8);
  }
}

.menu-section {
  padding: 24rpx;
}

.menu-group {
  margin-bottom: 24rpx;

  .group-title {
    font-size: 28rpx;
    font-weight: 500;
    color: #666;
    padding: 16rpx 8rpx;
  }
}

.menu-list {
  background-color: #fff;
  border-radius: 16rpx;
  overflow: hidden;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 28rpx 24rpx;
  border-bottom: 1rpx solid #f0f0f0;

  &:last-child {
    border-bottom: none;
  }

  &:active {
    background-color: #f5f5f5;
  }
}

.menu-icon {
  width: 80rpx;
  height: 80rpx;
  border-radius: 16rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 24rpx;
}

.menu-content {
  flex: 1;

  .menu-name {
    display: block;
    font-size: 30rpx;
    color: #333;
    margin-bottom: 8rpx;
  }

  .menu-desc {
    font-size: 24rpx;
    color: #999;
  }
}
</style>
