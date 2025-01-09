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
from bazario.asyncio import Dispatcher, NotificationHandler, RequestHandler
from bazario.plugins.asyncio_dishka import (
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

    async def handle(self, notification: MockNotification) -> None:
        self.messages.append(notification.data)


class MockRequestHandler(RequestHandler[MockRequest, str]):
    async def handle(self, request: MockRequest) -> str:
        return f"Processed: {request.data}"


@pytest.fixture
def container() -> AsyncContainer:
    provider = Provider(scope=Scope.APP)

    provider.provide(MockRequestHandler)
    provider.provide(MockNotificationHandler)
    provider.provide(WithParents[DishkaHandlerResolver])
    provider.provide(WithParents[DishkaRequestHandlerFinder])
    provider.provide(WithParents[DishkaNotificationHandlerFinder])
    provider.provide(dispatcher_factory)

    return make_async_container(provider)


@pytest.fixture
async def resolver(container: AsyncContainer) -> DishkaHandlerResolver:
    return await container.get(DishkaHandlerResolver)


@pytest.fixture
async def dispatcher(container: AsyncContainer) -> Dispatcher:
    return await container.get(Dispatcher)


@pytest.fixture
async def mock_notification_handler(
    container: AsyncContainer,
) -> MockNotificationHandler:
    return await container.get(MockNotificationHandler)


@pytest.fixture
async def request_handler_finder(
    container: AsyncContainer,
) -> DishkaRequestHandlerFinder:
    return await container.get(DishkaRequestHandlerFinder)


@pytest.fixture
async def notification_handler_finder(
    container: AsyncContainer,
) -> DishkaNotificationHandlerFinder:
    return await container.get(DishkaNotificationHandlerFinder)


@pytest.mark.asyncio
async def test_dishka_resolver(resolver: DishkaHandlerResolver) -> None:
    handler = await resolver.resolve(MockRequestHandler)
    assert isinstance(handler, MockRequestHandler)


@pytest.mark.asyncio
async def test_dishka_request_handler_finder(
    request_handler_finder: DishkaRequestHandlerFinder,
) -> None:
    handler_type = await request_handler_finder.find(MockRequest)

    assert handler_type is MockRequestHandler


@pytest.mark.asyncio
async def test_dishka_notification_handler_finder(
    notification_handler_finder: DishkaNotificationHandlerFinder,
) -> None:
    handler_types = await notification_handler_finder.find(MockNotification)
    assert next(iter(handler_types)) is MockNotificationHandler


@pytest.mark.asyncio
async def test_dispatcher_request_sending_with_dishka_plugin(
    dispatcher: Dispatcher,
) -> None:
    request = MockRequest(REQUEST_DATA)
    response = await dispatcher.send(request)

    assert response == f"Processed: {REQUEST_DATA}"


@pytest.mark.asyncio
async def test_dispatcher_notification_publishing_with_dishka_plugin(
    dispatcher: Dispatcher,
    mock_notification_handler: MockNotificationHandler,
) -> None:
    await dispatcher.publish(MockNotification(NOTIFICATION_DATA))
    assert mock_notification_handler.messages == [NOTIFICATION_DATA]
