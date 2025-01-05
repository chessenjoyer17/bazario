import logging
from dataclasses import dataclass
from uuid import UUID

from bazario.markers import Notification
from bazario.protocols.handler import NotificationHandler


@dataclass
class PostAdded(Notification):
    post_id: UUID


class LogOnPostAddedHandler(NotificationHandler[PostAdded]):
    def handle(self, notification: PostAdded) -> None:
        logging.info(f"Post {notification.post_id} added")
