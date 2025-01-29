from dataclasses import dataclass

import pytest
from dishka import (
    AsyncContainer,
    Provider,
    Scope,
    WithParents,
    make_async_container,
)

from bazario import Notification, Request
from bazario.asyncio import (
    Dispatcher,
    NotificationHandler,
    Registry,
    RequestHandler,
)
from bazario.asyncio.resolvers.dishka import DishkaResolver

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

    async def handle(self, notification: MockNotification) -> None:
        self.messages.append(notification.data)


class MockRequestHandler(RequestHandler[MockRequest, str]):
    async def handle(self, request: MockRequest) -> str:
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
def container() -> AsyncContainer:
    provider = Provider(scope=Scope.APP)

    provider.provide(MockRequestHandler)
    provider.provide(MockNotificationHandler)
    provider.provide(provide_registry)
    provider.provide(WithParents[Dispatcher])
    provider.provide(WithParents[DishkaResolver])

    return make_async_container(provider)


@pytest.fixture
async def resolver(container: AsyncContainer) -> DishkaResolver:
    return await container.get(DishkaResolver)


@pytest.fixture
async def dispatcher(container: AsyncContainer) -> Dispatcher:
    return await container.get(Dispatcher)


@pytest.fixture
async def mock_notification_handler(
    container: AsyncContainer,
) -> MockNotificationHandler:
    return await container.get(MockNotificationHandler)


@pytest.mark.asyncio
async def test_dishka_resolver(resolver: DishkaResolver) -> None:
    handler = await resolver.resolve(MockRequestHandler)
    assert isinstance(handler, MockRequestHandler)


@pytest.mark.asyncio
async def test_dispatcher_request_sending_with_dishka(
    dispatcher: Dispatcher,
) -> None:
    request = MockRequest(REQUEST_DATA)
    response = await dispatcher.send(request)

    assert response == f"Processed: {REQUEST_DATA}"


@pytest.mark.asyncio
async def test_dispatcher_notification_publishing_with_dishka(
    dispatcher: Dispatcher,
    mock_notification_handler: MockNotificationHandler,
) -> None:
    await dispatcher.publish(MockNotification(NOTIFICATION_DATA))
    assert mock_notification_handler.messages == [NOTIFICATION_DATA]
