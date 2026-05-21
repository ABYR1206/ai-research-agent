"""全局配置：路径常量与默认假设。"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STORAGE = ROOT / "storage"
EXCEL_DIR = STORAGE / "excel"
REPORT_DIR = STORAGE / "reports"
EXCEL_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# 默认 DCF 假设（用户可在前端覆盖）
DEFAULT_WACC = 0.09
DEFAULT_TERMINAL_GROWTH = 0.025
DEFAULT_FORECAST_YEARS = 5
DEFAULT_TAX_RATE = 0.21

SUPPORTED_TICKERS = ["AAPL", "TSLA", "NVDA", "TSM"]
