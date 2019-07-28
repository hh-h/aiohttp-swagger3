from aiohttp import web

from aiohttp_swagger3 import SwaggerDocs


async def test_no_docs(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")

    async def handler(request):
        return web.json_response()

    s.add_route("POST", "/r", handler)

    client = await aiohttp_client(app)
    resp = await client.post("/r", json={"array": "whatever"})
    assert resp.status == 200
