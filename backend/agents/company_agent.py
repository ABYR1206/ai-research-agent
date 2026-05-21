"""Module 2: 公司分析 Agent — 模板化生成商业模式与 SWOT。"""
from backend.schemas import CompanyProfile, CompanyAnalysis, SWOT


_TEMPLATES: dict[str, dict] = {
    "AAPL": {
        "segments": ["iPhone", "Mac", "iPad", "Wearables (AirPods/Watch)", "Services (App Store/iCloud/Apple Pay)"],
        "revenue_mix": "iPhone 约占 52%，Services 约占 22%（高毛利且持续扩张），Wearables 约占 10%，Mac 约占 8%，iPad 约占 7%。",
        "business_model": "硬件+服务+生态闭环：通过高端硬件锁定用户，再以软件/服务/订阅持续变现，形成强复购与高粘性。",
        "moat": ["品牌溢价与高端定位", "iOS/macOS 闭环生态", "全球零售与渠道网络", "自研芯片（Apple Silicon）"],
        "competitors": ["Samsung", "Xiaomi", "Huawei", "Microsoft", "Google"],
        "strengths": ["顶级品牌力", "极高毛利与现金流", "强大研发与供应链管理"],
        "weaknesses": ["过度依赖 iPhone", "对中国市场暴露较高", "硬件创新边际放缓"],
        "opportunities": ["AI on-device（Apple Intelligence）", "Services 持续增长", "印度等新兴市场"],
        "threats": ["监管反垄断（App Store 抽佣）", "中美脱钩与供应链风险", "汇率波动"],
        "risks": ["地缘政治冲击 iPhone 出货", "Services 监管风险", "AI 投入回报不确定性"],
    },
    "TSLA": {
        "segments": ["Automotive（Model 3/Y/S/X/Cybertruck）", "Energy Generation & Storage", "Services (FSD/Supercharging)"],
        "revenue_mix": "汽车业务约占 80%，能源约 10%，服务与其他约 10%；FSD 软件订阅潜力巨大。",
        "business_model": "垂直整合的电动车+能源+自动驾驶平台：自研三电、自建超充网络、软件 OTA 持续货币化。",
        "moat": ["先发与品牌", "超充网络规模", "FSD 数据飞轮", "成本曲线领先"],
        "competitors": ["BYD", "Volkswagen", "GM", "Ford", "Lucid", "Rivian"],
        "strengths": ["规模与成本优势", "技术领先（电池/软件/自动驾驶）", "强大现金储备"],
        "weaknesses": ["估值高、波动大", "产品矩阵相对单一", "降价侵蚀毛利"],
        "opportunities": ["Robotaxi/Optimus 商业化", "能源业务规模化", "新车型扩张（紧凑型/卡车）"],
        "threats": ["中国电动车价格战", "FSD 监管落地不确定", "原材料价格波动"],
        "risks": ["CEO 关键人风险", "FSD 法律风险", "中国市场份额承压"],
    },
    "NVDA": {
        "segments": ["Data Center（AI/HPC）", "Gaming", "Professional Visualization", "Automotive"],
        "revenue_mix": "Data Center 约占 87%（AI 训练/推理加速卡），Gaming 约 9%，其他 4%。",
        "business_model": "AI 算力垄断：GPU 硬件 + CUDA 软件生态 + NVLink/NVSwitch 系统，构成全栈 AI 平台。",
        "moat": ["CUDA 软件生态护城河", "AI 训练卡市占率 >90%", "系统级整合（DGX/HGX）"],
        "competitors": ["AMD", "Intel", "Google TPU", "AWS Trainium", "Broadcom"],
        "strengths": ["AI 算力绝对领导者", "极高毛利率与定价权", "强大研发投入"],
        "weaknesses": ["客户集中度高（云厂商）", "中国出口受限", "估值已 priced-in 高增长"],
        "opportunities": ["主权 AI（Sovereign AI）", "企业 AI 渗透", "推理需求爆发"],
        "threats": ["大客户自研芯片", "AI 资本开支周期性放缓", "中美科技脱钩"],
        "risks": ["AI 需求一旦放缓估值回撤剧烈", "出口管制升级", "供应链（TSMC/HBM）"],
    },
    "TSM": {
        "segments": ["高端先进制程（3nm/5nm/7nm）", "成熟制程（28nm 以上）", "封装与测试", "特色工艺"],
        "revenue_mix": "5nm 及以下先进制程约占 50%+（HPC/AI 客户），7nm 约 15%，成熟制程约 30%。",
        "business_model": "纯晶圆代工龙头：服务全球 Fabless（Apple/Nvidia/AMD/Qualcomm），赚取制造服务费。",
        "moat": ["先进制程技术领先 1-2 代", "客户与产线深度绑定", "巨额资本开支壁垒"],
        "competitors": ["Samsung Foundry", "Intel Foundry", "SMIC", "GlobalFoundries"],
        "strengths": ["技术领先全球", "客户结构优质", "稳定现金流与高 ROIC"],
        "weaknesses": ["地缘政治集中度高（台湾）", "资本开支沉重", "周期性较强"],
        "opportunities": ["AI 芯片代工需求爆发", "海外建厂（美国/日本/德国）分散风险", "CoWoS 封装产能扩张"],
        "threats": ["两岸地缘紧张", "客户去台化趋势", "Samsung/Intel 追赶"],
        "risks": ["台海冲突风险", "客户产能转移", "汇率（新台币/美元）"],
    },
}

_DEFAULT = {
    "segments": ["核心业务（数据缺失，建议查阅年报）"],
    "revenue_mix": "数据缺失：请补充各业务板块收入占比。",
    "business_model": "数据缺失：建议补充商业模式描述（产品/客户/盈利方式）。",
    "moat": ["数据缺失：建议补充护城河来源"],
    "competitors": ["数据缺失"],
    "strengths": ["数据缺失"], "weaknesses": ["数据缺失"],
    "opportunities": ["数据缺失"], "threats": ["数据缺失"],
    "risks": ["数据缺失：建议补充关键风险点"],
}


def analyze(profile: CompanyProfile) -> CompanyAnalysis:
    """生成公司分析。已知 ticker 走精细模板，未知走数据缺失模板。"""
    t = _TEMPLATES.get(profile.ticker.upper(), _DEFAULT)
    overview = (
        f"{profile.name}（{profile.ticker}）成立于美国/国际市场，属于 "
        f"{profile.sector} - {profile.industry} 行业，"
        f"当前市值约 ${profile.market_cap:,.0f} 百万美元（如已获取）。"
        if profile.market_cap else
        f"{profile.name}（{profile.ticker}），属于 {profile.sector} - {profile.industry}。"
    )
    return CompanyAnalysis(
        overview=overview,
        business_segments=t["segments"],
        revenue_mix=t["revenue_mix"],
        business_model=t["business_model"],
        moat=t["moat"],
        competitors=t["competitors"],
        swot=SWOT(
            strengths=t["strengths"],
            weaknesses=t["weaknesses"],
            opportunities=t["opportunities"],
            threats=t["threats"],
        ),
        risks=t["risks"],
    )
