from typing import Dict

from aiohttp import web

from .helpers import error_to_json


async def test_object_read_only_properties_skipped(swagger_docs, aiohttp_client):
    routes = web.RouteTableDef()

    @routes.post("/r")
    async def handler(request, body: Dict):
        """
        ---
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  boolean:
                    type: boolean
                    readOnly: true
                  integer:
                    type: integer
                    readOnly: true
                  number:
                    type: number
                    readOnly: true
                  string:
                    type: string
                    readOnly: true
                  array:
                    type: array
                    items:
                      type: string
                    readOnly: true
                  object:
                    type: object
                    readOnly: true

        responses:
          '200':
            description: OK.
        """
        return web.json_response(body)

    swagger = swagger_docs()
    swagger.add_routes(routes)

    client = await aiohttp_client(swagger._app)

    resp = await client.post("/r", json={})
    assert resp.status == 200
    assert await resp.json() == {}


async def test_object_read_only_properties_passed(swagger_docs, aiohttp_client):
    routes = web.RouteTableDef()

    @routes.post("/r")
    async def handler(request, body: Dict):
        """
        ---
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  boolean:
                    type: boolean
                    readOnly: true
                  integer:
                    type: integer
                    readOnly: true
                  number:
                    type: number
                    readOnly: true
                  string:
                    type: string
                    readOnly: true
                  array:
                    type: array
                    items:
                      type: string
                    readOnly: true
                  object:
                    type: object
                    readOnly: true

        responses:
          '200':
            description: OK.
        """
        return web.json_response(body)

    swagger = swagger_docs()
    swagger.add_routes(routes)

    client = await aiohttp_client(swagger._app)

    resp = await client.post(
        "/r",
        json={
            "boolean": True,
            "integer": 10,
            "number": 1.1,
            "string": "str",
            "array": [1, 2, 3],
            "object": {"some": "thing"},
        },
    )
    assert resp.status == 400
    error = error_to_json(await resp.text())
    msg = "property is read-only"
    assert error == {
        "body": {
            "boolean": msg,
            "integer": msg,
            "number": msg,
            "string": msg,
            "array": msg,
            "object": msg,
        }
    }


async def test_object_required_read_only_properties(swagger_docs, aiohttp_client):
    routes = web.RouteTableDef()

    @routes.post("/r")
    async def handler(request, body: Dict):
        """
        ---
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                required:
                  - id
                  - name
                  - description
                  - updated_at
                properties:
                  id:
                    type: integer
                    readOnly: true
                  name:
                    type: string
                  description:
                    type: string
                  updated_at:
                    type: integer
                    readOnly: true

        responses:
          '200':
            description: OK.
        """
        return web.json_response(body)

    swagger = swagger_docs()
    swagger.add_routes(routes)

    client = await aiohttp_client(swagger._app)

    body = {
        "name": "name1",
        "description": "description",
    }
    resp = await client.post("/r", json=body)
    assert resp.status == 200
    assert await resp.json() == body

    resp = await client.post(
        "/r",
        json={
            "id": 1,
            "name": "name1",
            "description": "description",
            "updated_at": 1609407277,
        },
    )
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {
        "body": {
            "id": "property is read-only",
            "updated_at": "property is read-only",
        }
    }


async def test_ignore_read_only(swagger_docs, aiohttp_client):
    async def handler(request, param_id: int, q: int):
        """
        ---
        parameters:

          - name: param_id
            in: path
            required: true
            schema:
              type: integer
              readOnly: true

          - name: q
            in: query
            required: true
            schema:
              type: integer
              readOnly: true

        responses:
          '200':
            description: OK.

        """
        return web.json_response({"param_id": param_id, "q": q})

    swagger = swagger_docs()
    swagger.add_route("GET", "/r/{param_id}", handler)

    client = await aiohttp_client(swagger._app)

    params = {
        "q": 15,
    }
    resp = await client.get("/r/10", params=params)
    assert resp.status == 200
    assert await resp.json() == {"param_id": 10, "q": 15}
