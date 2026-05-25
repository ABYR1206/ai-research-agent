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

# 按 sector 提供通用模板（用 profile.industry 拼接成业务描述）
_SECTOR_DEFAULTS = {
    "Technology": dict(
        segments=["软件 & 平台", "硬件 & 设备", "云服务 / SaaS", "研发与服务"],
        revenue_mix="收入来源以产品销售 + 订阅服务组合为主，毛利率较高，海外收入占比较大。",
        business_model="科技驱动 + 平台/生态变现：通过研发投入构建技术壁垒，再以软件订阅与服务持续货币化。",
        moat=["研发投入与技术积累", "客户/开发者生态", "规模效应与品牌"],
        competitors=["同行业领先科技公司（具体清单需结合细分赛道）"],
        strengths=["高毛利与现金流", "技术创新能力", "可扩展的商业模型"],
        weaknesses=["对关键产品依赖", "估值已 priced-in 增长", "客户集中度风险"],
        opportunities=["AI 与云转型", "国际化扩张", "新产品矩阵"],
        threats=["大厂跨界竞争", "监管反垄断", "宏观利率压估值"],
        risks=["技术迭代风险", "竞争加剧导致毛利下滑", "海外政策与汇率"],
    ),
    "Healthcare": dict(
        segments=["创新药 / 生物科技", "医疗器械", "医疗服务", "诊断与检测"],
        revenue_mix="多元化产品线收入，专利药/重磅产品贡献高毛利，区域市场分布全球化。",
        business_model="高研发投入 + 专利保护 + 全球商业化：通过临床研究形成创新药物 / 医疗器械护城河。",
        moat=["专利与监管壁垒", "全球销售网络", "临床数据与品牌信任"],
        competitors=["全球大型制药/医疗器械公司"],
        strengths=["现金流稳定", "高毛利率", "防御性消费属性"],
        weaknesses=["研发周期长 + 失败率高", "专利悬崖风险", "对核心产品依赖"],
        opportunities=["GLP-1 / 肿瘤免疫等创新方向", "AI 制药提升研发效率", "新兴市场支付能力提升"],
        threats=["医保压价（IRA 等）", "FDA 监管不确定性", "竞品仿制药"],
        risks=["临床试验失败", "重磅药专利到期", "诉讼与监管罚款"],
    ),
    "Financial Services": dict(
        segments=["商业银行业务", "投行 / 资本市场", "财富与资产管理", "支付服务"],
        revenue_mix="净利息收入 + 手续费收入 + 投资收益的组合，受利率与资本市场环境影响大。",
        business_model="规模化金融服务平台：通过资产负债表与客户网络赚取息差、手续费与管理费。",
        moat=["规模与资本基础", "客户关系与品牌", "牌照与监管合规壁垒"],
        competitors=["大型综合金融集团 / 全球同业"],
        strengths=["资本充足 + 现金流稳定", "多元化收入", "强监管下的稳定地位"],
        weaknesses=["对宏观利率敏感", "资本市场周期性", "信贷风险敞口"],
        opportunities=["财富管理需求增长", "金融科技整合", "新兴市场扩张"],
        threats=["利率快速下行压 NIM", "信贷质量恶化", "金融科技颠覆"],
        risks=["监管资本要求提升", "信用违约周期", "市场波动冲击交易收入"],
    ),
    "Consumer Cyclical": dict(
        segments=["核心消费产品", "国际市场", "新业务孵化"],
        revenue_mix="产品销售收入为主，区域上美国 / 欧洲 / 新兴市场分布，受可选消费需求周期影响。",
        business_model="品牌 + 渠道 + 供应链效率：通过品牌力定价、全球渠道触达与精益供应链获取竞争优势。",
        moat=["品牌资产", "渠道与零售网络", "供应链规模"],
        competitors=["同品类全球品牌"],
        strengths=["品牌溢价", "全球化布局", "渠道控制力"],
        weaknesses=["对经济周期敏感", "原材料与人工成本波动", "潮流变化风险"],
        opportunities=["DTC 与电商", "新兴市场中产扩张", "高端化趋势"],
        threats=["新兴品牌挤压", "汇率与关税", "可选消费疲软"],
        risks=["库存周期失误", "供应链中断", "品牌老化"],
    ),
    "Consumer Defensive": dict(
        segments=["核心必需消费品", "新兴品牌", "国际市场"],
        revenue_mix="必需消费品销售收入为主，需求刚性、抗周期，区域多元化降低单一市场风险。",
        business_model="品牌护城河 + 规模生产 + 全球分销：依靠品牌信任与渠道密度维持高市占。",
        moat=["品牌信任与历史", "规模采购与生产成本优势", "全球分销网络"],
        competitors=["国际消费品巨头 + 私有品牌"],
        strengths=["现金流稳定", "抗经济周期", "高股息回馈"],
        weaknesses=["增长受限于人口", "原材料成本承压", "私有品牌竞争"],
        opportunities=["新兴市场消费升级", "健康化产品创新", "DTC 渠道"],
        threats=["GLP-1 抑制食欲对食品行业影响", "通胀传导能力下降", "渠道集中度提升"],
        risks=["大宗原料价格波动", "汇率影响海外利润", "监管（糖税/添加剂）"],
    ),
    "Communication Services": dict(
        segments=["数字广告 / 媒体平台", "电信服务", "订阅与内容服务"],
        revenue_mix="广告 + 订阅 + 服务费的组合，广告与宏观经济周期相关，订阅与媒体内容粘性更强。",
        business_model="平台规模 + 用户时长 + 内容/数据壁垒：通过网络效应与算法持续优化变现效率。",
        moat=["用户规模与网络效应", "数据与算法", "内容版权与生态"],
        competitors=["全球互联网与媒体巨头"],
        strengths=["平台护城河深", "高毛利", "强大数据与 AI 能力"],
        weaknesses=["广告周期性", "监管不确定", "用户增长见顶"],
        opportunities=["AI 提升广告变现效率", "短视频/直播增量", "海外市场扩张"],
        threats=["新平台分流", "反垄断监管", "内容成本上涨"],
        risks=["广告周期下行", "监管诉讼", "用户隐私政策影响变现"],
    ),
    "Industrials": dict(
        segments=["核心工业产品", "服务与售后", "海外项目"],
        revenue_mix="产品销售 + 长期服务合同收入，订单周期长，与全球资本开支高度相关。",
        business_model="技术工程能力 + 长生命周期客户关系：通过设备销售带动多年服务收入。",
        moat=["工程技术与品牌", "全球客户与服务网络", "认证与监管壁垒"],
        competitors=["国际工业集团 + 区域龙头"],
        strengths=["现金流稳定", "客户黏性高", "技术积累深"],
        weaknesses=["资本开支重", "受宏观周期影响", "全球化运营复杂"],
        opportunities=["回流制造业 + 基建", "自动化与机器人", "国防开支增长"],
        threats=["供应链中断", "原材料价格波动", "客户资本开支下行"],
        risks=["大订单延期或取消", "汇率影响", "工厂安全与质量事故"],
    ),
    "Energy": dict(
        segments=["上游勘探开采", "炼化与销售", "新能源 / 转型业务"],
        revenue_mix="原油 / 天然气 / 成品油销售收入为主，受大宗商品价格影响最大。",
        business_model="资源储备 + 一体化运营 + 资本回报纪律：在大宗价格周期中通过规模和成本控制赚取超额回报。",
        moat=["资源储量", "炼化与物流网络", "上下游一体化"],
        competitors=["国际石油巨头 + 国家石油公司"],
        strengths=["现金流强劲", "高股息回馈", "资源储备充足"],
        weaknesses=["价格周期性强", "ESG 资金撤出压力", "新能源转型压力"],
        opportunities=["LNG 全球贸易", "新能源 / 氢能转型", "OPEC+ 减产支撑油价"],
        threats=["油价下行", "环保监管加严", "新能源替代"],
        risks=["大宗价格大幅波动", "地缘政治冲突", "环境事故与诉讼"],
    ),
    "Basic Materials": dict(
        segments=["金属采矿", "化工产品", "建筑材料"],
        revenue_mix="大宗原料销售收入，与铁矿石/铜/锂/煤等价格高度相关。",
        business_model="资源开采 + 加工 + 物流：依赖储量、矿山品位、能源成本等关键变量。",
        moat=["矿山资源与品位", "规模与成本曲线", "物流基础设施"],
        competitors=["全球矿业巨头"],
        strengths=["资源储量丰富", "规模化生产", "高股息"],
        weaknesses=["价格波动性大", "环保监管成本", "需求与中国房地产强相关"],
        opportunities=["电气化推动铜/锂结构性短缺", "基建周期", "新材料应用"],
        threats=["中国需求疲软", "大宗下行周期", "环保与社区抗议"],
        risks=["商品价格剧烈波动", "汇率波动", "矿山安全事故"],
    ),
    "Real Estate": dict(
        segments=["核心物业类型", "新兴资产（数据中心 / 物流）", "服务与管理"],
        revenue_mix="租金收入 + 资产管理费 + 资产增值收益，REIT 结构下大部分收益分派给股东。",
        business_model="资产开发 / 持有 + 租赁运营：通过长期资产积累实现现金流与资本增值双轨。",
        moat=["位置与物业组合", "租户长期合约", "规模化运营效率"],
        competitors=["大型 REIT + 地产开发商"],
        strengths=["现金流稳定", "高股息率", "通胀对冲属性"],
        weaknesses=["对利率高度敏感", "资产估值波动", "新项目周期长"],
        opportunities=["AI 数据中心需求", "物流地产增长", "降息周期估值修复"],
        threats=["利率高位压估值", "办公空置率上升", "再融资风险"],
        risks=["商业地产违约", "租户破产", "资产减值"],
    ),
    "Utilities": dict(
        segments=["电力发电与输配", "燃气供应", "可再生能源投资"],
        revenue_mix="受监管的电力 / 燃气销售收入为主，收入相对稳定。",
        business_model="受监管的天然垄断 + 资本开支驱动 ROE：通过监管批准的资本计划获得稳定回报。",
        moat=["监管特许经营权", "现有基础设施", "区域市场垄断"],
        competitors=["区域内其他公用事业公司"],
        strengths=["收入稳定", "高股息", "防御性极强"],
        weaknesses=["增长缓慢", "对利率敏感", "重资本开支"],
        opportunities=["AI 数据中心电力需求激增", "电网升级投资", "新能源转型"],
        threats=["监管不允许加价", "极端天气", "燃料成本波动"],
        risks=["监管裁决不利", "灾害事故", "再融资成本上升"],
    ),
}

