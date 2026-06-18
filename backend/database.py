import sqlite3
from datetime import datetime,UTC
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

DEFAULT_DB_PATH = Path("backend/multicloud.db")


def get_connection(db_path: str | Path | None = None) -> sqlite3.Connection:
    """Open a SQLite connection to the backend database."""
    database_path = Path(db_path) if db_path else DEFAULT_DB_PATH
    database_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(str(database_path))
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(db_path: str | Path | None = None) -> None:
    """Initialize the recommendation_history table in the SQLite database."""
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS recommendation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT,
                budget REAL,
                storage TEXT,
                compute_requirement TEXT,
                security_requirement TEXT,
                aiml_requirement TEXT,
                business_type TEXT,
                aws_score REAL,
                gcp_score REAL,
                esds_score REAL,
                recommended_platform TEXT,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def save_recommendation(
    user_name: str,
    budget: float,
    storage: str,
    compute_requirement: str,
    security_requirement: str,
    aiml_requirement: str,
    business_type: str,
    aws_score: float,
    gcp_score: float,
    esds_score: float,
    recommended_platform: str,
    db_path: str | Path | None = None,
) -> int:
    """Save a recommendation record and return the created row ID."""
    initialize_database(db_path)
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO recommendation_history (
                user_name,
                budget,
                storage,
                compute_requirement,
                security_requirement,
                aiml_requirement,
                business_type,
                aws_score,
                gcp_score,
                esds_score,
                recommended_platform,
                created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_name,
                budget,
                storage,
                compute_requirement,
                security_requirement,
                aiml_requirement,
                business_type,
                aws_score,
                gcp_score,
                esds_score,
                recommended_platform,
                datetime.utcnow().isoformat(),
            ),
        )
        conn.commit()
        return cursor.lastrowid


def get_recommendations(db_path: str | Path | None = None) -> List[Dict[str, Any]]:
    """Return all recommendation history rows as dictionaries."""
    initialize_database(db_path)
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM recommendation_history ORDER BY created_at DESC"
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def delete_recommendation(recommendation_id: int, db_path: str | Path | None = None) -> bool:
    """Delete a recommendation by ID and return True if a row was removed."""
    initialize_database(db_path)
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM recommendation_history WHERE id = ?",
            (recommendation_id,),
        )
        conn.commit()
        return cursor.rowcount > 0
