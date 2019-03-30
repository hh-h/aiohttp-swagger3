import functools
from typing import Optional, Union

import yaml
from aiohttp import web
from aiohttp.abc import AbstractView
from openapi_spec_validator import validate_v3_spec

from .routes import _SWAGGER_SPECIFICATION
from .swagger import Swagger
from .swagger_route import SwaggerRoute

try:
    from aiohttp.web_urldispatcher import _ExpectHandler, _WebHandler
except ImportError:
    _ExpectHandler, _WebHandler = None, None


class SwaggerFile(Swagger):
    __slots__ = ()

    def __init__(
        self,
        app: web.Application,
        ui_path: str,
        spec_file: str,
        *,
        validate: bool = True,
        request_key: str = "data",
    ) -> None:
        with open(spec_file) as f:
            spec = yaml.safe_load(f)
        validate_v3_spec(spec)

        super().__init__(app, ui_path, validate, spec, request_key)
        self._app[_SWAGGER_SPECIFICATION] = spec

    def add_route(
        self,
        method: str,
        path: str,
        handler: Union[_WebHandler, AbstractView],
        *,
        name: Optional[str] = None,
        expect_handler: Optional[_ExpectHandler] = None,
    ) -> web.AbstractRoute:
        lower_method = method.lower()
        if (
            self.validate
            and path in self.spec["paths"]
            and lower_method in self.spec["paths"][path]
        ):
            route = SwaggerRoute(lower_method, path, handler, swagger=self)
            handler = functools.partial(self._handle_swagger_call, route)

        return self._app.router.add_route(
            method, path, handler, name=name, expect_handler=expect_handler
        )
