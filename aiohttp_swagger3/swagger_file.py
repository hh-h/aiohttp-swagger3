import functools
from typing import Optional, Type, Union

import yaml
from aiohttp import hdrs, web
from aiohttp.abc import AbstractView
from openapi_spec_validator import validate_v3_spec

from .routes import _SWAGGER_SPECIFICATION
from .swagger import ExpectHandler, Swagger
from .swagger_route import SwaggerRoute, _SwaggerHandler


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
        handler: Union[_SwaggerHandler, Type[AbstractView]],
        *,
        name: Optional[str] = None,
        expect_handler: Optional[ExpectHandler] = None,
    ) -> web.AbstractRoute:
        if self.validate and path in self.spec["paths"]:
            if isinstance(handler, type) and issubclass(handler, AbstractView):
                for meth in hdrs.METH_ALL:
                    meth = meth.lower()
                    if meth not in self.spec["paths"][path]:
                        continue
                    handler_ = getattr(handler, meth, None)
                    if handler_ is None:
                        continue
                    route = SwaggerRoute(meth, path, handler_, swagger=self)
                    setattr(
                        handler,
                        meth,
                        functools.partialmethod(
                            self._handle_swagger_method_call, route
                        ),
                    )
            else:
                method_lower = method.lower()
                if method_lower in self.spec["paths"][path]:
                    route = SwaggerRoute(method_lower, path, handler, swagger=self)
                    handler = functools.partial(self._handle_swagger_call, route)

        return self._app.router.add_route(
            method, path, handler, name=name, expect_handler=expect_handler
        )
