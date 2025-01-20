from unittest.mock import AsyncMock, MagicMock

import pytest

from bazario import Notification, Request
from bazario.asyncio import (
    Dispatcher,
    HandleNext,
    NotificationHandler,
    PipelineBehavior,
    Registry,
    RequestHandler,
    Resolver,
)
from bazario.exceptions import HandlerNotFoundError


class DummyRequest(Request[int]):
    pass


class DummyNotification(Notification):
    pass


class DummyRequestHandler(RequestHandler[DummyRequest, int]):
    async def handle(self, request: DummyRequest) -> int:
        return 42


class DummyNotificationHandler(NotificationHandler[DummyNotification]):
    async def handle(self, notification: DummyNotification) -> None:
        pass


class ValidationBehavior(PipelineBehavior[DummyNotification, None]):
    async def handle(
        self,
        request: DummyNotification,
        handle_next: HandleNext[DummyNotification, None],
    ) -> None:
        if not hasattr(request, "validated"):
            request.validated = True

        await handle_next(request)


class ModifyingBehavior(PipelineBehavior[DummyRequest, int]):
    async def handle(
        self,
        request: DummyRequest,
        handle_next: HandleNext[DummyRequest, int],
    ) -> int:
        response = await handle_next(request)

        return response * 2


@pytest.fixture
def resolver() -> MagicMock:
    mock = MagicMock(spec=Resolver)
    mock.resolve.side_effect = lambda dependency_type: dependency_type()
    return mock


@pytest.fixture
def registry() -> MagicMock:
    mock = MagicMock(spec=Registry)
    mock.get_request_handler.side_effect = (
        lambda request_type: DummyRequestHandler
        if request_type is DummyRequest
        else None
    )
    mock.get_notification_handlers.side_effect = (
        lambda notification_type: [DummyNotificationHandler]
        if notification_type is DummyNotification
        else []
    )
    mock.get_pipeline_behaviors.return_value = []
    return mock


@pytest.fixture
def dispatcher(resolver: AsyncMock, registry: MagicMock) -> Dispatcher:
    return Dispatcher(resolver, registry)


@pytest.mark.asyncio
async def test_send_request_success(
    dispatcher: Dispatcher,
    resolver: AsyncMock,
) -> None:
    request = DummyRequest()
    result = await dispatcher.send(request)

    assert result == 42
    resolver.resolve.assert_called_once_with(DummyRequestHandler)


@pytest.mark.asyncio
async def test_send_request_handler_not_found(dispatcher: Dispatcher) -> None:
    class UnknownRequest(Request[int]):
        pass

    request = UnknownRequest()

    with pytest.raises(HandlerNotFoundError):
        await dispatcher.send(request)


@pytest.mark.asyncio
async def test_publish_notification_success(
    dispatcher: Dispatcher,
    resolver: AsyncMock,
) -> None:
    notification = DummyNotification()
    await dispatcher.publish(notification)

    resolver.resolve.assert_called_once_with(DummyNotificationHandler)


@pytest.mark.asyncio
async def test_publish_notification_no_handlers(
    dispatcher: Dispatcher,
    resolver: AsyncMock,
    registry: MagicMock,
) -> None:
    registry.get_notification_handlers.side_effect = (
        lambda notification_type: []
    )
    notification = DummyNotification()

    await dispatcher.publish(notification)

    resolver.resolve.assert_not_called()


@pytest.mark.asyncio
async def test_pipeline_behaviors_for_request(
    dispatcher: Dispatcher,
    registry: MagicMock,
) -> None:
    request = DummyRequest()

    behaviors = [ModifyingBehavior]
    registry.get_pipeline_behaviors.return_value = behaviors

    result = await dispatcher.send(request)

    assert result == 84  # 42 * 2


@pytest.mark.asyncio
async def test_pipeline_behaviors_for_notification(
    dispatcher: Dispatcher,
    registry: MagicMock,
) -> None:
    notification = DummyNotification()

    behaviors = [ValidationBehavior]
    registry.get_pipeline_behaviors.return_value = behaviors

    await dispatcher.publish(notification)

    assert hasattr(notification, "validated")
    assert notification.validated is True
