from typing import Protocol


class Notification(Protocol): ...


class Request[TRes](Protocol): ...
