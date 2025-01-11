from unittest.mock import AsyncMock, MagicMock

import pytest

from bazario import Notification, Request
from bazario.asyncio import (
    Dispatcher,
    HandleNext,
    HandlerFinder,
    NotificationHandler,
    PipelineBehavior,
    PipelineBehaviorRegistry,
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
        resolver: Resolver,
        target: DummyNotification,
        handle_next: HandleNext[DummyNotification, None],
    ) -> None:
        if not hasattr(target, "validated"):
            target.validated = True

        await handle_next(resolver, target)


class ModifyingBehavior(PipelineBehavior[DummyRequest, int]):
    async def handle(
        self,
        resolver: Resolver,
        target: DummyRequest,
        handle_next: HandleNext[DummyRequest, int],
    ) -> int:
        response = await handle_next(resolver, target)

        return response * 2


@pytest.fixture
def resolver() -> AsyncMock:
    mock = AsyncMock(spec=Resolver)
    mock.resolve.side_effect = lambda _: DummyRequestHandler()
    return mock


@pytest.fixture
def handler_finder() -> MagicMock:
    mock = MagicMock(spec=HandlerFinder)
    mock.find_with_request.side_effect = (
        lambda req_type: DummyRequestHandler
        if req_type is DummyRequest
        else None
    )
    mock.find_with_notification.side_effect = (
        lambda notif_type: [DummyNotificationHandler]
        if notif_type is DummyNotification
        else []
    )
    return mock


@pytest.fixture
def pipeline_behavior_registry() -> MagicMock:
    mock = MagicMock(spec=PipelineBehaviorRegistry)
    mock.get_behaviors.return_value = []
    return mock


@pytest.fixture
def dispatcher(
    resolver: AsyncMock,
    handler_finder: MagicMock,
    pipeline_behavior_registry: MagicMock,
) -> Dispatcher:
    return Dispatcher(resolver, handler_finder, pipeline_behavior_registry)


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
    handler_finder: MagicMock,
) -> None:
    handler_finder.find_with_notification.side_effect = lambda notif_type: []
    notification = DummyNotification()

    await dispatcher.publish(notification)

    resolver.resolve.assert_not_called()


@pytest.mark.asyncio
async def test_pipeline_behaviors_for_request(
    dispatcher: Dispatcher,
    resolver: AsyncMock,
    pipeline_behavior_registry: MagicMock,
) -> None:
    request = DummyRequest()

    behaviors = [ModifyingBehavior()]
    pipeline_behavior_registry.get_behaviors.return_value = behaviors

    result = await dispatcher.send(request)

    resolver.resolve.assert_called_once_with(DummyRequestHandler)
    assert result == 84  # 42 * 2


@pytest.mark.asyncio
async def test_pipeline_behaviors_for_notification(
    dispatcher: Dispatcher,
    resolver: AsyncMock,
    pipeline_behavior_registry: MagicMock,
) -> None:
    notification = DummyNotification()

    behaviors = [ValidationBehavior()]
    pipeline_behavior_registry.get_behaviors.return_value = behaviors

    await dispatcher.publish(notification)

    resolver.resolve.assert_called_once_with(DummyNotificationHandler)
    assert hasattr(notification, "validated")
    assert notification.validated is True
