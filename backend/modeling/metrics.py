"""根据 FinancialStatements 计算历史财务比率与均值。"""
from __future__ import annotations
import statistics
from backend.schemas import FinancialStatements, FinancialMetrics


def _safe_div(n: float, d: float) -> float:
    return n / d if d else 0.0


def compute(stmts: FinancialStatements) -> FinancialMetrics:
    """计算关键比率序列与均值。"""
    h = stmts.history
    years = [y.year for y in h]

    growth = [0.0]
    for i in range(1, len(h)):
        prev = h[i - 1].revenue
        growth.append(_safe_div(h[i].revenue - prev, prev) if prev else 0.0)

    gm = [_safe_div(y.gross_profit, y.revenue) for y in h]
    em = [_safe_div(y.ebit, y.revenue) for y in h]
    ebm = [_safe_div(y.ebitda, y.revenue) for y in h]
    nm = [_safe_div(y.net_income, y.revenue) for y in h]
    capex_pct = [_safe_div(y.capex, y.revenue) for y in h]
    nwc_pct = [_safe_div(y.nwc, y.revenue) for y in h]
    da_pct = [_safe_div(y.da, y.revenue) for y in h]

    # 税率：用 EBIT 与净利反推。但 EBIT - NI 还包含利息支出/非经常损益，
    # 直接反推容易过高。给上限 0.25 接近全球大公司平均有效税率。
    tax_rates = []
    for y in h:
        if y.ebit > 0 and y.net_income > 0:
            ratio = _safe_div(y.net_income, y.ebit)
            if ratio > 0.85:
                tax_rates.append(0.12)
            elif ratio < 0.55:
                tax_rates.append(0.25)
            else:
                tax_rates.append(round(1 - ratio, 4))
        else:
            tax_rates.append(0.21)

    def _avg(xs: list[float], skip_first: bool = False) -> float:
        ys = xs[1:] if skip_first and len(xs) > 1 else xs
        ys = [x for x in ys if x is not None]
        return statistics.fmean(ys) if ys else 0.0

    return FinancialMetrics(
        years=years,
        revenue_growth=growth,
        gross_margin=gm,
        ebit_margin=em,
        ebitda_margin=ebm,
        net_margin=nm,
        capex_pct=capex_pct,
        nwc_pct=nwc_pct,
        da_pct=da_pct,
        tax_rate=tax_rates,
        avg_revenue_growth=_avg(growth, skip_first=True),
        avg_ebit_margin=_avg(em),
        avg_capex_pct=_avg(capex_pct),
        avg_nwc_pct=_avg(nwc_pct),
        avg_da_pct=_avg(da_pct),
        avg_tax_rate=_avg(tax_rates),
    )
