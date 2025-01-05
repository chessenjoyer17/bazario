from uuid import UUID

from dishka import FromDishka
from litestar import Controller, get, post
from litestar.exceptions import HTTPException

from bazario.protocols.sender import Sender
from bazario_app.application.commands import AddPost
from bazario_app.application.models.post import Post
from bazario_app.application.queries import GetAllPosts, GetPostById
from bazario_app.presentation.sync_dishka import inject


class PostController(Controller):
    path = "/posts"

    @get(path="/", sync_to_thread=True)
    @inject
    def get_all(self, sender: FromDishka[Sender]) -> list[Post]:
        return sender.send(GetAllPosts())

    @get(path="/{post_id:uuid}", sync_to_thread=True)
    @inject
    def action_scoped_handler(self, post_id: UUID, sender: FromDishka[Sender]) -> Post:
        try:
            return sender.send(GetPostById(post_id))

        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    @post(path="/", sync_to_thread=True)
    @inject
    def add_one(self, data: AddPost, sender: FromDishka[Sender]) -> UUID:
        return sender.send(data)
