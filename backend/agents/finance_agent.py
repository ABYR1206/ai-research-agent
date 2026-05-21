"""Module 3a: 财务报表获取 + 指标计算 + 假设推导 + 预测。"""
from __future__ import annotations
from backend.schemas import FinancialStatements, FinancialMetrics, Forecast
from backend.data import fetcher, mock_data
from backend.modeling import metrics as metrics_mod, forecast as forecast_mod


def get_statements(ticker: str, source: str = "auto") -> tuple[FinancialStatements, list[str]]:
    """获取三表。auto: 先 yfinance 再 mock；yfinance: 严格；mock: 直接 mock。
    返回 (statements, data_gaps)。"""
    gaps: list[str] = []
    t = ticker.upper()
    if source == "mock":
        return mock_data.get_mock_statements(t), gaps
    if source == "yfinance":
        return fetcher.fetch_statements(t), gaps
    # auto
    try:
        return fetcher.fetch_statements(t), gaps
    except fetcher.DataSourceError as e:
        if mock_data.has_mock(t):
            gaps.append(f"yfinance 抓取失败（{e}），已 fallback 到内置 mock 数据。")
            return mock_data.get_mock_statements(t), gaps
        raise


def compute_metrics(stmts: FinancialStatements) -> FinancialMetrics:
    return metrics_mod.compute(stmts)


def build_forecast(stmts: FinancialStatements, metrics: FinancialMetrics,
                   user_assumptions=None) -> Forecast:
    """根据历史均值生成默认假设；若用户传入则覆盖。"""
    assump = forecast_mod.derive_assumptions(metrics)
    if user_assumptions:
        # 浅合并：用户传字段覆盖默认
        data = assump.model_dump()
        data.update({k: v for k, v in user_assumptions.model_dump().items() if v is not None})
        from backend.schemas import ForecastAssumptions
        assump = ForecastAssumptions(**data)
    return forecast_mod.project(stmts, assump)
