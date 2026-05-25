"""端到端编排器：串行调用 5 个 Agent + Excel/Markdown 输出。"""
from __future__ import annotations
import logging
import uuid
from pathlib import Path

from backend.schemas import GenerateResponse, ForecastAssumptions
from backend.data import fetcher, mock_data
from backend.agents import (
    industry_agent, company_agent, finance_agent,
    valuation_agent, report_agent,
)
from backend.outputs import excel_builder, report_builder
from backend.outputs.generate_dcf_excel import generate_dcf_excel
from backend.config import EXCEL_DIR, REPORT_DIR

log = logging.getLogger(__name__)


def _get_profile(ticker: str, source: str, gaps: list[str]):
    t = ticker.upper()
    if source == "mock":
        # 严格 mock：未知 ticker 也用合成数据，不报错
        if mock_data.has_mock(t):
            return mock_data.get_mock_profile(t)
        gaps.append(f"{t} 不在内置 mock 列表，使用合成演示数据（非真实财报）。")
        return mock_data.generate_synthetic_profile(t)
    if source == "yfinance":
        return fetcher.fetch_profile(t)
    # auto：yfinance → 内置 mock → 合成
    try:
        return fetcher.fetch_profile(t)
    except fetcher.DataSourceError as e:
        if mock_data.has_mock(t):
            gaps.append(f"yfinance 抓取失败，已 fallback 到内置 mock 数据。")
            return mock_data.get_mock_profile(t)
        gaps.append(f"yfinance 抓取失败且 {t} 不在内置 mock 列表，使用合成演示数据（非真实财报）。")
        return mock_data.generate_synthetic_profile(t)


def run(ticker: str, source: str = "auto",
        user_assumptions: ForecastAssumptions | None = None) -> GenerateResponse:
    """完整流水线：profile→industry→company→financials→forecast→dcf→excel→report。"""
    gaps: list[str] = []
    ticker = ticker.upper()

    profile = _get_profile(ticker, source, gaps)
    industry = industry_agent.analyze(profile)
    company = company_agent.analyze(profile)
    stmts, stmt_gaps = finance_agent.get_statements(ticker, source, sector_hint=profile.sector)
    gaps.extend(stmt_gaps)
    # 用 stmts 里的股数补 profile
    if not profile.shares_outstanding:
        profile.shares_outstanding = stmts.shares_outstanding

    metrics = finance_agent.compute_metrics(stmts)
    forecast = finance_agent.build_forecast(stmts, metrics, user_assumptions)
    dcf = valuation_agent.run(forecast, stmts, profile)

    # 输出文件
    file_id = f"{ticker}_{uuid.uuid4().hex[:8]}"
    excel_path = EXCEL_DIR / f"{file_id}.xlsx"
    report_path = REPORT_DIR / f"{file_id}.md"

    # 新版专业级 Excel 生成器：转成 dict schema 后调用 generate_dcf_excel
    historical_dict = {
        "years": [y.year for y in stmts.history],
        "revenue": [y.revenue for y in stmts.history],
        "ebit": [y.ebit for y in stmts.history],
        "net_income": [y.net_income for y in stmts.history],
        "depreciation_amortization": [y.da for y in stmts.history],
        "capex": [y.capex for y in stmts.history],
        "change_in_nwc": [
            (stmts.history[i].nwc - stmts.history[i - 1].nwc) if i > 0 else 0.0
            for i in range(len(stmts.history))
        ],
        "free_cash_flow": [y.fcf for y in stmts.history],
        "cash": [y.cash for y in stmts.history],
        "total_debt": [y.total_debt for y in stmts.history],
        "shares_outstanding": [stmts.shares_outstanding] * len(stmts.history),
    }
    a = forecast.assumptions
    assumptions_dict = {
        "forecast_years": [y.year for y in forecast.years],
        "revenue_growth": a.revenue_growth,
        "ebit_margin": [a.ebit_margin] * a.forecast_years,
        "tax_rate": a.tax_rate,
        "da_percent_revenue": a.da_pct,
        "capex_percent_revenue": a.capex_pct,
        "nwc_percent_revenue": a.nwc_pct,
        "wacc": a.wacc,
        "terminal_growth_rate": a.terminal_growth,
    }
    generate_dcf_excel(
        company_name=profile.name,
        ticker=profile.ticker,
        historical_data=historical_dict,
        assumptions=assumptions_dict,
        output_path=excel_path,
        current_price=profile.current_price or 0.0,
    )
    report = report_agent.write(profile, industry, company, stmts, metrics, forecast, dcf, gaps)
    report_builder.save_markdown(report, report_path)

    return GenerateResponse(
        profile=profile, industry=industry, company=company,
        statements=stmts, metrics=metrics, forecast=forecast, dcf=dcf,
        report=report, excel_file_id=file_id, report_file_id=file_id,
        data_gaps=gaps,
    )
