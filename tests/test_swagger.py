import itertools

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
                            "style": "simple",
                            "explode": False,
                        }
                    ],
                    "responses": {"200": {"description": "OK."}},
                }
            }
        },
    }


async def test_swagger_ui_index_html(swagger_docs, swagger_ui_settings, aiohttp_client):
    swagger = swagger_docs(swagger_ui_settings=swagger_ui_settings())

    client = await aiohttp_client(swagger._app)

    resp = await client.get("/docs/")
    assert resp.status == 200


async def test_redoc_ui_index_html(swagger_docs, redoc_ui_settings, aiohttp_client):
    swagger = swagger_docs(redoc_ui_settings=redoc_ui_settings())

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


async def test_incorrect_swagger_ui_path(swagger_docs, swagger_ui_settings):
    with pytest.raises(Exception) as exc_info:
        swagger_docs(swagger_ui_settings=swagger_ui_settings(path="docs"))
    assert str(exc_info.value) == "path should start with /"


async def test_incorrect_redoc_ui_path(swagger_docs, redoc_ui_settings):
    with pytest.raises(Exception) as exc_info:
        swagger_docs(redoc_ui_settings=redoc_ui_settings(path="docs"))
    assert str(exc_info.value) == "path should start with /"


async def test_incorrect_rapidoc_ui_path(swagger_docs, rapidoc_ui_settings):
    with pytest.raises(Exception) as exc_info:
        swagger_docs(rapidoc_ui_settings=rapidoc_ui_settings(path="docs"))
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


async def test_two_uis_one_path(
    swagger_ui_settings, redoc_ui_settings, rapidoc_ui_settings
):
    app = web.Application()
    with pytest.raises(Exception) as exc_info:
        SwaggerDocs(
            app,
            swagger_ui_settings=swagger_ui_settings(),
            redoc_ui_settings=redoc_ui_settings(),
        )
    assert str(exc_info.value) == "cannot bind two UIs on the same path"

    with pytest.raises(Exception) as exc_info:
        SwaggerDocs(
            app,
            swagger_ui_settings=swagger_ui_settings(),
            rapidoc_ui_settings=rapidoc_ui_settings(),
        )
    assert str(exc_info.value) == "cannot bind two UIs on the same path"

    with pytest.raises(Exception) as exc_info:
        SwaggerDocs(
            app,
            rapidoc_ui_settings=rapidoc_ui_settings(),
            redoc_ui_settings=redoc_ui_settings(),
        )
    assert str(exc_info.value) == "cannot bind two UIs on the same path"


async def test_all_uis(
    swagger_docs,
    swagger_ui_settings,
    redoc_ui_settings,
    rapidoc_ui_settings,
    aiohttp_client,
):
    swagger = swagger_docs(
        swagger_ui_settings=swagger_ui_settings(path="/swagger"),
        redoc_ui_settings=redoc_ui_settings(path="/redoc"),
        rapidoc_ui_settings=rapidoc_ui_settings(path="/rapidoc"),
    )

    client = await aiohttp_client(swagger._app)

    resp = await client.get("/swagger/")
    assert resp.status == 200

    resp = await client.get("/redoc/")
    assert resp.status == 200

    resp = await client.get("/rapidoc/")
    assert resp.status == 200


async def test_redoc_ui_expand_responses_validator(swagger_docs, redoc_ui_settings):
    swagger_docs(redoc_ui_settings=redoc_ui_settings(expandResponses="all"))
    swagger_docs(redoc_ui_settings=redoc_ui_settings(expandResponses=""))
    swagger_docs(redoc_ui_settings=redoc_ui_settings(expandResponses="200"))
    swagger_docs(redoc_ui_settings=redoc_ui_settings(expandResponses="200,300"))

    with pytest.raises(Exception) as exc_info:
        swagger_docs(redoc_ui_settings=redoc_ui_settings(expandResponses="abc"))
    assert (
        str(exc_info.value)
        == "expandResponses must be either 'all' or comma-separated list of http codes, got 'abc'"
    )

    with pytest.raises(Exception) as exc_info:
        swagger_docs(redoc_ui_settings=redoc_ui_settings(expandResponses="100,bca"))
    assert (
        str(exc_info.value)
        == "expandResponses must be either 'all' or comma-separated list of http codes, got 'bca'"
    )


async def test_redoc_ui_json_sample_expand_level_validator(
    swagger_docs, redoc_ui_settings
):
    swagger_docs(redoc_ui_settings=redoc_ui_settings(jsonSampleExpandLevel="all"))
    swagger_docs(redoc_ui_settings=redoc_ui_settings(jsonSampleExpandLevel=1))

    with pytest.raises(Exception) as exc_info:
        swagger_docs(redoc_ui_settings=redoc_ui_settings(jsonSampleExpandLevel="abc"))
    assert (
        str(exc_info.value)
        == "jsonSampleExpandLevel must be either 'all' or integer, got 'abc'"
    )

    with pytest.raises(Exception) as exc_info:
        swagger_docs(redoc_ui_settings=redoc_ui_settings(jsonSampleExpandLevel="5"))
    assert (
        str(exc_info.value)
        == "jsonSampleExpandLevel must be either 'all' or integer, got '5'"
    )


