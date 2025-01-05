from dataclasses import dataclass
from uuid import UUID, uuid4

from bazario_app.application.events import PostAdded
from bazario_app.application.models.post import Post
from bazario_app.application.ports.post_gateway import PostGateway
from bazario_app.application.ports.transaction import Transaction

from bazario.markers import Request
from bazario.protocols.handler import RequestHandler
from bazario.protocols.publisher import Publisher


@dataclass(frozen=True)
class AddPost(Request[UUID]):
    title: str
    content: str


class AddPostHandler(RequestHandler[UUID, AddPost]):
    def __init__(
        self,
        gateway: PostGateway,
        publisher: Publisher,
        transaction: Transaction,
    ) -> None:
        self._gateway = gateway
        self._publisher = publisher
        self._transaction = transaction

    def handle(self, request: AddPost) -> UUID:
        post = Post(uuid4(), request.title, request.content)

        self._gateway.insert(post)

        self._publisher.publish(PostAdded(post.id))

        self._transaction.commit()

        return post.id
