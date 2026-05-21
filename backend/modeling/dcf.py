"""Python 端 DCF 复算 + 敏感性矩阵。Excel 模型有独立公式，两边一致。"""
from __future__ import annotations
from backend.schemas import (
    Forecast, FinancialStatements, CompanyProfile, DCFValuation,
)


def _dcf_price(fcfs: list[float], wacc: float, g: float, net_debt: float, shares: float) -> float:
    """单次 DCF 计算返回隐含每股价格。"""
    if wacc <= g:
        return 0.0
    pv_sum = 0.0
    for t, fcf in enumerate(fcfs, start=1):
        pv_sum += fcf / ((1 + wacc) ** t)
    tv = fcfs[-1] * (1 + g) / (wacc - g)
    pv_tv = tv / ((1 + wacc) ** len(fcfs))
    ev = pv_sum + pv_tv
    equity = ev - net_debt
    return equity / shares if shares else 0.0


def run(forecast: Forecast, stmts: FinancialStatements, profile: CompanyProfile) -> DCFValuation:
    """执行 DCF 估值并生成 7×7 敏感性矩阵。"""
    a = forecast.assumptions
    fcfs = [y.fcf for y in forecast.years]
    last = stmts.history[-1]
    net_debt = max(0.0, last.total_debt - last.cash)
    shares = stmts.shares_outstanding

    # 主估值
    dfs = [1 / ((1 + a.wacc) ** t) for t in range(1, len(fcfs) + 1)]
    pv_fcf = [fcf * df for fcf, df in zip(fcfs, dfs)]
    tv = fcfs[-1] * (1 + a.terminal_growth) / (a.wacc - a.terminal_growth)
    pv_tv = tv * dfs[-1]
    ev = sum(pv_fcf) + pv_tv
    equity = ev - net_debt
    implied = equity / shares if shares else 0.0
    cur = profile.current_price
    upside = (implied - cur) / cur if cur else None

    # 敏感性：WACC 7-13%（7档），g 1-4%（7档，0.5% 步长）
    wacc_axis = [round(0.07 + i * 0.01, 4) for i in range(7)]
    growth_axis = [round(0.01 + i * 0.005, 4) for i in range(7)]
    sens: list[list[float]] = []
    for w in wacc_axis:
        row = [round(_dcf_price(fcfs, w, g, net_debt, shares), 2) for g in growth_axis]
        sens.append(row)

    return DCFValuation(
        fcf_forecast=[round(x, 2) for x in fcfs],
        discount_factors=[round(x, 4) for x in dfs],
        pv_fcf=[round(x, 2) for x in pv_fcf],
        terminal_value=round(tv, 2),
        pv_terminal=round(pv_tv, 2),
        enterprise_value=round(ev, 2),
        net_debt=round(net_debt, 2),
        equity_value=round(equity, 2),
        shares_outstanding=shares,
        implied_price=round(implied, 2),
        current_price=cur,
        upside=round(upside, 4) if upside is not None else None,
        sensitivity=sens,
        wacc_axis=wacc_axis,
        growth_axis=growth_axis,
    )
