import sqlite3
from datetime import datetime, timezone


class CanvasTokenRepository:
    def __init__(self, db_path: str = "canvas_app.db"):
        self.db_path = db_path
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS canvas_tokens (
                    profile_key TEXT PRIMARY KEY,
                    canvas_base_url TEXT NOT NULL,
                    access_token TEXT NOT NULL,
                    refresh_token TEXT,
                    expires_at INTEGER,
                    updated_at TEXT NOT NULL
                )
            """)

    def save_token(
        self,
        profile_key: str,
        canvas_base_url: str,
        access_token: str,
        refresh_token: str | None = None,
        expires_at: int | None = None,
    ):
        now = datetime.now(timezone.utc).isoformat()

        with self._connect() as conn:
            conn.execute("""
                INSERT INTO canvas_tokens (
                    profile_key, canvas_base_url, access_token,
                    refresh_token, expires_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(profile_key) DO UPDATE SET
                    canvas_base_url = excluded.canvas_base_url,
                    access_token = excluded.access_token,
                    refresh_token = excluded.refresh_token,
                    expires_at = excluded.expires_at,
                    updated_at = excluded.updated_at
            """, (
                profile_key,
                canvas_base_url,
                access_token,
                refresh_token,
                expires_at,
                now,
            ))

    def get_token(self, profile_key: str = "default"):
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute("""
                SELECT * FROM canvas_tokens
                WHERE profile_key = ?
            """, (profile_key,)).fetchone()

        return dict(row) if row else None