import functools
import warnings
from collections import defaultdict
from typing import Dict, Optional, Type, Union

import yaml
from aiohttp import hdrs, web
from aiohttp.abc import AbstractView

from .redoc_ui_settings import ReDocUiSettings
from .routes import _SWAGGER_SPECIFICATION
from .swagger import ExpectHandler, Swagger
from .swagger_route import SwaggerRoute, _SwaggerHandler
from .swagger_ui_settings import SwaggerUiSettings


class SwaggerDocs(Swagger):
    __slots__ = ()

    def __init__(
        self,
        app: web.Application,
        ui_path: Optional[str] = None,
        *,
        validate: bool = True,
        request_key: str = "data",
        title: str = "OpenAPI3",
        version: str = "1.0.0",
        description: Optional[str] = None,
        components: Optional[str] = None,
        swagger_ui_settings: Optional[SwaggerUiSettings] = None,
        redoc_ui_settings: Optional[ReDocUiSettings] = None,
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

        if swagger_ui_settings is None and ui_path is not None:
            warnings.warn(
                "ui_path is deprecated and will be removed in 0.4.0, use swagger_ui_settings instead.",
                FutureWarning,
            )
            swagger_ui_settings = SwaggerUiSettings(path=ui_path)

        super().__init__(
            app,
            validate=validate,
            spec=spec,
            request_key=request_key,
            swagger_ui_settings=swagger_ui_settings,
            redoc_ui_settings=redoc_ui_settings,
        )
        self._app[_SWAGGER_SPECIFICATION] = self.spec

    def _wrap_handler(
        self, method: str, path: str, handler: _SwaggerHandler, *, is_method: bool
    ) -> _SwaggerHandler:
        if not handler.__doc__ or "---" not in handler.__doc__:
            return handler
        *_, spec = handler.__doc__.split("---")
        method_spec = yaml.safe_load(spec)
        self.spec["paths"][path][method] = method_spec
        self.spec_validate(self.spec)
        self._app[_SWAGGER_SPECIFICATION] = self.spec
        if not self.validate:
            return handler
        route = SwaggerRoute(method, path, handler, swagger=self)
        if is_method:
            return functools.partialmethod(  # type: ignore
                self._handle_swagger_method_call, route
            )
        return functools.partial(self._handle_swagger_call, route)

    def add_route(
        self,
        method: str,
        path: str,
        handler: Union[_SwaggerHandler, Type[AbstractView]],
        *,
        name: Optional[str] = None,
        expect_handler: Optional[ExpectHandler] = None,
    ) -> web.AbstractRoute:
        if isinstance(handler, type) and issubclass(handler, AbstractView):
            for meth in hdrs.METH_ALL:
                meth = meth.lower()
                handler_ = getattr(handler, meth, None)
                if handler_ is not None:
                    setattr(
                        handler,
                        meth,
                        self._wrap_handler(meth, path, handler_, is_method=True),
                    )
        else:
            if method == hdrs.METH_ANY:
                for meth in (
                    hdrs.METH_GET,
                    hdrs.METH_POST,
                    hdrs.METH_PUT,
                    hdrs.METH_PATCH,
                    hdrs.METH_DELETE,
                ):
                    meth = meth.lower()
                    handler = self._wrap_handler(meth, path, handler, is_method=False)
            else:
                handler = self._wrap_handler(
                    method.lower(), path, handler, is_method=False
                )

        return self._app.router.add_route(
            method, path, handler, name=name, expect_handler=expect_handler
        )
