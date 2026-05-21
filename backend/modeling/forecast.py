"""根据历史指标推导 5 年预测假设并执行预测。"""
from __future__ import annotations
from backend.schemas import (
    FinancialStatements, FinancialMetrics, ForecastAssumptions,
    Forecast, ForecastYear,
)
from backend.config import DEFAULT_WACC, DEFAULT_TERMINAL_GROWTH, DEFAULT_FORECAST_YEARS


def derive_assumptions(metrics: FinancialMetrics) -> ForecastAssumptions:
    """基于历史均值生成默认假设。增长率采用递减路径（高 → 终值）。"""
    n = DEFAULT_FORECAST_YEARS
    base_g = max(0.02, min(0.25, metrics.avg_revenue_growth or 0.05))
    # 线性衰减到 terminal_growth
    growth_path = [
        round(base_g + (DEFAULT_TERMINAL_GROWTH - base_g) * (i / (n - 1)), 4)
        for i in range(n)
    ]
    return ForecastAssumptions(
        revenue_growth=growth_path,
        ebit_margin=round(max(0.05, metrics.avg_ebit_margin or 0.15), 4),
        tax_rate=round(metrics.avg_tax_rate or 0.21, 4),
        da_pct=round(max(0.01, metrics.avg_da_pct or 0.04), 4),
        capex_pct=round(max(0.02, metrics.avg_capex_pct or 0.05), 4),
        nwc_pct=round(metrics.avg_nwc_pct or 0.05, 4),
        wacc=DEFAULT_WACC,
        terminal_growth=DEFAULT_TERMINAL_GROWTH,
        forecast_years=n,
    )


def project(stmts: FinancialStatements, a: ForecastAssumptions) -> Forecast:
    """基于最近一年实际值，按假设逐年滚动预测 5 年 FCF。"""
    last = stmts.history[-1]
    base_year = last.year
    base_rev = last.revenue
    base_nwc = last.revenue * a.nwc_pct  # 预测期 NWC 用占比驱动

    years: list[ForecastYear] = []
    prev_rev = base_rev
    prev_nwc = base_nwc
    for i, g in enumerate(a.revenue_growth, start=1):
        rev = prev_rev * (1 + g)
        ebit = rev * a.ebit_margin
        nopat = ebit * (1 - a.tax_rate)
        da = rev * a.da_pct
        capex = rev * a.capex_pct
        nwc = rev * a.nwc_pct
        d_nwc = nwc - prev_nwc
        fcf = nopat + da - capex - d_nwc
        years.append(ForecastYear(
            year=base_year + i,
            revenue=round(rev, 2),
            ebit=round(ebit, 2),
            nopat=round(nopat, 2),
            da=round(da, 2),
            capex=round(capex, 2),
            nwc=round(nwc, 2),
            change_in_nwc=round(d_nwc, 2),
            fcf=round(fcf, 2),
        ))
        prev_rev = rev
        prev_nwc = nwc

    return Forecast(years=years, assumptions=a)
