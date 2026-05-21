"""Module 4: 研究报告撰写 Agent — Markdown 拼接，8 个章节。"""
from __future__ import annotations
from backend.schemas import (
    CompanyProfile, IndustryAnalysis, CompanyAnalysis,
    FinancialStatements, FinancialMetrics, Forecast, DCFValuation,
    ResearchReport, ReportSections,
)


def _rating(upside: float | None) -> str:
    if upside is None:
        return "中性 (Hold) — 当前价数据缺失"
    if upside > 0.20:
        return "**买入 (BUY)**"
    if upside > 0.05:
        return "**增持 (Overweight)**"
    if upside > -0.05:
        return "**中性 (Hold)**"
    if upside > -0.20:
        return "**减持 (Underweight)**"
    return "**卖出 (SELL)**"


def _pct(x: float | None) -> str:
    return f"{x*100:.1f}%" if x is not None else "N/A"


def _money(x: float | None) -> str:
    return f"${x:,.0f}M" if x is not None else "N/A"


def write(profile: CompanyProfile, industry: IndustryAnalysis,
          company: CompanyAnalysis, stmts: FinancialStatements,
          metrics: FinancialMetrics, forecast: Forecast,
          dcf: DCFValuation, data_gaps: list[str]) -> ResearchReport:
    """整合所有模块输出为正式研究报告（Markdown）。"""

    rating = _rating(dcf.upside)
    last = stmts.history[-1]

    # ---------- 各章节 ----------
    thesis = (
        f"我们对 **{profile.name} ({profile.ticker})** 给出 {rating} 评级，"
        f"DCF 模型隐含每股股价 **${dcf.implied_price:,.2f}**，"
        f"较当前股价 ${dcf.current_price or 0:.2f} 隐含 **{_pct(dcf.upside)}** 上行空间。"
        f"核心逻辑：(1) 公司在 {industry.sector} 行业具备 {', '.join(company.moat[:2])} 的护城河；"
        f"(2) 近 5 年收入复合增速 {_pct(metrics.avg_revenue_growth)}，"
        f"经营利润率维持 {_pct(metrics.avg_ebit_margin)} 水平；"
        f"(3) 未来 5 年 FCF 预测 CAGR 隐含 {_pct(((forecast.years[-1].fcf/max(forecast.years[0].fcf,1))**(1/4) - 1) if forecast.years[0].fcf > 0 else None)}。"
    )

    overview = (
        f"{company.overview}\n\n"
        f"**核心信息**\n\n"
        f"| 项目 | 数值 |\n|---|---|\n"
        f"| 股票代码 | {profile.ticker} |\n"
        f"| 行业 | {profile.sector} / {profile.industry} |\n"
        f"| 国家 | {profile.country} |\n"
        f"| 货币 | {profile.currency} |\n"
        f"| 市值 | {_money(profile.market_cap)} |\n"
        f"| 当前股价 | ${profile.current_price or 0:.2f} |\n"
        f"| 流通股本 | {profile.shares_outstanding or stmts.shares_outstanding:,.0f}M |\n"
        f"| 数据来源 | {stmts.data_source} |"
    )

    industry_md = (
        f"**行业定义**：{industry.definition}\n\n"
        f"**市场规模**：{industry.market_size}\n\n"
        f"**增长驱动因素**：\n" + "\n".join(f"- {d}" for d in industry.growth_drivers) + "\n\n"
        f"**竞争格局**：{industry.landscape}\n\n"
        f"**主要参与者**：{', '.join(industry.key_players)}\n\n"
        f"**行业风险**：\n" + "\n".join(f"- {r}" for r in industry.risks) + "\n\n"
        f"**未来 3-5 年展望**：{industry.outlook}"
    )

    business_md = (
        f"**主营业务板块**：\n" + "\n".join(f"- {s}" for s in company.business_segments) + "\n\n"
        f"**收入结构**：{company.revenue_mix}\n\n"
        f"**商业模式**：{company.business_model}\n\n"
        f"**核心竞争力（护城河）**：\n" + "\n".join(f"- {m}" for m in company.moat) + "\n\n"
        f"**主要竞争对手**：{', '.join(company.competitors)}\n\n"
        f"**SWOT 分析**\n\n"
        f"| 维度 | 内容 |\n|---|---|\n"
        f"| 优势 (S) | {'; '.join(company.swot.strengths)} |\n"
        f"| 劣势 (W) | {'; '.join(company.swot.weaknesses)} |\n"
        f"| 机会 (O) | {'; '.join(company.swot.opportunities)} |\n"
        f"| 威胁 (T) | {'; '.join(company.swot.threats)} |"
    )

    # 财务历史表
    hist_header = "| 年份 | 营收 | EBIT | 净利 | OCF | Capex | FCF | EBIT 利润率 | 营收增速 |\n|---|---|---|---|---|---|---|---|---|\n"
    hist_rows = "\n".join(
        f"| {y.year} | {_money(y.revenue)} | {_money(y.ebit)} | {_money(y.net_income)} | "
        f"{_money(y.operating_cf)} | {_money(y.capex)} | {_money(y.fcf)} | "
        f"{_pct(metrics.ebit_margin[i])} | {_pct(metrics.revenue_growth[i])} |"
        for i, y in enumerate(stmts.history)
    )
    fc_header = "| 年份 | 营收 | EBIT | NOPAT | D&A | Capex | ΔNWC | FCF |\n|---|---|---|---|---|---|---|---|\n"
    fc_rows = "\n".join(
        f"| {y.year}E | {_money(y.revenue)} | {_money(y.ebit)} | {_money(y.nopat)} | "
        f"{_money(y.da)} | {_money(y.capex)} | {_money(y.change_in_nwc)} | {_money(y.fcf)} |"
        for y in forecast.years
    )
    financial_md = (
        "### 历史财务（近 5 年）\n\n" + hist_header + hist_rows + "\n\n"
        "### 5 年预测\n\n" + fc_header + fc_rows + "\n\n"
        "**核心比率均值**：营收增速 " + _pct(metrics.avg_revenue_growth) +
        f"，EBIT 利润率 {_pct(metrics.avg_ebit_margin)}，"
        f"Capex 占比 {_pct(metrics.avg_capex_pct)}，"
        f"税率 {_pct(metrics.avg_tax_rate)}。"
    )

    a = forecast.assumptions
    valuation_md = (
        f"**估值方法**：5 年显式预测期 DCF + 永续增长终值（Gordon Growth）。\n\n"
        f"**关键假设**\n\n"
        f"| 假设 | 数值 |\n|---|---|\n"
        f"| WACC | {_pct(a.wacc)} |\n"
        f"| 永续增长率 g | {_pct(a.terminal_growth)} |\n"
        f"| EBIT 利润率 | {_pct(a.ebit_margin)} |\n"
        f"| 税率 | {_pct(a.tax_rate)} |\n"
        f"| Capex 占比 | {_pct(a.capex_pct)} |\n"
        f"| D&A 占比 | {_pct(a.da_pct)} |\n"
        f"| NWC 占比 | {_pct(a.nwc_pct)} |\n\n"
        f"**估值结果**\n\n"
        f"| 项目 | 数值 |\n|---|---|\n"
        f"| 显式期 PV(FCF) 合计 | {_money(sum(dcf.pv_fcf))} |\n"
        f"| 终值 (TV) | {_money(dcf.terminal_value)} |\n"
        f"| PV(终值) | {_money(dcf.pv_terminal)} |\n"
        f"| 企业价值 (EV) | {_money(dcf.enterprise_value)} |\n"
        f"| 减：净负债 | {_money(dcf.net_debt)} |\n"
        f"| 股权价值 | {_money(dcf.equity_value)} |\n"
        f"| 流通股本 (M) | {dcf.shares_outstanding:,.0f} |\n"
        f"| **隐含每股价格** | **${dcf.implied_price:,.2f}** |\n"
        f"| 当前股价 | ${dcf.current_price or 0:.2f} |\n"
        f"| **上行空间** | **{_pct(dcf.upside)}** |\n\n"
        f"**敏感性分析**（每股股价，WACC × 永续增长率）\n\n"
        + "| WACC \\ g | " + " | ".join(f"{g*100:.1f}%" for g in dcf.growth_axis) + " |\n"
        + "|---|" + "---|" * len(dcf.growth_axis) + "\n"
        + "\n".join(
            f"| {dcf.wacc_axis[i]*100:.1f}% | " + " | ".join(f"${v:,.1f}" for v in row) + " |"
            for i, row in enumerate(dcf.sensitivity)
        )
    )

    risks_md = (
        "**公司风险**：\n" + "\n".join(f"- {r}" for r in company.risks) + "\n\n"
        "**行业风险**：\n" + "\n".join(f"- {r}" for r in industry.risks) + "\n\n"
        "**估值风险**：\n"
        "- WACC 上行 100bps，隐含股价回撤约 10-15%\n"
        "- 永续增长率下调 100bps，隐含股价回撤约 8-12%\n"
        "- 收入增速不及预期或利润率下行将显著压低 FCF 预测\n"
    )

    conclusion = (
        f"基于 DCF 模型，{profile.ticker} 的隐含合理股价为 **${dcf.implied_price:,.2f}**，"
        f"较当前价隐含 **{_pct(dcf.upside)}** 上行空间，给予 {rating} 评级。\n\n"
        f"投资者需重点关注：(1) {company.risks[0] if company.risks else 'N/A'}; "
        f"(2) WACC 与永续增长率假设的敏感性；"
        f"(3) 行业层面的 {industry.risks[0] if industry.risks else 'N/A'}。\n\n"
        + ("> ⚠️ **数据缺失提示**：" + "; ".join(data_gaps) if data_gaps else "")
    )

    sections = ReportSections(
        thesis=thesis, overview=overview, industry=industry_md,
        business=business_md, financial=financial_md, valuation=valuation_md,
        risks=risks_md, conclusion=conclusion,
    )

    md = f"""# {profile.name} ({profile.ticker}) — 投资研究报告

> 评级：{rating}  ·  目标价：**${dcf.implied_price:,.2f}**  ·  当前价：${dcf.current_price or 0:.2f}  ·  上行空间：**{_pct(dcf.upside)}**

---

## 1. 投资逻辑 (Investment Thesis)

{thesis}

## 2. 公司概览 (Company Overview)

{overview}

## 3. 行业分析 (Industry Analysis)

{industry_md}

## 4. 商业模式分析 (Business Model Analysis)

{business_md}

## 5. 财务分析 (Financial Analysis)

{financial_md}

## 6. 估值 (Valuation)

{valuation_md}

## 7. 风险因素 (Risk Factors)

{risks_md}

## 8. 结论与建议 (Conclusion / Recommendation)

{conclusion}

---

*本报告由 AI Research Agent 自动生成，仅供课程演示与研究参考，不构成投资建议。数据来源：{stmts.data_source}。生成时间：模型版本 v0.1。*
"""

    return ResearchReport(
        company=profile, sections=sections, markdown=md, data_gaps=data_gaps,
    )
