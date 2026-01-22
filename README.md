# HMM Material Management System

物资供应链管理系统 - 建筑材料采购与供应链优化平台

## 项目简介

HMM Material 是一个全栈物资管理系统，专为建筑行业材料采购设计，支持：

- 工地管理与合同管理
- 厂家/供应商管理
- 订单管理（直接发货/委托供货/委托加工）
- AI 智能供应链分析与优化建议

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | FastAPI + SQLAlchemy + PostgreSQL |
| 前端 | Uni-app + Vue 3 + Pinia |
| AI | LangChain + OpenAI GPT-4 |

## 项目结构

```
hmm_material/
├── backend/                 # 后端 (Python FastAPI)
│   ├── app/
│   │   ├── main.py         # 入口文件
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据库模型
│   │   ├── schemas/        # Pydantic 验证
│   │   ├── api/            # API 路由
│   │   ├── services/       # 业务逻辑
│   │   └── ai/             # AI 集成
│   ├── requirements.txt
│   └── .env.example
├── frontend/                # 前端 (Uni-app)
│   ├── src/                # 源码目录
│   │   ├── pages/          # 页面组件
│   │   ├── store/          # 状态管理
│   │   ├── api/            # API 调用
│   │   └── utils/          # 工具函数
│   ├── vite.config.js
│   └── package.json
├── scripts/                 # 启动脚本
└── README.md
```

## 环境要求

| 依赖 | 版本要求 |
|------|---------|
| Python | >= 3.10 |
| Node.js | >= 18.0 |
| PostgreSQL | >= 14.0 |
| npm | >= 8.0 |

## 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd hmm_material
```

### 2. 后端启动

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，配置数据库连接等

# 创建数据库
createdb hmm_material

# 运行数据库迁移
alembic upgrade head

# 启动开发服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端启动后：
- API 地址: http://localhost:8000
- Swagger 文档: http://localhost:8000/docs
- ReDoc 文档: http://localhost:8000/redoc

### 3. 前端启动

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动 H5 开发服务器
npm run dev:h5
```

前端启动后访问: http://localhost:5173

### 4. 前端构建命令

| 命令 | 说明 |
|------|------|
| `npm run dev:h5` | H5 网页开发模式 |
| `npm run build:h5` | H5 网页生产构建 |
| `npm run dev:mp-weixin` | 微信小程序开发模式 |
| `npm run build:mp-weixin` | 微信小程序生产构建 |
| `npm run dev:app` | 原生 App 开发模式 |
| `npm run build:app` | 原生 App 生产构建 |

## 启动脚本

为了简化日常开发，可以使用以下启动脚本。

### 后端启动脚本

创建 `scripts/start-backend.sh`：

```bash
#!/bin/bash
cd "$(dirname "$0")/../backend"

# 检查虚拟环境是否存在，不存在则创建
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 检查依赖是否已安装
if ! pip show fastapi > /dev/null 2>&1; then
    echo "安装依赖..."
    pip install -r requirements.txt
fi

# 启动服务
echo "启动后端服务..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 前端启动脚本

创建 `scripts/start-frontend.sh`：

```bash
#!/bin/bash
cd "$(dirname "$0")/../frontend"

# 检查 node_modules 是否存在
if [ ! -d "node_modules" ]; then
    echo "安装依赖..."
    npm install
fi

# 启动服务
echo "启动前端服务..."
npm run dev:h5
```

### 使用方法

```bash
# 添加执行权限（首次）
chmod +x scripts/*.sh

# 启动后端（终端 1）
./scripts/start-backend.sh

# 启动前端（终端 2）
./scripts/start-frontend.sh
```

### 关于虚拟环境

| 操作 | 频率 | 说明 |
|------|------|------|
| 创建虚拟环境 | 一次 | 脚本会自动检查并创建 |
| 安装依赖 | 一次 | 依赖变化时重新安装 |
| 激活虚拟环境 | 每次启动 | 脚本会自动激活 |

> 虚拟环境用于隔离项目依赖，避免不同项目之间的包版本冲突。启动脚本已包含自动检查逻辑，可安全重复运行。

## 环境变量配置

编辑 `backend/.env` 文件：

```env
# 应用配置
APP_NAME=HMM Material Management
APP_ENV=development
DEBUG=True
SECRET_KEY=your-secret-key-change-in-production

# 数据库配置
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/hmm_material

# AI 配置 (可选)
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4

# CORS 配置
CORS_ORIGINS=["http://localhost:8080","http://localhost:5173"]
```

## 生产环境部署

### 后端

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 前端

```bash
# 构建 H5 版本
npm run build:h5

# 构建产物在 dist/build/h5 目录
```

## 用户角色

| 角色 | 说明 |
|------|------|
| admin | 系统管理员 |
| site_manager | 工地管理员 |
| site_staff | 工地员工 |
| agent | 厂家代理人 |
| manufacturer | 厂家员工 |

## License

MIT
