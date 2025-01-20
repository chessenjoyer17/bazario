from dataclasses import dataclass

import pytest
from dishka import Container, Provider, Scope, WithParents, make_container

from bazario import (
    Dispatcher,
    Notification,
    NotificationHandler,
    Registry,
    Request,
    RequestHandler,
)
from bazario.resolvers.dishka import DishkaResolver

REQUEST_DATA = "King's indian attack. The best opening for white!"
NOTIFICATION_DATA = (
    "Sicilian defense: Accelerated dragon variation. The best response to e4!"
)


@dataclass
class MockRequest(Request[str]):
    data: str


@dataclass
class MockNotification(Notification):
    data: str


class MockNotificationHandler(NotificationHandler[MockNotification]):
    def __init__(self) -> None:
        self.messages = []

    def handle(self, notification: MockNotification) -> None:
        self.messages.append(notification.data)


class MockRequestHandler(RequestHandler[MockRequest, str]):
    def handle(self, request: MockRequest) -> str:
        return f"Processed: {request.data}"


def provide_registry() -> Registry:
    registry = Registry()

    registry.add_request_handler(
        MockRequest,
        MockRequestHandler,
    )
    registry.add_notification_handlers(
        MockNotification,
        MockNotificationHandler,
    )
    return registry


@pytest.fixture
def container() -> Container:
    provider = Provider(scope=Scope.APP)

    provider.provide(Registry)
    provider.provide(MockRequestHandler)
    provider.provide(MockNotificationHandler)
    provider.provide(provide_registry)
    provider.provide(WithParents[Dispatcher])
    provider.provide(WithParents[DishkaResolver])

    return make_container(provider)


@pytest.fixture
def resolver(container: Container) -> DishkaResolver:
    return container.get(DishkaResolver)


@pytest.fixture
def dispatcher(container: Container) -> Dispatcher:
    return container.get(Dispatcher)


@pytest.fixture
def mock_notification_handler(container: Container) -> MockNotificationHandler:
    return container.get(MockNotificationHandler)


def test_dishka_resolver(resolver: DishkaResolver) -> None:
    handler = resolver.resolve(MockRequestHandler)
    assert isinstance(handler, MockRequestHandler)


def test_dispatcher_request_sending_with_dishka(
    dispatcher: Dispatcher,
) -> None:
    request = MockRequest(REQUEST_DATA)
    response = dispatcher.send(request)

    assert response == f"Processed: {REQUEST_DATA}"


def test_dispatcher_notification_publishing_with_dishka(
    dispatcher: Dispatcher,
    mock_notification_handler: MockNotificationHandler,
) -> None:
    dispatcher.publish(MockNotification(NOTIFICATION_DATA))
    assert mock_notification_handler.messages == [NOTIFICATION_DATA]
