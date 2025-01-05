from dataclasses import dataclass
from uuid import UUID

from bazario_app.application.models.post import Post
from bazario_app.application.ports.post_gateway import PostGateway

from bazario.markers import Request
from bazario.protocols.handler import RequestHandler


class GetAllPosts(Request[list[Post]]):
    pass


@dataclass(frozen=True)
class GetPostById(Request[Post]):
    post_id: UUID


# TODO: сделать ебучий хэндлер без параметров
class GetAllPostsHandler(RequestHandler[GetAllPosts, list[Post]]):
    def __init__(self, gateway: PostGateway) -> None:
        self._gateway = gateway

    def handle(self, request: GetAllPosts) -> list[Post]:
        return self._gateway.select()


class GetPostByIdHandler(RequestHandler[GetPostById, Post]):
    def __init__(self, gateway: PostGateway) -> None:
        self._gateway = gateway

    def handle(self, request: GetPostById) -> Post:
        post = self._gateway.select_where_id_is(request.post_id)

        if post is None:
            raise ValueError(f"Post with id {request.post_id} not found")

        return post
