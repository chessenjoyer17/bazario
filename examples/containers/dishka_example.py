from dataclasses import dataclass
from typing import Protocol
from uuid import UUID, uuid4

from dishka import Container, Provider, Scope, WithParents, make_container

from bazario import (
    Notification,
    NotificationHandler,
    Publisher,
    Request,
    RequestHandler,
    Sender,
)
from bazario.plugins.dishka import (
    DishkaHandlerResolver,
    DishkaNotificationHandlerFinder,
    DishkaRequestHandlerFinder,
    dispatcher_factory,
)


# domain entities
@dataclass
class Post:
    id: UUID
    title: str
    content: str


# application models
@dataclass(frozen=True)
class AddPost(Request[None]):
    title: str
    content: str


@dataclass(frozen=True)
class PostAdded(Notification):
    post_id: UUID


# application ports
class PostRepository(Protocol):
    def add(self, post: Post) -> None: ...


class TransactionCommiter(Protocol):
    def commit(self) -> None: ...


class Logger(Protocol):
    def log(self, message: str) -> None: ...


# application handlers
class AddPostHandler(RequestHandler[AddPost, None]):
    def __init__(
        self,
        publisher: Publisher,
        post_repository: PostRepository,
        transaction_commiter: TransactionCommiter,
    ) -> None:
        self._publisher = publisher
        self._post_repository = post_repository
        self._transaction_commiter = transaction_commiter

    def handle(self, request: AddPost) -> None:
        new_post = Post(
            id=uuid4(),
            title=request.title,
            content=request.content,
        )
        self._post_repository.add(new_post)
        self._publisher.publish(PostAdded(post_id=new_post.id))

        self._transaction_commiter.commit()


class LogOnPostAddedHandler(NotificationHandler[PostAdded]):
    def __init__(self, logger: Logger) -> None:
        self._logger = logger

    def handle(self, notification: PostAdded) -> None:
        message = "Post with id {post_id} was added"

        self._logger.log(message.format(post_id=notification.post_id))


# infrastructure adapters
class MockPostRepository:
    def __init__(self, logger: Logger) -> None:
        self._logger = logger

    def add(self, post: Post) -> None:
        message = "Post with id {post_id} was added to repository"
        self._logger.log(message.format(post_id=post.id))


class MockTransactionCommiter:
    def __init__(self, logger: Logger) -> None:
        self._logger = logger

    def commit(self) -> None:
        self._logger.log("Transaction commited")


class MockLogger:
    def log(self, message: str) -> None:
        print(message)  # noqa: T201


# presentation controllers
class PostController:
    def __init__(self, sender: Sender, logger: Logger) -> None:
        self._sender = sender
        self._logger = logger

    def add_post(self) -> None:
        request = AddPost(
            "Sicilian defense it so simple!",
            "Learn the sicilian defense: Najdorf variation.",
        )
        self._sender.send(request)
        self._logger.log("Post added successfully")


# composition root level: entrypoints, bootstrapping, ioc, configs, etc.
def build_container() -> Container:
    main_provider = Provider(scope=Scope.REQUEST)

    main_provider.provide(MockLogger, provides=Logger)
    main_provider.provide(MockPostRepository, provides=PostRepository)
    main_provider.provide(
        MockTransactionCommiter,
        provides=TransactionCommiter,
    )
    main_provider.provide(PostController)
    main_provider.provide(AddPostHandler)
    main_provider.provide(LogOnPostAddedHandler)
    main_provider.provide(WithParents[DishkaHandlerResolver])
    main_provider.provide(WithParents[DishkaRequestHandlerFinder])
    main_provider.provide(WithParents[DishkaNotificationHandlerFinder])
    main_provider.provide(dispatcher_factory)

    return make_container(main_provider)


def main() -> None:
    container = build_container()

    with container() as request_container:
        controller = request_container.get(PostController)

        controller.add_post()

    container.close()


if __name__ == "__main__":
    main()
