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
        sector="Basic Materials", industry="Copper & Gold Mining",
        country="China", currency="USD",
        market_cap=66_390, current_price=2.50, shares_outstanding=26_556.0,
    ),
    "MOUTAI": CompanyProfile(
        ticker="MOUTAI", name="Kweichow Moutai Co., Ltd. (贵州茅台)",
        sector="Consumer Defensive", industry="Beverages—Wineries & Distilleries",
        country="China", currency="USD",
        market_cap=261_320, current_price=208.0, shares_outstanding=1_256.0,
    ),
    "TENCENT": CompanyProfile(
        ticker="TENCENT", name="Tencent Holdings Ltd. (腾讯控股)",
        sector="Communication Services", industry="Internet Content & Information",
        country="Hong Kong", currency="USD",
        market_cap=455_700, current_price=49.0, shares_outstanding=9_300.0,
    ),
    "ICBC": CompanyProfile(
        ticker="ICBC", name="Industrial and Commercial Bank of China (工商银行)",
        sector="Financial Services", industry="Banks—Diversified",
        country="China", currency="USD",
        market_cap=345_714, current_price=0.97, shares_outstanding=356_406.0,
    ),
    "CATL": CompanyProfile(
        ticker="CATL", name="Contemporary Amperex Technology (宁德时代)",
        sector="Industrials", industry="Electrical Equipment & Parts",
        country="China", currency="USD",
        market_cap=154_000, current_price=35.0, shares_outstanding=4_400.0,
    ),
    "BYD": CompanyProfile(
        ticker="BYD", name="BYD Company Limited (比亚迪)",
        sector="Consumer Cyclical", industry="Auto Manufacturers",
        country="China", currency="USD",
        market_cap=113_490, current_price=39.0, shares_outstanding=2_910.0,
    ),
    "PINGAN": CompanyProfile(
        ticker="PINGAN", name="Ping An Insurance Group (中国平安)",
        sector="Financial Services", industry="Insurance—Diversified",
        country="China", currency="USD",
        market_cap=126_377, current_price=6.94, shares_outstanding=18_210.0,
    ),
    "BABA": CompanyProfile(
        ticker="BABA", name="Alibaba Group Holding Limited (阿里巴巴)",
        sector="Consumer Cyclical", industry="Internet Retail",
        country="China", currency="USD",
        market_cap=248_840, current_price=102.8, shares_outstanding=2_420.0,
    ),
    "HENGRUI": CompanyProfile(
        ticker="HENGRUI", name="Jiangsu Hengrui Pharmaceuticals (恒瑞医药)",
        sector="Healthcare", industry="Drug Manufacturers—Specialty",
        country="China", currency="USD",
        market_cap=44_277, current_price=6.94, shares_outstanding=6_380.0,
    ),
}

