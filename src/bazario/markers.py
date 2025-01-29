from typing import Generic, TypeVar

TRes = TypeVar("TRes")


class Request(Generic[TRes]):
    """Marker interface for requests"""


class Notification:
    """Marker interface for notifications"""
