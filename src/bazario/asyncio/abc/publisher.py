from typing import Protocol

from bazario.markers import Notification


class Publisher(Protocol):
    async def publish(self, notification: Notification) -> None: ...
