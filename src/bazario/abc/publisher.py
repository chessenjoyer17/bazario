from typing import Protocol

from bazario.markers import Notification


class Publisher(Protocol):
    def publish(self, notification: Notification) -> None: ...
