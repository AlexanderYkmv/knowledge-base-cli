import pytest

from knowledge.db import SQLiteStorage
from knowledge.service import KnowledgeService


@pytest.fixture
def service(tmp_path):
    storage = SQLiteStorage(tmp_path / "test.db")
    return KnowledgeService(storage)


def test_add_item(service):
    item = service.add_item("Python", "Programming language.")
    assert item.title == "Python"
    assert item.content == "Programming language."


def test_list_all(service):
    service.add_item("Python", "Programming language.")
    service.add_item("Docker", "Containerization tool.")

    assert len(service.list_all()) == 2


def test_search_by_word(service):
    service.add_item("Python", "Programming language.")
    service.add_item("Docker", "Containerization tool.")

    results = service.search_items_by_word("python")

    assert len(results) == 1
    assert results[0].title == "Python"