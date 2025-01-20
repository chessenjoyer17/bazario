### Step 1: Install bazario with dishka provider
```bash
pip install 'bazario[dishka]'
```

### Step 2: Setup bazario components(handlers, behaviors, etc) and container
``` python
# bootstap/ioc.py
from bazario import Dispatcher, Resolver
from bazario.resolvers.dishka import DishkaResolver

from dishka import Container, Provider, Scope, WithParents, make_container

def provide_registry() -> Registry:
    registry = Registry()
    registry.add_request_handler(CreateUserRequest, CreateUserHandler)
    registry.add_notification_handlers(UserCreatedNotification, UserCreatedHandler)
    return registry


def provide_container() -> Container:
    provider = Provider(scope=Scope.REQUEST)

    provider.provide(provide_registry)
    provider.provide(WithParents[Dispatcher])
    provider.provide_all(
        CreateUserHandler, 
        UserCreatedHandler,
    )
    
    return make_container(provider)
```

### Step 3: Use bazario with dishka
``` python
# presentation/rest/users.py
from your_framework import post, inject
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
