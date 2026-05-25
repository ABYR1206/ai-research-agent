"""内置 mock 数据：4 家公司近 5 年财务三表 + profile。
单位均为 USD millions，shares_outstanding 单位 millions。数据来源于公开年报近似值，
仅供课程演示使用，不保证准确性。"""
from __future__ import annotations
from backend.schemas import CompanyProfile, FinancialStatements, YearData


def _yd(year, rev, gp, ebit, ebitda, ni, ta, td, cash, eq, ocf, capex, da, nwc):
    fcf = ocf - capex
    return YearData(
        year=year, revenue=rev, gross_profit=gp, ebit=ebit, ebitda=ebitda,
        net_income=ni, total_assets=ta, total_debt=td, cash=cash, equity=eq,
        operating_cf=ocf, capex=capex, da=da, nwc=nwc, fcf=fcf,
    )


PROFILES: dict[str, CompanyProfile] = {
    "AAPL": CompanyProfile(
        ticker="AAPL", name="Apple Inc.", sector="Technology",
        industry="Consumer Electronics", country="United States", currency="USD",
        market_cap=3_400_000, current_price=220.0, shares_outstanding=15_400.0,
    ),
    "TSLA": CompanyProfile(
        ticker="TSLA", name="Tesla, Inc.", sector="Consumer Cyclical",
        industry="Auto Manufacturers", country="United States", currency="USD",
        market_cap=900_000, current_price=280.0, shares_outstanding=3_200.0,
    ),
    "NVDA": CompanyProfile(
        ticker="NVDA", name="NVIDIA Corporation", sector="Technology",
        industry="Semiconductors", country="United States", currency="USD",
        market_cap=3_200_000, current_price=130.0, shares_outstanding=24_600.0,
    ),
    "TSM": CompanyProfile(
        ticker="TSM", name="Taiwan Semiconductor Manufacturing Co.",
        sector="Technology", industry="Semiconductors", country="Taiwan",
        currency="USD", market_cap=900_000, current_price=175.0,
        shares_outstanding=5_186.0,
    ),
    "ZJMGF": CompanyProfile(
        ticker="ZJMGF", name="Zijin Mining Group Co., Ltd. (紫金矿业)",
        sector="Basic Materials",
        industry="Copper & Gold Mining",
        country="China", currency="USD",
        market_cap=66_390,  # ~2.5 USD * 26,556M shares
        current_price=2.50,  # A 股 ~18 RMB ≈ USD 2.5（汇率 7.2）
        shares_outstanding=26_556.0,  # A+H 总股本约 265.56 亿股
    ),
}

# 紫金矿业别名 → 标准 ticker
_TICKER_ALIAS = {
    "2899.HK": "ZJMGF",
    "02899.HK": "ZJMGF",
    "2899": "ZJMGF",
    "601899.SS": "ZJMGF",
    "601899.SH": "ZJMGF",
    "601899": "ZJMGF",
    "ZIJINMINING": "ZJMGF",
}


def _resolve(ticker: str) -> str:
    """把港股 / A 股 / ADR 代码统一映射到标准 ticker。"""
    t = ticker.upper().strip()
    return _TICKER_ALIAS.get(t, t)


