# Bazario

**Bazario** is a lightweight, expressive library for routing requests and notifications to the right handlers with ease. Designed for modular applications, it simplifies your codebase while staying powerful and flexible.

📚 [Documentation](https://chessenjoyer17.github.io/bazario/)

---

## 🚀 Quick Start

### Installation
Install Bazario with pip:
```bash
pip install bazario
```

### Define Your Logic

#### 1. Create a Request and its Handler
Define what you want to do with a `Request` and specify how it’s handled:
```python
# application/requests/create_user.py
from bazario import Request, RequestHandler

class CreateUserRequest(Request[str]):
    def __init__(self, username: str):
        self.username = username

class CreateUserHandler(RequestHandler[CreateUserRequest, str]):
    def handle(self, request: CreateUserRequest) -> str:
        return f"User {request.username} created!"
```

#### 2. Create a Notification and its Handler
Use `Notification` to broadcast events:
```python
# application/notifications/user_created.py
from bazario import Notification, NotificationHandler

class UserCreatedNotification(Notification):
    def __init__(self, user_id: str):
        self.user_id = user_id

class UserCreatedHandler(NotificationHandler[UserCreatedNotification]):
    def handle(self, notification: UserCreatedNotification) -> None:
        print(f"Notification: User {notification.user_id} was created.")
```

### Bring It All Together
Set up your `Dispatcher` to handle requests and notifications seamlessly:
```python
# bootstap/ioc.py
from bazario import Dispatcher, Resolver, Sender, Publisher
from bazario.resolvers.your_di_framework import YourDIFrameworkResolver

from your_di_framework import Container

def provide_registry() -> Registry:
    registry = Registry()
    registry.add_request_handler(CreateUserRequest, CreateUserHandler)
    registry.add_notification_handlers(UserCreatedNotification, UserCreatedHandler)
    return registry


def provide_resolver(container: Container) -> Resolver:
    return YourDIFrameworkResolver(container)


def provide_dispatcher(registry: Registry, resolver: Resolver) -> Dispatcher:
    return Dispatcher(resolver, registry)


def provide_container() -> Container:
    container = Container()
    container.register(Registry, provide_registry)
    container.register(Resolver, provide_resolver)
    container.register(Dispatcher, provide_dispatcher)
    container.register_aliases(Dispatcher, aliases=[Sender, Publisher])
    return container


# presentation/rest/users.py
from your_framework import post
from your_di_framework import inject
from bazario import Sender, Publisher

from application.requests.create_user import CreateUserRequest
from application.notifications.user_created import UserCreatedNotification

@post("/")
@inject
def create_user(sender: Sender, publisher: Publisher) -> None:
    response = sender.send(CreateUserRequest("john_doe"))
    print(response)  # Output: User john_doe created!
    publisher.publish(UserCreatedNotification("123"))  # Output: Notification: User 123 was created.
```

---

## ✨ Key Features

- **Request Handling**: A streamlined mechanism for handling requests with clear separation of responsibilities.
- **Event Handling**: Unified event publication and handling (Notifications) supporting both standard and async/await syntax while maintaining efficient in-memory processing.
- **Modular Architecture**: Clear separation of business logic, ports, and infrastructure, simplifying development and maintenance.
- **IoC Container Integration**: Support for DI frameworks enabling easy dependency management and modular configuration.
- **Testability**: Use of abstractions to easily mock infrastructure adapters for unit testing.
- **Asynchronous Support**: The **bazario.asyncio** package enables asynchronous handling, providing flexibility for applications requiring async logic.
- **Dependency Separation**: Controllers delegate handler resolution to **Bazario**, focusing solely on request parsing. This improves separation of responsibilities and enhances code maintainability.
- **Pipeline Behaviors**: Flexible middleware system for implementing cross-cutting concerns like logging, validation, and error handling without modifying handler logic.
- **Configurable Processing Chain**: Ability to create custom processing pipelines for both requests and notifications, enabling sophisticated pre- and post-processing workflows.

Bazario is optimized for synchronous in-memory processing and handler routing, making it ideal for applications requiring modularity, simplicity, and flexible handler management.

---
