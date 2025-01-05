from dishka import Provider, Scope, WithParents

from bazario_app.adapters.mock_gateway import MockGateway
from bazario_app.adapters.mock_transaction import MockTransaction
from bazario_app.application.commands import AddPostHandler
from bazario_app.application.events import LogOnPostAddedHandler
from bazario_app.application.queries import GetAllPostsHandler, GetPostByIdHandler


def adapters_provider() -> Provider:
    provider = Provider(scope=Scope.APP)

    provider.provide(WithParents[MockGateway])
    provider.provide(WithParents[MockTransaction])

    return provider


def application_handlers_provider() -> Provider:
    provider = Provider()

    provider.provide_all(
        AddPostHandler,
        GetAllPostsHandler,
        LogOnPostAddedHandler,
        scope=Scope.REQUEST,
    )
    provider.provide(GetPostByIdHandler, scope=Scope.ACTION)

    return provider
