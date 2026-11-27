from dataclasses import dataclass


@dataclass
class KnowledgeItem:
    id: int
    title: str
    content: str