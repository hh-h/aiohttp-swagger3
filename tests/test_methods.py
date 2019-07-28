from aiohttp import hdrs, web

from aiohttp_swagger3 import SwaggerDocs


async def test_allow_head(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")

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

    s.add_get("/r1/{param_id}", handler)
    s.add_get("/r2/{param_id}", handler, allow_head=False)

    client = await aiohttp_client(app)
    resp = await client.head("/r1/1")
    assert resp.status == 200

    resp = await client.head("/r2/1")
    assert resp.status == 405


async def test_meth_any(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")

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

    s.add_route("*", "/r/{param_id}", handler)

    client = await aiohttp_client(app)

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
