from unittest.mock import Mock

from bazario import Dispatcher, Notification


def test_publish_success() -> None:
    handler = Mock()
    resolver = Mock()
    resolver.resolve.return_value = handler
    finder = Mock()
    finder.find_with_notification.return_value = [
        "handler_type_1",
        "handler_type_2",
    ]

    dispatcher = Dispatcher(finder, resolver)
    notification = Mock(spec=Notification)

    dispatcher.publish(notification)

    finder.find_with_notification.assert_called_once_with(type(notification))
    resolver.resolve.assert_any_call("handler_type_1")
    resolver.resolve.assert_any_call("handler_type_2")

    assert handler.handle.call_count == 2
