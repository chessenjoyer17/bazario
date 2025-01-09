from unittest.mock import Mock

import pytest

from bazario import Dispatcher, Notification
from bazario.exceptions import NotificationHandlerNotSetError


def test_publish_success() -> None:
    handler = Mock()
    resolver = Mock()
    resolver.resolve.return_value = handler
    finder = Mock()
    finder.find.return_value = ["handler_type_1", "handler_type_2"]

    dispatcher = Dispatcher(resolver, Mock(), finder)
    notification = Mock(spec=Notification)

    dispatcher.publish(notification)

    finder.find.assert_called_once_with(type(notification))
    resolver.resolve.assert_any_call("handler_type_1")
    resolver.resolve.assert_any_call("handler_type_2")

    assert handler.handle.call_count == 2


def test_publish_handler_not_set() -> None:
    resolver = Mock()
    dispatcher = Dispatcher(resolver, Mock(), None)
    notification = Mock(spec=Notification)

    with pytest.raises(NotificationHandlerNotSetError):
        dispatcher.publish(notification)
