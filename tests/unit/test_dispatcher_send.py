from unittest.mock import Mock

import pytest

from bazario import Dispatcher, Request
from bazario.exceptions import HandlerNotFoundError


def test_send_success() -> None:
    handler = Mock()
    handler.handle.return_value = "result"
    resolver = Mock()
    resolver.resolve.return_value = handler
    finder = Mock()
    finder.find.return_value = "handler_type"

    dispatcher = Dispatcher(resolver, finder)
    request = Mock(spec=Request)

    result = dispatcher.send(request)

    finder.find.assert_called_once_with(type(request))
    resolver.resolve.assert_called_once_with("handler_type")
    handler.handle.assert_called_once_with(request)
    assert result == "result"


def test_send_handler_not_found() -> None:
    resolver = Mock()
    finder = Mock()
    finder.find.return_value = None

    dispatcher = Dispatcher(resolver, finder)
    request = Mock(spec=Request)

    with pytest.raises(HandlerNotFoundError) as exc_info:
        dispatcher.send(request)

    assert exc_info.value.target_type is type(request)
