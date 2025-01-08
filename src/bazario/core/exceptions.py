from bazario.markers import Notification, Request


class HandlerNotFoundError(Exception):
    def __init__(
        self,
        target_type: type[Request] | type[Notification],
    ) -> None:
        self.target_type = target_type

        super().__init__(
            f"Handler for target '{target_type.__name__}' not found.",
        )
