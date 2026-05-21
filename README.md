# AI Research Agent — 自动生成分析师研究报告

一个简化版投行/券商研究助理 AI Agent：输入股票代码 → 自动产出**行业分析 + 公司分析 + 财务三表 + 5 年预测 + DCF 估值 + 敏感性分析**，并下载**商务风格 Excel DCF 模型**和**Markdown 研究报告**。

> 课程作业（vibe coding）演示项目。数据仅供研究参考，不构成投资建议。

---

## 功能亮点

- **5 个 Agent 串行编排**：Industry → Company → Finance → Valuation → Report
- **7-Sheet Excel DCF 模型**：Summary / Assumptions / Historical / Forecast / DCF / Sensitivity / Charts
  - 所有公式真实可改，修改 Assumptions 浅黄单元格即可重算
  - 深蓝商务配色、输入/公式/输出三色区分、负数自动红字
- **结构化 Markdown 报告**：8 个章节（Thesis / Overview / Industry / Business / Financial / Valuation / Risks / Conclusion）
- **数据源多选**：yfinance 联网抓取 → 失败自动 fallback 到内置 Mock（AAPL/TSLA/NVDA/TSM）
- **Next.js 前端**：4 个 Tab + 敏感性热力图 + Recharts 图表 + 一键下载

---

## 项目结构

```
ai-research-agent/
├── backend/           # FastAPI + 5 个 Agent + Excel 生成
│   ├── main.py
│   ├── schemas.py
│   ├── config.py
│   ├── agents/        # Module 1-4 + orchestrator
│   ├── data/          # fetcher (yfinance) + mock_data + industry_kb
│   ├── modeling/      # metrics / forecast / dcf
│   ├── outputs/       # excel_builder / report_builder / styles
│   └── api/           # 4 个路由文件
├── frontend/          # Next.js 14 + Tailwind + Recharts
│   └── app/
├── storage/           # 运行时生成的 xlsx/md（自动创建）
├── requirements.txt
├── run.sh             # 一键启动
└── README.md
```

---

## 安装与运行

### 1. 安装依赖

```bash
# 后端
cd ai-research-agent
pip install -r requirements.txt

# 前端
cd frontend
npm install
cd ..
```

### 2. 启动（两种方式）

**方式 A：一键启动**

```bash
chmod +x run.sh
./run.sh
```

**方式 B：分别启动**

```bash
# Terminal 1 — 后端 (端口 8000)
uvicorn backend.main:app --reload

# Terminal 2 — 前端 (端口 3000)
cd frontend && npm run dev
```

### 3. 打开浏览器

- 前端 UI：http://localhost:3000
- 后端 API 文档：http://127.0.0.1:8000/docs

---

## 演示步骤（5 分钟）

1. 打开 http://localhost:3000
2. 输入 `AAPL`，数据源选「内置 Mock 数据」
3. 点 **🚀 生成研究报告**（约 3-5 秒）
4. 顶部彩色 banner 显示评级与目标价
5. 切换 4 个 Tab 查看分析内容；估值 Tab 含敏感性热力图
6. 点 **⬇ 下载 DCF Excel 模型** → 用 Excel/Numbers 打开
7. **关键演示**：在 Excel 的 `Assumptions` sheet 把 WACC 从 9% 改成 12%，切到 `DCF` sheet 看「Implied Share Price」自动重算下降
8. 点 **⬇ 下载 Markdown 报告** → 8 章节完整报告
9. 换 `TSLA / NVDA / TSM` 重复（4 家内置公司全部有真实近 5 年三表数据）

---

## API 端点

| Method | Path | 用途 |
|---|---|---|
| POST | `/report/generate` | 一键全流程（前端主用） |
| POST | `/analyze/industry` | 仅行业分析 |
| POST | `/analyze/company` | 仅公司分析 |
| POST | `/financial/extract` | 抓三表 + 算指标 |
| POST | `/valuation/dcf` | 自定义假设跑 DCF |
| GET | `/download/excel/{file_id}` | 下载 Excel |
| GET | `/download/report/{file_id}` | 下载 Markdown |
| GET | `/download/report/{file_id}/html` | 浏览器预览 HTML |

完整 OpenAPI 文档：http://127.0.0.1:8000/docs

---

## 命令行测试（不开前端）

```bash
# 完整流程
curl -X POST http://127.0.0.1:8000/report/generate \
  -H "Content-Type: application/json" \
  -d '{"ticker":"AAPL","source":"mock"}' | jq .

# 下载 Excel（用上一步返回的 excel_file_id）
curl -OJ http://127.0.0.1:8000/download/excel/AAPL_xxxxxxxx
```

或者直接跑 Python：

```python
from backend.agents.orchestrator import run
r = run("NVDA", source="mock")
print(r.dcf.implied_price, r.dcf.upside)
print(r.excel_file_id)  # → storage/excel/NVDA_xxx.xlsx
```

