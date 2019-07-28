from typing import Dict

from aiohttp import web

from aiohttp_swagger3 import SwaggerDocs


async def test_ref_parameter(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs", components="tests/testdata/components.yaml")

    async def handler(request, month: int):
        """
        ---
        parameters:

          - $ref: '#/components/parameters/Month'

        responses:
          '200':
            description: OK.

        """
        return web.json_response({"month": month})

    s.add_route("GET", "/r", handler)

    client = await aiohttp_client(app)

    params = {"month": 5}
    resp = await client.get("/r", params=params)
    assert resp.status == 200
    assert await resp.json() == params


async def test_ref(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs", components="tests/testdata/components.yaml")

    async def handler(request, body: Dict):
        """
        ---
        requestBody:
          required: true
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Pet'

        responses:
          '200':
            description: OK.

        """
        return web.json_response(body)

    s.add_route("POST", "/r", handler)

    client = await aiohttp_client(app)
    body = {"name": "pet", "age": 15}
    resp = await client.post("/r", json=body)
    assert resp.status == 200
    assert await resp.json() == body
