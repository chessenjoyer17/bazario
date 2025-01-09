from typing import TypeVar

from bazario.asyncio.aliases import HandlerType

THandler = TypeVar("THandler", bound=HandlerType)
