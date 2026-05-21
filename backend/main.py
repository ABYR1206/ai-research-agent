"""FastAPI 入口。"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api import analyze, financial, report, download

app = FastAPI(
    title="AI Research Agent",
    version="0.1.0",
    description="自动生成分析师研究报告 + DCF 估值 Excel 模型",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze.router, tags=["analyze"])
app.include_router(financial.router, tags=["financial"])
app.include_router(report.router, tags=["report"])
app.include_router(download.router, tags=["download"])


@app.get("/")
def root():
    return {
        "service": "AI Research Agent",
        "version": "0.1.0",
        "docs": "/docs",
        "endpoints": [
            "POST /report/generate",
            "POST /analyze/industry",
            "POST /analyze/company",
            "POST /financial/extract",
            "POST /valuation/dcf",
            "GET  /download/excel/{file_id}",
            "GET  /download/report/{file_id}",
        ],
        "supported_tickers_mock": ["AAPL", "TSLA", "NVDA", "TSM"],
    }


@app.get("/health")
def health():
    return {"status": "ok"}
