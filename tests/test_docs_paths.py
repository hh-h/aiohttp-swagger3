from functools import wraps

import pytest
from aiohttp import web


async def test_decorated_handlers(swagger_docs, aiohttp_client):
    def decorator(fn):
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            return await fn(*args, **kwargs)

        return wrapper

    @decorator
    async def handler(request, param_id: int):
        """
        ---
        parameters:

          - name: param_id
            in: path
            required: true
            schema:
              type: integer

        responses:
          '200':
            description: OK.

        """
        return web.json_response({"param_id": param_id})

    swagger = swagger_docs()
    swagger.add_route("GET", "/r/{param_id}", handler)

    client = await aiohttp_client(swagger._app)

    resp = await client.get("/r/10")
    assert resp.status == 200
    assert await resp.json() == {"param_id": 10}


async def test_path(swagger_docs, aiohttp_client):
    async def handler(request, param_id: int):
        """
        ---
        parameters:

          - name: param_id
            in: path
            required: true
            schema:
              type: integer

        responses:
          '200':
            description: OK.

        """
        return web.json_response({"param_id": param_id})

    swagger = swagger_docs()
    swagger.add_route("GET", "/r/{param_id}", handler)

    client = await aiohttp_client(swagger._app)

    resp = await client.get("/r/10")
    assert resp.status == 200
    assert await resp.json() == {"param_id": 10}


async def test_already_exists_path(swagger_docs, aiohttp_client):
    async def handler(request, param_id: int):
        """
        ---
        parameters:

          - name: param_id
            in: path
            required: true
            schema:
              type: integer

        responses:
          '200':
            description: OK.

        """
        return web.json_response({"param_id": param_id})

    swagger = swagger_docs()
    swagger.add_route("GET", r"/r/{param_id:\d+}", handler)

    with pytest.raises(Exception) as exc_info:
        swagger.add_route("GET", r"/r/{param_id:\w+}", handler)
    assert "get /r/{param_id} already exists" == str(exc_info.value)


async def test_path_with_regex(swagger_docs, aiohttp_client):
    async def handler(request, first_param_id: int, second_param_id: int, third_param_id: str):
        """
        ---
        parameters:

          - name: first_param_id
            in: path
            required: true
            schema:
              type: integer

          - name: second_param_id
            in: path
            required: true
            schema:
              type: integer

          - name: third_param_id
            in: path
            required: true
            schema:
              type: string

        responses:
          '200':
            description: OK.

        """
        return web.json_response(
            {"first_param_id": first_param_id, "second_param_id": second_param_id, "third_param_id": third_param_id}
        )

    swagger = swagger_docs()
    swagger.add_route("GET", r"/r/{first_param_id:\d+}/r/{second_param_id:\d+}/{third_param_id:\w{2,10}}", handler)

    client = await aiohttp_client(swagger._app)

    resp = await client.get("/r/10/r/11/abc")
    assert resp.status == 200
    assert await resp.json() == {"first_param_id": 10, "second_param_id": 11, "third_param_id": "abc"}
    assert "/r/{first_param_id}/r/{second_param_id}/{third_param_id}" in swagger.spec["paths"]
