from typing import Dict, List, Optional, Union

from aiohttp import web

from aiohttp_swagger3 import SwaggerDocs

from .helpers import error_to_json


async def test_minimum_maximum(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")

    async def handler(
        request,
        path_int: int,
        path_float: float,
        query_int: int,
        query_float: float,
        body: Dict,
    ):
        """
        ---
        parameters:

          - name: query_int
            in: query
            required: true
            schema:
              type: integer
              minimum: 10
              maximum: 20

          - name: query_float
            in: query
            required: true
            schema:
              type: number
              minimum: 10.1
              maximum: 19.9

          - name: path_int
            in: path
            required: true
            schema:
              type: integer
              minimum: 10
              maximum: 20

          - name: path_float
            in: path
            required: true
            schema:
              type: number
              minimum: 10.1
              maximum: 19.9

        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                required:
                  - int
                  - float
                properties:
                  int:
                    type: integer
                    minimum: 10
                    maximum: 20
                  float:
                    type: number
                    minimum: 10.1
                    maximum: 19.9

        responses:
          '200':
            description: OK.

        """
        return web.json_response(
            {
                "query_int": query_int,
                "query_float": query_float,
                "path_int": path_int,
                "path_float": path_float,
                "body": body,
            }
        )

    s.add_route("POST", "/r/{path_int}/{path_float}", handler)

    client = await aiohttp_client(app)

    int_param = 15
    float_param = 15.5
    body = {"int": int_param, "float": float_param}
    params = {"query_int": int_param, "query_float": str(float_param)}
    resp = await client.post(f"/r/{int_param}/{float_param}", params=params, json=body)
    assert resp.status == 200
    assert await resp.json() == {
        "query_int": int_param,
        "query_float": float_param,
        "path_int": int_param,
        "path_float": float_param,
        "body": body,
    }

    int_param = 10
    float_param = 10.1
    body = {"int": int_param, "float": float_param}
    params = {"query_int": int_param, "query_float": str(float_param)}
    resp = await client.post(f"/r/{int_param}/{float_param}", params=params, json=body)
    assert resp.status == 200
    assert await resp.json() == {
        "query_int": int_param,
        "query_float": float_param,
        "path_int": int_param,
        "path_float": float_param,
        "body": body,
    }

    int_param = 20
    float_param = 19.9
    body = {"int": int_param, "float": float_param}
    params = {"query_int": int_param, "query_float": str(float_param)}
    resp = await client.post(f"/r/{int_param}/{float_param}", params=params, json=body)
    assert resp.status == 200
    assert await resp.json() == {
        "query_int": int_param,
        "query_float": float_param,
        "path_int": int_param,
        "path_float": float_param,
        "body": body,
    }

    int_param = 5
    float_param = 5.5
    body = {"int": int_param, "float": float_param}
    params = {"query_int": int_param, "query_float": str(float_param)}
    resp = await client.post(f"/r/{int_param}/{float_param}", params=params, json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    msg_int = "value should be more than or equal to 10"
    msg_float = "value should be more than or equal to 10.1"
    assert error == {
        "query_int": msg_int,
        "query_float": msg_float,
        "body": {"int": msg_int, "float": msg_float},
        "path_int": msg_int,
        "path_float": msg_float,
    }

    int_param = 25
    float_param = 25.5
    body = {"int": int_param, "float": float_param}
    params = {"query_int": int_param, "query_float": str(float_param)}
    resp = await client.post(f"/r/{int_param}/{float_param}", params=params, json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    msg_int = "value should be less than or equal to 20"
    msg_float = "value should be less than or equal to 19.9"
    assert error == {
        "query_int": msg_int,
        "query_float": msg_float,
        "body": {"int": msg_int, "float": msg_float},
        "path_int": msg_int,
        "path_float": msg_float,
    }


async def test_exclusive_minimum_maximum(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")

    async def handler(
        request,
        path_int: int,
        path_float: float,
        query_int: int,
        query_float: float,
        body: Dict,
    ):
        """
        ---
        parameters:

          - name: query_int
            in: query
            required: true
            schema:
              type: integer
              minimum: 10
              maximum: 20
              exclusiveMinimum: true
              exclusiveMaximum: true

          - name: query_float
            in: query
            required: true
            schema:
              type: number
              minimum: 10.1
              maximum: 19.9
              exclusiveMinimum: true
              exclusiveMaximum: true

          - name: path_int
            in: path
            required: true
            schema:
              type: integer
              minimum: 10
              maximum: 20
              exclusiveMinimum: true
              exclusiveMaximum: true

          - name: path_float
            in: path
            required: true
            schema:
              type: number
              minimum: 10.1
              maximum: 19.9
              exclusiveMinimum: true
              exclusiveMaximum: true

        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                required:
                  - int
                  - float
                properties:
                  int:
                    type: integer
                    minimum: 10
                    maximum: 20
                    exclusiveMinimum: true
                    exclusiveMaximum: true
                  float:
                    type: number
                    minimum: 10.1
                    maximum: 19.9
                    exclusiveMinimum: true
                    exclusiveMaximum: true

        responses:
          '200':
            description: OK.

        """
        return web.json_response(
            {
                "query_int": query_int,
                "query_float": query_float,
                "path_int": path_int,
                "path_float": path_float,
                "body": body,
            }
        )

    s.add_route("POST", "/r/{path_int}/{path_float}", handler)

    client = await aiohttp_client(app)

    int_param = 10
    float_param = 10.1
    body = {"int": int_param, "float": float_param}
    params = {"query_int": int_param, "query_float": str(float_param)}
    resp = await client.post(f"/r/{int_param}/{float_param}", params=params, json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    msg_int = "value should be more than 10"
    msg_float = "value should be more than 10.1"
    assert error == {
        "query_int": msg_int,
        "query_float": msg_float,
        "body": {"int": msg_int, "float": msg_float},
        "path_int": msg_int,
        "path_float": msg_float,
    }

    int_param = 20
    float_param = 19.9
    body = {"int": int_param, "float": float_param}
    params = {"query_int": int_param, "query_float": str(float_param)}
    resp = await client.post(f"/r/{int_param}/{float_param}", params=params, json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    msg_int = "value should be less than 20"
    msg_float = "value should be less than 19.9"
    assert error == {
        "query_int": msg_int,
        "query_float": msg_float,
        "body": {"int": msg_int, "float": msg_float},
        "path_int": msg_int,
        "path_float": msg_float,
    }


async def test_int32_bounds(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")

    async def handler(request, path: int, query: int, body: Dict):
        """
        ---
        parameters:

          - name: query
            in: query
            required: true
            schema:
              type: integer
              format: int32

          - name: path
            in: path
            required: true
            schema:
              type: integer
              format: int32

        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                required:
                  - int
                properties:
                  int:
                    type: integer
                    format: int32

        responses:
          '200':
            description: OK.

        """
        return web.json_response({"query": query, "path": path, "body": body})

    s.add_route("POST", "/r/{path}", handler)

    client = await aiohttp_client(app)

    body_param = -2_147_483_649
    body = {"int": body_param}
    query_param = -2_147_483_649
    params = {"query": query_param}
    path_param = -2_147_483_649
    resp = await client.post(f"/r/{path_param}", params=params, json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    msg = "value out of bounds int32"
    assert error == {"query": msg, "body": {"int": msg}, "path": msg}

    body_param = 2_147_483_648
    body = {"int": body_param}
    query_param = 2_147_483_648
    params = {"query": query_param}
    path_param = 2_147_483_648
    resp = await client.post(f"/r/{path_param}", params=params, json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    msg = "value out of bounds int32"
    assert error == {"query": msg, "body": {"int": msg}, "path": msg}


async def test_min_max_length(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")

    async def handler(request, header: str, path: str, query: str, body: Dict):
        """
        ---
        parameters:

          - name: header
            in: header
            required: true
            schema:
              type: string
              minLength: 5
              maxLength: 10

          - name: query
            in: query
            required: true
            schema:
              type: string
              minLength: 5
              maxLength: 10

          - name: path
            in: path
            required: true
            schema:
              type: string
              minLength: 5
              maxLength: 10

        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                required:
                  - str
                properties:
                  str:
                    type: string
                    minLength: 5
                    maxLength: 10

        responses:
          '200':
            description: OK.

        """
        return web.json_response(
            {"header": header, "query": query, "path": path, "body": body}
        )

    s.add_route("POST", "/r/{path}", handler)

    client = await aiohttp_client(app)

    header_param = "string"
    headers = {"header": header_param}
    body_param = "string"
    body = {"str": body_param}
    query_param = "string"
    params = {"query": query_param}
    path_param = "string"
    resp = await client.post(
        f"/r/{path_param}", headers=headers, params=params, json=body
    )
    assert resp.status == 200
    assert await resp.json() == {
        "header": header_param,
        "query": query_param,
        "path": path_param,
        "body": body,
    }

    header_param = "str"
    headers = {"header": header_param}
    body_param = "str"
    body = {"str": body_param}
    query_param = "str"
    params = {"query": query_param}
    path_param = "str"
    resp = await client.post(
        f"/r/{path_param}", headers=headers, params=params, json=body
    )
    assert resp.status == 400
    error = error_to_json(await resp.text())
    msg = "value length should be more than 5"
    assert error == {"query": msg, "body": {"str": msg}, "header": msg, "path": msg}

    header_param = "long_string"
    headers = {"header": header_param}
    body_param = "long_string"
    body = {"str": body_param}
    query_param = "long_string"
    params = {"query": query_param}
    path_param = "long_string"
    resp = await client.post(
        f"/r/{path_param}", headers=headers, params=params, json=body
    )
    assert resp.status == 400
    error = error_to_json(await resp.text())
    msg = "value length should be less than 10"
    assert error == {"query": msg, "body": {"str": msg}, "header": msg, "path": msg}


async def test_one_of_basic(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")

    async def handler(request, int_or_bool: Union[int, bool], body: Dict):
        """
        ---
        parameters:

          - name: int_or_bool
            in: query
            required: true
            schema:
              oneOf:
                - type: integer
                - type: boolean

        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                required:
                  - int_or_bool
                properties:
                  int_or_bool:
                    oneOf:
                      - type: integer
                      - type: boolean

        responses:
          '200':
            description: OK.

        """
        return web.json_response({"int_or_bool": int_or_bool, "body": body})

    s.add_route("POST", "/r", handler)

    client = await aiohttp_client(app)
    params = {"int_or_bool": 10}
    body = {"int_or_bool": True}
    resp = await client.post("/r", params=params, json=body)
    assert resp.status == 200
    assert await resp.json() == {"int_or_bool": 10, "body": body}

    params = {"int_or_bool": "true"}
    body = {"int_or_bool": 10}
    resp = await client.post("/r", params=params, json=body)
    assert resp.status == 200
    assert await resp.json() == {"int_or_bool": True, "body": body}

    params = {"int_or_bool": "abc"}
    body = {"int_or_bool": "bca"}
    resp = await client.post("/r", params=params, json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {
        "int_or_bool": "fail to validate oneOf",
        "body": {"int_or_bool": "fail to validate oneOf"},
    }


async def test_default(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")

    async def handler(
        request, integer: int, number: float, string: str, boolean: bool, body: Dict
    ):
        """
        ---
        parameters:

          - name: integer
            in: query
            schema:
              type: integer
              default: 15

          - name: number
            in: query
            schema:
              type: number
              default: 15.5

          - name: string
            in: query
            schema:
              type: string
              default: string

          - name: boolean
            in: query
            schema:
              type: boolean
              default: True

        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  integer:
                    type: integer
                    default: 15
                  number:
                    type: number
                    default: 15.5
                  string:
                    type: string
                    default: string
                  boolean:
                    type: boolean
                    default: true

        responses:
          '200':
            description: OK.

        """
        return web.json_response(
            {
                "integer": integer,
                "number": number,
                "string": string,
                "boolean": boolean,
                "body": body,
            }
        )

    s.add_route("POST", "/r", handler)

    client = await aiohttp_client(app)
    resp = await client.post("/r", json={})
    assert resp.status == 200
    assert await resp.json() == {
        "integer": 15,
        "number": 15.5,
        "string": "string",
        "boolean": True,
        "body": {"integer": 15, "number": 15.5, "string": "string", "boolean": True},
    }


async def test_optional(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")

    async def handler(
        request,
        body: Dict,
        integer: Optional[int] = None,
        number: Optional[float] = None,
        string: Optional[str] = None,
        boolean: Optional[bool] = None,
    ):
        """
        ---
        parameters:

          - name: integer
            in: query
            schema:
              type: integer

          - name: number
            in: query
            schema:
              type: number

          - name: string
            in: query
            schema:
              type: string

          - name: boolean
            in: query
            schema:
              type: boolean

        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  integer:
                    type: integer
                  number:
                    type: number
                  string:
                    type: string
                  boolean:
                    type: boolean

        responses:
          '200':
            description: OK.

        """
        resp = {"body": body}
        if integer is not None:
            resp["integer"] = integer
        if number is not None:
            resp["number"] = number
        if string is not None:
            resp["string"] = string
        if boolean is not None:
            resp["boolean"] = boolean

        return web.json_response(resp)

    s.add_route("POST", "/r", handler)

    client = await aiohttp_client(app)
    resp = await client.post("/r", json={})
    assert resp.status == 200
    assert await resp.json() == {"body": {}}

    params = {
        "integer": 15,
        "number": str(15.5),
        "string": "string",
        "boolean": str(True).lower(),
    }
    body = {"integer": 15, "number": 15.5, "string": "string", "boolean": True}

    resp = await client.post("/r", params=params, json=body)
    assert resp.status == 200
    assert await resp.json() == {
        "integer": 15,
        "number": 15.5,
        "string": "string",
        "boolean": True,
        "body": {"integer": 15, "number": 15.5, "string": "string", "boolean": True},
    }


async def test_min_max_items(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")

    async def handler(request, header: List[int], query: List[int], body: Dict):
        """
        ---
        parameters:

          - name: header
            in: header
            required: true
            schema:
              type: array
              items:
                type: integer
              minItems: 2
              maxItems: 5

          - name: query
            in: query
            required: true
            schema:
              type: array
              items:
                type: integer
              minItems: 2
              maxItems: 5

        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                required:
                  - array
                properties:
                  array:
                    type: array
                    items:
                      type: integer
                    minItems: 2
                    maxItems: 5

        responses:
          '200':
            description: OK.

        """
        return web.json_response({"query": query, "header": header, "body": body})

    s.add_route("POST", "/r", handler)

    client = await aiohttp_client(app)

    header_param = [1, 2, 3]
    headers = {"header": ",".join(str(x) for x in header_param)}
    body_param = [1, 2, 3]
    body = {"array": body_param}
    query_param = [1, 2, 3]
    params = {"query": ",".join(str(x) for x in query_param)}
    resp = await client.post(f"/r", headers=headers, params=params, json=body)
    assert resp.status == 200
    assert await resp.json() == {
        "header": header_param,
        "query": query_param,
        "body": body,
    }

    header_param = [1]
    headers = {"header": ",".join(str(x) for x in header_param)}
    body_param = [1]
    body = {"array": body_param}
    query_param = [1]
    params = {"query": ",".join(str(x) for x in query_param)}
    resp = await client.post(f"/r", headers=headers, params=params, json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    msg = "number or items must be more than 2"
    assert error == {"query": msg, "body": {"array": msg}, "header": msg}

    header_param = [1, 2, 3, 4, 5, 6, 7]
    headers = {"header": ",".join(str(x) for x in header_param)}
    body_param = [1, 2, 3, 4, 5, 6, 7]
    body = {"array": body_param}
    query_param = [1, 2, 3, 4, 5, 6, 7]
    params = {"query": ",".join(str(x) for x in query_param)}
    resp = await client.post(f"/r", headers=headers, params=params, json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    msg = "number or items must be less than 5"
    assert error == {"query": msg, "body": {"array": msg}, "header": msg}


async def test_unique_items(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")

    async def handler(request, header: List[int], query: List[int], body: Dict):
        """
        ---
        parameters:

          - name: header
            in: header
            required: true
            schema:
              type: array
              items:
                type: integer
              uniqueItems: true

          - name: query
            in: query
            required: true
            schema:
              type: array
              items:
                type: integer
              uniqueItems: true

        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                required:
                  - array
                properties:
                  array:
                    type: array
                    items:
                      type: integer
                    uniqueItems: true

        responses:
          '200':
            description: OK.

        """
        return web.json_response({"query": query, "header": header, "body": body})

    s.add_route("POST", "/r", handler)

    client = await aiohttp_client(app)

    header_param = [1, 2, 3]
    headers = {"header": ",".join(str(x) for x in header_param)}
    body_param = [1, 2, 3]
    body = {"array": body_param}
    query_param = [1, 2, 3]
    params = {"query": ",".join(str(x) for x in query_param)}
    resp = await client.post(f"/r", headers=headers, params=params, json=body)
    assert resp.status == 200
    assert await resp.json() == {
        "header": header_param,
        "query": query_param,
        "body": body,
    }

    header_param = [1, 1]
    headers = {"header": ",".join(str(x) for x in header_param)}
    body_param = [1, 1]
    body = {"array": body_param}
    query_param = [1, 1]
    params = {"query": ",".join(str(x) for x in query_param)}
    resp = await client.post(f"/r", headers=headers, params=params, json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    msg = "all items must be unique"
    assert error == {"query": msg, "body": {"array": msg}, "header": msg}
