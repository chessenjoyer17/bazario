### Step 1: Install bazario with punq provider
```bash
pip install 'bazario[punq]'
```

### Step 2: Setup bazario components(handlers, behaviors, etc) and container
``` python
# bootstap/ioc.py
from bazario import Dispatcher, Resolver
from bazario.resolvers.punq import PunqResolver

from punq import Container

def provide_registry() -> Registry:
    registry = Registry()
    
    registry.add_request_handler(CreateUserRequest, CreateUserHandler)
    registry.add_notification_handlers(UserCreatedNotification, UserCreatedHandler)
    
    return registry


def provide_container() -> Container:
    container = Container()

    container.register(Dispatcher)
    container.register(Sender, Dispatcher)
    container.register(Publisher, Dispatcher)
    container.register(Resolver, PunqResolver)
    container.register(Registry, provide_registry)
    container.register(CreateUserHandler)
    container.register(UserCreatedHandler)
    
    return container
```

### Step 3: Use bazario with punq
``` python
# presentation/users.py
from punq import Container
from bazario import Sender, Publisher

from application.requests.create_user import CreateUserRequest
from application.notifications.user_created import UserCreatedNotification

def create_user(container: Container) -> None:
    sender = container.resolve(Sender)
    publisher = container.resolve(Publisher)
    response = sender.send(CreateUserRequest("john_doe"))
    print(response)  # Output: User john_doe created!
    publisher.publish(UserCreatedNotification("123"))  # Output: Notification: User 123 was created.
```
