import re
import sqlite3


def normalize_alias(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


class CanvasAliasRepository:
    def __init__(self, db_path: str = "canvas_app.db"):
        self.db_path = db_path
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS canvas_aliases (
                    alias_key TEXT NOT NULL,
                    entity_type TEXT NOT NULL,
                    canvas_id TEXT NOT NULL,
                    display_name TEXT NOT NULL,
                    course_id TEXT,
                    source TEXT NOT NULL DEFAULT 'system',
                    PRIMARY KEY(alias_key, entity_type)
                )
            """)

    def save_alias(
        self,
        alias_key: str,
        entity_type: str,
        canvas_id: str | int,
        display_name: str,
        course_id: str | int | None = None,
        source: str = "system",
    ):
        alias_key = normalize_alias(alias_key)

        with self._connect() as conn:
            conn.execute("""
                INSERT INTO canvas_aliases (
                    alias_key, entity_type, canvas_id, display_name, course_id, source
                )
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(alias_key, entity_type) DO UPDATE SET
                    canvas_id = excluded.canvas_id,
                    display_name = excluded.display_name,
                    course_id = excluded.course_id,
                    source = excluded.source
            """, (
                alias_key,
                entity_type,
                str(canvas_id),
                display_name,
                str(course_id) if course_id is not None else None,
                source,
            ))

    def resolve(self, entity_type: str, alias_key: str):
        alias_key = normalize_alias(alias_key)

        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute("""
                SELECT * FROM canvas_aliases
                WHERE entity_type = ? AND alias_key = ?
            """, (entity_type, alias_key)).fetchone()

        return dict(row) if row else None

    def list_aliases(self):
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("""
                SELECT * FROM canvas_aliases
                ORDER BY entity_type, alias_key
            """).fetchall()

        return [dict(row) for row in rows]