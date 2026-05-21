"""单独跑 Module 1 / Module 2 的 API。"""
from fastapi import APIRouter, HTTPException

from backend.schemas import IndustryAnalysis, CompanyAnalysis
from backend.agents import industry_agent, company_agent, orchestrator
from backend.data import fetcher, mock_data

router = APIRouter()


@router.post("/analyze/industry", response_model=IndustryAnalysis)
def analyze_industry(ticker: str, source: str = "auto"):
    try:
        profile = orchestrator._get_profile(ticker.upper(), source, [])
        return industry_agent.analyze(profile)
    except Exception as e:
        raise HTTPException(400, str(e))


@router.post("/analyze/company", response_model=CompanyAnalysis)
def analyze_company(ticker: str, source: str = "auto"):
    try:
        profile = orchestrator._get_profile(ticker.upper(), source, [])
        return company_agent.analyze(profile)
    except Exception as e:
        raise HTTPException(400, str(e))
