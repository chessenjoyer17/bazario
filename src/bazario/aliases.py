from typing import TypeAlias

from bazario.protocols.handler import NotificationHandler, RequestHandler

HandlerType: TypeAlias = RequestHandler | NotificationHandler
