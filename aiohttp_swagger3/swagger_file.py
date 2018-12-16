import functools
from typing import Any, Callable

import yaml
from aiohttp import web
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
        self, method: str, path: str, handler: Callable, **kwargs: Any
    ) -> web.ResourceRoute:
        lower_method = method.lower()
        if self.spec["paths"][path][lower_method]:
            route = SwaggerRoute(lower_method, path, handler, swagger=self, **kwargs)
            return self._app.router.add_route(
                method, path, functools.partial(self._handle_swagger_call, route)
            )
        else:
            return self._app.router.add_route(method, path, handler, **kwargs)
