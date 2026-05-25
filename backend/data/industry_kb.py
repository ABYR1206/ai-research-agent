"""行业知识库：按 sector → 模板化分析素材。"""
from __future__ import annotations
from backend.schemas import IndustryAnalysis


_KB: dict[str, dict] = {
    "Technology": {
        "definition": "科技行业涵盖半导体、消费电子、软件、云计算、互联网平台等子领域，是全球生产力提升与数字化转型的核心引擎。",
        "market_size": "全球科技行业规模超过 5 万亿美元，其中半导体约 6,000 亿美元，云服务约 6,800 亿美元。",
        "growth_drivers": [
            "生成式 AI 带来算力需求激增",
            "云计算与边缘计算加速渗透",
            "企业数字化转型与 SaaS 化",
            "5G/6G 与物联网设备普及",
            "新兴市场消费电子渗透率提升",
        ],
        "landscape": "由少数科技巨头主导（Apple、Microsoft、Alphabet、Amazon、Meta、Nvidia），形成寡头竞争；中游半导体环节由 TSMC、ASML 形成强护城河。",
        "key_players": ["Apple", "Microsoft", "Alphabet", "Amazon", "Meta", "Nvidia", "TSMC", "Samsung"],
        "risks": [
            "地缘政治与出口管制（中美科技脱钩、对华芯片限制）",
            "全球反垄断监管趋严",
            "技术迭代风险与资本开支周期",
            "宏观利率上行抑制估值",
        ],
        "outlook": "未来 3-5 年 AI 算力、企业 SaaS、自动驾驶、机器人将继续驱动结构性增长，行业整体复合增速预计 8-12%。",
    },
    "Consumer Cyclical": {
        "definition": "可选消费行业包括汽车、零售、酒店、奢侈品等周期性消费品类，与宏观经济和居民可支配收入高度相关。",
        "market_size": "全球可选消费市场规模超过 15 万亿美元，其中汽车产业约 3 万亿美元。",
        "growth_drivers": [
            "电动化与智能化对传统汽车的替代",
            "新兴市场中产阶级扩张",
            "DTC 与电商渠道渗透",
            "新能源补贴与产业政策",
        ],
        "landscape": "传统汽车厂商（Toyota、VW、GM）与新势力（Tesla、BYD）正面竞争，行业进入电动化淘汰赛。",
        "key_players": ["Tesla", "Toyota", "Volkswagen", "BYD", "GM", "Ford", "Stellantis"],
        "risks": [
            "原材料（锂、镍）价格波动",
            "贸易壁垒与关税政策",
            "高利率抑制大件消费",
            "产能过剩与价格战",
        ],
        "outlook": "电动车渗透率预计 2028 年达 40%+，但盈利能力分化加剧，头部集中度提升。",
    },
    "Healthcare": {
        "definition": "医疗保健行业涵盖制药、生物科技、医疗器械、医疗服务与健康管理，受人口老龄化、慢性病管理需求和创新药物推动。",
        "market_size": "全球医疗保健市场规模超过 11 万亿美元，其中制药约 1.6 万亿美元、医疗器械约 5,000 亿美元。",
        "growth_drivers": ["人口老龄化与慢病增长", "GLP-1/肿瘤免疫等创新药物突破", "AI 辅助诊断与精准医疗", "新兴市场支付能力提升"],
        "landscape": "大型跨国药企（Pfizer/JNJ/Roche/Novartis）与生物科技新势力并存，医疗器械龙头（Medtronic/Abbott/Stryker）格局稳定。",
        "key_players": ["Johnson & Johnson", "UnitedHealth", "Pfizer", "Eli Lilly", "Novo Nordisk", "Roche", "Merck"],
        "risks": ["专利悬崖（重磅药专利到期）", "美国 IRA 药价谈判与全球医保压价", "临床试验失败风险", "FDA/EMA 监管不确定性"],
        "outlook": "未来 3-5 年 GLP-1 减肥药、CAR-T 细胞治疗、AI 制药将驱动结构性增长，行业整体复合增速 6-9%。",
    },
    "Financial Services": {
        "definition": "金融服务行业包括银行、保险、资产管理、支付与金融科技，是经济体系的血脉。",
        "market_size": "全球金融服务市场规模约 28 万亿美元，其中银行业 7 万亿美元、资管 100 万亿美元（AUM）。",
        "growth_drivers": ["利率周期与净息差", "财富管理需求增长", "支付电子化与跨境支付", "金融科技对传统机构的赋能"],
        "landscape": "大型综合金融集团（JPMorgan/BAC/Citi）+ 资管巨头（BlackRock/Vanguard）+ 支付网络（Visa/Mastercard）+ 保险（Berkshire/AIG）。",
        "key_players": ["JPMorgan Chase", "Bank of America", "Visa", "Mastercard", "Berkshire Hathaway", "BlackRock"],
        "risks": ["利率快速下行压缩 NIM", "信贷质量恶化（商业地产/消费贷）", "监管资本要求趋严（Basel IV）", "金融科技颠覆"],
        "outlook": "未来 3-5 年高利率环境利好银行，资管行业被动化与另类资产并行；金融科技整合加速。",
    },
    "Consumer Defensive": {
        "definition": "必需消费品涵盖食品饮料、日用品、烟草、零售，需求刚性、抗周期性强。",
        "market_size": "全球必需消费品市场规模约 10 万亿美元。",
        "growth_drivers": ["新兴市场消费升级", "健康化与有机化趋势", "DTC 与电商渠道", "品牌力定价权"],
        "landscape": "国际巨头（P&G/Unilever/Nestle/Coca-Cola/Pepsi）+ 大型零售（Walmart/Costco）主导。",
        "key_players": ["Walmart", "Procter & Gamble", "Coca-Cola", "PepsiCo", "Costco", "Nestle"],
        "risks": ["原材料与人工成本上涨", "私有品牌挤压", "新兴市场汇率波动", "健康监管（糖税等）"],
        "outlook": "未来 3-5 年增速 3-5%，估值溢价反映防御属性；GLP-1 药物长期影响零食/糖饮消费需关注。",
    },
    "Communication Services": {
        "definition": "通信服务涵盖电信运营商、互联网媒体、社交平台、流媒体、游戏与广告。",
        "market_size": "全球数字广告 7,000 亿美元，流媒体 1,500 亿美元，电信服务 1.7 万亿美元。",
        "growth_drivers": ["数字广告份额提升", "流媒体订阅增长", "AI 提升广告变现效率", "5G/6G 部署"],
        "landscape": "广告寡头（Alphabet/Meta）+ 流媒体（Netflix/Disney）+ 电信龙头（Verizon/AT&T/T-Mobile）。",
        "key_players": ["Alphabet", "Meta", "Netflix", "Disney", "Verizon", "AT&T", "Spotify"],
        "risks": ["广告周期性波动", "TikTok 等新平台分流", "内容成本上涨", "监管反垄断"],
        "outlook": "AI 推荐 + 短视频 + 体育版权将主导未来 3 年，广告 5-7%、流媒体 8-10% 增速。",
    },
    "Industrials": {
        "definition": "工业行业涵盖航空航天、国防、机械、运输、商业服务，与全球资本开支周期高度相关。",
        "market_size": "全球工业市场规模超过 15 万亿美元。",
        "growth_drivers": ["回流制造业与基建投资", "国防开支增长", "自动化与机器人", "电气化与能源转型"],
        "landscape": "航空航天双寡头（Boeing/Airbus）+ 工业巨头（GE/Honeywell/Caterpillar/Deere）。",
        "key_players": ["Boeing", "Lockheed Martin", "Caterpillar", "Deere", "Honeywell", "Union Pacific"],
        "risks": ["供应链中断", "原材料价格波动", "客户资本开支周期下行", "地缘政治影响出口"],
        "outlook": "国防与航空航天将受益于地缘紧张，制造业回流与基建支持中期需求。",
    },
    "Energy": {
        "definition": "能源行业涵盖油气勘探开采、炼化、管输、油服与新能源，受大宗商品价格驱动。",
        "market_size": "全球油气市场规模约 5 万亿美元（按收入计），新能源 1.5 万亿美元。",
        "growth_drivers": ["OPEC+ 减产支撑油价", "LNG 全球贸易扩张", "上游资本回报纪律", "新能源转型投资"],
        "landscape": "国际石油巨头（ExxonMobil/Chevron/Shell/BP）+ 油服（SLB/Halliburton）+ 美国页岩油商。",
        "key_players": ["ExxonMobil", "Chevron", "Shell", "TotalEnergies", "ConocoPhillips", "Saudi Aramco"],
        "risks": ["油价大幅下跌", "ESG 资金撤出", "新能源替代加速", "地缘政治冲突"],
        "outlook": "未来 3-5 年油气需求仍温和增长，新能源转型加速但传统能源仍提供高现金回报。",
    },
    "Basic Materials": {
        "definition": "基础材料涵盖金属采矿、化工、建材、纸业，是制造业的上游原料供应商。",
        "market_size": "全球基础材料市场规模约 4 万亿美元。",
        "growth_drivers": ["电气化推动铜/锂/镍需求", "基建与房地产周期", "新材料创新", "中国需求复苏"],
        "landscape": "矿业巨头（BHP/Rio Tinto/Vale/Glencore）+ 化工龙头（Dow/Linde/Air Liquide）。",
        "key_players": ["BHP", "Rio Tinto", "Linde", "Air Liquide", "Freeport-McMoRan", "Newmont"],
        "risks": ["大宗商品价格周期性", "中国地产持续下行", "环保监管加严", "汇率波动"],
        "outlook": "电气化转型驱动铜/铝/锂结构性短缺，未来 3-5 年金属价格中枢上移。",
    },
    "Real Estate": {
        "definition": "房地产涵盖 REITs（数据中心/物流/医疗/办公/零售/住宅）和地产开发与服务。",
        "market_size": "全球商业地产规模超过 35 万亿美元。",
        "growth_drivers": ["AI 算力推动数据中心 REIT", "电商支撑物流地产", "人口老龄化利好医疗 REIT", "利率下行支撑估值"],
        "landscape": "美国大型 REIT（Prologis/Equinix/Welltower）+ 跨国地产服务（CBRE/JLL）。",
        "key_players": ["Prologis", "Equinix", "American Tower", "Welltower", "Public Storage", "Simon Property"],
        "risks": ["利率持续高位压估值", "办公楼空置率上升", "商业地产违约", "再融资风险"],
        "outlook": "数据中心与物流 REIT 跑赢，传统办公与零售承压；降息周期将带来估值修复。",
    },
    "Utilities": {
        "definition": "公用事业涵盖电力、燃气、水务等监管型行业，现金流稳定、股息率高。",
        "market_size": "全球公用事业市场规模约 4 万亿美元（按收入计）。",
        "growth_drivers": ["AI 数据中心电力需求激增", "电网升级与新能源并网投资", "电气化进程", "ESG 资金偏好"],
        "landscape": "美国大型电力公司（NextEra/Duke/Southern）+ 多元化公用事业集团（Iberdrola/Enel）。",
        "key_players": ["NextEra Energy", "Duke Energy", "Southern Company", "Dominion", "Iberdrola"],
        "risks": ["利率高位抑制估值", "监管不允许加价", "极端天气与电网投资压力", "燃料成本波动"],
        "outlook": "AI 算力扩张催生 10 年内电力需求复合增长 3-5%，是结构性新增长曲线。",
    },
}

_DEFAULT = {
    "definition": "该行业为目标公司所属赛道，下游需求由宏观经济、技术演进与监管政策共同驱动。",
    "market_size": "数据缺失：建议查阅 IBISWorld / Statista / 行业协会报告以获取精确市场规模。",
    "growth_drivers": [
        "终端需求结构性增长",
        "技术与产品升级",
        "产业链国产化或全球化",
    ],
    "landscape": "行业呈现头部集中趋势，目标公司面临既有龙头与新兴挑战者的双重竞争。",
    "key_players": ["数据缺失：建议补充主要竞争对手清单"],
    "risks": [
        "宏观经济波动",
        "监管政策变化",
        "技术替代风险",
        "原材料与汇率波动",
    ],
    "outlook": "未来 3-5 年行业预计保持中高个位数增长，结构性机会大于总量机会。",
}


def analyze_sector(sector: str) -> IndustryAnalysis:
    """根据 sector 名称返回行业分析。未知 sector 走默认模板。"""
    kb = _KB.get(sector, _DEFAULT)
    return IndustryAnalysis(sector=sector, **kb)