STATEMENTS: dict[str, FinancialStatements] = {
    "AAPL": FinancialStatements(
        ticker="AAPL", shares_outstanding=15_400.0, data_source="mock",
        history=[
            _yd(2020, 274515, 104956, 66288, 77344, 57411, 323888, 112436, 90943, 65339, 80674, 7309,  11056, -3500),
            _yd(2021, 365817, 152836, 108949, 120233, 94680, 351002, 124719, 62639, 63090, 104038, 11085, 11284, -8500),
            _yd(2022, 394328, 170782, 119437, 130541, 99803, 352755, 120069, 48304, 50672, 122151, 10708, 11104, -12000),
            _yd(2023, 383285, 169148, 114301, 125820, 96995, 352583, 111088, 61555, 62146, 110543, 10959, 11519, -2000),
            _yd(2024, 391035, 180683, 123216, 134661, 93736, 364980, 106629, 65171, 56950, 118254, 9447,  11445,  -3000),
        ],
    ),
    "TSLA": FinancialStatements(
        ticker="TSLA", shares_outstanding=3_200.0, data_source="mock",
        history=[
            _yd(2020, 31536, 6630,  1994,  4224,  721,   52148, 13279, 19384, 22225, 5943,  3242, 2322, 1500),
            _yd(2021, 53823, 13606, 6523,  9100,  5519,  62131, 9560,  18144, 30189, 11497, 8014, 2911, 2800),
            _yd(2022, 81462, 20853, 13656, 17575, 12556, 82338, 5748,  22185, 44704, 14724, 7163, 3543, 4200),
            _yd(2023, 96773, 17660, 8891,  13234, 14997, 106618, 9573, 29094, 62634, 13256, 8898, 4667, 5800),
            _yd(2024, 97690, 17450, 7076,  12200, 7091,  122070, 13624, 36556, 70852, 14923, 11340, 5368, 7000),
        ],
    ),
    "NVDA": FinancialStatements(
        ticker="NVDA", shares_outstanding=24_600.0, data_source="mock",
        history=[
            _yd(2020, 10918, 6768,  2846,  3677,  2796,  17315, 2000,  10897, 12204, 4761,  489,  381,  900),
            _yd(2021, 16675, 10396, 4532,  5691,  4332,  28791, 6963,  11561, 16893, 5822,  1128, 1098, 1700),
            _yd(2022, 26914, 17475, 10041, 11351, 9752,  44187, 10946, 21208, 26612, 9108,  976,  1544, 2900),
            _yd(2023, 26974, 15356, 4224,  5860,  4368,  41182, 9709,  13296, 22101, 5641,  1833, 1544, 3800),
            _yd(2024, 60922, 44301, 32972, 35583, 29760, 65728, 9709,  25984, 42978, 28090, 1069, 1508, 6500),
        ],
    ),
    "TSM": FinancialStatements(
        ticker="TSM", shares_outstanding=5_186.0, data_source="mock",
        history=[
            _yd(2020, 45510, 24043, 18102, 28290, 17597, 80793, 10620, 22360, 53462, 27338, 17240, 10188, 2500),
            _yd(2021, 56822, 29470, 22167, 35596, 21323, 105069, 21063, 38244, 67212, 36973, 30040, 13429, 3200),
            _yd(2022, 75884, 45110, 36000, 51970, 34000, 129000, 30000, 47700, 83000, 50000, 36300, 15970, 5000),
            _yd(2023, 69300, 36400, 27800, 41700, 26900, 138000, 32000, 53600, 92000, 42500, 30450, 13900, 4200),
            _yd(2024, 87000, 47900, 36800, 53100, 35100, 162000, 28500, 65000, 110000, 53400, 28400, 16300, 5400),
        ],
    ),
    # 紫金矿业 — 数据基于公司年报 2020-2024，按 1 USD = 7.0 RMB 换算到 USD millions
    # 来源：紫金矿业官网 / 上交所披露 / 2024 年报摘要
    # 原始 RMB 亿元：2020-2024 营收 1715/2251/2703/2934/3036；归母净利 65/157/200/211/321；
    # OCF 143/261/287/369/489；2024 总资产 3966 亿、净资产 1398 亿（归母）、负债率 55%
    "ZJMGF": FinancialStatements(
        ticker="ZJMGF", shares_outstanding=26_556.0, data_source="mock",
        history=[
            # year, rev, gp,    ebit, ebitda, ni,  ta,   td,    cash,  eq,    ocf,  capex, da,   nwc
            _yd(2020, 24500, 4900, 3186,  4001,  928,  22829, 9000, 1500, 7000,  2043, 1929, 815,  2000),
            _yd(2021, 32157, 7080, 5145,  6174,  2243, 28286, 12000, 2050, 9000, 3729, 3000, 1029, 2800),
            _yd(2022, 38614, 8495, 6178,  7664,  2857, 35430, 16000, 2286, 12000, 4100, 4000, 1486, 3200),
            _yd(2023, 41914, 9221, 6707,  8622,  3014, 49143, 25000, 3357, 17000, 5271, 4071, 1915, 3700),
            _yd(2024, 43371, 9974, 8030,  10244, 4579, 56657, 31164, 4429, 25500, 6980, 4214, 2214, 4600),
        ],
    ),
}


