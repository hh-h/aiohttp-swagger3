import functools
from collections import defaultdict
from typing import Any, Callable, Dict, Optional

import yaml
from aiohttp import web
from openapi_spec_validator import validate_v3_spec

from .routes import _SWAGGER_SPECIFICATION
from .swagger import Swagger
from .swagger_route import SwaggerRoute


class SwaggerDocs(Swagger):
    def __init__(
        self,
        app: web.Application,
        ui_path: str,
        *,
        title: str = "OpenAPI3",
        version: str = "1.0.0",
        description: Optional[str] = None,
        components: Optional[str] = None,
    ) -> None:
        spec: Dict = {
            "openapi": "3.0.0",
            "info": {"title": title, "version": version},
            "paths": defaultdict(lambda: defaultdict(dict)),
        }
        if description is not None:
            spec["info"]["description"] = description

        if components:
            with open(components) as f:
                spec.update(yaml.load(f))

        super().__init__(app, ui_path, spec)

    def add_route(
        self, method: str, path: str, handler: Callable, **kwargs: Any
    ) -> web.ResourceRoute:
        if handler.__doc__ and "---" in handler.__doc__:
            *_, spec = handler.__doc__.split("---")
            method_spec = yaml.load(spec)
            method_lower = method.lower()
            self.spec["paths"][path][method_lower] = method_spec
            validate_v3_spec(self.spec)
            route = SwaggerRoute(method_lower, path, handler, swagger=self, **kwargs)
            self._app[_SWAGGER_SPECIFICATION] = self.spec
            return self._app.router.add_route(
                method, path, functools.partial(self._handle_swagger_call, route)
            )
        else:
            return self._app.router.add_route(method, path, handler, **kwargs)
