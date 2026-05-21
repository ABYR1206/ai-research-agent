"""yfinance 数据抓取封装。失败抛 DataSourceError，由 orchestrator 决定 fallback。"""
from __future__ import annotations
import logging
from typing import Optional

import pandas as pd

from backend.schemas import CompanyProfile, FinancialStatements, YearData

log = logging.getLogger(__name__)


class DataSourceError(Exception):
    pass


def _safe_row(df: pd.DataFrame, candidates: list[str]) -> Optional[pd.Series]:
    """从 df.index 中按候选名取第一个命中的行。"""
    if df is None or df.empty:
        return None
    for c in candidates:
        if c in df.index:
            return df.loc[c]
    return None


def _v(row: Optional[pd.Series], col, default: float = 0.0) -> float:
    if row is None or col not in row.index:
        return default
    val = row[col]
    if pd.isna(val):
        return default
    return float(val) / 1_000_000  # 转 millions


def fetch_profile(ticker: str) -> CompanyProfile:
    """从 yfinance 拉取公司基础信息。"""
    try:
        import yfinance as yf
    except ImportError as e:
        raise DataSourceError(f"yfinance not installed: {e}")
    try:
        t = yf.Ticker(ticker)
        info = t.info or {}
        if not info or "symbol" not in info and "shortName" not in info:
            raise DataSourceError(f"yfinance returned empty info for {ticker}")
        return CompanyProfile(
            ticker=ticker.upper(),
            name=info.get("longName") or info.get("shortName") or ticker,
            sector=info.get("sector") or "Unknown",
            industry=info.get("industry") or "Unknown",
            country=info.get("country") or "United States",
            currency=info.get("currency") or "USD",
            market_cap=(info.get("marketCap") or 0) / 1_000_000 or None,
            current_price=info.get("currentPrice") or info.get("regularMarketPrice"),
            shares_outstanding=(info.get("sharesOutstanding") or 0) / 1_000_000 or None,
        )
    except DataSourceError:
        raise
    except Exception as e:
        raise DataSourceError(f"fetch_profile({ticker}) failed: {e}") from e


def fetch_statements(ticker: str) -> FinancialStatements:
    """拉取三表近 5 年数据并转为 YearData 列表。"""
    try:
        import yfinance as yf
    except ImportError as e:
        raise DataSourceError(f"yfinance not installed: {e}")
    try:
        t = yf.Ticker(ticker)
        income = t.financials       # 损益
        balance = t.balance_sheet   # 资产负债
        cf = t.cashflow             # 现金流
        info = t.info or {}
        if income is None or income.empty:
            raise DataSourceError(f"empty income statement for {ticker}")

        # 列是日期，倒序（最新在前）。取最近 5 年并按年份升序
        cols = list(income.columns)[:5][::-1]

        rev_row = _safe_row(income, ["Total Revenue", "Revenue"])
        gp_row = _safe_row(income, ["Gross Profit"])
        ebit_row = _safe_row(income, ["EBIT", "Operating Income", "Operating Income Loss"])
        ebitda_row = _safe_row(income, ["EBITDA", "Normalized EBITDA"])
        ni_row = _safe_row(income, ["Net Income", "Net Income Common Stockholders"])
        tax_row = _safe_row(income, ["Tax Provision", "Income Tax Expense"])
        pretax_row = _safe_row(income, ["Pretax Income", "Income Before Tax"])

        ta_row = _safe_row(balance, ["Total Assets"])
        td_row = _safe_row(balance, ["Total Debt", "Long Term Debt"])
        cash_row = _safe_row(balance, ["Cash And Cash Equivalents", "Cash"])
        eq_row = _safe_row(balance, ["Stockholders Equity", "Total Equity Gross Minority Interest"])
        ca_row = _safe_row(balance, ["Current Assets", "Total Current Assets"])
        cl_row = _safe_row(balance, ["Current Liabilities", "Total Current Liabilities"])

        ocf_row = _safe_row(cf, ["Operating Cash Flow", "Cash Flow From Continuing Operating Activities"])
        capex_row = _safe_row(cf, ["Capital Expenditure", "Capital Expenditures"])
        da_row = _safe_row(cf, ["Depreciation And Amortization", "Depreciation Amortization Depletion"])

        history: list[YearData] = []
        for c in cols:
            year = pd.Timestamp(c).year
            rev = _v(rev_row, c)
            ebit = _v(ebit_row, c)
            da = _v(da_row, c)
            ebitda_val = _v(ebitda_row, c) or (ebit + da)
            ca = _v(ca_row, c); cl = _v(cl_row, c)
            capex = abs(_v(capex_row, c))
            ocf = _v(ocf_row, c)
            history.append(YearData(
                year=year,
                revenue=rev,
                gross_profit=_v(gp_row, c),
                ebit=ebit,
                ebitda=ebitda_val,
                net_income=_v(ni_row, c),
                total_assets=_v(ta_row, c),
                total_debt=_v(td_row, c),
                cash=_v(cash_row, c),
                equity=_v(eq_row, c),
                operating_cf=ocf,
                capex=capex,
                da=da,
                nwc=ca - cl,
                fcf=ocf - capex,
            ))

        shares = (info.get("sharesOutstanding") or 0) / 1_000_000
        if not shares:
            raise DataSourceError(f"missing shares outstanding for {ticker}")

        return FinancialStatements(
            ticker=ticker.upper(),
            shares_outstanding=shares,
            history=history,
            data_source="yfinance",
        )
    except DataSourceError:
        raise
    except Exception as e:
        raise DataSourceError(f"fetch_statements({ticker}) failed: {e}") from e
