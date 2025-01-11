# Bazario

**Bazario** is a lightweight handler routing library designed for modular applications, implementing the CQRS (Command and Query Responsibility Segregation) pattern. It simplifies development by providing centralized handling of requests (Requests) and events (Notifications), with efficient handler routing and support for both synchronous and asynchronous operations.

### Key Features
- **Request Handling**: A streamlined mechanism for handling requests with clear separation of responsibilities
- **Event Handling**: Unified event publication and handling (Notifications) supporting both standard and async/await syntax while maintaining efficient in-memory processing
- **Modular Architecture**: Clear separation of business logic, ports, and infrastructure, simplifying development and maintenance
- **IoC Container Integration**: Support for DI frameworks like Dishka, enabling easy dependency management and modular configuration
- **Testability**: Use of protocols (Protocol) to easily mock infrastructure adapters for unit testing
- **Asynchronous Support**: The **asyncio** package enables asynchronous handling, providing flexibility for applications requiring async logic
- **Dependency Separation**: Controllers delegate handler resolution to **Bazario**, focusing solely on request parsing. This improves separation of responsibilities and enhances code maintainability
- **Pipeline Behaviors**: Flexible middleware system for implementing cross-cutting concerns like logging, validation, and error handling without modifying handler logic
- **Configurable Processing Chain**: Ability to create custom processing pipelines for both requests and notifications, enabling sophisticated pre- and post-processing workflows

Bazario is optimized for synchronous in-memory processing and handler routing, making it ideal for applications requiring modularity, simplicity, and flexible handler management.

## Installation
Bazario is available on PyPI: https://pypi.org/project/bazario/
```shell
pip install bazario
```

To install Bazario with a DI provider:
```shell
pip install "bazario[dishka]"
```

