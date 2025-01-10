**Bazario** is a lightweight handler routing library designed for modular applications, utilizing the CQRS (Command and Query Responsibility Segregation) pattern. It simplifies development by providing centralized handling of requests (Requests) and events (Notifications), with efficient handler routing and support for both synchronous and asynchronous operations.

### Key Features:
- **Requests**: A simplified mechanism for handling requests (Requests) with clear separation of responsibilities.
- **Event Handling**: Event publication and handling (Notifications) for both synchronous and asynchronous communication between components.
- **Modular Architecture**: Clear separation of business logic, ports, and infrastructure, simplifying development and maintenance.
- **Integration with DI Containers**: Supports DI frameworks like Dishka, enabling easy dependency management and modular configuration.
- **Testability**: Protocols (Protocol) are used to easily mock infrastructure adapters for unit testing.
- **Support for Asynchronous Handlers**: **Bazario** includes an **asyncio** package, allowing for asynchronous handling, providing flexibility for applications requiring async logic.
- **Dependency Separation**: Controllers no longer need to resolve handlers themselves. They simply parse the request, and **Bazario** handles the processing and routing. This improves responsibility separation and makes controller code cleaner and more maintainable.

Bazario is optimized for synchronous in-memory processing and handler routing, making it an ideal choice for applications that require modularity, simplicity, and flexible handler management.

# Installation
Bazario is available on pypi: https://pypi.org/project/bazario/
``` shell
pip install bazario
```
also you can install bazario with di provider, for an example:
``` shell
pip install "bazario[dishka]"
```

# Examples
You can find more examples in [this folder](https://github.com/chessenjoyer17/bazario/tree/dev/examples)

## Create requests with handlers for them
``` python
from bazario import Request, RequestHandler
# ... other imports


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
## Choose DI framework plugin
``` python
from bazario import Dispatcher
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
    # other registrations like PostRepository, TransactionCommiter, etc.

    return make_container(main_provider)
```
## Main usage
``` python
from bazario import Sender


with container() as request_container:
    sender = request_container.get(Sender)

    request = AddPost(
        title="Sicilian defense. The way to destroy e4!",
        description="In this article we are talking about the sicilian defense: e4-c5!?",
    )
    post_id = sender.send(request)
    print(f"Post with id {post_id} was added")
```

## Notifications publishing
Define notifications and its handlers
``` python
from bazario import Notification, NotificationHandler


@dataclass(frozen=True)
class PostAdded(Notification):
    post_id: int
    user_id: int


class PostAddedFirstHandler(NotificationHandler[PostAdded]):
    def handle(self, notification: PostAdded) -> None:
        logger.info(
            "Post first added: post_id=%s,  user_id=%s", 
            notification.post_id, notification.user_id,
        )


class PostAddedSecondHandler(NotificationHandler[PostAdded]):
    def handle(self, notification: PostAdded) -> None:
        logger.info(
            "Post second added: post_id=%s,  user_id=%s", 
            notification.post_id, notification.user_id,
        )
```
## Register handlers to your container(for an example in dishka)
``` python
def build_container() -> Container:
    ...
    main_provider.provide(PostAddedFirstHandler)
    main_provider.provide(PostAddedSecondHandler)
    ...
```
## Finally you can use notifications and publish them
``` python
...
from bazario import Publisher


class AddPostHandler(RequestHandler[AddPost, int]):
    def __init__(
        self,
        publisher: Publisher,
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
            post_id=post_id,
            user_id=user_id,
        ))
        # Post first added: post_id=1,  user_id=2
        # Post second added: post_id=1,  user_id=2
        self._transaction_commiter.commit()

        return new_post.id
```

### Why **Bazario**?
I reviewed existing alternatives and found several issues that **Bazario** solves:

- **Lack of support for both synchronous and asynchronous handlers**: Most libraries require choosing between synchronous or asynchronous processing, limiting flexibility.  
  **Bazario** addresses this issue by supporting both synchronous and asynchronous handling through the **asyncio** package for async operations. This allows the library to be used in various types of applications without limiting the developer’s choice of processing type.

- **Control over IoC container and scope creation**: This is often handled by the library itself, leading to bugs and side effects. It can also reduce performance, as multiple parallel containers could be created.  
  **Bazario** allows the client to control the IoC container and scope creation, giving full control over the container’s lifecycle and preventing performance issues or side effects caused by redundant container instances.

- **Code duplication when registering handlers**: In many libraries, handlers need to be registered both in the library’s object and in the IoC container, which results in code duplication.  
  **Bazario** eliminates this duplication by ensuring that handlers are registered directly in the IoC container, making the code cleaner and easier to maintain, and reducing unnecessary configuration.

- **Lack of modularity**: In other libraries, integrating different DI frameworks is challenging without rewriting significant portions of the logic.  
  **Bazario** solves this problem by utilizing a modular plugin system, allowing easy integration with any DI framework. This provides the ability to use **Bazario** in different environments without being tied to a specific DI framework.

- **Violation of SOLID principles**: Some libraries do not fully adhere to SOLID principles, making the code more complex and harder to maintain.  
  **Bazario** fully adheres to SOLID principles, particularly ISP (Interface Segregation Principle). For example, instead of tightly coupling everything to a Dispatcher, **Bazario** separates responsibilities by introducing the **Publisher** protocol for event publication and the **Sender** protocol for sending requests, leading to better responsibility separation and reduced unnecessary dependencies.

- **Dependency Separation**: In traditional approaches, controllers often handle both request parsing and handler resolution, which increases their complexity and reduces testability.  
  **Bazario** addresses this by delegating all handler routing responsibilities to **Bazario**, allowing controllers to focus solely on parsing requests. This improves responsibility separation and makes controller code cleaner and more testable.
