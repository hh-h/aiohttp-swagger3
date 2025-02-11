from aiohttp import hdrs, web


async def test_allow_head(swagger_docs, aiohttp_client):
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

    swagger = swagger_docs()
    swagger.add_get("/r1/{param_id}", handler)
    swagger.add_get("/r2/{param_id}", handler, allow_head=False)

    client = await aiohttp_client(swagger._app)
    resp = await client.head("/r1/1")
    assert resp.status == 200

    resp = await client.head("/r2/1")
    assert resp.status == 405


async def test_meth_any(swagger_docs, aiohttp_client):
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

    swagger = swagger_docs()
    swagger.add_route("*", "/r/{param_id}", handler)

    client = await aiohttp_client(swagger._app)

    for method in (
        hdrs.METH_GET,
        hdrs.METH_POST,
        hdrs.METH_PUT,
        hdrs.METH_PATCH,
        hdrs.METH_DELETE,
    ):
        resp = await getattr(client, method.lower())("/r/10")
        assert resp.status == 200
        assert await resp.json() == {"param_id": 10}


async def test_all_methods(swagger_docs, aiohttp_client):
    class View(web.View):
        async def get(self):
            """
            ---

            responses:
              '200':
                description: OK.

            """
            return web.json_response()

    async def handler(request):
        """
        ---

        responses:
          '200':
            description: OK.

        """
        return web.json_response()

    swagger = swagger_docs()
    swagger.add_get("/r", handler, allow_head=False)
    swagger.add_head("/r", handler)
    swagger.add_put("/r", handler)
    swagger.add_patch("/r", handler)
    swagger.add_post("/r", handler)
    swagger.add_delete("/r", handler)
    swagger.add_options("/r", handler)
    swagger.add_view("/r2", View)

    client = await aiohttp_client(swagger._app)

    for method in (
        hdrs.METH_GET,
        hdrs.METH_HEAD,
        hdrs.METH_POST,
        hdrs.METH_PUT,
        hdrs.METH_PATCH,
        hdrs.METH_DELETE,
        hdrs.METH_OPTIONS,
    ):
        resp = await getattr(client, method.lower())("/r")
        assert resp.status == 200

    resp = await client.get("/r2")
    assert resp.status == 200
