from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Generic, TypeAlias, TypeVar

TRes = TypeVar("TRes")
TRequest = TypeVar("TRequest")


HandleNext: TypeAlias = Callable[[TRequest], TRes]


class PipelineBehavior(Generic[TRequest, TRes], ABC):
    @abstractmethod
    def handle(
        self,
        request: TRequest,
        handle_next: HandleNext[TRequest, TRes],
    ) -> TRes: ...
