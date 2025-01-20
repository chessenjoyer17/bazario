from dataclasses import dataclass
from typing import TypeVar

import pytest
from punq import Container, Scope

from bazario import (
    Dispatcher,
    Notification,
    NotificationHandler,
    Registry,
    Request,
    RequestHandler,
    Resolver,
)

TDependency = TypeVar("TDependency")


class PunqResolver(Resolver):
    def __init__(self, container: Container) -> None:
        self._container = container

    def resolve(self, dependency_type: type[TDependency]) -> TDependency:
        return self._container.resolve(dependency_type)


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
    container = Container()

    container.register(MockRequestHandler, scope=Scope.singleton)
    container.register(MockNotificationHandler, scope=Scope.singleton)
    container.register(
        Registry,
        provide_registry,
        scope=Scope.singleton,
    )
    container.register(Dispatcher, scope=Scope.singleton)
    container.register(PunqResolver, scope=Scope.singleton)
    container.register(Resolver, PunqResolver, scope=Scope.singleton)

    return container


@pytest.fixture
def resolver(container: Container) -> PunqResolver:
    return container.resolve(PunqResolver)


@pytest.fixture
def dispatcher(container: Container) -> Dispatcher:
    return container.resolve(Dispatcher)


@pytest.fixture
def mock_notification_handler(container: Container) -> MockNotificationHandler:
    return container.resolve(MockNotificationHandler)


def test_punq_resolver(resolver: PunqResolver) -> None:
    handler = resolver.resolve(MockRequestHandler)
    assert isinstance(handler, MockRequestHandler)


def test_dispatcher_request_sending_with_punq(
    dispatcher: Dispatcher,
) -> None:
    request = MockRequest(REQUEST_DATA)
    response = dispatcher.send(request)

    assert response == f"Processed: {REQUEST_DATA}"


def test_dispatcher_notification_publishing_with_punq(
    dispatcher: Dispatcher,
    mock_notification_handler: MockNotificationHandler,
) -> None:
    dispatcher.publish(MockNotification(NOTIFICATION_DATA))
    assert mock_notification_handler.messages == [NOTIFICATION_DATA]