_DEFAULT_FALLBACK = dict(
    segments=["核心业务（详见公司年报）"],
    revenue_mix="收入结构尚需结合公司年报与行业研究补充。",
    business_model="基于所在行业的典型商业模式，详细分析建议查阅最新年报与投资者关系材料。",
    moat=["品牌与市场地位", "客户关系与渠道", "运营效率"],
    competitors=["同行业主要竞争对手（具体清单建议结合行业研究补充）"],
    strengths=["运营基础稳健", "行业经验积累", "现金流支撑发展"],
    weaknesses=["行业竞争激烈", "对宏观环境敏感", "增长曲线尚需验证"],
    opportunities=["行业结构性增长", "新产品 / 新市场扩张", "技术升级红利"],
    threats=["竞争加剧", "宏观经济波动", "监管政策变化"],
    risks=["宏观与行业周期", "经营执行风险", "外部环境不确定性"],
)


def analyze(profile: CompanyProfile) -> CompanyAnalysis:
    """生成公司分析。已知 mock ticker 走精细模板，未知 ticker 按 sector 走通用模板。"""
    t_upper = profile.ticker.upper()
    if t_upper in _TEMPLATES:
        t = _TEMPLATES[t_upper]
    else:
        t = _SECTOR_DEFAULTS.get(profile.sector, _DEFAULT_FALLBACK)
    overview = (
        f"{profile.name}（{profile.ticker}）属于 {profile.sector} - {profile.industry} 行业，"
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
