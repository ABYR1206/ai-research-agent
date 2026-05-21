"""财务三表抽取 + DCF 单独接口。"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.schemas import (
    FinancialStatements, FinancialMetrics, DCFValuation,
    ForecastAssumptions, Forecast,
)
from backend.agents import finance_agent, valuation_agent, orchestrator

router = APIRouter()


class ExtractResponse(BaseModel):
    statements: FinancialStatements
    metrics: FinancialMetrics


@router.post("/financial/extract", response_model=ExtractResponse)
def extract(ticker: str, source: str = "auto"):
    try:
        stmts, _ = finance_agent.get_statements(ticker.upper(), source)
        metrics = finance_agent.compute_metrics(stmts)
        return ExtractResponse(statements=stmts, metrics=metrics)
    except Exception as e:
        raise HTTPException(400, str(e))


class DCFRequest(BaseModel):
    ticker: str
    source: str = "auto"
    assumptions: ForecastAssumptions | None = None


class DCFResponse(BaseModel):
    forecast: Forecast
    dcf: DCFValuation


@router.post("/valuation/dcf", response_model=DCFResponse)
def run_dcf(req: DCFRequest):
    try:
        profile = orchestrator._get_profile(req.ticker.upper(), req.source, [])
        stmts, _ = finance_agent.get_statements(req.ticker.upper(), req.source)
        metrics = finance_agent.compute_metrics(stmts)
        forecast = finance_agent.build_forecast(stmts, metrics, req.assumptions)
        dcf = valuation_agent.run(forecast, stmts, profile)
        return DCFResponse(forecast=forecast, dcf=dcf)
    except Exception as e:
        raise HTTPException(400, str(e))
