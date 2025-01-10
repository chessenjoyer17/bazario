from unittest.mock import AsyncMock

import pytest

from bazario import Notification
from bazario.asyncio import Dispatcher


@pytest.mark.asyncio
async def test_publish_success() -> None:
    handler = AsyncMock()
    resolver = AsyncMock()
    resolver.resolve.return_value = handler
    finder = AsyncMock()
    finder.find_with_notification.return_value = [
        "handler_type_1",
        "handler_type_2",
    ]

    dispatcher = Dispatcher(finder, resolver)
    notification = AsyncMock(spec=Notification)

    await dispatcher.publish(notification)

    finder.find_with_notification.assert_awaited_once_with(type(notification))
    resolver.resolve.assert_any_await("handler_type_1")
    resolver.resolve.assert_any_await("handler_type_2")
    assert handler.handle.await_count == 2
