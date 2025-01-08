from typing import Protocol, TypeVar, runtime_checkable

from bazario.markers import Notification, Request

TRes = TypeVar("TRes", covariant=True)
TReq = TypeVar("TReq", bound=Request, contravariant=True)
TNot = TypeVar("TNot", bound=Notification, contravariant=True)


@runtime_checkable
class RequestHandler(Protocol[TReq, TRes]):
    def handle(self, request: TReq) -> TRes: ...


@runtime_checkable
class NotificationHandler(Protocol[TNot]):
    def handle(self, notification: TNot) -> None: ...
