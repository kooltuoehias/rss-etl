import sqlite3
from typing import List, Dict

def load_articles_to_sqlite(articles: List[Dict], db_path: str = "data/articles.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table with UNIQUE constraint on title
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE,  -- UNIQUE constraint on title
            url TEXT,
            published DATETIME,
            source TEXT,
            summary TEXT,
            category TEXT
        )
    """)
    
    new_articles = 0
    for article in articles:
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO articles (title, url, published, source, summary, category)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                article.get("title"),
                article.get("link"),  # Assuming your extract uses "link"
                article.get("published"),
                article.get("source"),
                article.get("summary"),
                article.get("category", "Uncategorized")
            ))
            if cursor.rowcount > 0:  # Check if row was actually inserted
                new_articles += 1
        except sqlite3.Error as e:
            print(f"Error inserting article: {e}")
    
    conn.commit()
    conn.close()
    print(f"Inserted {new_articles} new articles out of {len(articles)} total")
    return new_articles
