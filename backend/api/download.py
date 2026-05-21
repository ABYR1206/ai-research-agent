"""文件下载接口。"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, HTMLResponse

from backend.config import EXCEL_DIR, REPORT_DIR
from backend.outputs.report_builder import to_html
from backend.schemas import ResearchReport

router = APIRouter()


@router.get("/download/excel/{file_id}")
def download_excel(file_id: str):
    path = EXCEL_DIR / f"{file_id}.xlsx"
    if not path.exists():
        raise HTTPException(404, "Excel file not found")
    return FileResponse(
        path,
        filename=f"{file_id}.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@router.get("/download/report/{file_id}")
def download_report(file_id: str):
    path = REPORT_DIR / f"{file_id}.md"
    if not path.exists():
        raise HTTPException(404, "Report not found")
    return FileResponse(path, filename=f"{file_id}.md", media_type="text/markdown")


@router.get("/download/report/{file_id}/html", response_class=HTMLResponse)
def view_report_html(file_id: str):
    path = REPORT_DIR / f"{file_id}.md"
    if not path.exists():
        raise HTTPException(404, "Report not found")
    md = path.read_text(encoding="utf-8")
    from backend.schemas import CompanyProfile, ReportSections
    fake = ResearchReport(
        company=CompanyProfile(ticker=file_id.split("_")[0], name=file_id, sector="", industry=""),
        sections=ReportSections(thesis="", overview="", industry="", business="",
                                 financial="", valuation="", risks="", conclusion=""),
        markdown=md,
    )
    return to_html(fake)