## Examples
Find more examples in the [examples folder](https://github.com/chessenjoyer17/bazario/tree/dev/examples)

### Requests and Request Handlers

**Requests** in Bazario represent actions that return a result. They are used to perform operations that require a return value, such as creating, reading, or updating data.

**Request Handlers** are responsible for processing requests and generating the corresponding results.

Here's an example of defining a request and its handler:
```python
from bazario import Request, RequestHandler

@dataclass(frozen=True)
class AddPost(Request[int]):
    title: str
    content: str

class AddPostHandler(RequestHandler[AddPost, int]):
    def __init__(
        self,
        post_factory: PostFactory,
        user_provider: UserProvider,
        post_repository: PostRepository,
        transaction_commiter: TransactionCommiter,
    ) -> None:
        self._post_factory = post_factory
        self._user_provider = user_provider
        self._post_repository = post_repository
        self._transaction_commiter = transaction_commiter
    
    def handle(self, request: AddPost) -> int:
        user_id = self._user_provider.get_id()
        new_post = self._post_factory.create(
            title=request.title,
            content=request.content,
            owner_id=user_id,
        )
        self._post_repository.add(new_post)
        self._transaction_commiter.commit()

        return new_post.id
```

### Configuring DI Framework
This example demonstrates how to configure your dependency injection (DI) framework (Dishka in this case) to work with Bazario:
```python
from bazario import Dispatcher, PipelineBehaviorRegistry
from bazario.plugins.dishka import (
    DishkaHandlerFinder,
    DishkaHandlerResolver,
)
from dishka import Provider, Scope, make_container

def build_container() -> Container:
    main_provider = Provider(scope=Scope.REQUEST)

    main_provider.provide(AddPostHandler)
    main_provider.provide(WithParents[Dispatcher])
    main_provider.provide(WithParents[DishkaHandlerFinder])
    main_provider.provide(WithParents[DishkaHandlerResolver])
    # Additional registrations (PostRepository, TransactionCommiter, etc.)

    return make_container(main_provider)
```

### Basic Usage
This example showcases the basic usage of sending a request via the `Sender` protocol:
```python
from bazario import Sender

with container() as request_container:
    sender = request_container.get(Sender)

    request = AddPost(
        title="Sicilian Defense: Countering e4!",
        description="An in-depth analysis of the Sicilian Defense: e4-c5!?",
    )
    post_id = sender.send(request)
    print(f"Post with ID {post_id} was added")
```

### Notifications and Event Handling

**Notifications** in Bazario represent events that are published in response to certain actions. They are used to notify other parts of the system about changes that have occurred, without requiring a return result.

**Notification Handlers** are responsible for processing these notifications.

Here's an example of defining a notification and its handlers:
Define notifications and their handlers:
```python
from bazario import Notification, NotificationHandler

@dataclass(frozen=True)
class PostAdded(Notification):
    post_id: int
    user_id: int

class PostAddedFirstHandler(NotificationHandler[PostAdded]):
    def handle(self, notification: PostAdded) -> None:
        logger.info(
            "Post first added: post_id=%s, user_id=%s",
            notification.post_id, notification.user_id,
        )

class PostAddedSecondHandler(NotificationHandler[PostAdded]):
    def handle(self, notification: PostAdded) -> None:
        logger.info(
            "Post second added: post_id=%s, user_id=%s",
            notification.post_id, notification.user_id,
        )
```

Register handlers in your container:
```python
def build_container() -> Container:
    # ...
    main_provider.provide(PostAddedFirstHandler)
    main_provider.provide(PostAddedSecondHandler)
    # ...
```

Implementation of notification publication within the request handler:
```python
from bazario import Publisher

class AddPostHandler(RequestHandler[AddPost, int]):
    def __init__(
        self,
        publisher: Publisher, # for notification publishing
        post_factory: PostFactory,
        user_provider: UserProvider,
        post_repository: PostRepository,
        transaction_commiter: TransactionCommiter,
    ) -> None:
        self._publisher = publisher
        self._post_factory = post_factory
        self._user_provider = user_provider
        self._post_repository = post_repository
        self._transaction_commiter = transaction_commiter
    
    def handle(self, request: AddPost) -> int:
        user_id = self._user_provider.get_id()
        new_post = self._post_factory.create(
            title=request.title,
            content=request.content,
            owner_id=user_id,
        )
        self._post_repository.add(new_post)
        self._publisher.publish(PostAdded(
            post_id=new_post.id,
            user_id=user_id,
        )) # notification publishing
        self._transaction_commiter.commit()

        return new_post.id
```

## Pipeline Behaviors
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
    registry.add_Behaviors(Request, RequestLoggingBehavior())
    registry.add_Behaviors(Notification, NotificationLoggingBehavior())
    registry.add_Behaviors(AddPost, AddPostLoggingBehavior())
    registry.add_Behaviors(PostAdded, PostAddedLoggingBehavior())

    return registry
```

The execution order follows these rules:
1. Global behaviors (registered for base types like `Request` or `Notification`) execute first
2. Specific behaviors (registered for concrete types like `AddPost` or `PostAdded`) execute after global ones
3. Within each category (global/specific), behaviors execute in the order they were registered
4. For a single request/notification, all applicable behaviors form a chain in this order

Example of execution flow for an `AddPost` request:
```python
def build_registry() -> PipelineBehaviorRegistry:
    registry = PipelineBehaviorRegistry()
    
    registry.add_Behaviors(Request, RequestLoggingBehavior())
    registry.add_Behaviors(
        AddPost, 
        ValidationBehavior(), 
        MetricsBehavior(),
    )

    return registry

# Execution sequence for AddPost request:
# 1. RequestLoggingBehavior
# 2. ValidationBehavior
# 3. MetricsBehavior
# 4. Actual AddPost handler
```

Configure the IoC container:
```python
def build_container() -> Container:
    # ...
    main_provider.provide(build_registry)
    # Note: The Dispatcher depends on PipelineBehaviorRegistry.
    # If you're not using pipeline behaviors, register PipelineBehaviorRegistry directly:
    # main_provider.provide(PipelineBehaviorRegistry)
    # ...
```

### Benefits of Pipeline Behaviors
Pipeline behaviors solve several common issues:
- Centralize cross-cutting concerns
- Keep handlers focused on business logic
- Enable flexible behavior execution order
- Eliminate code duplication in validation and response modification

## Why Choose Bazario?

Bazario addresses several limitations found in alternative libraries:

1. **Flexible Handler Support**: Supports both synchronous and asynchronous handlers through the **asyncio** package

2. **IoC Container Control**: Gives developers full control over container lifecycle and scope creation

3. **Simplified Registration**: Eliminates code duplication by registering handlers directly in the IoC container

4. **Enhanced Modularity**: Features a plugin system for easy integration with various DI frameworks

5. **SOLID Compliance**: Strictly adheres to SOLID principles, particularly the Interface Segregation Principle

6. **Clean Separation**: Controllers focus on request parsing while Bazario handles routing, improving code organization and testability

7. **Powerful Pipeline System**: Offers a sophisticated behavior pipeline architecture that allows developers to:
   - Implement cross-cutting concerns without modifying existing code
   - Create reusable middleware components
   - Configure different processing chains for different types of requests and notifications
   - Add monitoring, logging, and error handling in a centralized way

8. **Flexible Processing Control**: Enables fine-grained control over request and notification processing through:
   - Custom pipeline behaviors for specific request or notification types
   - Global behaviors for all requests or notifications
   - Configurable execution order of pipeline behaviors
   - Easy integration of new processing requirements without changing handler logic