def get_mock_profile(ticker: str) -> CompanyProfile:
    """返回内置 profile，未知 ticker 抛 KeyError。支持 ticker alias 解析。"""
    t = _resolve(ticker)
    if t not in PROFILES:
        raise KeyError(f"No mock profile for {t}; supported: {list(PROFILES.keys())}")
    return PROFILES[t]


def get_mock_statements(ticker: str) -> FinancialStatements:
    t = _resolve(ticker)
    if t not in STATEMENTS:
        raise KeyError(f"No mock statements for {t}")
    return STATEMENTS[t]


def has_mock(ticker: str) -> bool:
    return _resolve(ticker) in PROFILES


# ============================================================================
# 合成数据生成器：给任意 ticker 编一组合理的 5 年财务数据，标注为"演示数据"
# ============================================================================
import hashlib

# 行业典型财务结构模板（基于美股大类均值）
_INDUSTRY_TEMPLATES = {
    "Technology": dict(rev_base=50_000, growth=0.12, gross_m=0.55, ebit_m=0.25,
                       capex_pct=0.05, da_pct=0.04, nwc_pct=-0.02, tax=0.16, shares=2_000),
    "Healthcare": dict(rev_base=30_000, growth=0.08, gross_m=0.65, ebit_m=0.22,
                       capex_pct=0.06, da_pct=0.05, nwc_pct=0.05, tax=0.18, shares=1_500),
    "Financial Services": dict(rev_base=80_000, growth=0.06, gross_m=0.45, ebit_m=0.30,
                               capex_pct=0.03, da_pct=0.03, nwc_pct=0.0, tax=0.22, shares=3_000),
    "Consumer Cyclical": dict(rev_base=40_000, growth=0.10, gross_m=0.30, ebit_m=0.12,
                              capex_pct=0.06, da_pct=0.04, nwc_pct=0.08, tax=0.21, shares=1_200),
    "Consumer Defensive": dict(rev_base=60_000, growth=0.05, gross_m=0.35, ebit_m=0.15,
                                capex_pct=0.04, da_pct=0.03, nwc_pct=0.05, tax=0.20, shares=2_500),
    "Communication Services": dict(rev_base=70_000, growth=0.08, gross_m=0.55, ebit_m=0.28,
                                    capex_pct=0.10, da_pct=0.08, nwc_pct=0.02, tax=0.18, shares=2_800),
    "Industrials": dict(rev_base=35_000, growth=0.06, gross_m=0.28, ebit_m=0.13,
                        capex_pct=0.05, da_pct=0.04, nwc_pct=0.10, tax=0.22, shares=1_300),
    "Energy": dict(rev_base=100_000, growth=0.05, gross_m=0.30, ebit_m=0.18,
                   capex_pct=0.12, da_pct=0.09, nwc_pct=0.06, tax=0.25, shares=2_000),
    "Basic Materials": dict(rev_base=30_000, growth=0.05, gross_m=0.30, ebit_m=0.15,
                            capex_pct=0.08, da_pct=0.06, nwc_pct=0.12, tax=0.22, shares=1_000),
    "Real Estate": dict(rev_base=8_000, growth=0.07, gross_m=0.60, ebit_m=0.35,
                        capex_pct=0.20, da_pct=0.15, nwc_pct=0.02, tax=0.15, shares=800),
    "Utilities": dict(rev_base=25_000, growth=0.04, gross_m=0.45, ebit_m=0.20,
                      capex_pct=0.18, da_pct=0.10, nwc_pct=0.03, tax=0.20, shares=900),
}

_DEFAULT_TEMPLATE = _INDUSTRY_TEMPLATES["Technology"]


def _ticker_seed(ticker: str) -> float:
    """根据 ticker 字符生成一个 0.7-1.3 的稳定缩放因子，让不同公司数字不同。"""
    h = int(hashlib.md5(ticker.encode()).hexdigest()[:8], 16)
    return 0.7 + (h % 1000) / 1000 * 0.6  # 0.7-1.3


