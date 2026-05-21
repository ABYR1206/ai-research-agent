"use client";
import { useState } from "react";
import FinancialTable from "./FinancialTable";
import ValuationCard from "./ValuationCard";

const TABS = ["行业分析", "公司分析", "财务分析", "估值与报告"] as const;

export default function ResultTabs({ result }: { result: any }) {
  const [tab, setTab] = useState<typeof TABS[number]>("估值与报告");
  const { industry, company, statements, metrics, forecast, dcf, report } = result;

  return (
    <section className="bg-white rounded-2xl shadow-lg border border-slate-200 overflow-hidden">
      <div className="flex border-b border-slate-200 bg-slate-50">
        {TABS.map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`px-5 py-3 text-sm font-semibold transition ${
              tab === t ? "bg-white text-brand border-b-2 border-brand" : "text-slate-500 hover:text-brand"
            }`}
          >{t}</button>
        ))}
      </div>

      <div className="p-6 max-h-[70vh] overflow-y-auto">
        {tab === "行业分析" && <IndustryView data={industry} />}
        {tab === "公司分析" && <CompanyView data={company} />}
        {tab === "财务分析" && <FinancialTable stmts={statements} metrics={metrics} forecast={forecast} />}
        {tab === "估值与报告" && (
          <div className="space-y-6">
            <ValuationCard dcf={dcf} />
            <details className="bg-slate-50 rounded-lg p-4 border">
              <summary className="cursor-pointer font-semibold text-brand">📄 查看完整 Markdown 报告</summary>
              <pre className="mt-3 whitespace-pre-wrap text-xs leading-relaxed">{report.markdown}</pre>
            </details>
          </div>
        )}
      </div>
    </section>
  );
}

function IndustryView({ data }: { data: any }) {
  return (
    <div className="space-y-4 text-slate-700">
      <Section title="行业定义">{data.definition}</Section>
      <Section title="市场规模">{data.market_size}</Section>
      <Section title="增长驱动因素"><ul className="list-disc pl-5">{data.growth_drivers.map((d: string, i: number) => <li key={i}>{d}</li>)}</ul></Section>
      <Section title="竞争格局">{data.landscape}</Section>
      <Section title="主要参与者">{data.key_players.join(" · ")}</Section>
      <Section title="行业风险"><ul className="list-disc pl-5">{data.risks.map((d: string, i: number) => <li key={i}>{d}</li>)}</ul></Section>
      <Section title="未来 3-5 年展望">{data.outlook}</Section>
    </div>
  );
}

function CompanyView({ data }: { data: any }) {
  return (
    <div className="space-y-4 text-slate-700">
      <Section title="公司概览">{data.overview}</Section>
      <Section title="主营业务"><ul className="list-disc pl-5">{data.business_segments.map((d: string, i: number) => <li key={i}>{d}</li>)}</ul></Section>
      <Section title="收入结构">{data.revenue_mix}</Section>
      <Section title="商业模式">{data.business_model}</Section>
      <Section title="核心竞争力（护城河）"><ul className="list-disc pl-5">{data.moat.map((d: string, i: number) => <li key={i}>{d}</li>)}</ul></Section>
      <Section title="主要竞争对手">{data.competitors.join(" · ")}</Section>
      <div className="grid grid-cols-2 gap-3">
        <SWOTBox color="bg-emerald-50 border-emerald-300" title="S 优势" items={data.swot.strengths} />
        <SWOTBox color="bg-orange-50 border-orange-300" title="W 劣势" items={data.swot.weaknesses} />
        <SWOTBox color="bg-blue-50 border-blue-300" title="O 机会" items={data.swot.opportunities} />
        <SWOTBox color="bg-red-50 border-red-300" title="T 威胁" items={data.swot.threats} />
      </div>
      <Section title="公司风险"><ul className="list-disc pl-5">{data.risks.map((d: string, i: number) => <li key={i}>{d}</li>)}</ul></Section>
    </div>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div>
      <h3 className="font-bold text-brand mb-1">{title}</h3>
      <div>{children}</div>
    </div>
  );
}

function SWOTBox({ color, title, items }: { color: string; title: string; items: string[] }) {
  return (
    <div className={`rounded-lg border p-3 ${color}`}>
      <div className="font-bold mb-1">{title}</div>
      <ul className="list-disc pl-5 text-sm">{items.map((s, i) => <li key={i}>{s}</li>)}</ul>
    </div>
  );
}
