from aiohttp import web


async def test_no_docs(swagger_docs, aiohttp_client):
    async def handler(request):
        return web.json_response()

    swagger = swagger_docs()
    swagger.add_route("POST", "/r", handler)

    client = await aiohttp_client(swagger._app)
    resp = await client.post("/r", json={"array": "whatever"})
    assert resp.status == 200
