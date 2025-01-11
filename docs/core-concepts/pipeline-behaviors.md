Pipeline behaviors in **Bazario** enable pre- and post-processing logic for requests and notifications. These behaviors form a chain around the core handler logic and can modify or enhance the data flow.

### Defining Pipeline Behaviors
```python
from bazario import (
    PipelineBehavior,
    Resolver,
    HandleNext,
    Request,
    Notification,
)

# Behavior for all requests
class RequestLoggingBehavior(PipelineBehavior[Request, Any]):
    def handle(
        self,
        resolver: Resolver,
        target: Request,
        handle_next: HandleNext[Request, Any],
    ) -> Any:
        logger = resolver.resolve(Logger)
        logger.log_info("Before request handler execution")
        response = handle_next(resolver, target)
        logger.log_info(f"After request handler execution. Response: {response}")
        
        return response

# Behavior for all notifications
class NotificationLoggingBehavior(PipelineBehavior[Notification, None]):
    def handle(
        self,
        resolver: Resolver,
        target: Notification,
        handle_next: HandleNext[Notification, None],
    ) -> None:
        logger = resolver.resolve(Logger)
        logger.log_info("Before notification handler execution")
        handle_next(resolver, target)
        logger.log_info("After notification handler execution")

# Behavior specific to AddPost request
class AddPostLoggingBehavior(PipelineBehavior[AddPost, int]):
    def handle(
        self,
        resolver: Resolver,
        target: AddPost,
        handle_next: HandleNext[AddPost, int],
    ) -> int:
        logger = resolver.resolve(Logger)
        logger.log_info("Before post addition")
        response = handle_next(resolver, target)
        logger.log_info(f"After post addition: id = {response}")
        
        return response

# Behavior specific to PostAdded notification
class PostAddedLoggingBehavior(PipelineBehavior[PostAdded, None]):
    def handle(
        self,
        resolver: Resolver,
        target: PostAdded,
        handle_next: HandleNext[PostAdded, None],
    ) -> None:
        logger = resolver.resolve(Logger)
        logger.log_info("Before post added handler execution")
        handle_next(resolver, target)
        logger.log_info(f"After post added handler execution: id = {target.post_id}")
```

### Registering Pipeline Behaviors
Define the factory function for `PipelineBehaviorRegistry`. The order of behavior registration determines the execution sequence - behaviors are executed in the order they are added:

```python
from bazario import PipelineBehaviorRegistry

def build_registry() -> PipelineBehaviorRegistry:
    registry = PipelineBehaviorRegistry()
    # Behaviors will execute in this order:
    # 1. RequestLoggingBehavior
    # 2. NotificationLoggingBehavior
    # 3. AddPostLoggingBehavior
    # 4. PostAddedLoggingBehavior
    registry.add_behaviours(Request, RequestLoggingBehaviour())
    registry.add_behaviours(Notification, NotificationLoggingBehaviour())
    registry.add_behaviours(AddPost, AddPostLoggingBehaviour())
    registry.add_behaviours(PostAdded, PostAddedLoggingBehaviour())

    return registry
```

The execution order follows these rules:
1. Global behaviors (registered for base types like `Request` or `Notification`) execute first
2. Specific behaviors (registered for concrete types like `AddPost` or `PostAdded`) execute after global ones
3. Within each category (global/specific), behaviors execute in the order they were registered
4. For a single request/notification, all applicable behaviors form a chain in this order

Example of execution flow for an `AddPost` request:
```python
def build_registry() -> PipelineBehaviourRegistry:
    registry = PipelineBehaviourRegistry()
    
    registry.add_behaviours(Request, RequestLoggingBehaviour())
    registry.add_behaviours(
        AddPost, 
        ValidationBehaviour(), 
        MetricsBehaviour(),
    )

    return registry

# Execution sequence for AddPost request:
# 1. RequestLoggingBehaviour
# 2. ValidationBehaviour
# 3. MetricsBehaviour
# 4. Actual AddPost handler
```

Configure the IoC container:
```python
def build_container() -> Container:
    # ...
    main_provider.provide(build_registry)
    # Note: The Dispatcher depends on PipelineBehaviourRegistry.
    # If you're not using pipeline behaviors, register PipelineBehaviourRegistry directly:
    # main_provider.provide(PipelineBehaviourRegistry)
    # ...
```

### Benefits of Pipeline Behaviors
Pipeline behaviors solve several common issues:
- Centralize cross-cutting concerns
- Keep handlers focused on business logic
- Enable flexible behavior execution order
- Eliminate code duplication in validation and response modification
