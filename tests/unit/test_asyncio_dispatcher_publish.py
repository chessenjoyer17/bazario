from unittest.mock import AsyncMock

import pytest

from bazario import Notification
from bazario.asyncio import Dispatcher
from bazario.exceptions import NotificationHandlerNotSetError


@pytest.mark.asyncio
async def test_publish_success() -> None:
    handler = AsyncMock()
    resolver = AsyncMock()
    resolver.resolve.return_value = handler
    finder = AsyncMock()
    finder.find.return_value = ["handler_type_1", "handler_type_2"]

    dispatcher = Dispatcher(resolver, AsyncMock(), finder)
    notification = AsyncMock(spec=Notification)

    await dispatcher.publish(notification)

    finder.find.assert_awaited_once_with(type(notification))
    resolver.resolve.assert_any_await("handler_type_1")
    resolver.resolve.assert_any_await("handler_type_2")
    assert handler.handle.await_count == 2


@pytest.mark.asyncio
async def test_publish_handler_not_set() -> None:
    resolver = AsyncMock()
    dispatcher = Dispatcher(resolver, AsyncMock(), None)
    notification = AsyncMock(spec=Notification)

    with pytest.raises(NotificationHandlerNotSetError):
        await dispatcher.publish(notification)