async def test_default_serialization(swagger_docs, swagger_ui_settings, aiohttp_client):
    async def handler(request):
        """
        ---
        parameters:

          - name: path_param
            in: path
            required: true
            schema:
              type: integer

          - name: query_param
            in: query
            required: true
            schema:
              type: integer

          - name: header_param
            in: header
            required: true
            schema:
              type: integer

          - name: cookie_param
            in: cookie
            required: true
            schema:
              type: integer

        responses:
          '200':
            description: OK.

        """
        return web.json_response()

    swagger = swagger_docs(swagger_ui_settings=swagger_ui_settings())
    swagger.add_route("GET", "/r/{path_param}", handler)

    client = await aiohttp_client(swagger._app)

    resp = await client.get("/docs/swagger.json")
    assert resp.status == 200
    assert await resp.json() == {
        "openapi": "3.0.0",
        "info": {"title": "OpenAPI3", "version": "1.0.0"},
        "paths": {
            "/r/{path_param}": {
                "get": {
                    "parameters": [
                        {
                            "in": "path",
                            "name": "path_param",
                            "required": True,
                            "schema": {"type": "integer"},
                            "style": "simple",
                            "explode": False,
                        },
                        {
                            "in": "query",
                            "name": "query_param",
                            "required": True,
                            "schema": {"type": "integer"},
                            "style": "form",
                            "explode": True,
                        },
                        {
                            "in": "header",
                            "name": "header_param",
                            "required": True,
                            "schema": {"type": "integer"},
                            "style": "simple",
                            "explode": False,
                        },
                        {
                            "in": "cookie",
                            "name": "cookie_param",
                            "required": True,
                            "schema": {"type": "integer"},
                            "style": "form",
                            "explode": True,
                        },
                    ],
                    "responses": {"200": {"description": "OK."}},
                }
            }
        },
    }


async def test_redoc_ui_static_files(swagger_docs, redoc_ui_settings, aiohttp_client):
    swagger = swagger_docs(redoc_ui_settings=redoc_ui_settings())

    client = await aiohttp_client(swagger._app)

    resp = await client.get("/docs/redoc_ui_static/redoc.standalone.js")
    assert resp.status == 200

    resp = await client.get(
        "/docs/redoc_ui_static/fonts/"
        "montserrat/montserrat-v14-cyrillic-ext_vietnamese_latin-ext_latin_cyrillic-300.woff2"
    )
    assert resp.status == 200

    resp = await client.get(
        "/docs/redoc_ui_static/fonts/"
        "roboto/roboto-v20-greek-ext_cyrillic-ext_vietnamese_latin-ext_latin_greek_cyrillic-300.woff2"
    )
    assert resp.status == 200


async def test_rapidoc_ui_static_files(
    swagger_docs, rapidoc_ui_settings, aiohttp_client
):
    swagger = swagger_docs(rapidoc_ui_settings=rapidoc_ui_settings())

    client = await aiohttp_client(swagger._app)

    resp = await client.get("/docs/rapidoc_ui_static/rapidoc-min.js")
    assert resp.status == 200

    resp = await client.get("/docs/rapidoc_ui_static/rapidoc-regular.woff2")
    assert resp.status == 200

    resp = await client.get("/docs/rapidoc_ui_static/roboto-mono-bold.woff2")
    assert resp.status == 200


@pytest.mark.parametrize(
    ("field", "value"),
    list(
        itertools.product(
            (
                "bg_color",
                "text_color",
                "nav_bg_color",
                "nav_text_color",
                "nav_hover_bg_color",
                "nav_hover_text_color",
                "nav_accent_color",
            ),
            ("#test", "asdlkalsdk", "#12", "#AAAAAAA", "#fffff"),
        ),
    ),
)
async def test_rapidoc_ui_hex_color_validator_invalid(
    field, value, rapidoc_ui_settings
):
    with pytest.raises(Exception) as exc_info:
        rapidoc_ui_settings(**{field: value})
    assert str(exc_info.value) == f"{field} must be valid HEX color"


@pytest.mark.parametrize(
    ("field", "value"),
    list(
        itertools.product(
            (
                "bg_color",
                "text_color",
                "nav_bg_color",
                "nav_text_color",
                "nav_hover_bg_color",
                "nav_hover_text_color",
                "nav_accent_color",
            ),
            ("#333", "#AAAA", "#FFFff4", "#bbbbbbbb"),
        ),
    ),
)
async def test_rapidoc_ui_hex_color_validator(field, value, rapidoc_ui_settings):
    rapidoc_ui_settings(**{field: value})


async def test_rapidoc_ui_bg_color_default(rapidoc_ui_settings):
    rus = rapidoc_ui_settings(theme="light")
    assert rus.bg_color == "#fff"

    rus = rapidoc_ui_settings(theme="dark")
    assert rus.bg_color == "#333"


async def test_rapidoc_ui_text_color_default(rapidoc_ui_settings):
    rus = rapidoc_ui_settings(theme="light")
    assert rus.text_color == "#444"

    rus = rapidoc_ui_settings(theme="dark")
    assert rus.text_color == "#bbb"
