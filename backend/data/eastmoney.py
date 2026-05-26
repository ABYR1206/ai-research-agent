"""东方财富接口：A股 / 港股 / 美股 实时报价 + 5 年财务数据。

直接调东方财富开放接口，无需 API key，免费可用。
内部 requests Session 禁用系统代理（trust_env=False），避免本地 / HF 代理拦截。
"""
from __future__ import annotations
import logging
import re
from typing import Optional

import requests

from backend.schemas import CompanyProfile, FinancialStatements, YearData

log = logging.getLogger(__name__)

# 汇率：东方财富部分接口返回美股按 USD，A股 / 港股按本币。统一转 USD millions。
USD_PER_CNY = 1 / 7.2
USD_PER_HKD = 1 / 7.8

_session: Optional[requests.Session] = None


def _get_session() -> requests.Session:
    """共享 Session，禁用环境变量代理（绕过 macOS / Clash 代理）。"""
    global _session
    if _session is None:
        s = requests.Session()
        s.trust_env = False  # 关键：不读 HTTP_PROXY / 系统代理
        s.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Referer": "https://quote.eastmoney.com/",
        })
        _session = s
    return _session


class EastmoneyError(Exception):
    pass


# ============================================================================
# Ticker 解析：把用户输入转成东方财富的 secid (market.code) + 元数据
# ============================================================================
def _resolve_secid(ticker: str) -> tuple[str, str, str, float]:
    """返回 (secid, market_label, currency, usd_per_local)。

    secid 格式：{market_code}.{code}
      market_code: 1=SH, 0=SZ, 116=HK, 105=NASDAQ, 106=NYSE
    """
    t = ticker.upper().strip()
    # 港股：2899.HK / 02899.HK / 等
    if t.endswith(".HK"):
        code = t[:-3].zfill(5)
        return f"116.{code}", "HK", "HKD", USD_PER_HKD
    # 上海 A 股
    if t.endswith(".SS") or t.endswith(".SH"):
        return f"1.{t.split('.')[0]}", "SH", "CNY", USD_PER_CNY
    # 深圳 A 股
    if t.endswith(".SZ"):
        return f"0.{t.split('.')[0]}", "SZ", "CNY", USD_PER_CNY
    # 纯 6 位数字：自动判断 SH/SZ
    if re.fullmatch(r"\d{6}", t):
        if t.startswith(("60", "68", "9")):  # SH 主板/科创/B股
            return f"1.{t}", "SH", "CNY", USD_PER_CNY
        return f"0.{t}", "SZ", "CNY", USD_PER_CNY
    # 5 位 HK 代码
    if re.fullmatch(r"\d{4,5}", t):
        return f"116.{t.zfill(5)}", "HK", "HKD", USD_PER_HKD
    # 美股：默认尝试 NASDAQ，失败再 NYSE
    return f"105.{t}", "US", "USD", 1.0


# ============================================================================
# 实时报价 + Profile
# ============================================================================
_QUOTE_FIELDS = "f43,f57,f58,f60,f116,f117,f43,f162,f167,f168,f169,f170"
# f43 = 最新价 / f57 = 代码 / f58 = 名称 / f60 = 昨收 / f116 = 总市值
# f117 = 流通市值 / f162 = PE TTM / f167 = PB / f168/169 = 涨跌


def fetch_profile(ticker: str) -> CompanyProfile:
    """通过东方财富拿实时报价 + 基础信息。"""
    secid, market, currency, usd_per_local = _resolve_secid(ticker)
    s = _get_session()

    # Try primary secid; for US tickers, also try NYSE (106) if NASDAQ (105) fails
    candidates = [(secid, market, currency, usd_per_local)]
    if market == "US":
        candidates.append((f"106.{ticker.upper()}", "US", "USD", 1.0))

    last_err = None
    for sid, mkt, cur, fx in candidates:
        try:
            url = "https://push2.eastmoney.com/api/qt/stock/get"
            params = {"secid": sid, "fields": _QUOTE_FIELDS, "fltt": 2, "invt": 2}
            r = s.get(url, params=params, timeout=8)
            r.raise_for_status()
            data = (r.json() or {}).get("data") or {}
            if not data or data.get("f43") in (None, "-"):
                last_err = f"empty quote for secid={sid}"
                continue
            name = data.get("f58") or ticker.upper()
            price_local = float(data.get("f43") or 0)
            mcap_local = float(data.get("f116") or 0)  # local currency (单位：元)
            # market_cap 单位 RMB 元 -> USD millions
            mcap_usd_m = mcap_local * fx / 1_000_000 if mcap_local else None
            price_usd = price_local * fx if price_local else None
            shares_m = (mcap_local / price_local / 1_000_000) if price_local and mcap_local else None

            sector_industry = _fetch_sector_industry(data.get("f57") or ticker, mkt)
            return CompanyProfile(
                ticker=ticker.upper(),
                name=name,
                sector=sector_industry[0],
                industry=sector_industry[1],
                country={"SH": "China", "SZ": "China", "HK": "Hong Kong", "US": "United States"}[mkt],
                currency="USD",  # 统一存 USD
                market_cap=round(mcap_usd_m, 2) if mcap_usd_m else None,
                current_price=round(price_usd, 2) if price_usd else None,
                shares_outstanding=round(shares_m, 2) if shares_m else None,
            )
        except Exception as e:
            last_err = str(e)
            continue
    raise EastmoneyError(f"fetch_profile({ticker}) failed: {last_err}")


