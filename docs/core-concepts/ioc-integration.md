This example demonstrates how to configure your dependency injection (DI) framework (Dishka in this case) to work with Bazario:
```python
from bazario import Dispatcher, PipelineBehaviourRegistry
from bazario.plugins.dishka import (
    DishkaHandlerFinder,
    DishkaResolver,
)
from dishka import Provider, Scope, make_container

def build_container() -> Container:
    main_provider = Provider(scope=Scope.REQUEST)

    main_provider.provide(AddPostHandler)
    main_provider.provide(WithParents[Dispatcher])
    main_provider.provide(WithParents[DishkaHandlerFinder])
    main_provider.provide(WithParents[DishkaResolver])
    # Additional registrations (PostRepository, TransactionCommiter, etc.)

    return make_container(main_provider)
```
