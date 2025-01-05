from bazario.core.handler_key import NotificationHandlerKey, RequestHandlerKey
from bazario.markers import Notification, Request

type RequestHandlers = dict[type[Request], RequestHandlerKey]
type NotificationHandlers = dict[type[Notification], list[NotificationHandlerKey]]
