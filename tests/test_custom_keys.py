from aiohttp import web


async def test_custom_request_key(swagger_docs, aiohttp_client):
    routes = web.RouteTableDef()

    @routes.post("/r/{path}")
    async def handler(request, header: str, query: str, path: str, body: str):
        """
        ---
        parameters:

          - name: header
            in: header
            required: true
            schema:
              type: string

          - name: query
            in: query
            required: true
            schema:
              type: string

          - name: path
            in: path
            required: true
            schema:
              type: string

        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: string

        responses:
          '200':
            description: OK.
        """
        assert "data" not in request
        assert "test_key_321" in request
        assert request["test_key_321"]["header"] == header
        assert request["test_key_321"]["query"] == query
        assert request["test_key_321"]["path"] == path
        assert request["test_key_321"]["body"] == body
        return web.json_response()

    swagger = swagger_docs(request_key="test_key_321")
    swagger.add_routes(routes)

    client = await aiohttp_client(swagger._app)

    params = {"query": "str"}
    headers = {"header": "str"}
    req = "str"
    resp = await client.post("/r/str", headers=headers, params=params, json=req)
    assert resp.status == 200
