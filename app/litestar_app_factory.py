from litestar import Litestar
from litestar.middleware.base import DefineMiddleware
from litestar.openapi import OpenAPIConfig
from litestar.openapi.spec import Components, SecurityScheme
from dishka import make_async_container
from dishka.integrations import litestar as litestar_integration
from dishka.integrations import faststream as faststream_integration

from app.auth.controllers.auth_ctrl import AuthController
from app.items.controllers import ItemController, ItemsCommandsDecoupled
from app.diskha_dependencies import AppProvider, UnitTestProvider, IntegrationTestProvider
from app.authentication_middleware import JWTAuthenticationMiddleware
from app.faststream_app_factory import create_faststream_app, lifespan_broker, FastStreamBroker, FastStream


def create_app() -> Litestar:
    auth_mw = create_auth_middleware()
    app = Litestar(
        debug=True,
        route_handlers=get_route_handlers(),
        openapi_config=create_openapi_config(),
        middleware=[
            # auth_mw
        ],
        on_startup=[on_startup],
        on_shutdown=[on_shutdown],
        lifespan=[lifespan_broker],
    )
    faststream_app: FastStream = create_faststream_app()
    broker: FastStreamBroker = faststream_app.broker
    container = make_async_container(AppProvider(), context={FastStreamBroker: broker})
    app.state.broker = broker
    litestar_integration.setup_dishka(container, app)
    faststream_integration.setup_dishka(container, faststream_app, auto_inject=True)
    return app


def create_unit_test_app() -> Litestar:
    auth_mw = create_auth_middleware()
    app = Litestar(
        debug=True,
        route_handlers=get_route_handlers(),
        openapi_config=create_openapi_config(),
        middleware=[
            auth_mw
        ],
        on_startup=[on_startup],
        on_shutdown=[on_shutdown],
        lifespan=[lifespan_broker],
    )
    faststream_app: FastStream = create_faststream_app()
    broker: FastStreamBroker = faststream_app.broker
    container = make_async_container(UnitTestProvider(), context={FastStreamBroker: broker})
    app.state.broker = broker
    litestar_integration.setup_dishka(container, app)
    faststream_integration.setup_dishka(container, faststream_app, auto_inject=True)
    return app


def create_integration_test_app() -> Litestar:
    auth_mw = create_auth_middleware()
    app = Litestar(
        debug=True,
        route_handlers=get_route_handlers(),
        openapi_config=create_openapi_config(),
        middleware=[
            auth_mw
        ],
        on_startup=[on_startup],
        on_shutdown=[on_shutdown],
        lifespan=[lifespan_broker],
    )
    faststream_app: FastStream = create_faststream_app()
    broker: FastStreamBroker = faststream_app.broker
    container = make_async_container(IntegrationTestProvider(), context={FastStreamBroker: broker})
    app.state.broker = broker
    litestar_integration.setup_dishka(container, app)
    faststream_integration.setup_dishka(container, faststream_app, auto_inject=True)
    return app



def get_route_handlers():
    return [
        AuthController
        , ItemController
        , ItemsCommandsDecoupled
        ]


def create_openapi_config():
    security_schemes = {
        "BearerAuth": SecurityScheme(
            type="http",
            scheme="bearer",
            bearer_format="JWT",  # Optional: Specify the format of the token (e.g., JWT)
        )
    }
    openapi_config = OpenAPIConfig(
        title="My API",
        version="1.0.0",
        description="A sample Litestar API with Swagger enabled",
        components=Components(security_schemes=security_schemes),
        security=[{"BearerAuth": []}],
    )
    return openapi_config


def create_auth_middleware():
    auth_mw = DefineMiddleware(JWTAuthenticationMiddleware, exclude="schema")
    return auth_mw


async def on_startup(app: Litestar):
    return


async def on_shutdown(app: Litestar):
    return

