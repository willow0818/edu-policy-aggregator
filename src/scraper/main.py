"""
Main entry point for the education policy scraper.
Orchestrates scraping, classification, and output generation.
"""

import json
import os
import sys
from datetime import datetime
from typing import List, Dict

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper.config import SOURCES, PROVINCIAL_SOURCES, OUTPUT_SETTINGS
from scraper.classifier import ArticleClassifier
from scraper.moe_scraper import scrape_moe
from scraper.news_scraper import NewsScraper
from scraper.vendor_news_scraper import scrape_all_vendors
from scraper.deduplicator import deduplicate_articles


def load_existing_articles(filepath: str) -> List[Dict]:
    """Load existing articles from JSON file."""
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("articles", [])
        except Exception as e:
            print(f"Error loading existing articles: {e}")
    return []


def save_articles(articles: List[Dict], filepath: str, metadata: Dict):
    """Save articles to JSON file."""
    output_dir = os.path.dirname(filepath)
    os.makedirs(output_dir, exist_ok=True)

    data = {
        "articles": articles,
        "metadata": metadata
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(articles)} articles to {filepath}")


def classify_and_filter(articles: List[Dict]) -> List[Dict]:
    """Classify articles and filter by relevance."""
    classifier = ArticleClassifier()
    filtered_articles = []

    for article in articles:
        title = article.get("title", "")
        content = article.get("summary", "")

        is_relevant, score, categories = classifier.classify(title, content)

        if is_relevant:
            article["score"] = score
            article["categories"] = categories
            article["primary_category"] = classifier.get_category(title, content)
            filtered_articles.append(article)

    return filtered_articles


def scrape_all_sources() -> List[Dict]:
    """Scrape all enabled sources."""
    all_articles = []

    # Scrape Ministry of Education
    if SOURCES.get("moe", {}).get("enabled", False):
        print("Scraping Ministry of Education...")
        moe_articles = scrape_moe()
        all_articles.extend(moe_articles)
        print(f"  Found {len(moe_articles)} articles from MOE")

    # Scrape news sources
    news_sources = [
        ("新华网", "http://www.news.cn/rss/education.xml"),
        ("人民网教育", "http://paper.people.com.cn/jyb/rss/education.xml"),
    ]

    for name, url in news_sources:
        source_key = None
        for key, val in SOURCES.items():
            if val.get("name") == name and val.get("enabled", False):
                source_key = key
                break

        if source_key:
            print(f"Scraping {name}...")
            scraper = NewsScraper(name, url)
            articles = scraper.scrape()
            all_articles.extend(articles)
            print(f"  Found {len(articles)} articles")

    # Scrape vendor sources
    print("Scraping EdTech vendor news...")
    vendor_articles = scrape_all_vendors()
    all_articles.extend(vendor_articles)
    print(f"  Found {len(vendor_articles)} articles from vendors")

    return all_articles


def main():
    """Main execution function."""
    print("=" * 60)
    print("Education Policy Aggregator")
    print(f"Started at: {datetime.now().isoformat()}")
    print("=" * 60)

    start_time = datetime.now()

    # Output file path
    output_file = OUTPUT_SETTINGS["articles_file"]

    # Load existing articles (for deduplication)
    existing_articles = load_existing_articles(output_file)
    print(f"Loaded {len(existing_articles)} existing articles")

    # Scrape all sources
    print("\n--- Scraping Phase ---")
    new_articles = scrape_all_sources()
    print(f"Total scraped: {len(new_articles)} articles")

    # Deduplicate
    print("\n--- Deduplication Phase ---")
    all_articles = deduplicate_articles(new_articles, existing_articles)
    print(f"After deduplication: {len(all_articles)} unique articles")

    # Classify and filter
    print("\n--- Classification Phase ---")
    filtered_articles = classify_and_filter(all_articles)
    print(f"After classification: {len(filtered_articles)} relevant articles")

    # Sort by date (newest first)
    filtered_articles.sort(
        key=lambda x: x.get("published_date", ""),
        reverse=True
    )

    # Generate metadata
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    metadata = {
        "version": "1.0",
        "total_count": len(filtered_articles),
        "last_updated": end_time.isoformat(),
        "scrape_duration_seconds": duration,
        "sources_covered": [SOURCES.get("moe", {}).get("name", "教育部")],
    }

    # Save output
    print("\n--- Saving Phase ---")
    save_articles(filtered_articles, output_file, metadata)

    print("\n" + "=" * 60)
    print("Scrape completed successfully!")
    print(f"Duration: {duration:.2f} seconds")
    print(f"Articles: {len(filtered_articles)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
