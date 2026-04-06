"""
SQLite database for storing Trump quotes.
"""
import sqlite3
import os
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "trump_quotes.db"

SPECIES_TOPIC_MAP = {
    'golfer': ['golf', 'weekend', 'leisure'],
    'executive_pen': ['policy', 'executive', 'order'],
    'truth_social': ['media', 'social', 'post'],
    'media_enemy': ['media', 'fake_news', 'press'],
    'biden_hunter': ['biden', 'election', 'politics'],
    'china_tariff': ['trade', 'china', 'economy'],
    'election_stolen': ['election', 'politics'],
    'self_contradiction': ['self', 'politics'],
}

def get_connection():
    """Get database connection."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database schema."""
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quote TEXT NOT NULL,
            source TEXT,
            date TEXT,
            context TEXT,
            topic TEXT
        )
    """)
    # 添加索引优化查询性能
    conn.execute("CREATE INDEX IF NOT EXISTS idx_quotes_topic ON quotes(topic)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_quotes_quote ON quotes(quote)")
    conn.commit()
    conn.close()

def add_quote(quote: str, source: str = None, date: str = None, context: str = None, topic: str = None):
    """Add a single quote to the database."""
    conn = get_connection()
    conn.execute(
        "INSERT INTO quotes (quote, source, date, context, topic) VALUES (?, ?, ?, ?, ?)",
        (quote, source, date, context, topic)
    )
    conn.commit()
    conn.close()

def add_quotes(quotes: list):
    """Add multiple quotes at once."""
    conn = get_connection()
    conn.executemany(
        "INSERT INTO quotes (quote, source, date, context, topic) VALUES (?, ?, ?, ?, ?)",
        quotes
    )
    conn.commit()
    conn.close()

def get_quotes_by_topic(topic: str, limit: int = 20) -> list:
    """Get quotes filtered by topic."""
    conn = get_connection()
    cursor = conn.execute(
        "SELECT * FROM quotes WHERE topic = ? LIMIT ?",
        (topic, limit)
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_all_quotes(limit: int = 1000) -> list:
    """Get all quotes."""
    conn = get_connection()
    cursor = conn.execute("SELECT * FROM quotes LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_random_quotes(n: int = 10) -> list:
    """Get random quotes for persona building."""
    conn = get_connection()
    cursor = conn.execute("SELECT * FROM quotes ORDER BY RANDOM() LIMIT ?", (n,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def search_quotes(keyword: str, limit: int = 20) -> list:
    """Search quotes by keyword."""

    if not keyword or not keyword.strip():
        return []

    conn = get_connection()
    cursor = conn.execute(
        "SELECT * FROM quotes WHERE quote LIKE ? LIMIT ?",
        (f"%{keyword}%", limit)
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def count_quotes() -> int:
    """Count total quotes in database."""
    conn = get_connection()
    cursor = conn.execute("SELECT COUNT(*) FROM quotes")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_quotes_by_species(species: str, limit: int = 10) -> list:
    """Get quotes by Trump species (mapped from topics)."""
    topics = SPECIES_TOPIC_MAP.get(species, ['self'])
    conn = get_connection()
    placeholders = ','.join(['?'] * len(topics))
    cursor = conn.execute(
        f"SELECT * FROM quotes WHERE topic IN ({placeholders}) LIMIT ?",
        (*topics, limit)
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}")
    print(f"Total quotes: {count_quotes()}")
