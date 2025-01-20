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
from bazario import PipelineBehavior, HandleNext, Request

class AuthenticationCheckBehavior(PipelineBehavior[Request, Any]):
    def __init__(self, user_provider: UserProvider) -> None:
        self._user_provider = user_provider

    def handle(self, request: Request, handle_next: HandleNext[Request, Any]) -> Any:
        # Check if user is authenticated
        if not self._user_provider.is_authenticated():
            raise PermissionError("User is not authenticated.")
        
        # Proceed to the next handler or behavior
        return handle_next(request)


# Behavior for all notifications
class AddToEventStoreBehavior(PipelineBehavior[Notification, None]):
    def __init__(self, event_store: EventStore) -> None:
        self._event_store = event_store

    def handle(
        self, 
        request: Notification, 
        handle_next: HandleNext[Notification, None],
    ) -> None:
        self._event_store.add(request)
        return handle_next(request)

# Behavior specific to AddPost request
class AddPostValidationBehavior(PipelineBehavior[AddPost, int]):
    def handle(
        self,
        request: AddPost,
        handle_next: HandleNext[AddPost, int],
    ) -> int:
        if not request.title:
            raise ValidationError("Title required")

        if not request.content:
            raise ValidationError("Content required")

        return handle_next(request)

# Behavior specific to PostAdded notification
class PostAddedEmailBehavior(PipelineBehavior[PostAdded, None]):
    def __init__(self, email_service: EmailService) -> None:
        self._email_service = email_service

    def handle(self, request: PostAdded, handle_next: HandleNext[PostAdded, None]) -> None:
        # Send a thank-you email to the user
        self._email_service.send_email(
            to_user_id=request.user_id,
            subject="Thank you for adding a post!",
            body=f"Dear User {request.user_id}, thank you for your post with ID {request.post_id}!"
        )
        
        # Proceed with the next behavior or handler
        return handle_next(request)
```

### Registering Pipeline Behaviors
Register your behaviors to `Registry`. The order of behavior registration determines the execution sequence - behaviors are executed in the order they are added:

```python
from bazario import Registry

def provide_registry() -> Registry:
    registry = Registry()
    # Behaviors will execute in this order:
    # 1. AuthenticationCheckBehavior
    # 2. AddToEventStoreBehavior
    # 3. AddPostValidationBehavior
    # 4. PostAddedEmailBehavior
    registry.add_pipeline_behaviors(Request, AuthenticationCheckBehavior)
    registry.add_pipeline_behaviors(Notification, AddToEventStoreBehavior)
    registry.add_pipeline_behaviors(AddPost, AddPostValidationBehavior)
    registry.add_pipeline_behaviors(PostAdded, PostAddedEmailBehavior)

    return registry
```

The execution order follows these rules:
1. Global behaviors (registered for base types like `Request` or `Notification`) execute first
2. Specific behaviors (registered for concrete types like `AddPost` or `PostAdded`) execute after global ones
3. Within each category (global/specific), behaviors execute in the order they were registered
4. For a single request/notification, all applicable behaviors form a chain in this order

Example of execution flow for an `AddPost` request:
```python
def provide_registry() -> Registry:
    registry = Registry()
    
    registry.add_behaviors(Request, RequestLoggingBehavior)
    registry.add_behaviors(AddPost, ValidationBehavior, MetricsBehavior)

    return registry

# Execution sequence for AddPost request:
# 1. RequestLoggingBehavior
# 2. ValidationBehavior
# 3. MetricsBehavior
# 4. Actual AddPost handler
```

Add to your IoC Container:
```python
# ...
container.register(Registry, provide_registry)
# ...
```

### Benefits of Pipeline Behaviors
Pipeline behaviors solve several common issues:
- Centralize cross-cutting concerns
- Keep handlers focused on business logic
- Enable flexible behavior execution order
- Eliminate code duplication in validation and response modification
