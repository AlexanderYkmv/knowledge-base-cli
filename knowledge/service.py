from knowledge.model import KnowledgeItem
from knowledge.db import SQLiteStorage


class KnowledgeService:
    def __init__(self, storage: SQLiteStorage):
        self.storage = storage

    def add_item(self, title: str, content: str) -> KnowledgeItem:
        if not title or not title.strip():
            raise ValueError("Title cannot be empty.")

        if not content or not content.strip():
            raise ValueError("Content cannot be empty.")

        return self.storage.add(title.strip(), content.strip())

    def list_all(self) -> list[KnowledgeItem]:
        return self.storage.get_all()

    def get_by_id(self, item_id: int) -> KnowledgeItem:
        item = self.storage.get_by_id(item_id)

        if item is None:
            raise ValueError(
                f"Item with ID {item_id} was not found."
            )

        return item

    def search_items_by_word(self, query: str) -> list[KnowledgeItem]:
        if not query or not query.strip():
            raise ValueError("Search query cannot be empty.")

        return self.storage.search_items_by_word(query.strip())

    def delete_item(self, item_id: int) -> None:
        if item_id <= 0:
            raise ValueError("ID must be a positive number.")

        deleted = self.storage.delete(item_id)

        if not deleted:
            raise ValueError(
                f"Item with ID {item_id} was not found."
            )