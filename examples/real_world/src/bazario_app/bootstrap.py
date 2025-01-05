from dishka import Container, Scope, make_container
from litestar import Litestar
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import SwaggerRenderPlugin

from bazario.core.dispatcher import Dispatcher
from bazario.core.factories import get_builder
from bazario.resolvers.dishka import (
    DishkaResolver,
    bazario_provider,
)
from bazario.resolvers.dishka import setup_dishka as setup_bazario_dishka
from bazario_app.application.commands import AddPostHandler
from bazario_app.application.events import LogOnPostAddedHandler
from bazario_app.application.queries import GetAllPostsHandler, GetPostByIdHandler
from bazario_app.di_container import adapters_provider, application_handlers_provider
from bazario_app.presentation.post_controller import PostController
from bazario_app.presentation.sync_dishka import setup_dishka as setup_litestar_dishka


def error_handler(_, exc: Exception):
    raise exc


def get_container() -> Container:
    return make_container(
        bazario_provider(),
        adapters_provider(),
        application_handlers_provider(),
    )


def get_dispatcher(container: Container) -> Dispatcher:
    dispatcher = (
        get_builder()
        .with_resolver(DishkaResolver(container))
        .with_request_handler(AddPostHandler)
        .with_request_handler(
            GetPostByIdHandler,
            DishkaResolver(container, Scope.ACTION),
        )
        .with_request_handler(GetAllPostsHandler)
        .with_notification_handler(LogOnPostAddedHandler)
        .build()
    )

    return dispatcher


def get_application() -> Litestar:
    application = Litestar(
        openapi_config=OpenAPIConfig(
            title="Хуй знает",
            description="А не ебу",
            version="0.1.0",
            path="/swagger",
            render_plugins=[SwaggerRenderPlugin()],
        ),
        exception_handlers={Exception: error_handler},
    )
    application.register(PostController)

    return application


def bootstrap() -> Litestar:
    container = get_container()
    application = get_application()
    dispatcher = get_dispatcher(container)

    setup_bazario_dishka(container, dispatcher)
    setup_litestar_dishka(container, application)

    return application
