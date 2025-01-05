from bazario.markers import Notification, Request
from bazario.protocols.handler import NotificationHandler, RequestHandler


def extract_request_type_from_handler(handler: type[RequestHandler]) -> type[Request]:
    for base in handler.__orig_bases__:
        if base.__origin__ is RequestHandler:
            for arg in base.__args__:
                if issubclass(arg, Request) or arg is Request:
                    return arg

    raise ValueError(f"No Request type found in {handler}")


def extract_notification_type_from_handler(
    handler: type[NotificationHandler],
) -> type[Notification]:
    for base in handler.__orig_bases__:
        if base.__origin__ is NotificationHandler:
            for arg in base.__args__:
                if issubclass(arg, Notification) or arg is Notification:
                    return arg

    raise ValueError(f"No Notification type found in {handler}")
