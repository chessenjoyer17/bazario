from bazario.abc.handler import NotificationHandler, RequestHandler
from bazario.abc.pipeline_behavior import PipelineBehavior
from bazario.markers import Notification, Request


class Registry:
    request_handlers: dict[type[Request], type[RequestHandler]]
    notification_handlers: dict[
        type[Notification],
        list[type[NotificationHandler]],
    ]
    pipeline_behaviors: dict[type, list[type[PipelineBehavior]]]

    def __init__(self) -> None:
        self.request_handlers = {}
        self.notification_handlers = {}
        self.pipeline_behaviors = {}

    def add_request_handler(
        self,
        request_type: type[Request],
        request_handler: type[RequestHandler],
    ) -> None:
        self.request_handlers[request_type] = request_handler

    def add_notification_handlers(
        self,
        notification_type: type[Notification],
        *notification_handlers: type[NotificationHandler],
    ) -> None:
        self.notification_handlers.setdefault(notification_type, []).extend(
            notification_handlers,
        )

    def add_pipeline_behaviors(
        self,
        request_type: type,
        *pipeline_behaviors: type[PipelineBehavior],
    ) -> None:
        self.pipeline_behaviors.setdefault(request_type, []).extend(
            pipeline_behaviors,
        )

    def get_request_handler(
        self,
        request_type: type[Request],
    ) -> type[RequestHandler] | None:
        return self.request_handlers.get(request_type)

    def get_notification_handlers(
        self,
        notification_type: type[Notification],
    ) -> list[type[NotificationHandler]]:
        return [
            handler
            for notification, handlers in self.notification_handlers.items()
            for handler in handlers
            if issubclass(notification_type, notification)
        ]

    def get_pipeline_behaviors(
        self,
        request_type: type,
    ) -> list[type[PipelineBehavior]]:
        return [
            behavior
            for request, behaviors in self.pipeline_behaviors.items()
            for behavior in behaviors
            if issubclass(request_type, request)
        ]
