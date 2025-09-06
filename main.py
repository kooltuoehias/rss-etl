# main.py
import json
from etl.extract import extract_rss_articles
from etl.transform import transform_articles
from etl.load import load_articles_to_sqlite

def load_feeds_from_json(path: str) -> list:
    with open(path, "r") as f:
        config = json.load(f)
    return config.get("rss_feeds", [])

def run_etl():
    print("🔍 Loading RSS feed URLs...")
    feed_urls = load_feeds_from_json("config/feeds.json")

    print("📥 Extracting articles...")
    raw_articles = extract_rss_articles(feed_urls)

    print(f"🧪 Transforming {len(raw_articles)} articles...")
    transformed_articles = transform_articles(raw_articles)


    print("💾 Loading into SQLite database...")
    load_articles_to_sqlite(transformed_articles)

    print("✅ ETL pipeline completed successfully.")

if __name__ == "__main__":
    run_etl()

