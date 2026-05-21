#!/usr/bin/env bash
# 一键启动后端 + 前端
set -e
cd "$(dirname "$0")"

# 后台启动后端
echo "🚀 启动后端 FastAPI (http://127.0.0.1:8000)..."
(uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload &)

sleep 2
echo "🚀 启动前端 Next.js (http://localhost:3000)..."
cd frontend
npm run dev
