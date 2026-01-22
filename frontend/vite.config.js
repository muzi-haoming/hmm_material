import { defineConfig } from 'vite'
import uni from '@dcloudio/vite-plugin-uni'
import path from 'path'

// uview-plus 需要的主题变量（完整版）
const uviewThemeVars = `
$u-primary: #3c9cff;
$u-primary-dark: #398ade;
$u-primary-disabled: #9acafc;
$u-primary-light: #ecf5ff;
$u-warning: #f9ae3d;
$u-warning-dark: #f1a532;
$u-warning-disabled: #f9d39b;
$u-warning-light: #fdf6ec;
$u-success: #5ac725;
$u-success-dark: #53b81f;
$u-success-disabled: #a9de8e;
$u-success-light: #f5fff0;
$u-error: #f56c6c;
$u-error-dark: #e45656;
$u-error-disabled: #f9b4b4;
$u-error-light: #fef0f0;
$u-info: #909399;
$u-info-dark: #82848a;
$u-info-disabled: #c8c9cc;
$u-info-light: #f4f4f5;
$u-main-color: #303133;
$u-content-color: #606266;
$u-tips-color: #909193;
$u-light-color: #c0c4cc;
$u-border-color: #e4e7ed;
$u-bg-color: #f3f4f6;
$u-disabled-color: #c8c9cc;
$u-form-item-height: 70rpx;
$u-form-item-border-color: #dcdfe6;
`

export default defineConfig({
  plugins: [uni()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src')
    }
  },
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: uviewThemeVars,
        api: 'modern-compiler',
        silenceDeprecations: ['legacy-js-api', 'import', 'global-builtin']
      }
    }
  }
})
