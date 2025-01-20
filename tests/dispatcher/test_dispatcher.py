from unittest.mock import MagicMock

import pytest

from bazario import (
    Dispatcher,
    HandleNext,
    Notification,
    NotificationHandler,
    PipelineBehavior,
    Registry,
    Request,
    RequestHandler,
    Resolver,
)
from bazario.exceptions import HandlerNotFoundError


class DummyRequest(Request[int]):
    pass


class DummyNotification(Notification):
    pass


class DummyRequestHandler(RequestHandler[DummyRequest, int]):
    def handle(self, request: DummyRequest) -> int:
        return 42


class DummyNotificationHandler(NotificationHandler[DummyNotification]):
    def handle(self, notification: DummyNotification) -> None:
        pass


class ValidationBehavior(PipelineBehavior[DummyNotification, None]):
    def handle(
        self,
        request: DummyNotification,
        handle_next: HandleNext[DummyNotification, None],
    ) -> None:
        if not hasattr(request, "validated"):
            request.validated = True

        return handle_next(request)


class ModifyingBehavior(PipelineBehavior[DummyRequest, int]):
    def handle(
        self,
        request: DummyRequest,
        handle_next: HandleNext[DummyRequest, int],
    ) -> None:
        response = handle_next(request)

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
def dispatcher(resolver: MagicMock, registry: MagicMock) -> Dispatcher:
    return Dispatcher(resolver, registry)


def test_send_request_success(
    dispatcher: Dispatcher,
    resolver: MagicMock,
) -> None:
    request = DummyRequest()
    result = dispatcher.send(request)

    assert result == 42
    resolver.resolve.assert_called_once_with(DummyRequestHandler)


def test_send_request_handler_not_found(dispatcher: Dispatcher) -> None:
    class UnknownRequest(Request[int]):
        pass

    request = UnknownRequest()

    with pytest.raises(HandlerNotFoundError):
        dispatcher.send(request)


def test_publish_notification_success(
    dispatcher: Dispatcher,
    resolver: MagicMock,
) -> None:
    notification = DummyNotification()
    dispatcher.publish(notification)

    resolver.resolve.assert_called_once_with(DummyNotificationHandler)


def test_publish_notification_no_handlers(
    dispatcher: Dispatcher,
    resolver: MagicMock,
    registry: MagicMock,
) -> None:
    registry.get_notification_handlers.side_effect = (
        lambda notification_type: []
    )
    notification = DummyNotification()

    dispatcher.publish(notification)

    resolver.resolve.assert_not_called()


def test_pipeline_behaviors_for_request(
    dispatcher: Dispatcher,
    registry: MagicMock,
) -> None:
    request = DummyRequest()

    behaviors = [ModifyingBehavior]
    registry.get_pipeline_behaviors.return_value = behaviors

    result = dispatcher.send(request)

    assert result == 84  # 42 * 2


def test_pipeline_behaviors_for_notification(
    dispatcher: Dispatcher,
    registry: MagicMock,
) -> None:
    notification = DummyNotification()

    behaviors = [ValidationBehavior]
    registry.get_pipeline_behaviors.return_value = behaviors

    dispatcher.publish(notification)

    assert hasattr(notification, "validated")
    assert notification.validated is True
