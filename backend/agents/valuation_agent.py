"""Module 3b: DCF 估值。"""
from backend.schemas import Forecast, FinancialStatements, CompanyProfile, DCFValuation
from backend.modeling import dcf as dcf_mod


def run(forecast: Forecast, stmts: FinancialStatements,
        profile: CompanyProfile) -> DCFValuation:
    return dcf_mod.run(forecast, stmts, profile)
