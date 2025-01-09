from typing import TypeVar

from bazario.aliases import HandlerType

THandler = TypeVar("THandler", bound=HandlerType)