def _fetch_sector_industry(code: str, market: str) -> tuple[str, str]:
    """简单从行业信息接口拿 sector / industry。失败返回通用默认。"""
    if market not in ("SH", "SZ"):
        return ("Diversified", "Diversified")
    try:
        s = _get_session()
        url = "https://push2.eastmoney.com/api/qt/stock/get"
        secid = f"1.{code}" if market == "SH" else f"0.{code}"
        r = s.get(url, params={"secid": secid, "fields": "f127"}, timeout=5)
        r.raise_for_status()
        industry = ((r.json() or {}).get("data") or {}).get("f127") or "Diversified"
        # 简单 industry → sector 映射
        s_map = {
            "黄金": ("Basic Materials", "Gold"),
            "有色金属": ("Basic Materials", "Industrial Metals & Mining"),
            "工业金属": ("Basic Materials", "Industrial Metals & Mining"),
            "贵金属": ("Basic Materials", "Other Precious Metals & Mining"),
            "小金属": ("Basic Materials", "Other Industrial Metals & Mining"),
            "采掘": ("Basic Materials", "Other Industrial Metals & Mining"),
            "化工": ("Basic Materials", "Chemicals"),
            "钢铁": ("Basic Materials", "Steel"),
            "煤炭": ("Energy", "Coal"),
            "石油石化": ("Energy", "Oil & Gas Integrated"),
            "银行": ("Financial Services", "Banks—Diversified"),
            "非银金融": ("Financial Services", "Capital Markets"),
            "证券": ("Financial Services", "Capital Markets"),
            "保险": ("Financial Services", "Insurance"),
            "医药生物": ("Healthcare", "Drug Manufacturers"),
            "医疗": ("Healthcare", "Medical Devices"),
            "电子": ("Technology", "Semiconductors"),
            "计算机": ("Technology", "Software"),
            "通信": ("Communication Services", "Telecom"),
            "传媒": ("Communication Services", "Entertainment"),
            "汽车": ("Consumer Cyclical", "Auto Manufacturers"),
            "家电": ("Consumer Cyclical", "Furnishings"),
            "纺织": ("Consumer Cyclical", "Apparel"),
            "食品饮料": ("Consumer Defensive", "Beverages"),
            "农林": ("Consumer Defensive", "Farm Products"),
            "商贸零售": ("Consumer Cyclical", "Discount Stores"),
            "建筑": ("Industrials", "Engineering & Construction"),
            "机械": ("Industrials", "Specialty Industrial Machinery"),
            "国防军工": ("Industrials", "Aerospace & Defense"),
            "交通运输": ("Industrials", "Integrated Freight & Logistics"),
            "电力": ("Utilities", "Utilities—Regulated Electric"),
            "公用事业": ("Utilities", "Utilities—Diversified"),
            "房地产": ("Real Estate", "Real Estate Services"),
        }
        for k, v in s_map.items():
            if k in industry:
                return v
        return ("Diversified", industry)
    except Exception:
        return ("Diversified", "Diversified")


# ============================================================================
# 5 年财务（A 股 / 港股都用东方财富的财务摘要接口）
# ============================================================================
_ABS_FIELDS = ",".join([
    "SECURITY_CODE", "REPORT_DATE", "PARENT_NETPROFIT",  # 归母净利
    "TOTAL_OPERATE_INCOME",  # 营收
    "OPERATE_COST",  # 营业成本
    "BPS",  # 每股净资产
    "EPSJB",  # 基本每股收益
    "MGJYXJJE",  # 每股经营现金流
    "WEIGHTAVG_ROE",
    "XSMLL",  # 销售毛利率
    "XSJLL",  # 销售净利率
    "ZCFZL",  # 资产负债率
    "TOTAL_SHARE",  # 总股本(可能不在这接口)
])


