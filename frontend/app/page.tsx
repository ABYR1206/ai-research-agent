"use client";
import { useState } from "react";
import InputPanel from "./components/InputPanel";
import ResultTabs from "./components/ResultTabs";
import DownloadBar from "./components/DownloadBar";
import { generateReport } from "@/lib/api";

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleGenerate(ticker: string, source: string) {
    setLoading(true); setError(null);
    try {
      const data = await generateReport(ticker, source);
      setResult(data);
    } catch (e: any) {
      setError(e?.response?.data?.detail || e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="max-w-6xl mx-auto p-6 space-y-6">
      <header className="text-center pt-4 pb-2">
        <h1 className="text-4xl font-extrabold text-brand">AI Research Agent</h1>
        <p className="text-slate-500 mt-2">自动生成行业 · 公司 · 财务 · DCF 估值的分析师研究报告</p>
      </header>

      <InputPanel onGenerate={handleGenerate} loading={loading} />

      {error && (
        <div className="bg-red-50 border border-red-300 text-red-700 rounded-lg p-4">
          ❌ {error}
        </div>
      )}

      {loading && (
        <div className="bg-white rounded-2xl shadow p-12 text-center text-slate-500">
          <div className="animate-spin inline-block w-8 h-8 border-4 border-brand border-t-transparent rounded-full"></div>
          <div className="mt-4">Agent 编排中：行业 → 公司 → 财务 → 预测 → DCF → Excel → 报告...</div>
        </div>
      )}

      {result && !loading && (
        <>
          <section className="bg-gradient-to-r from-brand to-brand-light rounded-2xl p-6 text-white shadow-lg">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
              <div>
                <div className="text-sm opacity-80">{result.profile.sector} / {result.profile.industry}</div>
                <h2 className="text-3xl font-bold">{result.profile.name} ({result.profile.ticker})</h2>
                <div className="text-sm opacity-90 mt-1">
                  当前价 ${result.profile.current_price?.toFixed(2) || "N/A"} · 隐含价 ${result.dcf.implied_price?.toFixed(2)} ·
                  上行 {result.dcf.upside !== null ? `${(result.dcf.upside * 100).toFixed(1)}%` : "N/A"}
                </div>
              </div>
              <DownloadBar fileId={result.excel_file_id} />
            </div>
            {result.data_gaps.length > 0 && (
              <div className="mt-3 text-xs bg-yellow-200/20 rounded p-2">
                ⚠️ 数据提示：{result.data_gaps.join(" / ")}
              </div>
            )}
          </section>

          <ResultTabs result={result} />
        </>
      )}

      <footer className="text-center text-xs text-slate-400 py-4">
        AI Research Agent v0.1 · 课程演示项目 · 数据仅供研究参考，不构成投资建议
      </footer>
    </main>
  );
}
