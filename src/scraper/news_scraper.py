"""
Generic news scraper for mainstream media RSS feeds.
"""

import feedparser
import hashlib
from datetime import datetime
from typing import List, Dict, Optional


class NewsScraper:
    """Scraper for news RSS feeds."""

    def __init__(self, source_name: str, source_url: str):
        self.source_name = source_name
        self.source_url = source_url

    def scrape(self) -> List[Dict]:
        """Scrape articles from RSS feed."""
        articles = []

        try:
            feed = feedparser.parse(self.source_url)

            for entry in feed.entries:
                article = {
                    "id": self._generate_id(entry.get("link", "")),
                    "title": entry.get("title", ""),
                    "source": self.source_name,
                    "source_url": self.source_url,
                    "source_type": "news",
                    "url": entry.get("link", ""),
                    "published_date": self._parse_date(entry.get("published", "")),
                    "scraped_date": datetime.now().isoformat(),
                    "summary": entry.get("summary", "")[:200],
                    "content_hash": "",
                    "is_new": True,
                }
                articles.append(article)

        except Exception as e:
            print(f"Error scraping {self.source_name}: {e}")

        return articles

    def _generate_id(self, url: str) -> str:
        """Generate unique ID from URL."""
        return hashlib.sha256(url.encode()).hexdigest()[:16]

    def _parse_date(self, date_str: str) -> Optional[str]:
        """Parse date string to YYYY-MM-DD format."""
        if not date_str:
            return None

        try:
            from email.utils import parsedate_to_datetime
            dt = parsedate_to_datetime(date_str)
            return dt.strftime("%Y-%m-%d")
        except:
            return None


def scrape_news(source_name: str, source_url: str) -> List[Dict]:
    """Convenience function to scrape news."""
    scraper = NewsScraper(source_name, source_url)
    return scraper.scrape()
