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
}


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
}


def get_mock_profile(ticker: str) -> CompanyProfile:
    """返回内置 profile，未知 ticker 抛 KeyError。"""
    t = ticker.upper()
    if t not in PROFILES:
        raise KeyError(f"No mock profile for {t}; supported: {list(PROFILES.keys())}")
    return PROFILES[t]


def get_mock_statements(ticker: str) -> FinancialStatements:
    t = ticker.upper()
    if t not in STATEMENTS:
        raise KeyError(f"No mock statements for {t}")
    return STATEMENTS[t]


def has_mock(ticker: str) -> bool:
    return ticker.upper() in PROFILES
