import "./globals.css";

export const metadata = { title: "AI Research Agent", description: "自动生成分析师研究报告" };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh-CN">
      <body className="min-h-screen">{children}</body>
    </html>
  );
}
