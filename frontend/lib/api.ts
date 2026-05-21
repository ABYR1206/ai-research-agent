import axios from "axios";

// 生产环境（Vercel）通过 NEXT_PUBLIC_API_BASE 注入 Render 后端 URL；
// 本地开发不设此变量时走 /api 相对路径，由 next.config.js rewrites 转发到 127.0.0.1:8000。
const BASE = process.env.NEXT_PUBLIC_API_BASE || "/api";

export const api = axios.create({ baseURL: BASE, timeout: 90000 });

export async function generateReport(ticker: string, source: string) {
  const { data } = await api.post("/report/generate", { ticker, source });
  return data;
}

const fileBase = () => process.env.NEXT_PUBLIC_API_BASE || "/api";
export const downloadExcelUrl = (id: string) => `${fileBase()}/download/excel/${id}`;
export const downloadReportUrl = (id: string) => `${fileBase()}/download/report/${id}`;
export const viewReportHtmlUrl = (id: string) => `${fileBase()}/download/report/${id}/html`;
