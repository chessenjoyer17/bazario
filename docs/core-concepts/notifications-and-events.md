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

Add handlers to `Registry`:
``` python
# ...
registry.add_notification_handlers(
    PostAdded, 
    PostAddedFirstHandler,
    PostAddedSecondHandler,
)
# ...
```

Add handlers to your IoC container:
``` python
# ...
container.register(PostAddedFirstHandler)
container.register(PostAddedSecondHandler)
# ...
```
Finally, you can publish natifications:
``` python
from bazario import Publisher


def controller(publisher: Publisher) -> None:
    publisher.publish(PostAdded(post_id=1, user_id=1))
    # Post first added: post_id=1, user_id=1
    # Post second added: post_id=1, user_id=1
```
