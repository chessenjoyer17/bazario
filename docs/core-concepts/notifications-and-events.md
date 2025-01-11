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
``` python
def build_container() -> Container:
    # ...
    main_provider.provide(PostAddedFirstHandler)
    main_provider.provide(PostAddedSecondHandler)
    # ...
```
Implementation of notification publication within the request handler:
``` python
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
