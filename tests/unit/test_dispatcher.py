from unittest.mock import MagicMock

import pytest

from bazario import (
    Dispatcher,
    HandleNext,
    HandlerFinder,
    Notification,
    NotificationHandler,
    PipelineBehaviour,
    PipelineBehaviourRegistry,
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


class ValidationBehaviour(PipelineBehaviour[DummyNotification, None]):
    def handle(
        self,
        resolver: Resolver,
        target: DummyNotification,
        handle_next: HandleNext[DummyNotification, None],
    ) -> None:
        if not hasattr(target, "validated"):
            target.validated = True

        return handle_next(resolver, target)


class ModifyingBehaviour(PipelineBehaviour[DummyRequest, int]):
    def handle(
        self,
        resolver: Resolver,
        target: DummyRequest,
        handle_next: HandleNext[DummyRequest, int],
    ) -> None:
        response = handle_next(resolver, target)

        return response * 2


@pytest.fixture
def resolver() -> MagicMock:
    mock = MagicMock(spec=Resolver)
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
def pipeline_behaviour_registry() -> MagicMock:
    mock = MagicMock(spec=PipelineBehaviourRegistry)
    mock.get_behaviours.return_value = []
    return mock


@pytest.fixture
def dispatcher(
    resolver: MagicMock,
    handler_finder: MagicMock,
    pipeline_behaviour_registry: MagicMock,
) -> Dispatcher:
    return Dispatcher(resolver, handler_finder, pipeline_behaviour_registry)


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
    handler_finder: MagicMock,
) -> None:
    handler_finder.find_with_notification.side_effect = lambda notif_type: []
    notification = DummyNotification()

    dispatcher.publish(notification)

    resolver.resolve.assert_not_called()


def test_pipeline_behaviours_for_request(
    dispatcher: Dispatcher,
    resolver: MagicMock,
    pipeline_behaviour_registry: MagicMock,
) -> None:
    request = DummyRequest()

    behaviours = [ModifyingBehaviour()]
    pipeline_behaviour_registry.get_behaviours.return_value = behaviours

    result = dispatcher.send(request)

    resolver.resolve.assert_called_once_with(DummyRequestHandler)
    assert result == 84  # 42 * 2


def test_pipeline_behaviours_for_notification(
    dispatcher: Dispatcher,
    resolver: MagicMock,
    pipeline_behaviour_registry: MagicMock,
) -> None:
    notification = DummyNotification()

    behaviours = [ValidationBehaviour()]
    pipeline_behaviour_registry.get_behaviours.return_value = behaviours

    dispatcher.publish(notification)

    resolver.resolve.assert_called_once_with(DummyNotificationHandler)
    assert hasattr(notification, "validated")
    assert notification.validated is True
