"""Markdown / HTML 报告输出。"""
from __future__ import annotations
from pathlib import Path
from backend.schemas import ResearchReport


def save_markdown(report: ResearchReport, path: Path) -> Path:
    path.write_text(report.markdown, encoding="utf-8")
    return path


def to_html(report: ResearchReport) -> str:
    """简易 Markdown→HTML 转换（不依赖额外包，足以浏览器预览）。"""
    md = report.markdown
    # 极简转换：标题、列表、表格、强调
    import re
    html = md
    html = re.sub(r"^### (.*)$", r"<h3>\1</h3>", html, flags=re.M)
    html = re.sub(r"^## (.*)$", r"<h2>\1</h2>", html, flags=re.M)
    html = re.sub(r"^# (.*)$", r"<h1>\1</h1>", html, flags=re.M)
    html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)
    html = html.replace("\n\n", "</p><p>")
    return f"""<!doctype html><html><head><meta charset='utf-8'>
<title>{report.company.ticker} Research Report</title>
<style>
body{{font-family:-apple-system,Segoe UI,Helvetica,Arial;max-width:900px;margin:40px auto;padding:0 20px;color:#222;line-height:1.6}}
h1{{color:#1F3864;border-bottom:3px solid #1F3864;padding-bottom:8px}}
h2{{color:#1F3864;margin-top:32px}}
table{{border-collapse:collapse;margin:12px 0}}
th,td{{border:1px solid #ccc;padding:6px 10px}}
th{{background:#1F3864;color:white}}
blockquote{{border-left:4px solid #1F3864;padding-left:16px;color:#555}}
</style></head><body><p>{html}</p></body></html>"""
