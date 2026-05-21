"""Module 1: 行业分析 Agent。"""
from backend.schemas import CompanyProfile, IndustryAnalysis
from backend.data.industry_kb import analyze_sector


def analyze(profile: CompanyProfile) -> IndustryAnalysis:
    """根据公司 sector 查询行业知识库。"""
    return analyze_sector(profile.sector)