# 全量真实 mock 公司：所有市场代码统一映射到标准内部 ticker
_TICKER_ALIAS = {
    # 紫金矿业
    "2899.HK": "ZJMGF", "02899.HK": "ZJMGF", "2899": "ZJMGF",
    "601899.SS": "ZJMGF", "601899.SH": "ZJMGF", "601899": "ZJMGF",
    "ZIJINMINING": "ZJMGF",
    # 贵州茅台
    "600519.SS": "MOUTAI", "600519.SH": "MOUTAI", "600519": "MOUTAI",
    "MOUTAI.SS": "MOUTAI", "KWEICHOWMOUTAI": "MOUTAI", "茅台": "MOUTAI",
    # 腾讯控股
    "0700.HK": "TENCENT", "00700.HK": "TENCENT", "0700": "TENCENT",
    "00700": "TENCENT", "700.HK": "TENCENT", "TCEHY": "TENCENT",
    "腾讯": "TENCENT",
    # 工商银行
    "601398.SS": "ICBC", "601398.SH": "ICBC", "601398": "ICBC",
    "1398.HK": "ICBC", "01398.HK": "ICBC", "IDCBY": "ICBC",
    "工商银行": "ICBC",
    # 宁德时代
    "300750.SZ": "CATL", "300750": "CATL", "CATLBATTERY": "CATL",
    "宁德时代": "CATL",
    # 比亚迪
    "002594.SZ": "BYD", "002594": "BYD",
    "1211.HK": "BYD", "01211.HK": "BYD", "BYDDY": "BYD", "BYDDF": "BYD",
    "比亚迪": "BYD",
    # 中国平安
    "601318.SS": "PINGAN", "601318.SH": "PINGAN", "601318": "PINGAN",
    "2318.HK": "PINGAN", "02318.HK": "PINGAN", "PNGAY": "PINGAN",
    "平安": "PINGAN", "中国平安": "PINGAN",
    # 阿里巴巴
    "9988.HK": "BABA", "09988.HK": "BABA",
    "BABA.US": "BABA", "ALIBABA": "BABA", "阿里巴巴": "BABA", "阿里": "BABA",
    # 恒瑞医药
    "600276.SS": "HENGRUI", "600276.SH": "HENGRUI", "600276": "HENGRUI",
    "1276.HK": "HENGRUI", "01276.HK": "HENGRUI",
    "恒瑞": "HENGRUI", "恒瑞医药": "HENGRUI",
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
            # 2025 数据来自 2025 年报：营收 3491 亿 RMB / 归母净利 518 亿 / OCF 754 亿 / TA 3966 亿
            _yd(2021, 32157, 7080, 5145,  6174,  2243, 28286, 12000, 2050, 9000, 3729, 3000, 1029, 2800),
            _yd(2022, 38614, 8495, 6178,  7664,  2857, 35430, 16000, 2286, 12000, 4100, 4000, 1486, 3200),
            _yd(2023, 41914, 9221, 6707,  8622,  3014, 49143, 25000, 3357, 17000, 5271, 4071, 1915, 3700),
            _yd(2024, 43371, 9974, 8030,  10244, 4579, 56657, 31164, 4429, 25500, 6980, 4214, 2214, 4600),
            _yd(2025, 48483, 13444, 10666, 13333, 7191, 55083, 35000, 5333, 25521, 10472, 4848, 2667, 5818),
        ],
    ),
    # 贵州茅台：高毛利(~92%)、轻资产、几乎无负债、现金巨多。RMB→USD/7.2
    "MOUTAI": FinancialStatements(
        ticker="MOUTAI", shares_outstanding=1_256.0, data_source="mock",
        history=[
            # 2025 数据来自 2025 年报：营收总 1721 亿 RMB（首次下降）/ 归母净利 823 亿 / OCF 615 亿
            _yd(2021, 15208, 13991, 10650, 10870, 7292,  34000, 360, 19500, 27000, 7747, 304, 220,  4800),
            _yd(2022, 17236, 15897, 12100, 12330, 8708,  39500, 400, 22500, 31500, 9054, 345, 230,  5500),
            _yd(2023, 20514, 18933, 14550, 14800, 10375, 47000, 410, 26500, 37000, 11000, 410, 250, 6500),
            _yd(2024, 24181, 22321, 17300, 17580, 12028, 55500, 425, 31000, 43500, 13000, 484, 280, 7700),
            _yd(2025, 23896, 21983, 15294, 15581, 11433, 58275, 425, 32000, 46000, 8545,  478, 287, 1195),
        ],
    ),
    # 腾讯：互联网平台，订阅+广告+游戏。RMB→USD/7.2
    "TENCENT": FinancialStatements(
        ticker="TENCENT", shares_outstanding=9_300.0, data_source="mock",
        history=[
            # 2025 数据基于 Q3 +15% YoY + 全年估算：营收 ~7,580 亿 RMB / Non-IFRS NI ~2,800 亿
            _yd(2021, 77792, 33950, 30700, 35000, 31222, 215000, 35000, 24500, 124000, 32700, 5460, 4300, 12500),
            _yd(2022, 77028, 33330, 26100, 31200, 26139, 212000, 36000, 23000, 130000, 32500, 4622, 5100, 11800),
            _yd(2023, 84583, 40990, 32600, 38400, 16000, 220000, 35500, 24500, 138000, 31500, 5075, 5800, 12800),
            _yd(2024, 91708, 47650, 36500, 42700, 26958, 235000, 36000, 27500, 152000, 38400, 5500, 6200, 14000),
            _yd(2025, 105278, 56055, 44500, 51000, 32350, 252000, 38000, 30000, 168000, 45000, 6200, 6500, 15000),
        ],
    ),
    # 工商银行：DCF 中 total_debt 只算批发融资（bonds + interbank），不算存款。
    # cash 含 央行准备金。RMB→USD/7.2
    "ICBC": FinancialStatements(
        ticker="ICBC", shares_outstanding=356_406.0, data_source="mock",
        history=[
            # 2025 数据来自年报：营收 8,383 亿 RMB / 归母净利 3,686 亿 / 总资产 53.48 万亿 RMB (+9.5%)
            _yd(2021, 130319, 51000, 60500, 61500, 48375, 5100000, 65000, 380000, 410000, 60000, 12500, 5300, 0),
            _yd(2022, 127389, 50800, 62500, 63500, 50069, 5400000, 68000, 410000, 440000, 62000, 13000, 5500, 0),
            _yd(2023, 116903, 47200, 63000, 64000, 50708, 5650000, 70000, 440000, 470000, 63000, 13500, 5800, 0),
            _yd(2024, 114194, 46100, 63500, 64500, 50819, 5900000, 72000, 470000, 500000, 64000, 14000, 6000, 0),
            _yd(2025, 116426, 47000, 64500, 65500, 51495, 7000000, 75000, 500000, 530000, 65000, 14500, 6200, 0),
        ],
    ),
    # 宁德时代：动力电池龙头，资本开支极重。RMB→USD/7.2
    "CATL": FinancialStatements(
        ticker="CATL", shares_outstanding=4_400.0, data_source="mock",
        history=[
            # 2025 数据来自年报：营收 4,237 亿 RMB (+17%) / 归母净利 722 亿 (+42%) / OCF 1,332 亿
            _yd(2021, 18111, 4500, 2750,  3700, 2208,  25000, 4200, 7800, 8400, 5300, 1750, 950,  1700),
            _yd(2022, 45639, 9200, 5400,  7400, 4264,  45500, 9500, 16500, 13500, 8700, 4200, 2000, 4300),
            _yd(2023, 55681, 13100, 7800, 10800, 6125, 53000, 11200, 19500, 18000, 12300, 4800, 3000, 5300),
            _yd(2024, 50278, 12550, 8800, 12000, 7042, 56500, 11800, 22000, 21500, 13500, 4500, 3200, 4800),
            _yd(2025, 58847, 15459, 13371, 16902, 10028, 65000, 13500, 25000, 26000, 18503, 4708, 3531, 5885),
        ],
    ),
    # 比亚迪：电动车 + 电池。td 只算有息负债；Capex 取经常性水平（去掉扩产期 one-off）。RMB→USD/7.2
    "BYD": FinancialStatements(
        ticker="BYD", shares_outstanding=2_910.0, data_source="mock",
        history=[
            # 2025 数据来自年报：营收 8,040 亿 RMB (+3.5%) / 归母净利 326 亿 / OCF 591 亿 / 现金 1,678 亿
            _yd(2021, 30014, 4050, 2700,  4300, 417,  41500, 5500, 2500, 8200, 4500, 2100, 1600, 3000),
            _yd(2022, 58903, 10000, 6400, 9200, 2306, 65500, 7000, 6900, 10500, 19400, 4500, 2800, 5900),
            _yd(2023, 83653, 16800, 11500, 15800, 4167, 88500, 8500, 11500, 14800, 23800, 6000, 4300, 8400),
            _yd(2024, 107931, 21500, 16800, 22800, 5597, 106000, 9500, 15500, 20000, 27000, 7500, 6000, 10800),
            _yd(2025, 111662, 20099, 6038, 12700, 4530, 122000, 10000, 23306, 23500, 8213, 6700, 6700, 11166),
        ],
    ),
    # 中国平安：DCF 中 td 只算有息负债（保单准备金不算）。RMB→USD/7.2
    "PINGAN": FinancialStatements(
        ticker="PINGAN", shares_outstanding=18_210.0, data_source="mock",
        history=[
            # 2025 数据来自年报：营收 10,505 亿 RMB (+2.1%) / 归母净利 1,348 亿 (+6.5%)
            _yd(2021, 163944, 64500, 19200, 21500, 14111, 1330000, 30000, 78000, 120000, 23000, 3300, 2300, 0),
            _yd(2022, 154250, 60500, 15800, 18000, 11639, 1380000, 32000, 80000, 130000, 19500, 3100, 2200, 0),
            _yd(2023, 168472, 65500, 16200, 18800, 11903, 1450000, 34000, 85000, 135000, 20000, 3300, 2600, 0),
            _yd(2024, 174819, 68500, 23800, 26500, 17583, 1530000, 36000, 92000, 145000, 28500, 3600, 2700, 0),
            _yd(2025, 145904, 58000, 26200, 29000, 18719, 1600000, 38000, 100000, 156000, 35000, 3900, 2900, 0),
        ],
    ),
    # 阿里巴巴：电商 + 云。财年 4-3 月制。RMB→USD/7.2
    "BABA": FinancialStatements(
        ticker="BABA", shares_outstanding=2_420.0, data_source="mock",
        history=[
            _yd(2021, 99625,  41600, 25700, 32000, 20889, 250000, 22000, 70000, 145000, 32500, 6800, 6300, 12500),
            _yd(2022, 118486, 43500, 11100, 18000, 8597,  264000, 25500, 67000, 145000, 26500, 9200, 6900, 13500),
            _yd(2023, 120653, 44900, 13500, 20500, 10111, 270000, 27500, 70000, 152000, 27500, 7100, 7000, 14000),
            _yd(2024, 130722, 49500, 14300, 22000, 11069, 286000, 30000, 80000, 165000, 30500, 7800, 7700, 15000),
            _yd(2025, 138375, 53300, 22500, 30500, 17278, 305000, 31000, 84000, 178000, 35000, 8200, 8000, 15800),
        ],
    ),
    # 恒瑞医药：创新药龙头，高研发投入。RMB→USD/7.2
    "HENGRUI": FinancialStatements(
        ticker="HENGRUI", shares_outstanding=6_380.0, data_source="mock",
        history=[
            # 2025 数据来自年报：营收 316 亿 RMB (+13%) / 归母净利 77.11 亿 (+21.7%)
            _yd(2021, 3597, 3120, 820,  990,  625,  4900, 95, 1220, 4350, 700,  170, 170, 750),
            _yd(2022, 2958, 2540, 720,  900,  542,  4950, 90, 1280, 4500, 620,  155, 180, 650),
            _yd(2023, 3167, 2710, 800,  990,  597,  5100, 92, 1380, 4750, 680,  165, 190, 700),
            _yd(2024, 3875, 3340, 1120, 1330, 875,  5400, 95, 1500, 5050, 920,  175, 210, 850),
            _yd(2025, 4393, 3795, 1390, 1620, 1071, 5800, 100, 1700, 5500, 1100, 195, 230, 950),
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
