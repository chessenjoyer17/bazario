# 🔔 Notifications & Handlers
> Modern event handling with Bazario

<div class="animated-card" markdown="1">

## 🌟 What are Notifications?

**Notifications** in Bazario represent events that are published in response to certain actions. Think of them as messengers that broadcast changes throughout your system, without expecting a response back.

</div>

## 🛠️ Implementation Guide

### 📝 Example: Defining Notifications and Handlers

<div class="code-window" markdown="1">

```python
from bazario import Notification, NotificationHandler
from dataclasses import dataclass

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
</div>

## 🔌 Setup Process
1️⃣ Register with Registry
```python
registry.add_notification_handlers(
    PostAdded, 
    PostAddedFirstHandler,
    PostAddedSecondHandler,
)
```
2️⃣ Configure IoC Container
```python
container.register(PostAddedFirstHandler)
container.register(PostAddedSecondHandler)
```
3️⃣ Publishing Notifications
```python
from bazario import Publisher

def controller(publisher: Publisher) -> None:
    publisher.publish(PostAdded(post_id=1, user_id=1))
    # ✨ Output:
    # Post first added: post_id=1, user_id=1
    # Post second added: post_id=1, user_id=1
```

<details>
<summary>📚 Original Documentation</summary>
<span style="font-size: 1.3em">

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


registry.add_notification_handlers(
    PostAdded, 
    PostAddedFirstHandler,
    PostAddedSecondHandler,
)


container.register(PostAddedFirstHandler)
container.register(PostAddedSecondHandler)


def controller(publisher: Publisher) -> None:
    publisher.publish(PostAdded(post_id=1, user_id=1))
    # Post first added: post_id=1, user_id=1
    # Post second added: post_id=1, user_id=1
```
</span>
</details>



