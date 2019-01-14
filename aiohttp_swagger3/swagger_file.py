import functools
from typing import Optional, Union

import yaml
from aiohttp import web
from aiohttp.abc import AbstractView
from aiohttp.web_urldispatcher import _ExpectHandler, _WebHandler
from openapi_spec_validator import validate_v3_spec

from .routes import _SWAGGER_SPECIFICATION
from .swagger import Swagger
from .swagger_route import SwaggerRoute


class SwaggerFile(Swagger):
    def __init__(self, app: web.Application, ui_path: str, spec_file: str) -> None:
        with open(spec_file) as f:
            spec = yaml.load(f)
        validate_v3_spec(spec)

        super().__init__(app, ui_path, spec)
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
        if path in self.spec["paths"] and lower_method in self.spec["paths"][path]:
            route = SwaggerRoute(lower_method, path, handler, swagger=self)
            handler = functools.partial(self._handle_swagger_call, route)

        return self._app.router.add_route(
            method, path, handler, name=name, expect_handler=expect_handler
        )
