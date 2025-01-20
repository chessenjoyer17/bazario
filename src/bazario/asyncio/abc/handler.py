from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from bazario.markers import Notification, Request

TRes_co = TypeVar("TRes_co", covariant=True)
TReq_contra = TypeVar("TReq_contra", bound=Request, contravariant=True)
TNot_contra = TypeVar("TNot_contra", bound=Notification, contravariant=True)


class RequestHandler(Generic[TReq_contra, TRes_co], ABC):
    @abstractmethod
    async def handle(self, request: TReq_contra) -> TRes_co: ...


class NotificationHandler(Generic[TNot_contra], ABC):
    @abstractmethod
    async def handle(self, notification: TNot_contra) -> None: ...
