"""
Configuration for education policy scraper.
Contains source definitions, keywords, and classification rules.

数据源策略: 优先使用可访问的第三方媒体RSS，政策信息来自多家媒体转载，
交叉验证确保可靠性。
"""

# ===== Data Sources (Third-party Media - More Reliable) =====
SOURCES = {
    # 新华网 - 教育频道 (国家政策主要来源)
    "news_xinhua": {
        "name": "新华网教育",
        "name_en": "Xinhua Education",
        "type": "industry",
        "source_type": "rss",
        "url": "http://www.news.cn/rss/education.xml",
        "enabled": True,
        "category": "行业",
    },
    # 人民网 - 教育 (政策转载)
    "news_people": {
        "name": "人民网教育",
        "name_en": "People's Daily Education",
        "type": "industry",
        "source_type": "rss",
        "url": "http://paper.people.com.cn/jyb/rss/education.xml",
        "enabled": True,
        "category": "行业",
    },
    # 光明日报 - 教育
    "news_gmw": {
        "name": "光明日报教育",
        "name_en": "Guangming Daily Education",
        "type": "industry",
        "source_type": "rss",
        "url": "http://www.gmw.cn/rss/education.xml",
        "enabled": True,
        "category": "行业",
    },
    # 中国教育报 RSS
    "news_jyb": {
        "name": "中国教育报",
        "name_en": "China Education Daily",
        "type": "industry",
        "source_type": "rss",
        "url": "http://paper.jyb.cn/rss/education.xml",
        "enabled": True,
        "category": "行业",
    },
    # 36kr - 教育科技
    "news_36kr": {
        "name": "36氪教育",
        "name_en": "36Kr Education",
        "type": "industry",
        "source_type": "rss",
        "url": "https://36kr.com/feed/education",
        "enabled": True,
        "category": "行业",
    },
}

# ===== Policy Sources (Direct Government - Using Search Engine Cached) =====
# 由于政府网站直接爬取困难，政策信息主要通过媒体转载获取
# 但以下源可作为补充验证
POLICY_SOURCES = {
    # 微信公众号 - 主流媒体政策解读
    "wechat_moe": {
        "name": "教育部官方微信",
        "type": "policy",
        "source_type": "rss",
        "url": "https://mp.weixin.qq.com/rss",
        "enabled": False,  # 微信需要特殊处理
    },
}

# ===== Provincial Sources (Media Reports) =====
# 省级政策通过媒体转载获取，减少直接爬取
PROVINCIAL_VIA_MEDIA = {
    # 通过媒体搜索"省份 + 政策关键词"获取
    "media_guangdong": {
        "name": "广东省政策(媒体转载)",
        "type": "provincial",
        "enabled": True,
        "keywords": ["广东", "职业教育", "教育厅"],
    },
    "media_zhejiang": {
        "name": "浙江省政策(媒体转载)",
        "type": "provincial",
        "enabled": True,
        "keywords": ["浙江", "本科教育", "教育厅"],
    },
    "media_beijing": {
        "name": "北京市政策(媒体转载)",
        "type": "provincial",
        "enabled": True,
        "keywords": ["北京", "教育改革", "教委"],
    },
}

# ===== Vendor/Industry News Sources =====
VENDOR_SOURCES = {
    "vendor_zhongjiao": {
        "name": "中教畅享",
        "type": "vendor",
        "source_type": "rss",
        "url": "https://www.zhongjiao.cn/feed",
        "enabled": True,
    },
    "vendor_chaoxing": {
        "name": "超星",
        "type": "vendor",
        "source_type": "rss",
        "url": "https://www.chaoxing.com/rss",
        "enabled": False,  # 可能没有RSS
    },
}

# ===== Classification Keywords =====
CLASSIFIER_KEYWORDS = {
    "include": {
        # Vocational education (职业教育)
        "职业教育": 3,
        "高职": 3,
        "职业院校": 3,
        "技工院校": 2,
        "技能人才": 2,
        "职业技能": 2,
        "产教融合": 2,
        "双高计划": 2,
        "1+X证书": 2,
        "学徒制": 2,
        "职业技能等级": 2,

        # Higher education / undergraduate (本科教育)
        "本科教育": 3,
        "高等院校": 3,
        "高校": 2,
        "本科院校": 3,
        "研究生": 1,
        "硕博": 1,
        "学科建设": 1,
        "一流大学": 2,
        "一流学科": 2,
        "拔尖人才培养": 2,
        "通识教育": 1,

        # Policy related
        "教育部": 2,
        "人社部": 2,
        "教育厅": 2,
        "实施意见": 1,
        "行动计划": 1,
        "高质量发展": 1,
        "数字化转型": 1,
    },
    "exclude": {
        # K-12 related (strong negative)
        "中小学": -10,
        "义务教育": -10,
        "幼儿园": -10,
        "学前教育": -5,
        "初中": -5,
        "小学": -5,
        "高中": -3,
        "普通高中": -3,
        "中考": -5,
        "高考": -3,
        "义务教育阶段": -10,
        "基础教育": -2,
        "少年宫": -5,
        "校外培训": -3,
        "培训机构": -3,
        "k12": -10,
        "学区房": -5,
        "择校": -3,

        # Non-relevant
        "体育": -1,
        "艺术": -1,
        "文艺": -1,
    }
}

# Policy level detection keywords
POLICY_LEVEL_KEYWORDS = {
    "国家": ["教育部", "人社部", "国务院", "国家标准", "国家级"],
    "省级": ["省教育厅", "省人社厅", "省人民政府", "广东省", "浙江省", "江苏省", "山东省", "四川省"],
}

# Education level detection keywords
EDUCATION_LEVEL_KEYWORDS = {
    "职业教育": ["职业教育", "高职", "职业院校", "技工", "技能人才", "产教融合", "1+X", "学徒制"],
    "本科教育": ["本科教育", "高等院校", "高校", "本科院校", "学科建设", "一流大学", "研究生", "硕博"],
}

# Score threshold for inclusion
SCORE_THRESHOLD = 0

# ===== Scraping Settings =====
SCRAPING_SETTINGS = {
    "timeout": 30,
    "retry_count": 3,
    "retry_delay": 2,
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

# ===== Output Settings =====
OUTPUT_SETTINGS = {
    "data_dir": "data",
    "articles_file": "data/articles.json",
    "keep_articles_days": 180,
}

# ===== Content Categories =====
CATEGORIES = {
    "vocational": "职业教育",
    "undergraduate": "本科教育",
    "news": "资讯",
    "policy": "政策",
}
