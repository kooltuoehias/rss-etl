import feedparser
from typing import List, Dict

def extract_rss_articles(feed_urls: List[str]) -> List[Dict]:
    articles = []

    for url in feed_urls:
        print(f"Fetching: {url}")
        feed = feedparser.parse(url)

        for entry in feed.entries:
            article = {
                "source": feed.feed.get("title", "Unknown Source"),
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
                "summary": entry.get("summary", "")
            }
            articles.append(article)

    return articles

# Example usage
if __name__ == "__main__":
    rss_feeds = [
        "https://www.medicalxpress.com/rss-feed/",
        "https://www.medscape.com/rssfeeds",
        "https://www.statnews.com/feed/"
    ]

    extracted_articles = extract_rss_articles(rss_feeds)

    for article in extracted_articles[:5]:  # Show first 5
        print(f"\n📰 {article['title']}")
        print(f"🔗 {article['link']}")
        print(f"📅 {article['published']}")
        print(f"📌 Source: {article['source']}")