---

## Excel 公式说明

所有计算 sheet 用真实公式（非硬编码数字）：

- **Forecast sheet**
  - `Revenue_t = Revenue_{t-1} * (1 + Assumptions!Growth_t)`
  - `EBIT = Revenue * Assumptions!EBIT_Margin`
  - `NOPAT = EBIT * (1 - Tax_Rate)`
  - `FCF = NOPAT + D&A - Capex - ΔNWC`
- **DCF sheet**
  - `DiscountFactor = 1 / (1 + WACC)^t`
  - `PV_FCF = FCF * DiscountFactor`
  - `Terminal Value = FCF_5 * (1 + g) / (WACC - g)`
  - `Enterprise Value = Σ PV_FCF + PV_Terminal`
  - `Equity Value = EV - Net Debt`
  - `Implied Share Price = Equity Value / Shares Outstanding`

---

## 技术栈

| 层 | 技术 |
|---|---|
| 前端 | Next.js 14 (App Router) + React 18 + TypeScript + Tailwind CSS + Recharts |
| 后端 | Python 3.10+ + FastAPI + Pydantic v2 |
| 数据 | yfinance + pandas + numpy |
| Excel | openpyxl（公式 + 图表 + 条件格式）|
| Agent | 普通 Python workflow（无 LLM 依赖，纯模板化 + 规则化生成）|

---

## 支持的公司（Mock 数据）

| Ticker | 公司 | 行业 |
|---|---|---|
| AAPL | Apple Inc. | Consumer Electronics |
| TSLA | Tesla, Inc. | Auto Manufacturers |
| NVDA | NVIDIA Corporation | Semiconductors |
| TSM | Taiwan Semiconductor | Semiconductors |

其他公司选 `auto` 或 `yfinance` 模式会尝试联网抓取；抓不到则报错（建议改 `mock` 演示已有 ticker）。

---

## 🚀 部署到公网（Vercel + Render，全免费）

架构：**前端 Vercel** + **后端 Render**。两者都从同一个 GitHub 仓库自动部署。

### Step 1 — 推到 GitHub

```bash
cd ai-research-agent
git init -b main
git add .
git commit -m "Initial commit: AI Research Agent MVP"

# 在 https://github.com/new 创建一个空仓库（名字随意，建议 ai-research-agent）
# 然后：
git remote add origin https://github.com/<你的用户名>/ai-research-agent.git
git push -u origin main
```

### Step 2 — 部署后端到 Render

1. 注册 https://render.com（用 GitHub 登录最快）
2. Dashboard → **New** → **Blueprint**
3. 选择刚才的 GitHub 仓库 → Render 会自动识别 `render.yaml`
4. 点 **Apply** → 等 3-5 分钟构建（pandas/numpy 编译慢）
5. 完成后会拿到一个 URL，形如 `https://ai-research-agent-api.onrender.com`
6. 打开 `https://<url>/health` 验证返回 `{"status":"ok"}`

> ⚠️ Render 免费层 15 分钟无请求会休眠，下次首请求约 30s 冷启动。生产用可升级 $7/月。

### Step 3 — 部署前端到 Vercel

1. 注册 https://vercel.com（用 GitHub 登录）
2. **Add New** → **Project** → Import 刚才的仓库
3. **Root Directory** 选 `frontend` ⚠️ 关键！
4. **Environment Variables** 添加：
   - Key: `NEXT_PUBLIC_API_BASE`
   - Value: Step 2 拿到的 Render URL（**不要带尾斜杠**）
5. 点 **Deploy** → 2 分钟构建完成
6. Vercel 会给一个公开 URL，形如 `https://ai-research-agent.vercel.app` —— **这个 URL 就能发给别人**

### Step 4 — 验证

打开 Vercel URL → 输入 `AAPL` → 选「内置 Mock 数据」→ 点生成。
首次点击因为 Render 后端可能在冷启动，会等约 30 秒；之后 5 秒内出结果。

### 后续更新

任何 `git push` 都会触发 Vercel + Render 自动重新部署，无需任何额外操作。

---

## 已知限制

- 文本生成基于模板（非 LLM），措辞固定；如需更自然的文本可在 `agents/report_agent.py` 中接入 LLM
- Mock 三表数据为公开年报近似值，仅供演示
- 敏感性分析在 Excel 中以静态值呈现（受 openpyxl 限制），主模型 WACC/g 改了后由 Excel 自动重算 DCF sheet 的隐含股价
- 当前不做 10-K PDF 解析、不存数据库、无用户系统

---

## 文件输出位置

- Excel：`storage/excel/{ticker}_{id}.xlsx`
- Markdown：`storage/reports/{ticker}_{id}.md`

每次生成会产生一个新 `file_id`（不会覆盖），可手动清理。
