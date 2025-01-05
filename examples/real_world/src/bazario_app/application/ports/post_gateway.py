from typing import Protocol
from uuid import UUID

from bazario_app.application.models.post import Post


class PostGateway(Protocol):
    def select(self) -> list[Post]: ...
    def insert(self, post: Post) -> None: ...
    def select_where_id_is(self, id: UUID) -> Post | None: ...
