from typing import Protocol, TypeVar, runtime_checkable

from bazario.markers import Notification, Request

TRes_co = TypeVar("TRes_co", covariant=True)
TReq_contra = TypeVar("TReq_contra", bound=Request, contravariant=True)
TNot_contra = TypeVar("TNot_contra", bound=Notification, contravariant=True)


@runtime_checkable
class RequestHandler(Protocol[TReq_contra, TRes_co]):
    async def handle(self, request: TReq_contra) -> TRes_co: ...


@runtime_checkable
class NotificationHandler(Protocol[TNot_contra]):
    async def handle(self, notification: TNot_contra) -> None: ...
