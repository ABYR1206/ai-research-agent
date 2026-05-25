"""Module 3a: 财务报表获取 + 指标计算 + 假设推导 + 预测。"""
from __future__ import annotations
from backend.schemas import FinancialStatements, FinancialMetrics, Forecast
from backend.data import fetcher, mock_data, eastmoney
from backend.modeling import metrics as metrics_mod, forecast as forecast_mod


def get_statements(ticker: str, source: str = "auto",
                    sector_hint: str = "Technology") -> tuple[FinancialStatements, list[str]]:
    """获取三表。auto/mock: 都会兜底到合成数据，永不报错。yfinance: 严格。
    返回 (statements, data_gaps)。sector_hint 用于合成时选行业模板。"""
    gaps: list[str] = []
    t = ticker.upper()
    if source == "mock":
        if mock_data.has_mock(t):
            return mock_data.get_mock_statements(t), gaps
        return mock_data.generate_synthetic_statements(t, sector_hint), gaps
    if source == "yfinance":
        return fetcher.fetch_statements(t), gaps
    if source == "eastmoney":
        return eastmoney.fetch_statements(t), gaps
    # auto：东方财富 → yfinance → mock → 合成
    try:
        return eastmoney.fetch_statements(t), gaps
    except eastmoney.EastmoneyError:
        try:
            return fetcher.fetch_statements(t), gaps
        except fetcher.DataSourceError:
            if mock_data.has_mock(t):
                gaps.append("实时接口抓取失败，三表已 fallback 到内置 mock 数据。")
                return mock_data.get_mock_statements(t), gaps
            return mock_data.generate_synthetic_statements(t, sector_hint), gaps


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
