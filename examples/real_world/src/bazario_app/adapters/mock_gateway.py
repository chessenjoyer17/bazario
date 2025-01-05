from uuid import UUID

from bazario_app.application.models.post import Post
from bazario_app.application.ports.post_gateway import PostGateway


class MockGateway(PostGateway):
    def __init__(self) -> None:
        self._posts: list[Post] = []

    def select(self) -> list[Post]:
        return self._posts

    def insert(self, post: Post) -> None:
        self._posts.append(post)

    def select_where_id_is(self, id: UUID) -> Post | None:
        for post in self._posts:
            if post.id == id:
                return post

        return None
