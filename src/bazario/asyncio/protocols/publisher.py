from typing import Protocol, runtime_checkable

from bazario.markers import Notification


@runtime_checkable
class Publisher(Protocol):
    async def publish(self, notification: Notification) -> None: ...
