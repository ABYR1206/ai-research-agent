# Hugging Face Spaces 用的 Docker 镜像。
# 安装 Python 依赖 + uvicorn 起 FastAPI，监听 HF Spaces 默认端口 7860。
FROM python:3.12-slim

WORKDIR /app

# numpy/pandas 编译可能需要 gcc
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY backend ./backend

# storage 目录用于生成 Excel / Markdown 输出
RUN mkdir -p storage/excel storage/reports && \
    chmod -R 777 storage

ENV PORT=7860 \
    PYTHONUNBUFFERED=1

EXPOSE 7860

CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT}"]
