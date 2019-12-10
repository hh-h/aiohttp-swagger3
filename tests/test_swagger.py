import pytest
from aiohttp import hdrs, web

from aiohttp_swagger3 import SwaggerDocs, SwaggerFile


async def test_swagger_json(swagger_docs, swagger_ui_settings, aiohttp_client):
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

    swagger = swagger_docs(
        swagger_ui_settings=swagger_ui_settings(),
        title="test app",
        version="2.2.2",
        description="test description",
    )
    swagger.add_route("GET", "/r/{param_id}", handler)

    client = await aiohttp_client(swagger._app)

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


async def test_index_html(swagger_docs, swagger_ui_settings, aiohttp_client):
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

    swagger = swagger_docs(swagger_ui_settings=swagger_ui_settings())
    swagger.add_route("GET", "/r/{param_id}", handler)

    client = await aiohttp_client(swagger._app)

    resp = await client.get("/docs/")
    assert resp.status == 200


async def test_redirect(swagger_docs, swagger_ui_settings, aiohttp_client):
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

    swagger = swagger_docs(swagger_ui_settings=swagger_ui_settings())
    swagger.add_route("GET", "/r/{param_id}", handler)

    client = await aiohttp_client(swagger._app)

    resp = await client.get("/docs", allow_redirects=False)
    assert resp.status == 301
    assert "/docs/" == resp.headers.get(hdrs.LOCATION) or resp.headers.get(hdrs.URI)


async def test_incorrect_ui_path(swagger_docs, swagger_ui_settings):
    with pytest.raises(Exception) as exc_info:
        swagger_docs(swagger_ui_settings=swagger_ui_settings(path="docs"))
    assert str(exc_info.value) == "path should start with /"


async def test_swagger_json_renders_datetime(
    swagger_docs, swagger_ui_settings, aiohttp_client
):
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

    swagger = swagger_docs(swagger_ui_settings=swagger_ui_settings())
    swagger.add_route("GET", "/r", handler)

    client = await aiohttp_client(swagger._app)

    resp = await client.get("/docs/swagger.json")
    assert resp.status == 200


async def test_no_swagger_routes(swagger_docs, swagger_ui_settings, aiohttp_client):
    async def handler(request):
        return web.json_response()

    swagger = swagger_docs(swagger_ui_settings=swagger_ui_settings())
    swagger.add_route("GET", "/r", handler)

    client = await aiohttp_client(swagger._app)

    resp = await client.get("/docs/swagger.json")
    assert resp.status == 200


async def test_bind_swagger_to_root(swagger_docs, swagger_ui_settings, aiohttp_client):
    async def handler(request):
        """
        ---

        responses:
          '200':
            description: OK.

        """
        return web.json_response()

    swagger = swagger_docs(swagger_ui_settings=swagger_ui_settings(path="/"))
    swagger.add_route("GET", "/r", handler)

    client = await aiohttp_client(swagger._app)

    resp = await client.get("/")
    assert resp.status == 200

    resp = await client.get("/swagger.json")
    assert resp.status == 200

    resp = await client.get("/r")
    assert resp.status == 200


async def test_no_ui(swagger_docs, aiohttp_client):
    swagger = swagger_docs()

    client = await aiohttp_client(swagger._app)
    resp = await client.get("/docs")
    assert resp.status == 404


async def test_both_paths(swagger_ui_settings, aiohttp_client):
    app = web.Application()
    swagger = SwaggerDocs(
        app, "/docs1", swagger_ui_settings=swagger_ui_settings(path="/docs2")
    )

    client = await aiohttp_client(swagger._app)

    resp = await client.get("/docs1/")
    assert resp.status == 404

    resp = await client.get("/docs2/")
    assert resp.status == 200


async def test_deprecated_ui_path():
    app = web.Application()
    with pytest.warns(
        FutureWarning,
        match="ui_path is deprecated and will be removed in 0.4.0, use swagger_ui_settings instead.",
    ):
        SwaggerDocs(app, "/docs")

    with pytest.warns(
        FutureWarning,
        match="ui_path is deprecated and will be removed in 0.4.0, use swagger_ui_settings instead.",
    ):
        SwaggerFile(app, "/docs", "tests/testdata/petstore.yaml")


async def test_swagger_file_no_spec():
    app = web.Application()
    with pytest.raises(Exception) as exc_info:
        SwaggerFile(app)
    assert str(exc_info.value) == "spec file with swagger schema must be provided"
