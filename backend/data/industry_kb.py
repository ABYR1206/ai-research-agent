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
