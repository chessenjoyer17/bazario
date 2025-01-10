from unittest.mock import AsyncMock

import pytest

from bazario import Request
from bazario.asyncio import Dispatcher
from bazario.exceptions import HandlerNotFoundError


@pytest.mark.asyncio
async def test_send_success() -> None:
    handler = AsyncMock()
    handler.handle.return_value = "result"
    resolver = AsyncMock()
    resolver.resolve.return_value = handler
    finder = AsyncMock()
    finder.find_with_request.return_value = "handler_type"

    dispatcher = Dispatcher(finder, resolver)
    request = AsyncMock(spec=Request)

    result = await dispatcher.send(request)

    finder.find_with_request.assert_awaited_once_with(type(request))
    resolver.resolve.assert_awaited_once_with("handler_type")
    handler.handle.assert_awaited_once_with(request)
    assert result == "result"


@pytest.mark.asyncio
async def test_send_handler_not_found() -> None:
    resolver = AsyncMock()
    finder = AsyncMock()
    finder.find_with_request.return_value = None

    dispatcher = Dispatcher(finder, resolver)
    request = AsyncMock(spec=Request)

    with pytest.raises(HandlerNotFoundError) as exc_info:
        await dispatcher.send(request)

    assert exc_info.value.target_type is type(request)