def _ticker_seed_shares(ticker: str) -> float:
    """独立 hash bit：让 shares outstanding 缩放与 revenue 不相关，
    这样隐含价（=equity/shares）才会真的因 ticker 不同。"""
    h = int(hashlib.md5(ticker.encode()).hexdigest()[8:16], 16)
    return 0.5 + (h % 1000) / 1000 * 2.0  # 0.5-2.5


def _ticker_seed_growth(ticker: str) -> float:
    """让增速也微调一下，使不同 ticker 估值结果差异更大。"""
    h = int(hashlib.md5(ticker.encode()).hexdigest()[16:24], 16)
    return 0.7 + (h % 1000) / 1000 * 0.6  # 0.7-1.3


def generate_synthetic_profile(ticker: str, sector: str | None = None,
                                industry: str | None = None) -> CompanyProfile:
    """为未知 ticker 生成合成 profile。优先查内置 ticker→sector 映射表，
    没命中再用调用方传入的 sector 或默认 Technology。"""
    from backend.data import ticker_sector
    t = ticker.upper()
    info = ticker_sector.lookup(t)
    if info:
        eff_sector, eff_industry, eff_name = info
    else:
        eff_sector = sector or "Technology"
        eff_industry = industry or "Diversified"
        eff_name = f"{t} Corporation"
    tpl = _INDUSTRY_TEMPLATES.get(eff_sector, _DEFAULT_TEMPLATE)
    scale = _ticker_seed(t)
    share_scale = _ticker_seed_shares(t)
    base_rev = tpl["rev_base"] * scale * (1 + tpl["growth"]) ** 5
    return CompanyProfile(
        ticker=t,
        name=eff_name,
        sector=eff_sector,
        industry=eff_industry,
        country="United States",
        currency="USD",
        market_cap=base_rev * 3.5,
        current_price=round(50 + scale * 100, 2),
        shares_outstanding=tpl["shares"] * share_scale,
    )


def generate_synthetic_statements(ticker: str, sector: str = "Technology") -> FinancialStatements:
    """为未知 ticker 生成 5 年合成历史财务数据。所有数字基于行业典型结构 + ticker 哈希缩放。"""
    t = ticker.upper()
    tpl = _INDUSTRY_TEMPLATES.get(sector, _DEFAULT_TEMPLATE)
    scale = _ticker_seed(t)
    growth_scale = _ticker_seed_growth(t)
    base_year = 2020
    history = []
    rev = tpl["rev_base"] * scale
    nwc_running = rev * tpl["nwc_pct"]
    for i in range(5):
        # 让增速逐年衰减一点点 + 每个 ticker 微调增速曲线
        g = tpl["growth"] * growth_scale * (1 - i * 0.05)
        if i > 0:
            rev = rev * (1 + g)
        gp = rev * tpl["gross_m"]
        ebit = rev * tpl["ebit_m"]
        da = rev * tpl["da_pct"]
        ebitda = ebit + da
        ni = ebit * (1 - tpl["tax"])
        capex = rev * tpl["capex_pct"]
        nwc_new = rev * tpl["nwc_pct"]
        ocf = ni + da
        fcf = ocf - capex
        history.append(YearData(
            year=base_year + i, revenue=round(rev, 1), gross_profit=round(gp, 1),
            ebit=round(ebit, 1), ebitda=round(ebitda, 1), net_income=round(ni, 1),
            total_assets=round(rev * 1.8, 1), total_debt=round(rev * 0.3, 1),
            cash=round(rev * 0.2, 1), equity=round(rev * 0.7, 1),
            operating_cf=round(ocf, 1), capex=round(capex, 1), da=round(da, 1),
            nwc=round(nwc_new, 1), fcf=round(fcf, 1),
        ))
        nwc_running = nwc_new

    return FinancialStatements(
        ticker=t, shares_outstanding=tpl["shares"] * _ticker_seed_shares(t),
        history=history, data_source="synthetic",
    )
