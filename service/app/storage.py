import sqlite3
from datetime import datetime
import os
from typing import Optional, Dict, Any

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "deals.db")

class DealDatabase:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.init_db()

    def init_db(self):
        """Initialize all tables according to the structured schema."""
        c = self.conn.cursor()

        # Main deals table
        c.execute("""
            CREATE TABLE IF NOT EXISTS deals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hash TEXT UNIQUE NOT NULL,
                raw_text TEXT NOT NULL,
                status TEXT NOT NULL,
                error TEXT,
                created_at TEXT NOT NULL
            )
        """)

        # Entities table
        c.execute("""
            CREATE TABLE IF NOT EXISTS deal_entities (
                deal_id INTEGER PRIMARY KEY,
                company TEXT,
                sector TEXT,
                geography TEXT,
                stage TEXT,
                round_size TEXT,
                FOREIGN KEY (deal_id) REFERENCES deals(id) ON DELETE CASCADE
            )
        """)

        # Founders (list)
        c.execute("""
            CREATE TABLE IF NOT EXISTS deal_founders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                deal_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                FOREIGN KEY (deal_id) REFERENCES deals(id) ON DELETE CASCADE
            )
        """)

        # Notable metrics (list)
        c.execute("""
            CREATE TABLE IF NOT EXISTS deal_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                deal_id INTEGER NOT NULL,
                metric TEXT NOT NULL,
                FOREIGN KEY (deal_id) REFERENCES deals(id) ON DELETE CASCADE
            )
        """)

        # Investment brief (list with order)
        c.execute("""
            CREATE TABLE IF NOT EXISTS investment_brief_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                deal_id INTEGER NOT NULL,
                item TEXT NOT NULL,
                position INTEGER,
                FOREIGN KEY (deal_id) REFERENCES deals(id) ON DELETE CASCADE
            )
        """)

        # Tags (list)
        c.execute("""
            CREATE TABLE IF NOT EXISTS deal_tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                deal_id INTEGER NOT NULL,
                tag TEXT NOT NULL,
                FOREIGN KEY (deal_id) REFERENCES deals(id) ON DELETE CASCADE
            )
        """)

        self.conn.commit()

    def save_deal(
        self,
        hash_: str,
        raw_text: str,
        extracted: Dict[str, Any],
        status: str,
        error: Optional[str] = None
    ):
        """Save a deal in structured tables."""
        cur = self.conn.cursor()

        # Insert main deal
        cur.execute("""
            INSERT OR IGNORE INTO deals (hash, raw_text, status, error, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (hash_, raw_text, status, error, datetime.utcnow().isoformat()))

        deal_id = cur.lastrowid
        if deal_id == 0:
            # Deal already exists
            deal_id = cur.execute("SELECT id FROM deals WHERE hash = ?", (hash_,)).fetchone()[0]

        entities = extracted.get("entities", {})

        # Entities
        cur.execute("""
            INSERT OR REPLACE INTO deal_entities
            (deal_id, company, sector, geography, stage, round_size)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            deal_id,
            entities.get("company"),
            entities.get("sector"),
            entities.get("geography"),
            entities.get("stage"),
            entities.get("round_size"),
        ))

        # Founders
        for f in entities.get("founders") or []:
            cur.execute(
                "INSERT INTO deal_founders (deal_id, name) VALUES (?, ?)",
                (deal_id, f)
            )

        # Metrics
        for m in entities.get("notable_metrics") or []:
            cur.execute(
                "INSERT INTO deal_metrics (deal_id, metric) VALUES (?, ?)",
                (deal_id, m)
            )

        # Investment brief
        for i, item in enumerate(extracted.get("investment_brief") or []):
            cur.execute(
                "INSERT INTO investment_brief_items (deal_id, item, position) VALUES (?, ?, ?)",
                (deal_id, item, i)
            )

        # Tags
        for tag in extracted.get("tags") or []:
            cur.execute(
                "INSERT INTO deal_tags (deal_id, tag) VALUES (?, ?)",
                (deal_id, tag)
            )

        self.conn.commit()

    def get_deal_by_id(self, deal_id: int) -> Optional[Dict[str, Any]]:
        """Fetch a deal and reconstruct JSON-like structure."""
        cur = self.conn.cursor()
        deal_row = cur.execute("SELECT * FROM deals WHERE id = ?", (deal_id,)).fetchone()
        if not deal_row:
            return None

        entities_row = cur.execute("SELECT * FROM deal_entities WHERE deal_id = ?", (deal_id,)).fetchone()

        # Fetch lists
        founders = [r[0] for r in cur.execute("SELECT name FROM deal_founders WHERE deal_id = ?", (deal_id,))]
        metrics = [r[0] for r in cur.execute("SELECT metric FROM deal_metrics WHERE deal_id = ?", (deal_id,))]
        brief = [r[0] for r in cur.execute("SELECT item FROM investment_brief_items WHERE deal_id = ? ORDER BY position",(deal_id,)).fetchall()]
        tags = [r[0] for r in cur.execute("SELECT tag FROM deal_tags WHERE deal_id = ?", (deal_id,))]

        return {
            "hash": deal_row[1],
            "raw_text": deal_row[2],
            "status": deal_row[3],
            "error": deal_row[4],
            "created_at": deal_row[5],
            "entities": {
                "company": entities_row[1] if entities_row else None,
                "sector": entities_row[2] if entities_row else None,
                "geography": entities_row[3] if entities_row else None,
                "stage": entities_row[4] if entities_row else None,
                "round_size": entities_row[5] if entities_row else None,
                "founders": founders,
                "notable_metrics": metrics
            },
            "investment_brief": brief,
            "tags": tags
        }
    
    def get_latest_deals(self, limit: int = 10) -> list[dict]:
        """Fetch latest deals (top-level info only)."""
        cur = self.conn.cursor()
        rows = cur.execute(
            "SELECT id, hash, status, error, created_at FROM deals ORDER BY id DESC LIMIT ?",
            (limit,)
        ).fetchall()

        # Convert to list of dicts
        return [
            {
                "id": row[0],
                "hash": row[1],
                "status": row[2],
                "error": row[3],
                "created_at": row[4]
            }
            for row in rows
        ]


    def close(self):
        self.conn.close()
