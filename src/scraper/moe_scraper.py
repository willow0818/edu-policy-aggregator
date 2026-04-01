"""
Scraper for Ministry of Education RSS feeds.
"""

import feedparser
import hashlib
from datetime import datetime
from typing import List, Dict, Optional
from .config import SCRAPING_SETTINGS


class MOEScraper:
    """Scraper for Ministry of Education RSS feed."""

    def __init__(self):
        self.source_name = "教育部"
        self.source_url = "http://www.moe.gov.cn/rss/news.xml"
        self.settings = SCRAPING_SETTINGS

    def scrape(self) -> List[Dict]:
        """
        Scrape articles from MOE RSS feed.

        Returns:
            List of article dictionaries
        """
        articles = []

        try:
            feed = feedparser.parse(self.source_url)

            for entry in feed.entries:
                article = {
                    "id": self._generate_id(entry.get("link", "")),
                    "title": entry.get("title", ""),
                    "source": self.source_name,
                    "source_url": self.source_url,
                    "source_type": "national",
                    "url": entry.get("link", ""),
                    "published_date": self._parse_date(entry.get("published", "")),
                    "scraped_date": datetime.now().isoformat(),
                    "summary": entry.get("summary", "")[:200],
                    "content_hash": "",
                    "is_new": True,
                }
                articles.append(article)

        except Exception as e:
            print(f"Error scraping MOE: {e}")

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


def scrape_moe() -> List[Dict]:
    """Convenience function to scrape MOE."""
    scraper = MOEScraper()
    return scraper.scrape()
