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
