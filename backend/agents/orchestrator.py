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
from backend.config import EXCEL_DIR, REPORT_DIR

log = logging.getLogger(__name__)


def _get_profile(ticker: str, source: str, gaps: list[str]):
    t = ticker.upper()
    if source == "mock":
        return mock_data.get_mock_profile(t)
    if source == "yfinance":
        return fetcher.fetch_profile(t)
    # auto
    try:
        return fetcher.fetch_profile(t)
    except fetcher.DataSourceError as e:
        if mock_data.has_mock(t):
            gaps.append(f"yfinance profile 抓取失败（{e}），fallback 到内置 mock。")
            return mock_data.get_mock_profile(t)
        raise


def run(ticker: str, source: str = "auto",
        user_assumptions: ForecastAssumptions | None = None) -> GenerateResponse:
    """完整流水线：profile→industry→company→financials→forecast→dcf→excel→report。"""
    gaps: list[str] = []
    ticker = ticker.upper()

    profile = _get_profile(ticker, source, gaps)
    industry = industry_agent.analyze(profile)
    company = company_agent.analyze(profile)
    stmts, stmt_gaps = finance_agent.get_statements(ticker, source)
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

    excel_builder.build(profile, stmts, metrics, forecast, dcf, excel_path)
    report = report_agent.write(profile, industry, company, stmts, metrics, forecast, dcf, gaps)
    report_builder.save_markdown(report, report_path)

    return GenerateResponse(
        profile=profile, industry=industry, company=company,
        statements=stmts, metrics=metrics, forecast=forecast, dcf=dcf,
        report=report, excel_file_id=file_id, report_file_id=file_id,
        data_gaps=gaps,
    )
