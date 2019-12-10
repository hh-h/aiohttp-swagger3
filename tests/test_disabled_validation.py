from aiohttp import web


async def test_validation_false(swagger_docs, swagger_ui_settings, aiohttp_client):
    routes = web.RouteTableDef()

    @routes.post("/r")
    async def handler(request):
        """
        ---
        parameters:

          - name: query
            in: query
            required: true
            schema:
              type: string

        responses:
          '200':
            description: OK.
        """
        assert "data" not in request
        assert request.rel_url.query["query"] == "str"
        return web.json_response()

    swagger = swagger_docs(swagger_ui_settings=swagger_ui_settings(), validate=False)
    swagger.add_routes(routes)

    client = await aiohttp_client(swagger._app)

    params = {"query": "str"}
    resp = await client.post("/r", params=params)
    assert resp.status == 200

    resp = await client.get("/docs/")
    assert resp.status == 200

    resp = await client.get("/docs/swagger.json")
    assert resp.status == 200
    spec = await resp.json()
    assert spec["paths"] == {
        "/r": {
            "post": {
                "parameters": [
                    {
                        "name": "query",
                        "in": "query",
                        "required": True,
                        "schema": {"type": "string"},
                    }
                ],
                "responses": {"200": {"description": "OK."}},
            }
        }
    }


async def test_spec_file_validation_false(
    swagger_file, swagger_ui_settings, aiohttp_client
):
    async def handler(request):
        assert "data" not in request
        assert request.rel_url.query["query"] == "str"
        return web.json_response()

    swagger = swagger_file(swagger_ui_settings=swagger_ui_settings(), validate=False)
    swagger.add_get("/pets", handler)

    client = await aiohttp_client(swagger._app)

    params = {"query": "str"}
    resp = await client.get("/pets", params=params)
    assert resp.status == 200

    resp = await client.get("/docs/")
    assert resp.status == 200

    resp = await client.get("/docs/swagger.json")
    assert resp.status == 200
    spec = await resp.json()
    assert "/pets" in spec["paths"]
