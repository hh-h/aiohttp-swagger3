from aiohttp import web

from aiohttp_swagger3 import SwaggerDocs


async def test_named_resources(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")

    async def handler(request):
        return web.json_response()

    s.add_routes(
        [web.get("/", handler, name="get"), web.post("/", handler, name="post")]
    )

    assert "get" in app.router
    assert "post" in app.router
