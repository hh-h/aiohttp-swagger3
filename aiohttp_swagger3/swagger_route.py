from typing import Any, Callable, Dict, List

from aiohttp import web

from .parameter import Parameter
from .swagger import Swagger
from .validators import MISSING, ValidatorError, schema_to_validator


class SwaggerRoute:
    def __init__(
        self,
        method: str,
        path: str,
        handler: Callable,
        *,
        swagger: Swagger,
        **kwargs: Any
    ) -> None:
        self.method = method
        self.path = path
        self.handler = handler
        self.kwargs = kwargs
        self.qp: List[Parameter] = []
        self.pp: List[Parameter] = []
        self.hp: List[Parameter] = []
        self.bp: Dict[str, Parameter] = {}
        self._swagger = swagger
        parameters = self._swagger.spec["paths"][path][method].get("parameters")
        body = self._swagger.spec["paths"][path][method].get("requestBody")
        components = self._swagger.spec.get("components", {})
        if parameters is not None:
            for param in parameters:
                if "$ref" in param:
                    if not components:
                        raise Exception("file with components definitions is missing")
                    # '#/components/parameters/Month'
                    *_, section, obj = param["$ref"].split("/")
                    param = components[section][obj]
                parameter = Parameter(
                    param["name"],
                    schema_to_validator(param["schema"], components),
                    param.get("required", False),
                )
                if param["in"] == "query":
                    self.qp.append(parameter)
                elif param["in"] == "path":
                    self.pp.append(parameter)
                elif param["in"] == "header":
                    self.hp.append(parameter)

        if body is not None:
            for media_type, value in body["content"].items():
                # check that we have handler for media_type
                self._swagger.get_media_type_handler(media_type)
                value = body["content"][media_type]
                self.bp[media_type] = Parameter(
                    "body",
                    schema_to_validator(value["schema"], components),
                    body.get("required", False),
                )
        self.params = handler.__code__.co_varnames

    async def parse(self, request: web.Request) -> Dict:
        params = {"request": request}
        request["data"] = {}
        # query parameters
        errors: Dict = {}
        if self.qp:
            for param in self.qp:
                if param.required:
                    try:
                        v = request.rel_url.query.getall(param.name)
                    except KeyError:
                        errors[param.name] = "is required"
                        continue
                    if len(v) == 1:
                        v = v[0]
                else:
                    v = request.rel_url.query.getall(param.name, MISSING)
                    if v != MISSING and len(v) == 1:
                        v = v[0]
                try:
                    value = param.validator.validate(v, True)
                except ValidatorError as e:
                    errors[param.name] = e.error
                    continue
                if value != MISSING:
                    request["data"][param.name] = value
                    if param.name in self.params:
                        params[param.name] = value
        # body parameters
        if self.bp:
            media_type = request.headers["Content-Type"]
            if media_type not in self.bp:
                raise Exception("no content-type handler")
            handler = self._swagger.get_media_type_handler(media_type)
            param = self.bp[media_type]
            try:
                v = await handler(request)
            except ValidatorError as e:
                errors[param.name] = e.error
            else:
                try:
                    # TODO it can be not False
                    value = param.validator.validate(v, False)
                except ValidatorError as e:
                    errors[param.name] = e.error
                else:
                    request["data"][param.name] = value
                    if param.name in self.params:
                        params[param.name] = value
        # header parameters
        if self.hp:
            for param in self.hp:
                if param.required:
                    try:
                        v = request.headers.getone(param.name)
                    except KeyError:
                        errors[param.name] = "is required"
                        continue
                else:
                    v = request.headers.get(param.name, MISSING)
                try:
                    value = param.validator.validate(v, True)
                except ValidatorError as e:
                    errors[param.name] = e.error
                    continue
                if value != MISSING:
                    request["data"][param.name] = value
                    if param.name in self.params:
                        params[param.name] = value
        # path parameters
        if self.pp:
            for param in self.pp:
                v = request.match_info[param.name]
                try:
                    value = param.validator.validate(v, True)
                except ValidatorError as e:
                    errors[param.name] = e.error
                    continue
                request["data"][param.name] = value
                if param.name in self.params:
                    params[param.name] = value
        if errors:
            raise web.HTTPBadRequest(reason=errors)
        return params
