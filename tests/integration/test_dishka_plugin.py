from dataclasses import dataclass

import pytest
from dishka import Container, Provider, Scope, WithParents, make_container

from bazario import (
    Dispatcher,
    Notification,
    NotificationHandler,
    PipelineBehaviourRegistry,
    Request,
    RequestHandler,
)
from bazario.plugins.dishka import DishkaHandlerFinder, DishkaResolver

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
    provider.provide(PipelineBehaviourRegistry)
    provider.provide(WithParents[Dispatcher])
    provider.provide(WithParents[DishkaResolver])
    provider.provide(WithParents[DishkaHandlerFinder])

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


@pytest.fixture
def handler_finder(container: Container) -> DishkaHandlerFinder:
    return container.get(DishkaHandlerFinder)


def test_dishka_resolver(resolver: DishkaResolver) -> None:
    handler = resolver.resolve(MockRequestHandler)
    assert isinstance(handler, MockRequestHandler)


def test_dishka_handler_finder_with_request(
    handler_finder: DishkaHandlerFinder,
) -> None:
    handler_type = handler_finder.find_with_request(MockRequest)

    assert handler_type is MockRequestHandler


def test_dishka_handler_finder_with_notification(
    handler_finder: DishkaHandlerFinder,
) -> None:
    handler_types = handler_finder.find_with_notification(MockNotification)
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
