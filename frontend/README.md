# HMM Material - Frontend

物资管理系统前端应用

## 技术栈

- **框架**: Uni-app 3.0+ (跨平台)
- **UI**: Vue 3.4 + uview-plus 3.2
- **状态管理**: Pinia 2.1
- **构建工具**: Vite 5.0
- **样式**: Sass/SCSS

## 支持平台

- H5 网页
- 微信小程序
- 原生 App (Android/iOS)

## 目录结构

```
frontend/
├── pages/              # 页面组件
│   ├── login/          # 登录页
│   ├── index/          # 首页
│   ├── order/          # 订单管理
│   ├── site/           # 工地管理
│   ├── manufacturer/   # 厂家管理
│   ├── contract/       # 合同管理
│   ├── delegation/     # 委托管理
│   └── user/           # 用户中心
├── store/              # Pinia 状态管理
├── api/                # API 调用
├── utils/              # 工具函数
├── static/             # 静态资源
├── pages.json          # 路由配置
├── manifest.json       # 应用配置
├── package.json
└── README.md
```

## 环境要求

- Node.js >= 18.0
- npm >= 8.0

## 快速启动

### 方式一：使用启动脚本（推荐）

```bash
# 在项目根目录执行
./scripts/start-frontend.sh
```

### 方式二：手动启动

```bash
# 1. 安装依赖（首次或依赖更新后）
npm install

# 2. 启动开发服务器
npm run dev:h5
```

## 日常开发启动

```bash
npm run dev:h5
```

## 开发命令

| 命令 | 说明 |
|------|------|
| `npm run dev:h5` | H5 网页开发模式 |
| `npm run dev:mp-weixin` | 微信小程序开发模式 |
| `npm run dev:app` | 原生 App 开发模式 |

## 构建命令

| 命令 | 说明 | 输出目录 |
|------|------|---------|
| `npm run build:h5` | H5 生产构建 | `dist/build/h5` |
| `npm run build:mp-weixin` | 微信小程序构建 | `dist/build/mp-weixin` |
| `npm run build:app` | 原生 App 构建 | `dist/build/app` |

## 服务地址

| 环境 | 地址 |
|------|------|
| 开发环境 | http://localhost:5173 |
| 后端 API | http://localhost:8000/api/v1 |

## API 配置

编辑 `utils/request.js` 中的 `baseURL`：

```javascript
// 开发环境
const baseURL = 'http://localhost:8000/api/v1'

// 生产环境
const baseURL = '/api/v1'
```

## 页面路由

| 页面 | 路径 | 说明 |
|------|------|------|
| 首页 | `/pages/index/index` | 仪表盘 |
| 登录 | `/pages/login/login` | 用户登录 |
| 订单列表 | `/pages/order/list` | 订单管理 |
| 订单详情 | `/pages/order/detail` | 订单详情 |
| 工地列表 | `/pages/site/list` | 工地管理 |
| 厂家列表 | `/pages/manufacturer/list` | 厂家管理 |
| 合同列表 | `/pages/contract/list` | 合同管理 |
| 委托列表 | `/pages/delegation/list` | 委托管理 |
| 个人中心 | `/pages/user/profile` | 用户信息 |

## 微信小程序开发

1. 运行 `npm run dev:mp-weixin`
2. 打开微信开发者工具
3. 导入 `dist/dev/mp-weixin` 目录
4. 配置 AppID

## 注意事项

- 开发前确保后端服务已启动
- 微信小程序需要配置合法域名
- 生产环境需修改 API 地址
