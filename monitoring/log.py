# monitoring/log.py

"""
Tahminleri SQLite veritabanına loglayan monitoring modülü.
"""

import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, Optional

DB_PATH = Path(__file__).resolve().parent / "predictions.db"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    user_id TEXT,
    product_id TEXT,
    probability REAL NOT NULL,
    is_reorder INTEGER NOT NULL,
    threshold REAL NOT NULL
);
"""


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(_SCHEMA)
        conn.commit()


def log_prediction(
    features: Dict[str, Any],
    probability: float,
    is_reorder: int,
    threshold: float,
) -> None:
    init_db()

    user_id: Optional[Any] = features.get("user_id")
    product_id: Optional[Any] = features.get("product_id")

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO predictions (
                created_at, user_id, product_id, probability, is_reorder, threshold
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.utcnow().isoformat(),
                str(user_id) if user_id is not None else None,
                str(product_id) if product_id is not None else None,
                float(probability),
                int(is_reorder),
                float(threshold),
            ),
        )
        conn.commit()
