"""所有 Pydantic 数据模型集中定义。"""
from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field


class CompanyProfile(BaseModel):
    ticker: str
    name: str
    sector: str
    industry: str
    country: str = "United States"
    currency: str = "USD"
    market_cap: Optional[float] = None  # in millions
    current_price: Optional[float] = None
    shares_outstanding: Optional[float] = None  # in millions


class IndustryAnalysis(BaseModel):
    sector: str
    definition: str
    market_size: str
    growth_drivers: list[str]
    landscape: str
    key_players: list[str]
    risks: list[str]
    outlook: str


class SWOT(BaseModel):
    strengths: list[str]
    weaknesses: list[str]
    opportunities: list[str]
    threats: list[str]


class CompanyAnalysis(BaseModel):
    overview: str
    business_segments: list[str]
    revenue_mix: str
    business_model: str
    moat: list[str]
    competitors: list[str]
    swot: SWOT
    risks: list[str]


class YearData(BaseModel):
    """单年度财务数据，所有金额单位 USD millions。"""
    year: int
    revenue: float = 0
    gross_profit: float = 0
    ebit: float = 0
    ebitda: float = 0
    net_income: float = 0
    total_assets: float = 0
    total_debt: float = 0
    cash: float = 0
    equity: float = 0
    operating_cf: float = 0
    capex: float = 0
    da: float = 0
    nwc: float = 0  # net working capital
    fcf: float = 0


class FinancialStatements(BaseModel):
    ticker: str
    currency: str = "USD"
    unit: str = "millions"
    history: list[YearData]  # 近 5 年，按年份升序
    shares_outstanding: float  # millions
    data_source: str  # "yfinance" 或 "mock"


class FinancialMetrics(BaseModel):
    years: list[int]
    revenue_growth: list[float]
    gross_margin: list[float]
    ebit_margin: list[float]
    ebitda_margin: list[float]
    net_margin: list[float]
    capex_pct: list[float]  # capex / revenue
    nwc_pct: list[float]
    da_pct: list[float]
    tax_rate: list[float]
    # 历史均值（用于驱动预测）
    avg_revenue_growth: float
    avg_ebit_margin: float
    avg_capex_pct: float
    avg_nwc_pct: float
    avg_da_pct: float
    avg_tax_rate: float


class ForecastAssumptions(BaseModel):
    revenue_growth: list[float]  # 长度 = forecast_years
    ebit_margin: float
    tax_rate: float
    da_pct: float
    capex_pct: float
    nwc_pct: float
    wacc: float
    terminal_growth: float
    forecast_years: int = 5


class ForecastYear(BaseModel):
    year: int
    revenue: float
    ebit: float
    nopat: float
    da: float
    capex: float
    nwc: float
    change_in_nwc: float
    fcf: float


class Forecast(BaseModel):
    years: list[ForecastYear]
    assumptions: ForecastAssumptions


class DCFValuation(BaseModel):
    fcf_forecast: list[float]
    discount_factors: list[float]
    pv_fcf: list[float]
    terminal_value: float
    pv_terminal: float
    enterprise_value: float
    net_debt: float
    equity_value: float
    shares_outstanding: float
    implied_price: float
    current_price: Optional[float] = None
    upside: Optional[float] = None
    sensitivity: list[list[float]]  # [wacc_row][g_col] 隐含股价
    wacc_axis: list[float]
    growth_axis: list[float]


class ReportSections(BaseModel):
    thesis: str
    overview: str
    industry: str
    business: str
    financial: str
    valuation: str
    risks: str
    conclusion: str


class ResearchReport(BaseModel):
    company: CompanyProfile
    sections: ReportSections
    markdown: str
    data_gaps: list[str] = Field(default_factory=list)


# --- API 请求/响应 ---

class GenerateRequest(BaseModel):
    ticker: str
    source: str = "auto"  # auto | yfinance | mock
    assumptions: Optional[ForecastAssumptions] = None


class GenerateResponse(BaseModel):
    profile: CompanyProfile
    industry: IndustryAnalysis
    company: CompanyAnalysis
    statements: FinancialStatements
    metrics: FinancialMetrics
    forecast: Forecast
    dcf: DCFValuation
    report: ResearchReport
    excel_file_id: str
    report_file_id: str
    data_gaps: list[str]
