from typing import Dict

from aiohttp import web


async def test_ref_parameter(swagger_docs_with_components, aiohttp_client):
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

    swagger = swagger_docs_with_components()
    swagger.add_route("GET", "/r", handler)

    client = await aiohttp_client(swagger._app)

    params = {"month": 5}
    resp = await client.get("/r", params=params)
    assert resp.status == 200
    assert await resp.json() == params


async def test_ref(swagger_docs_with_components, aiohttp_client):
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

    swagger = swagger_docs_with_components()
    swagger.add_route("POST", "/r", handler)

    client = await aiohttp_client(swagger._app)
    body = {"name": "pet", "age": 15}
    resp = await client.post("/r", json=body)
    assert resp.status == 200
    assert await resp.json() == body
