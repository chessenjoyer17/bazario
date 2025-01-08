from typing import Protocol, runtime_checkable

from bazario.markers import Notification


@runtime_checkable
class Publisher(Protocol):
    def publish(self, notification: Notification) -> None: ...
