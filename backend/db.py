import sqlite3
from pathlib import Path

from backend.models import KnowledgeItem


class SQLiteStorage:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self._initialize_database()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _initialize_database(self):
        with self._get_connection() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS knowledge_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL
                )
                """
            )

    def add(self, title: str, content: str) -> KnowledgeItem:
        with self._get_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO knowledge_items (title, content)
                VALUES (?, ?)
                """,
                (title, content),
            )

            item_id = cursor.lastrowid

        return KnowledgeItem(
            id=item_id,
            title=title,
            content=content,
        )

    def get_all(self) -> list[KnowledgeItem]:
        with self._get_connection() as connection:
            rows = connection.execute(
                """
                SELECT id, title, content
                FROM knowledge_items
                ORDER BY id
                """
            ).fetchall()

        return [
            KnowledgeItem(id=row[0], title=row[1], content=row[2])
            for row in rows
        ]

    def get_by_id(self, item_id: int) -> KnowledgeItem | None:
        with self._get_connection() as connection:
            row = connection.execute(
                """
                SELECT id, title, content
                FROM knowledge_items
                WHERE id = ?
                """,
                (item_id,),
            ).fetchone()

        if row is None:
            return None

        return KnowledgeItem(
            id=row[0],
            title=row[1],
            content=row[2],
        )

    def search(self, query: str) -> list[KnowledgeItem]:
        search_term = f"%{query}%"

        with self._get_connection() as connection:
            rows = connection.execute(
                """
                SELECT id, title, content
                FROM knowledge_items
                WHERE title LIKE ? COLLATE NOCASE
                   OR content LIKE ? COLLATE NOCASE
                ORDER BY id
                """,
                (search_term, search_term),
            ).fetchall()

        return [
            KnowledgeItem(id=row[0], title=row[1], content=row[2])
            for row in rows
        ]

    def delete(self, item_id: int) -> bool:
        with self._get_connection() as connection:
            cursor = connection.execute(
                """
                DELETE FROM knowledge_items
                WHERE id = ?
                """,
                (item_id,),
            )

            return cursor.rowcount > 0