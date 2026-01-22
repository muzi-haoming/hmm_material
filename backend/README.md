# HMM Material - Backend

物资管理系统后端服务

## 技术栈

- **框架**: FastAPI 0.104+
- **数据库**: PostgreSQL + AsyncPG
- **ORM**: SQLAlchemy 2.0+ (异步)
- **认证**: JWT + bcrypt
- **AI**: LangChain + OpenAI GPT-4

## 目录结构

```
backend/
├── app/
│   ├── main.py          # 应用入口
│   ├── core/            # 核心配置
│   │   ├── config.py    # 配置管理
│   │   ├── database.py  # 数据库连接
│   │   └── security.py  # 安全工具
│   ├── models/          # 数据库模型
│   ├── schemas/         # Pydantic 验证
│   ├── api/             # API 路由
│   │   └── v1/
│   │       └── endpoints/
│   ├── services/        # 业务逻辑
│   └── ai/              # AI 集成
├── requirements.txt
├── .env.example
└── README.md
```

## 环境要求

- Python >= 3.10
- PostgreSQL >= 14.0

## 快速启动

### 方式一：使用启动脚本（推荐）

```bash
# 在项目根目录执行
./scripts/start-backend.sh
```

### 方式二：手动启动

```bash
# 1. 创建虚拟环境（首次）
python -m venv venv

# 2. 激活虚拟环境
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. 安装依赖（首次或依赖更新后）
pip install -r requirements.txt

# 4. 配置环境变量（首次）
cp .env.example .env
# 编辑 .env 文件

# 5. 创建数据库（首次）
createdb hmm_material

# 6. 运行数据库迁移
alembic upgrade head

# 7. 启动开发服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 日常开发启动

```bash
# 激活虚拟环境并启动
source venv/bin/activate && uvicorn app.main:app --reload --port 8000
```

## 服务地址

| 服务 | 地址 |
|------|------|
| API | http://localhost:8000 |
| Swagger 文档 | http://localhost:8000/docs |
| ReDoc 文档 | http://localhost:8000/redoc |

## 环境变量

编辑 `.env` 文件：

```env
# 应用配置
APP_NAME=HMM Material Management
APP_ENV=development
DEBUG=True
SECRET_KEY=your-secret-key

# 数据库
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/hmm_material

# AI (可选)
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4

# CORS
CORS_ORIGINS=["http://localhost:5173"]
```

## 常用命令

```bash
# 启动开发服务器
uvicorn app.main:app --reload --port 8000

# 生产环境启动
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# 创建数据库迁移
alembic revision --autogenerate -m "description"

# 执行迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1
```

## API 模块

| 模块 | 路径 | 说明 |
|------|------|------|
| auth | `/api/v1/auth` | 认证登录 |
| users | `/api/v1/users` | 用户管理 |
| sites | `/api/v1/sites` | 工地管理 |
| manufacturers | `/api/v1/manufacturers` | 厂家管理 |
| contracts | `/api/v1/contracts` | 合同管理 |
| products | `/api/v1/products` | 产品管理 |
| orders | `/api/v1/orders` | 订单管理 |
| delegations | `/api/v1/delegations` | 委托管理 |
