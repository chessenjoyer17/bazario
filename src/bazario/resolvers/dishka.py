from dishka import (
    DEFAULT_COMPONENT,
    AnyOf,
    BaseScope,
    Container,
    DependencyKey,
    Provider,
    Scope,
)

from bazario.protocols.dispatcher import Dispatcher
from bazario.protocols.publisher import Publisher
from bazario.protocols.resolver import HandlerResolver
from bazario.protocols.sender import Sender


class DishkaResolver(HandlerResolver):
    def __init__(
        self,
        container: Container,
        scope: BaseScope = Scope.REQUEST,
    ) -> None:
        self._container = container
        self._scope = scope

    def resolve[T](self, key: type[T]) -> T:
        with self._container(scope=self._scope) as container:
            return container.get(key)


def bazario_provider() -> Provider:
    provider = Provider(scope=Scope.APP)

    provider.from_context(Dispatcher, scope=Scope.APP)
    provider.alias(Dispatcher, provides=AnyOf[Sender, Publisher])

    return provider


def setup_dishka(container: Container, dispatcher: Dispatcher) -> None:
    key = DependencyKey(Dispatcher, DEFAULT_COMPONENT)
    container.context[key] = dispatcher
