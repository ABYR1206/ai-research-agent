"use client";
import { downloadExcelUrl, downloadReportUrl, viewReportHtmlUrl } from "@/lib/api";

export default function DownloadBar({ fileId }: { fileId: string }) {
  return (
    <div className="flex flex-wrap gap-3">
      <a href={downloadExcelUrl(fileId)} download
         className="bg-emerald-600 hover:bg-emerald-700 text-white px-4 py-2 rounded-lg font-semibold shadow">
        ⬇ 下载 DCF Excel 模型
      </a>
      <a href={downloadReportUrl(fileId)} download
         className="bg-brand hover:bg-brand-dark text-white px-4 py-2 rounded-lg font-semibold shadow">
        ⬇ 下载 Markdown 报告
      </a>
      <a href={viewReportHtmlUrl(fileId)} target="_blank" rel="noreferrer"
         className="bg-slate-700 hover:bg-slate-800 text-white px-4 py-2 rounded-lg font-semibold shadow">
        🔍 浏览器预览报告
      </a>
    </div>
  );
}
