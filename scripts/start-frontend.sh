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
