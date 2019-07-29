from aiohttp import web

from aiohttp_swagger3 import SwaggerDocs

from .helpers import error_to_json


async def test_header(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")

    async def handler(request):
        """
        ---
        parameters:

          - name: x-request-id
            in: header
            required: true
            schema:
              type: string

        responses:
          '200':
            description: OK.

        """
        return web.json_response({"x-request-id": request["data"]["x-request-id"]})

    s.add_route("GET", "/r", handler)

    client = await aiohttp_client(app)

    headers = {"x-request-id": "some_request_id"}
    resp = await client.get("/r", headers=headers)
    assert resp.status == 200
    assert await resp.json() == headers


async def test_header_always_lower_case(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")

    async def handler(request):
        """
        ---
        parameters:

          - name: X-REQUEST-ID
            in: header
            required: true
            schema:
              type: string

        responses:
          '200':
            description: OK.

        """
        assert "X-REQUEST-ID" not in request["data"]
        return web.json_response({"x-request-id": request["data"]["x-request-id"]})

    s.add_route("GET", "/r", handler)

    client = await aiohttp_client(app)

    header_name = "X-REQUEST-ID"
    header_value = "some_request_id"
    headers = {header_name: header_value}
    resp = await client.get("/r", headers=headers)
    assert resp.status == 200
    assert await resp.json() == {header_name.lower(): header_value}


async def test_missing_header_parameter(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")

    async def handler(request):
        """
        ---
        parameters:

          - name: variable
            in: header
            required: true
            schema:
              type: integer

        responses:
          '200':
            description: OK.

        """
        return web.json_response()

    s.add_route("GET", "/r", handler)

    client = await aiohttp_client(app)
    resp = await client.get("/r")
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"variable": "is required"}


async def test_optional_header(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")

    async def handler(request):
        """
        ---
        parameters:

          - name: X-USER-ID
            in: header
            schema:
              type: integer

        responses:
          '200':
            description: OK.

        """
        user_id = request["data"].get("x-user-id", 50)
        return web.json_response({"x-user-id": user_id})

    s.add_route("GET", "/r", handler)

    client = await aiohttp_client(app)

    resp = await client.get("/r")
    assert resp.status == 200
    assert await resp.json() == {"x-user-id": 50}
