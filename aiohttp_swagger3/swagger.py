import pathlib
from collections import defaultdict
from typing import TYPE_CHECKING, Any, Callable, DefaultDict, Dict, List

from aiohttp import hdrs, web

from .handlers import application_json
from .routes import _SWAGGER_INDEX_HTML, _redirect, _swagger_home, _swagger_spec

if TYPE_CHECKING:
    from .swagger_route import SwaggerRoute


class Swagger:
    def __init__(self, app: web.Application, ui_path: str, spec: Dict) -> None:
        if not ui_path.startswith("/"):
            raise Exception("ui_path should start with /")
        ui_path = ui_path.rstrip("/")
        self._app = app
        self.spec = spec

        self.handlers: DefaultDict[
            str, Dict[str, Callable[[web.Request], Any]]
        ] = defaultdict(dict)

        self._app.router.add_route("GET", ui_path, _redirect)
        self._app.router.add_route("GET", f"{ui_path}/", _swagger_home)
        self._app.router.add_route("GET", f"{ui_path}/swagger.json", _swagger_spec)

        base_path = pathlib.Path(__file__).parent
        self._app.router.add_static(f"{ui_path}/static", base_path / "swagger_ui")

        with open(base_path / "swagger_ui/index.html") as f:
            self._app[_SWAGGER_INDEX_HTML] = f.read()

        self.register_media_type_handler("application/json", application_json)

    async def _handle_swagger_call(
        self, route: "SwaggerRoute", request: web.Request
    ) -> web.Response:
        kwargs = await route.parse(request)
        return await route.handler(**kwargs)

    def add_route(
        self,
        method: str,
        path: str,
        handler: Callable[[web.Request], web.Response],
        **kwargs: Any,
    ) -> web.ResourceRoute:
        raise NotImplementedError

    def add_head(
        self, path: str, handler: Callable[[web.Request], web.Response], **kwargs: Any
    ) -> web.ResourceRoute:
        return self.add_route(hdrs.METH_HEAD, path, handler, **kwargs)

    def add_get(
        self, path: str, handler: Callable[[web.Request], web.Response], **kwargs: Any
    ) -> web.ResourceRoute:
        return self.add_route(hdrs.METH_GET, path, handler, **kwargs)

    def add_post(
        self, path: str, handler: Callable[[web.Request], web.Response], **kwargs: Any
    ) -> web.ResourceRoute:
        return self.add_route(hdrs.METH_POST, path, handler, **kwargs)

    def add_put(
        self, path: str, handler: Callable[[web.Request], web.Response], **kwargs: Any
    ) -> web.ResourceRoute:
        return self.add_route(hdrs.METH_PUT, path, handler, **kwargs)

    def add_patch(
        self, path: str, handler: Callable[[web.Request], web.Response], **kwargs: Any
    ) -> web.ResourceRoute:
        return self.add_route(hdrs.METH_PATCH, path, handler, **kwargs)

    def add_delete(
        self, path: str, handler: Callable[[web.Request], web.Response], **kwargs: Any
    ) -> web.ResourceRoute:
        return self.add_route(hdrs.METH_DELETE, path, handler, **kwargs)

    def add_routes(self, routes: List[web.RouteDef]) -> None:
        for route_obj in routes:
            route_obj.register(self)

    def register_media_type_handler(
        self, media_type: str, handler: Callable[[web.Request], Any]
    ) -> None:
        typ, subtype = media_type.split("/")
        self.handlers[typ][subtype] = handler

    def get_media_type_handler(self, media_type: str) -> Callable[[web.Request], Any]:
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
