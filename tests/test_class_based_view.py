from typing import Dict, Optional

from aiohttp import web


async def test_class_based_view(swagger_docs, aiohttp_client):
    class View(web.View):
        async def get(self, param_id: int):
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
            assert self.request["data"]["param_id"] == param_id
            return web.json_response({"param_id": param_id})

        async def post(self, param_id: int, body: Dict):
            """
            ---
            parameters:

              - name: param_id
                in: path
                required: true
                schema:
                  type: integer

            requestBody:
              required: true
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      integer:
                        type: integer

            responses:
              '200':
                description: OK.

            """
            return web.json_response({"param_id": param_id, "body": body})

    swagger = swagger_docs()
    swagger.add_routes([web.view("/r/{param_id}", View)])

    client = await aiohttp_client(swagger._app)

    resp = await client.get("/r/10")
    assert resp.status == 200
    assert await resp.json() == {"param_id": 10}

    body = {"integer": 20}
    resp = await client.post("/r/20", json=body)
    assert resp.status == 200
    assert await resp.json() == {"param_id": 20, "body": body}


async def test_decorated_class_based_view(swagger_docs, aiohttp_client):
    routes = web.RouteTableDef()

    @routes.view("/r/{param_id}")
    class View(web.View):
        async def get(self, param_id: int):
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

        async def post(self, param_id: int, body: Dict):
            """
            ---
            parameters:

              - name: param_id
                in: path
                required: true
                schema:
                  type: integer

            requestBody:
              required: true
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      integer:
                        type: integer

            responses:
              '200':
                description: OK.

            """
            return web.json_response({"param_id": param_id, "body": body})

    swagger = swagger_docs()
    swagger.add_routes(routes)

    client = await aiohttp_client(swagger._app)

    resp = await client.get("/r/10")
    assert resp.status == 200
    assert await resp.json() == {"param_id": 10}

    body = {"integer": 20}
    resp = await client.post("/r/20", json=body)
    assert resp.status == 200
    assert await resp.json() == {"param_id": 20, "body": body}


async def test_class_based_spec_file(swagger_file, aiohttp_client):
    class Pets(web.View):
        async def get(self, limit: Optional[int] = None):
            pets = []
            for i in range(limit or 3):
                pets.append({"id": i, "name": f"pet_{i}", "tag": f"tag_{i}"})
            return web.json_response(pets)

        async def post(self, body: Dict):
            return web.json_response(body, status=201)

    swagger = swagger_file()
    swagger.add_routes([web.view("/pets", Pets)])

    client = await aiohttp_client(swagger._app)

    resp = await client.get("/pets", params={"limit": 1})
    assert resp.status == 200
    assert await resp.json() == [{"id": 0, "name": "pet_0", "tag": "tag_0"}]

    resp = await client.get("/pets")
    assert resp.status == 200
    assert await resp.json() == [
        {"id": 0, "name": "pet_0", "tag": "tag_0"},
        {"id": 1, "name": "pet_1", "tag": "tag_1"},
        {"id": 2, "name": "pet_2", "tag": "tag_2"},
    ]

    req = {"id": 10, "name": "pet", "tag": "tag"}
    resp = await client.post("/pets", json=req)
    assert resp.status == 201
    assert await resp.json() == req
