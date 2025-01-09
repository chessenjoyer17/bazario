from typing import TypeAlias

from bazario.asyncio.protocols.handler import (
    NotificationHandler,
    RequestHandler,
)

HandlerType: TypeAlias = RequestHandler | NotificationHandler
