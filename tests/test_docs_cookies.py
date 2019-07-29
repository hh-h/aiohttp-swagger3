from typing import List, Optional

from aiohttp import web

from aiohttp_swagger3 import SwaggerDocs

from .helpers import error_to_json


async def test_cookies(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")

    async def handler(
        request, array: List[int], integer: int, string: str, boolean: bool
    ):
        """
        ---
        parameters:

          - name: array
            in: cookie
            required: true
            schema:
              type: array
              items:
                type: integer

          - name: integer
            in: cookie
            required: true
            schema:
              type: integer

          - name: string
            in: cookie
            required: true
            schema:
              type: string

          - name: boolean
            in: cookie
            required: true
            schema:
              type: boolean

        responses:
          '200':
            description: OK.

        """
        return web.json_response(
            {"array": array, "integer": integer, "string": string, "boolean": boolean}
        )

    s.add_route("POST", "/r", handler)

    client = await aiohttp_client(app)

    c1 = [1, 2, 3, 4, 5]
    c2 = 100
    c3 = "string"
    c4 = False
    cookies = {
        "array": ",".join(str(x) for x in c1),
        "integer": c2,
        "string": c3,
        "boolean": str(c4).lower(),
    }
    resp = await client.post(f"/r", cookies=cookies)
    assert resp.status == 200
    assert await resp.json() == {
        "array": c1,
        "integer": c2,
        "string": c3,
        "boolean": c4,
    }


async def test_missing_cookies(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")

    async def cookie_handler(
        request,
        integer: int,
        array: Optional[List[int]] = None,
        string: Optional[str] = None,
        boolean: bool = True,
    ):
        """
        ---
        parameters:

          - name: array
            in: cookie
            schema:
              type: array
              items:
                type: integer

          - name: integer
            in: cookie
            schema:
              type: integer
              default: 200

          - name: string
            in: cookie
            schema:
              type: string

          - name: boolean
            in: cookie
            schema:
              type: boolean

        responses:
          '200':
            description: OK.

        """
        return web.json_response(
            {"array": array, "integer": integer, "string": string, "boolean": boolean}
        )

    s.add_route("POST", "/r", cookie_handler)

    client = await aiohttp_client(app)

    resp = await client.post(f"/r")
    assert resp.status == 200
    assert await resp.json() == {
        "array": None,
        "integer": 200,
        "string": None,
        "boolean": True,
    }


async def test_missing_cookie_parameter(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")

    async def handler(request):
        """
        ---
        parameters:

          - name: variable
            in: cookie
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


async def test_fail_validation(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")

    async def handler(request, int32: int):
        """
        ---
        parameters:

          - name: int32
            in: cookie
            required: true
            schema:
              type: integer
              format: int32

        responses:
          '200':
            description: OK.

        """
        return web.json_response({"int32": int32})

    s.add_route("POST", "/r", handler)

    client = await aiohttp_client(app)

    cookies = {"int32": "abc"}
    resp = await client.post(f"/r", cookies=cookies)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"int32": "value should be type of int"}
