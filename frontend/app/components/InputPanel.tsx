"use client";
import { useState } from "react";

interface Props {
  onGenerate: (ticker: string, source: string) => void;
  loading: boolean;
}

const PRESETS = ["AAPL", "TSLA", "NVDA", "TSM"];

export default function InputPanel({ onGenerate, loading }: Props) {
  const [ticker, setTicker] = useState("AAPL");
  const [source, setSource] = useState("auto");

  return (
    <section className="bg-white rounded-2xl shadow-lg p-6 border border-slate-200">
      <h2 className="text-lg font-bold text-brand mb-4">输入参数</h2>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="md:col-span-1">
          <label className="block text-sm font-semibold text-slate-700 mb-1">股票代码</label>
          <input
            value={ticker}
            onChange={(e) => setTicker(e.target.value.toUpperCase())}
            className="w-full border border-slate-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-brand outline-none"
            placeholder="AAPL / TSLA / NVDA / TSM"
          />
          <div className="flex gap-2 mt-2 flex-wrap">
            {PRESETS.map((t) => (
              <button
                key={t}
                onClick={() => setTicker(t)}
                className="text-xs px-2 py-1 rounded bg-slate-100 hover:bg-brand hover:text-white transition"
              >{t}</button>
            ))}
          </div>
        </div>

        <div className="md:col-span-1">
          <label className="block text-sm font-semibold text-slate-700 mb-1">数据源</label>
          <select
            value={source}
            onChange={(e) => setSource(e.target.value)}
            className="w-full border border-slate-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-brand outline-none"
          >
            <option value="auto">自动（推荐）：东方财富 实时 → yfinance → Mock → 合成兜底</option>
            <option value="eastmoney">仅东方财富（A 股 / 港股 / 美股 实时）</option>
            <option value="mock">Mock + 合成数据（演示最稳）</option>
            <option value="yfinance">仅 yfinance（部分公司可能失败）</option>
          </select>
        </div>

        <div className="md:col-span-1 flex items-end">
          <button
            disabled={loading || !ticker}
            onClick={() => onGenerate(ticker, source)}
            className="w-full bg-brand hover:bg-brand-dark text-white font-semibold py-2.5 rounded-lg disabled:opacity-50 transition"
          >
            {loading ? "生成中... (约 5-15 秒)" : "🚀 生成研究报告"}
          </button>
        </div>
      </div>
    </section>
  );
}
