import functools
from collections import defaultdict
from typing import Dict, Optional, Union

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


class SwaggerDocs(Swagger):
    __slots__ = ()

    def __init__(
        self,
        app: web.Application,
        ui_path: str,
        *,
        validate: bool = True,
        request_key: str = "data",
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
                spec.update(yaml.safe_load(f))

        super().__init__(app, ui_path, validate, spec, request_key)

    def add_route(
        self,
        method: str,
        path: str,
        handler: Union[_WebHandler, AbstractView],
        *,
        name: Optional[str] = None,
        expect_handler: Optional[_ExpectHandler] = None,
    ) -> web.AbstractRoute:
        if self.validate and handler.__doc__ and "---" in handler.__doc__:
            *_, spec = handler.__doc__.split("---")
            method_spec = yaml.safe_load(spec)
            method_lower = method.lower()
            self.spec["paths"][path][method_lower] = method_spec
            validate_v3_spec(self.spec)
            route = SwaggerRoute(method_lower, path, handler, swagger=self)
            self._app[_SWAGGER_SPECIFICATION] = self.spec
            handler = functools.partial(self._handle_swagger_call, route)

        return self._app.router.add_route(
            method, path, handler, name=name, expect_handler=expect_handler
        )
