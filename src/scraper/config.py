"""
Configuration for education policy scraper.
Contains source definitions, keywords, and classification rules.
"""

# ===== Data Sources =====
SOURCES = {
    "moe": {
        "name": "教育部",
        "name_en": "Ministry of Education",
        "type": "national",
        "source_type": "rss",
        "url": "http://www.moe.gov.cn/rss/news.xml",
        "enabled": True,
    },
    "mohrss": {
        "name": "人社部",
        "name_en": "Ministry of Human Resources and Social Security",
        "type": "national",
        "source_type": "web",
        "url": "https://www.mohrss.gov.cn/xxgk/zyrmzfzc/",
        "enabled": True,
    },
    "news_xinhua": {
        "name": "新华网",
        "name_en": "Xinhua News",
        "type": "news",
        "source_type": "rss",
        "url": "http://www.news.cn/rss/education.xml",
        "enabled": True,
    },
    "news_people": {
        "name": "人民网教育",
        "name_en": "People's Daily Education",
        "type": "news",
        "source_type": "rss",
        "url": "http://paper.people.com.cn/jyb/rss/education.xml",
        "enabled": True,
    },
}

# ===== Provincial Sources =====
PROVINCIAL_SOURCES = {
    "beijing": {
        "name": "北京市教育委员会",
        "type": "provincial",
        "url": "http://jw.beijing.gov.cn/",
        "enabled": False,  # Will implement later
    },
    "shanghai": {
        "name": "上海市教育委员会",
        "type": "provincial",
        "url": "http://edu.shanghai.gov.cn/",
        "enabled": False,
    },
    "guangdong": {
        "name": "广东省教育厅",
        "type": "provincial",
        "url": "http://edu.gd.gov.cn/",
        "enabled": False,
    },
}

# ===== Classification Keywords =====
CLASSIFIER_KEYWORDS = {
    "include": {
        # Vocational education
        "职业教育": 3,
        "高职": 3,
        "职业院校": 3,
        "技工院校": 2,
        "技能人才": 2,
        "职业技能": 2,
        "产教融合": 2,
        "双高计划": 2,

        # Higher education / undergraduate
        "本科教育": 3,
        "高等院校": 3,
        "高校": 2,
        "本科院校": 3,
        "研究生": 1,
        "硕博": 1,
        "学科建设": 1,
        "一流大学": 2,
        "一流学科": 2,

        # General (context dependent)
        "教育改革": 1,
        "教育政策": 1,
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
    }
}

# Score threshold for inclusion
SCORE_THRESHOLD = 0

# ===== Scraping Settings =====
SCRAPING_SETTINGS = {
    "timeout": 30,  # seconds per source
    "retry_count": 3,
    "retry_delay": 2,  # seconds
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

# ===== Output Settings =====
OUTPUT_SETTINGS = {
    "data_dir": "data",
    "articles_file": "data/articles.json",
    "keep_articles_days": 180,  # Keep articles for 6 months
}

# ===== Content Categories =====
CATEGORIES = {
    "vocational": "职业教育",
    "undergraduate": "本科教育",
    "news": "资讯",
    "policy": "政策",
}
