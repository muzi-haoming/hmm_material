import { defineConfig } from 'vite'
import uni from '@dcloudio/vite-plugin-uni'
import path from 'path'

// uview-plus 需要的主题变量
const uviewThemeVars = `
$u-primary: #007AFF;
$u-success: #52c41a;
$u-warning: #faad14;
$u-error: #f5222d;
$u-info: #1890ff;
$u-main-color: #333333;
$u-content-color: #666666;
$u-tips-color: #999999;
$u-light-color: #c0c4cc;
$u-border-color: #e8e8e8;
$u-bg-color: #f5f5f5;
$u-disabled-color: #c8c9cc;
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
