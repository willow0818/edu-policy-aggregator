"""
Deduplication logic for scraped articles.
"""

import hashlib
from typing import List, Dict, Set


class Deduplicator:
    """Removes duplicate articles based on URL and content."""

    def __init__(self):
        self.seen_urls: Set[str] = set()
        self.seen_hashes: Set[str] = set()

    def add_article(self, article: Dict) -> bool:
        """
        Add an article to the deduplication cache.

        Returns:
            True if article is new (not a duplicate), False if duplicate
        """
        url = article.get("url", "")

        # Check URL-based deduplication
        if url in self.seen_urls:
            return False

        # Check content hash deduplication
        content_hash = article.get("content_hash", "")
        if content_hash and content_hash in self.seen_hashes:
            return False

        # Mark as seen
        self.seen_urls.add(url)
        if content_hash:
            self.seen_hashes.add(content_hash)

        return True

    def deduplicate(self, articles: List[Dict]) -> List[Dict]:
        """
        Remove duplicate articles from a list.

        Returns:
            List of unique articles
        """
        unique_articles = []

        for article in articles:
            if self.add_article(article):
                unique_articles.append(article)

        return unique_articles


def deduplicate_articles(new_articles: List[Dict], existing_articles: List[Dict] = None) -> List[Dict]:
    """
    Deduplicate articles, optionally merging with existing articles.

    Args:
        new_articles: List of newly scraped articles
        existing_articles: List of previously scraped articles

    Returns:
        List of unique articles
    """
    dedup = Deduplicator()

    # First add existing articles to the cache
    if existing_articles:
        for article in existing_articles:
            dedup.add_article(article)

    # Then filter new articles
    return dedup.deduplicate(new_articles)
