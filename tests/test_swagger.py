import pytest
from aiohttp import hdrs, web

from aiohttp_swagger3 import SwaggerDocs


async def test_swagger_json(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(
        app, "/docs", title="test app", version="2.2.2", description="test description"
    )

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

    s.add_route("GET", "/r/{param_id}", handler)

    client = await aiohttp_client(app)

    resp = await client.get("/docs/swagger.json")
    assert resp.status == 200
    assert await resp.json() == {
        "openapi": "3.0.0",
        "info": {
            "title": "test app",
            "version": "2.2.2",
            "description": "test description",
        },
        "paths": {
            "/r/{param_id}": {
                "get": {
                    "parameters": [
                        {
                            "in": "path",
                            "name": "param_id",
                            "required": True,
                            "schema": {"type": "integer"},
                        }
                    ],
                    "responses": {"200": {"description": "OK."}},
                }
            }
        },
    }


async def test_index_html(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")

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

    s.add_route("GET", "/r/{param_id}", handler)

    client = await aiohttp_client(app)

    resp = await client.get("/docs/")
    assert resp.status == 200


async def test_redirect(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")

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

    s.add_route("GET", "/r/{param_id}", handler)

    client = await aiohttp_client(app)

    resp = await client.get("/docs", allow_redirects=False)
    assert resp.status == 301
    assert "/docs/" == resp.headers.get(hdrs.LOCATION) or resp.headers.get(hdrs.URI)


async def test_incorrect_ui_path(loop):
    app = web.Application(loop=loop)
    with pytest.raises(Exception) as exc_info:
        SwaggerDocs(app, "docs")
    assert str(exc_info.value) == "ui_path should start with /"


async def test_swagger_json_renders_datetime(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(
        app, "/docs", title="test app", version="2.2.2", description="test description"
    )

    async def handler(request):
        """
        ---
        parameters:

          - name: date
            in: query
            schema:
              type: string
              format: date
              example: 2019-01-01

        responses:
          '200':
            description: OK.

        """
        return web.json_response()

    s.add_route("GET", "/r", handler)

    client = await aiohttp_client(app)

    resp = await client.get("/docs/swagger.json")
    assert resp.status == 200


async def test_no_swagger(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")

    async def handler(request):
        return web.json_response()

    s.add_route("GET", "/r", handler)

    client = await aiohttp_client(app)

    resp = await client.get("/docs/swagger.json")
    assert resp.status == 200


async def test_bind_swagger_to_root(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/")

    async def handler(request):
        """
        ---

        responses:
          '200':
            description: OK.

        """
        return web.json_response()

    s.add_route("GET", "/r", handler)

    client = await aiohttp_client(app)

    resp = await client.get("/")
    assert resp.status == 200

    resp = await client.get("/swagger.json")
    assert resp.status == 200

    resp = await client.get("/r")
    assert resp.status == 200
