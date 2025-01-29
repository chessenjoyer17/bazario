from abc import ABC, abstractmethod
from collections.abc import Callable, Coroutine
from typing import Any, Generic, TypeAlias, TypeVar

TRes = TypeVar("TRes")
TRequest = TypeVar("TRequest")


HandleNext: TypeAlias = Callable[[TRequest], Coroutine[Any, Any, TRes]]


class PipelineBehavior(Generic[TRequest, TRes], ABC):
    @abstractmethod
    async def handle(
        self,
        request: TRequest,
        handle_next: HandleNext[TRequest, TRes],
    ) -> TRes: ...