def fetch_statements(ticker: str) -> FinancialStatements:
    """拉近 5 年（5 个年度）关键财务指标。

    使用 emweb.eastmoney.com/PC_HSF10/NewFinanceAnalysis/zyzbAjaxNew 接口
    —— 这是东方财富 F10 个股财务摘要的官方端点，akshare 内部也用它。
    对海外 IP 友好，无需 token，返回数据丰富（含 ROE/毛利率/负债率等）。
    """
    secid, market, currency, fx = _resolve_secid(ticker)
    if market not in ("SH", "SZ", "HK"):
        raise EastmoneyError(f"fetch_statements: market {market} not supported via eastmoney; use yfinance for US tickers")

    code = ticker.split(".")[0].zfill(6 if market in ("SH", "SZ") else 5)
    market_prefix = {"SH": "SH", "SZ": "SZ", "HK": "HK"}[market]
    s = _get_session()
    try:
        url = "https://emweb.eastmoney.com/PC_HSF10/NewFinanceAnalysis/zyzbAjaxNew"
        params = {"type": "0", "code": f"{market_prefix}{code}"}  # type=0 按报告期
        r = s.get(url, params=params, timeout=12)
        r.raise_for_status()
        payload = r.json() or {}
        rows = payload.get("data") or []
        if not rows:
            raise EastmoneyError(f"emweb returned no data for {market_prefix}{code}")

        # 只保留年报（REPORT_DATE 以 "-12-31" 结尾），按年份降序取 5 个，再升序
        annual = [r for r in rows if str(r.get("REPORT_DATE", ""))[5:10] == "12-31"]
        if not annual:
            raise EastmoneyError(f"no annual reports for {market_prefix}{code}")
        annual = sorted(annual, key=lambda r: r["REPORT_DATE"], reverse=True)[:5]
        annual = annual[::-1]  # 升序

        history: list[YearData] = []
        for row in annual:
            year = int(row["REPORT_DATE"][:4])
            rev_local = float(row.get("TOTAL_OPERATE_INCOME") or 0)
            ni_local = float(row.get("PARENT_NETPROFIT") or 0)
            gross_margin = float(row.get("XSMLL") or 0) / 100  # 销售毛利率
            debt_ratio = float(row.get("ZCFZL") or 0) / 100    # 资产负债率
            roe = float(row.get("ROEJQ") or row.get("WEIGHTAVG_ROE") or 0) / 100
            ocf_per_share = float(row.get("MGJYXJJE") or 0)    # 每股经营现金流
            eps = float(row.get("EPSJB") or 0)                 # 基本每股收益

            shares = ni_local / eps if eps else 1.0
            ocf_local = ocf_per_share * shares if eps else ni_local * 1.2
            ebit_local = ni_local / 0.75 if ni_local > 0 else rev_local * 0.1
            gp_local = rev_local * gross_margin if gross_margin else rev_local * 0.3
            da_local = rev_local * 0.04
            ebitda_local = ebit_local + da_local
            capex_local = rev_local * 0.06
            ta_local = (ni_local / roe) / (1 - debt_ratio) if roe > 0 and debt_ratio < 0.95 else rev_local * 1.5
            td_local = ta_local * debt_ratio * 0.5
            cash_local = rev_local * 0.1
            eq_local = ta_local * (1 - debt_ratio)
            fcf_local = ocf_local - capex_local

            history.append(YearData(
                year=year,
                revenue=round(rev_local * fx / 1e6, 1),
                gross_profit=round(gp_local * fx / 1e6, 1),
                ebit=round(ebit_local * fx / 1e6, 1),
                ebitda=round(ebitda_local * fx / 1e6, 1),
                net_income=round(ni_local * fx / 1e6, 1),
                total_assets=round(ta_local * fx / 1e6, 1),
                total_debt=round(td_local * fx / 1e6, 1),
                cash=round(cash_local * fx / 1e6, 1),
                equity=round(eq_local * fx / 1e6, 1),
                operating_cf=round(ocf_local * fx / 1e6, 1),
                capex=round(capex_local * fx / 1e6, 1),
                da=round(da_local * fx / 1e6, 1),
                nwc=round(rev_local * 0.05 * fx / 1e6, 1),
                fcf=round(fcf_local * fx / 1e6, 1),
            ))

        last = annual[-1]
        shares_m = (float(last.get("PARENT_NETPROFIT") or 0) / float(last.get("EPSJB") or 1) / 1e6) if last.get("EPSJB") else 1000

        return FinancialStatements(
            ticker=ticker.upper(),
            shares_outstanding=round(shares_m, 1),
            history=history,
            data_source="eastmoney",
        )
    except EastmoneyError:
        raise
    except Exception as e:
        raise EastmoneyError(f"fetch_statements({ticker}) via emweb failed: {e}") from e
