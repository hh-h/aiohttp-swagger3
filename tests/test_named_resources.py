from aiohttp import web


async def test_named_resources(swagger_docs):
    async def handler(request):
        return web.json_response()

    swagger = swagger_docs()
    swagger.add_routes(
        [web.get("/", handler, name="get"), web.post("/", handler, name="post")]
    )

    assert "get" in swagger._app.router
    assert "post" in swagger._app.router
