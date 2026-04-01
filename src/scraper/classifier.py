"""
Content classifier for education policy articles.
Uses keyword scoring to determine if an article is relevant.
"""

import jieba
import re
from typing import List, Tuple
from .config import CLASSIFIER_KEYWORDS, SCORE_THRESHOLD


class ArticleClassifier:
    """Classifies articles based on keyword matching."""

    def __init__(self):
        # Load keywords into jieba for better Chinese word segmentation
        for keyword in CLASSIFIER_KEYWORDS["include"].keys():
            jieba.add_word(keyword)
        for keyword in CLASSIFIER_KEYWORDS["exclude"].keys():
            jieba.add_word(keyword)

        self.include_keywords = CLASSIFIER_KEYWORDS["include"]
        self.exclude_keywords = CLASSIFIER_KEYWORDS["exclude"]

    def classify(self, title: str, content: str = "") -> Tuple[bool, float, List[str]]:
        """
        Classify an article as relevant or not.

        Args:
            title: Article title
            content: Article content (optional, used for additional context)

        Returns:
            Tuple of (is_relevant, score, matched_categories)
        """
        # Combine title and content for scoring
        text = title + " " + (content[:500] if content else "")

        # Segment text
        words = set(jieba.cut(text))

        score = 0
        matched_categories = []

        # Check include keywords
        for keyword, weight in self.include_keywords.items():
            if keyword in text:
                score += weight
                # Track which category matched
                if weight >= 3:
                    matched_categories.append(keyword)

        # Check exclude keywords
        for keyword, weight in self.exclude_keywords.items():
            if keyword in text:
                score += weight

        # Determine relevance
        is_relevant = score > SCORE_THRESHOLD

        return is_relevant, score, matched_categories

    def get_category(self, title: str, content: str = "") -> str:
        """
        Determine the primary category of an article.

        Returns:
            Category string: "职业教育", "本科教育", "资讯", or "政策"
        """
        text = (title + " " + (content[:500] if content else "")).lower()

        # Vocational education indicators
        vocational_keywords = ["职业教育", "高职", "职业院校", "技工", "技能人才", "产教融合"]
        undergraduate_keywords = ["本科", "高校", "高等院校", "研究生", "学科建设", "一流大学"]

        vocational_count = sum(1 for k in vocational_keywords if k in text)
        undergraduate_count = sum(1 for k in undergraduate_keywords if k in text)

        if vocational_count > undergraduate_count:
            return "职业教育"
        elif undergraduate_count > vocational_count:
            return "本科教育"
        else:
            return "政策"


def classify_article(title: str, content: str = "") -> Tuple[bool, float, List[str]]:
    """
    Convenience function for quick classification.
    """
    classifier = ArticleClassifier()
    return classifier.classify(title, content)
