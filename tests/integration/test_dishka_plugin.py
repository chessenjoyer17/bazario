from dataclasses import dataclass

import pytest
from dishka import Container, Provider, Scope, WithParents, make_container

from bazario import (
    Dispatcher,
    Notification,
    NotificationHandler,
    Request,
    RequestHandler,
)
from bazario.plugins.dishka import (
    DishkaHandlerResolver,
    DishkaNotificationHandlerFinder,
    DishkaRequestHandlerFinder,
    dispatcher_factory,
)

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


@pytest.fixture
def container() -> Container:
    provider = Provider(scope=Scope.APP)

    provider.provide(MockRequestHandler)
    provider.provide(MockNotificationHandler)
    provider.provide(WithParents[DishkaHandlerResolver])
    provider.provide(WithParents[DishkaRequestHandlerFinder])
    provider.provide(WithParents[DishkaNotificationHandlerFinder])
    provider.provide(dispatcher_factory)

    return make_container(provider)


@pytest.fixture
def resolver(container: Container) -> DishkaHandlerResolver:
    return container.get(DishkaHandlerResolver)


@pytest.fixture
def dispatcher(container: Container) -> Dispatcher:
    return container.get(Dispatcher)


@pytest.fixture
def mock_notification_handler(container: Container) -> MockNotificationHandler:
    return container.get(MockNotificationHandler)


@pytest.fixture
def request_handler_finder(container: Container) -> DishkaRequestHandlerFinder:
    return container.get(DishkaRequestHandlerFinder)


@pytest.fixture
def notification_handler_finder(
    container: Container,
) -> DishkaNotificationHandlerFinder:
    return container.get(DishkaNotificationHandlerFinder)


def test_dishka_resolver(resolver: DishkaHandlerResolver) -> None:
    handler = resolver.resolve(MockRequestHandler)
    assert isinstance(handler, MockRequestHandler)


def test_dishka_request_handler_finder(
    request_handler_finder: DishkaRequestHandlerFinder,
) -> None:
    handler_type = request_handler_finder.find(MockRequest)

    assert handler_type is MockRequestHandler


def test_dishka_notification_handler_finder(
    notification_handler_finder: DishkaNotificationHandlerFinder,
) -> None:
    handler_types = notification_handler_finder.find(MockNotification)
    assert next(iter(handler_types)) is MockNotificationHandler


def test_dispatcher_request_sending_with_dishka_plugin(
    dispatcher: Dispatcher,
) -> None:
    request = MockRequest(REQUEST_DATA)
    response = dispatcher.send(request)

    assert response == f"Processed: {REQUEST_DATA}"


def test_dispatcher_notification_publishing_with_dishka_plugin(
    dispatcher: Dispatcher,
    mock_notification_handler: MockNotificationHandler,
) -> None:
    dispatcher.publish(MockNotification(NOTIFICATION_DATA))
    assert mock_notification_handler.messages == [NOTIFICATION_DATA]
