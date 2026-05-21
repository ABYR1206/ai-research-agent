"use client";

const fmtM = (x: number) => `$${(x || 0).toLocaleString(undefined, { maximumFractionDigits: 1 })}M`;
const fmt$ = (x: number) => `$${(x || 0).toFixed(2)}`;
const fmtPct = (x: number | null | undefined) =>
  x === null || x === undefined ? "N/A" : `${(x * 100).toFixed(1)}%`;

function rating(upside: number | null | undefined): { label: string; color: string } {
  if (upside === null || upside === undefined) return { label: "Hold", color: "bg-slate-400" };
  if (upside > 0.2) return { label: "BUY", color: "bg-emerald-600" };
  if (upside > 0.05) return { label: "Overweight", color: "bg-green-500" };
  if (upside > -0.05) return { label: "Hold", color: "bg-slate-500" };
  if (upside > -0.2) return { label: "Underweight", color: "bg-orange-500" };
  return { label: "SELL", color: "bg-red-600" };
}

function heatColor(v: number, min: number, max: number): string {
  if (max === min) return "bg-slate-100";
  const t = (v - min) / (max - min);
  const r = Math.round(248 + (99 - 248) * t);
  const g = Math.round(105 + (190 - 105) * t);
  const b = Math.round(107 + (123 - 107) * t);
  return `rgb(${r},${g},${b})`;
}

export default function ValuationCard({ dcf }: { dcf: any }) {
  const r = rating(dcf.upside);
  const flat = dcf.sensitivity.flat() as number[];
  const min = Math.min(...flat), max = Math.max(...flat);

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Stat label="隐含每股股价" value={fmt$(dcf.implied_price)} highlight />
        <Stat label="当前股价" value={fmt$(dcf.current_price || 0)} />
        <Stat label="上行空间" value={fmtPct(dcf.upside)} highlight />
        <div className={`rounded-xl p-4 text-white ${r.color} flex flex-col justify-center`}>
          <div className="text-xs opacity-90">评级</div>
          <div className="text-2xl font-bold">{r.label}</div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <table className="w-full text-sm border border-slate-200 rounded-lg overflow-hidden">
          <tbody>
            <Row k="企业价值 (EV)" v={fmtM(dcf.enterprise_value)} />
            <Row k="减：净负债" v={fmtM(dcf.net_debt)} />
            <Row k="股权价值" v={fmtM(dcf.equity_value)} />
            <Row k="终值 (TV)" v={fmtM(dcf.terminal_value)} />
            <Row k="PV(终值)" v={fmtM(dcf.pv_terminal)} />
            <Row k="PV(FCF) 合计" v={fmtM(dcf.pv_fcf.reduce((a: number, b: number) => a + b, 0))} />
            <Row k="流通股本 (M)" v={dcf.shares_outstanding.toLocaleString()} />
          </tbody>
        </table>

        <div>
          <div className="text-sm font-semibold text-slate-700 mb-2">敏感性分析（WACC × g → 每股股价）</div>
          <table className="text-xs border-collapse w-full">
            <thead>
              <tr>
                <th className="border p-1 bg-brand text-white">WACC \ g</th>
                {dcf.growth_axis.map((g: number) => (
                  <th key={g} className="border p-1 bg-slate-200">{(g * 100).toFixed(1)}%</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {dcf.sensitivity.map((row: number[], i: number) => (
                <tr key={i}>
                  <td className="border p-1 bg-slate-200 font-semibold">
                    {(dcf.wacc_axis[i] * 100).toFixed(1)}%
                  </td>
                  {row.map((v, j) => (
                    <td key={j} className="border p-1 text-right" style={{ background: heatColor(v, min, max) }}>
                      ${v.toFixed(0)}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

function Stat({ label, value, highlight }: { label: string; value: string; highlight?: boolean }) {
  return (
    <div className={`rounded-xl p-4 border ${highlight ? "bg-emerald-50 border-emerald-300" : "bg-white border-slate-200"}`}>
      <div className="text-xs text-slate-500">{label}</div>
      <div className={`text-2xl font-bold ${highlight ? "text-emerald-700" : "text-slate-800"}`}>{value}</div>
    </div>
  );
}

function Row({ k, v }: { k: string; v: string }) {
  return (
    <tr className="border-b last:border-b-0">
      <td className="px-3 py-2 text-slate-600">{k}</td>
      <td className="px-3 py-2 text-right font-semibold">{v}</td>
    </tr>
  );
}
