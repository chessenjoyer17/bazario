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
### Basic Usage
This example showcases the basic usage of sending a request via the `Sender` protocol:
```python
from bazario import Sender

def controller(sender: Sender) -> None:
    request = AddPost(
        title="Sicilian Defense: Countering e4!",
        description="An in-depth analysis of the Sicilian Defense: e4-c5!?",
    )
    post_id = sender.send(request)
    print(f"Post with ID {post_id} was added")
```