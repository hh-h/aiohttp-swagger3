import pathlib
from collections import defaultdict
from typing import (
    TYPE_CHECKING,
    Any,
    Awaitable,
    Callable,
    DefaultDict,
    Dict,
    Optional,
    Tuple,
    Type,
)

from aiohttp import hdrs, web
from aiohttp.abc import AbstractView

from .handlers import application_json, x_www_form_urlencoded
from .routes import _SWAGGER_INDEX_HTML, _redirect, _swagger_home, _swagger_spec

if TYPE_CHECKING:
    from .swagger_route import SwaggerRoute


WebHandler = Callable[[web.Request], Awaitable[web.StreamResponse]]
ExpectHandler = Callable[[web.Request], Awaitable[None]]


class Swagger(web.UrlDispatcher):
    __slots__ = ("_app", "validate", "spec", "request_key", "handlers")

    def __init__(
        self,
        app: web.Application,
        ui_path: str,
        validate: bool,
        spec: Dict,
        request_key: str,
    ) -> None:
        if not ui_path.startswith("/"):
            raise Exception("ui_path should start with /")
        ui_path = ui_path.rstrip("/")
        self._app = app
        self.validate = validate
        self.spec = spec
        self.request_key = request_key

        self.handlers: DefaultDict[
            str, Dict[str, Callable[[web.Request], Awaitable[Tuple[Any, bool]]]]
        ] = defaultdict(dict)

        self._app.router.add_route("GET", ui_path, _redirect)
        self._app.router.add_route("GET", f"{ui_path}/", _swagger_home)
        self._app.router.add_route("GET", f"{ui_path}/swagger.json", _swagger_spec)

        base_path = pathlib.Path(__file__).parent
        self._app.router.add_static(f"{ui_path}/static", base_path / "swagger_ui")

        with open(base_path / "swagger_ui/index.html") as f:
            self._app[_SWAGGER_INDEX_HTML] = f.read()

        self.register_media_type_handler("application/json", application_json)
        self.register_media_type_handler(
            "application/x-www-form-urlencoded", x_www_form_urlencoded
        )

        super().__init__()

    async def _handle_swagger_call(
        self, route: "SwaggerRoute", request: web.Request
    ) -> web.StreamResponse:
        kwargs = await route.parse(request)
        return await route.handler(**kwargs)

    async def _handle_swagger_method_call(
        self, view: web.View, route: "SwaggerRoute"
    ) -> web.StreamResponse:
        kwargs = await route.parse(view.request)
        return await route.handler(view, **kwargs)

    def add_head(
        self, path: str, handler: WebHandler, **kwargs: Any
    ) -> web.AbstractRoute:
        return self.add_route(hdrs.METH_HEAD, path, handler, **kwargs)

    def add_options(
        self, path: str, handler: WebHandler, **kwargs: Any
    ) -> web.AbstractRoute:
        return self.add_route(hdrs.METH_OPTIONS, path, handler, **kwargs)

    def add_get(
        self,
        path: str,
        handler: WebHandler,
        name: Optional[str] = None,
        allow_head: bool = True,
        **kwargs: Any,
    ) -> web.AbstractRoute:
        if allow_head:
            self.add_route(hdrs.METH_HEAD, path, handler, **kwargs)
        return self.add_route(hdrs.METH_GET, path, handler, name=name, **kwargs)

    def add_post(
        self, path: str, handler: WebHandler, **kwargs: Any
    ) -> web.AbstractRoute:
        return self.add_route(hdrs.METH_POST, path, handler, **kwargs)

    def add_put(
        self, path: str, handler: WebHandler, **kwargs: Any
    ) -> web.AbstractRoute:
        return self.add_route(hdrs.METH_PUT, path, handler, **kwargs)

    def add_patch(
        self, path: str, handler: WebHandler, **kwargs: Any
    ) -> web.AbstractRoute:
        return self.add_route(hdrs.METH_PATCH, path, handler, **kwargs)

    def add_delete(
        self, path: str, handler: WebHandler, **kwargs: Any
    ) -> web.AbstractRoute:
        return self.add_route(hdrs.METH_DELETE, path, handler, **kwargs)

    def add_view(
        self, path: str, handler: Type[AbstractView], **kwargs: Any
    ) -> web.AbstractRoute:
        return self.add_route(hdrs.METH_ANY, path, handler, **kwargs)

    def register_media_type_handler(
        self,
        media_type: str,
        handler: Callable[[web.Request], Awaitable[Tuple[Any, bool]]],
    ) -> None:
        typ, subtype = media_type.split("/")
        self.handlers[typ][subtype] = handler

    def get_media_type_handler(
        self, media_type: str
    ) -> Callable[[web.Request], Awaitable[Tuple[Any, bool]]]:
        typ, subtype = media_type.split("/")
        if typ not in self.handlers:
            if "*" not in self.handlers:
                raise Exception(f"register handler for {media_type} first")
            elif "*" not in self.handlers["*"]:
                raise Exception("missing handler for media type */*")
            else:
                return self.handlers["*"]["*"]
        if subtype not in self.handlers[typ]:
            if "*" not in self.handlers[typ]:
                raise Exception(f"register handler for {media_type} first")
            return self.handlers[typ]["*"]
        return self.handlers[typ][subtype]
