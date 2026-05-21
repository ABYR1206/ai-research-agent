"""一键全流程：/report/generate。"""
from fastapi import APIRouter, HTTPException

from backend.schemas import GenerateRequest, GenerateResponse
from backend.agents import orchestrator

router = APIRouter()


@router.post("/report/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest):
    try:
        return orchestrator.run(req.ticker, req.source, req.assumptions)
    except KeyError as e:
        raise HTTPException(404, f"Unknown ticker: {e}")
    except Exception as e:
        raise HTTPException(500, f"Pipeline failed: {e}")
