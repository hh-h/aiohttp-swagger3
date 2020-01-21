import json
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
    Set,
    Tuple,
    Type,
)

import fastjsonschema
from aiohttp import hdrs, web
from aiohttp.abc import AbstractView

from .handlers import application_json, x_www_form_urlencoded
from .index_templates import RAPIDOC_UI_TEMPLATE, REDOC_UI_TEMPLATE, SWAGGER_UI_TEMPLATE
from .routes import (
    _RAPIDOC_UI_INDEX_HTML,
    _REDOC_UI_INDEX_HTML,
    _SWAGGER_UI_INDEX_HTML,
    _rapidoc_ui,
    _redirect,
    _redoc_ui,
    _swagger_spec,
    _swagger_ui,
)
from .ui_settings import RapiDocUiSettings, ReDocUiSettings, SwaggerUiSettings

if TYPE_CHECKING:
    from .swagger_route import SwaggerRoute


WebHandler = Callable[[web.Request], Awaitable[web.StreamResponse]]
ExpectHandler = Callable[[web.Request], Awaitable[None]]


class Swagger(web.UrlDispatcher):
    __slots__ = ("_app", "validate", "spec", "request_key", "handlers", "spec_validate")

    def __init__(
        self,
        app: web.Application,
        *,
        validate: bool,
        spec: Dict,
        request_key: str,
        swagger_ui_settings: Optional[SwaggerUiSettings],
        redoc_ui_settings: Optional[ReDocUiSettings],
        rapidoc_ui_settings: Optional[RapiDocUiSettings],
    ) -> None:
        self._app = app
        self.validate = validate
        self.spec = spec
        self.request_key = request_key
        self.handlers: DefaultDict[
            str, Dict[str, Callable[[web.Request], Awaitable[Tuple[Any, bool]]]]
        ] = defaultdict(dict)

        uis = (rapidoc_ui_settings, redoc_ui_settings, swagger_ui_settings)
        paths: Set[str] = set()
        for ui in uis:
            if ui is None:
                continue
            if ui.path in paths:
                raise Exception("cannot bind two UIs on the same path")
            paths.add(ui.path)

        base_path = pathlib.Path(__file__).parent
        with open(base_path / "schema/schema.json") as f:
            schema = json.load(f)

        self.spec_validate = fastjsonschema.compile(
            schema, formats={"uri-reference": r"^\w+:(\/?\/?)[^\s]+\Z|^#(\/\w+)+"}
        )
        self.spec_validate(self.spec)

        if swagger_ui_settings is not None:
            ui_path = swagger_ui_settings.path
            if not ui_path.startswith("/"):
                raise Exception("path should start with /")
            need_redirect = ui_path != "/"
            ui_path = ui_path.rstrip("/")
            if need_redirect:
                self._app.router.add_route("GET", ui_path, _redirect)
            self._app.router.add_route("GET", f"{ui_path}/", _swagger_ui)
            self._app.router.add_route("GET", f"{ui_path}/swagger.json", _swagger_spec)

            self._app.router.add_static(
                f"{ui_path}/swagger_ui_static", base_path / "swagger_ui"
            )

            self._app[_SWAGGER_UI_INDEX_HTML] = SWAGGER_UI_TEMPLATE.substitute(
                {"settings": json.dumps(swagger_ui_settings.to_settings())}
            )

        if redoc_ui_settings is not None:
            ui_path = redoc_ui_settings.path
            if not ui_path.startswith("/"):
                raise Exception("path should start with /")
            need_redirect = ui_path != "/"
            ui_path = ui_path.rstrip("/")
            if need_redirect:
                self._app.router.add_route("GET", ui_path, _redirect)
            self._app.router.add_route("GET", f"{ui_path}/", _redoc_ui)
            self._app.router.add_route("GET", f"{ui_path}/swagger.json", _swagger_spec)

            self._app.router.add_static(
                f"{ui_path}/redoc_ui_static", base_path / "redoc_ui"
            )

            self._app[_REDOC_UI_INDEX_HTML] = REDOC_UI_TEMPLATE.substitute(
                {"settings": json.dumps(redoc_ui_settings.to_settings())}
            )

        if rapidoc_ui_settings is not None:
            ui_path = rapidoc_ui_settings.path
            if not ui_path.startswith("/"):
                raise Exception("path should start with /")
            need_redirect = ui_path != "/"
            ui_path = ui_path.rstrip("/")
            if need_redirect:
                self._app.router.add_route("GET", ui_path, _redirect)
            self._app.router.add_route("GET", f"{ui_path}/", _rapidoc_ui)
            self._app.router.add_route("GET", f"{ui_path}/swagger.json", _swagger_spec)

            self._app.router.add_static(
                f"{ui_path}/rapidoc_ui_static", base_path / "rapidoc_ui"
            )

            self._app[_RAPIDOC_UI_INDEX_HTML] = RAPIDOC_UI_TEMPLATE.substitute(
                {"settings": json.dumps(rapidoc_ui_settings.to_settings())}
            )

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
            elif subtype not in self.handlers["*"]:
                if "*" not in self.handlers["*"]:
                    raise Exception("missing handler for media type */*")
                return self.handlers["*"]["*"]
            else:
                return self.handlers["*"][subtype]
        if subtype not in self.handlers[typ]:
            if "*" not in self.handlers[typ]:
                raise Exception(f"register handler for {media_type} first")
            return self.handlers[typ]["*"]
        return self.handlers[typ][subtype]
