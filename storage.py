import sqlite3
from datetime import datetime


def init_db():
    conn = sqlite3.connect("data/deals.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS deals (
            id INTEGER PRIMARY KEY,
            hash TEXT UNIQUE,
            raw_text TEXT,
            extracted_json TEXT,
            status TEXT,
            error TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    return conn


def save_deal(conn, hash_, raw, extracted, status, error=None):
    conn.execute(
        """
        INSERT OR IGNORE INTO deals
        (hash, raw_text, extracted_json, status, error, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (hash_, raw, extracted, status, error, datetime.utcnow().isoformat())
    )
    conn.commit()
