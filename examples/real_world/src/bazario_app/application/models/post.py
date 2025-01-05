from dataclasses import dataclass
from uuid import UUID


@dataclass
class Post:
    id: UUID
    title: str
    content: str
