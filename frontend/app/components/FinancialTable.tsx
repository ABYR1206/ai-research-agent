"use client";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, Legend } from "recharts";

const fmtM = (x: number) => (x || 0).toLocaleString(undefined, { maximumFractionDigits: 0 });
const fmtPct = (x: number) => `${(x * 100).toFixed(1)}%`;

export default function FinancialTable({ stmts, metrics, forecast }: any) {
  const histChart = stmts.history.map((y: any) => ({ year: y.year, Revenue: y.revenue, FCF: y.fcf }));
  const fcChart = forecast.years.map((y: any) => ({ year: `${y.year}E`, Revenue: y.revenue, FCF: y.fcf }));
  const combined = [...histChart, ...fcChart];

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl border border-slate-200 p-4">
          <h4 className="font-semibold text-brand mb-2">营收趋势（历史 + 预测）</h4>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={combined}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="year" /><YAxis /><Tooltip />
              <Bar dataKey="Revenue" fill="#1F3864" />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="bg-white rounded-xl border border-slate-200 p-4">
          <h4 className="font-semibold text-brand mb-2">自由现金流趋势</h4>
          <ResponsiveContainer width="100%" height={220}>
            <LineChart data={combined}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="year" /><YAxis /><Tooltip /><Legend />
              <Line type="monotone" dataKey="FCF" stroke="#10b981" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div>
        <h4 className="font-semibold text-brand mb-2">历史财务（USD millions）</h4>
        <div className="overflow-x-auto">
          <table className="text-sm border-collapse w-full">
            <thead>
              <tr className="bg-brand text-white">
                <th className="border p-2 text-left">Item</th>
                {stmts.history.map((y: any) => <th key={y.year} className="border p-2">{y.year}</th>)}
              </tr>
            </thead>
            <tbody>
              {[
                ["Revenue", "revenue"], ["Gross Profit", "gross_profit"],
                ["EBIT", "ebit"], ["Net Income", "net_income"],
                ["Operating CF", "operating_cf"], ["Capex", "capex"],
                ["FCF", "fcf"],
              ].map(([label, key]) => (
                <tr key={key} className="even:bg-slate-50">
                  <td className="border p-2 font-semibold">{label}</td>
                  {stmts.history.map((y: any) => (
                    <td key={y.year} className="border p-2 text-right">{fmtM(y[key])}</td>
                  ))}
                </tr>
              ))}
              <tr className="bg-amber-50 font-semibold">
                <td className="border p-2">Revenue Growth</td>
                {metrics.revenue_growth.map((g: number, i: number) => (
                  <td key={i} className="border p-2 text-right">{fmtPct(g)}</td>
                ))}
              </tr>
              <tr className="bg-amber-50 font-semibold">
                <td className="border p-2">EBIT Margin</td>
                {metrics.ebit_margin.map((g: number, i: number) => (
                  <td key={i} className="border p-2 text-right">{fmtPct(g)}</td>
                ))}
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div>
        <h4 className="font-semibold text-brand mb-2">5 年预测（USD millions）</h4>
        <div className="overflow-x-auto">
          <table className="text-sm border-collapse w-full">
            <thead>
              <tr className="bg-emerald-700 text-white">
                <th className="border p-2 text-left">Item</th>
                {forecast.years.map((y: any) => <th key={y.year} className="border p-2">{y.year}E</th>)}
              </tr>
            </thead>
            <tbody>
              {[["Revenue", "revenue"], ["EBIT", "ebit"], ["NOPAT", "nopat"],
                ["D&A", "da"], ["Capex", "capex"], ["ΔNWC", "change_in_nwc"], ["FCF", "fcf"]].map(
                ([label, key]) => (
                  <tr key={key} className="even:bg-slate-50">
                    <td className="border p-2 font-semibold">{label}</td>
                    {forecast.years.map((y: any) => (
                      <td key={y.year} className="border p-2 text-right">{fmtM(y[key])}</td>
                    ))}
                  </tr>
                )
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
