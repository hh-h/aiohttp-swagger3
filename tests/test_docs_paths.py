from functools import wraps

from aiohttp import web


async def test_decorated_handlers(swagger_docs, aiohttp_client):
    def decorator(fn):
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            return await fn(*args, **kwargs)

        return wrapper

    @decorator
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
    swagger.add_route("GET", "/r/{param_id}", handler)

    client = await aiohttp_client(swagger._app)

    resp = await client.get("/r/10")
    assert resp.status == 200
    assert await resp.json() == {"param_id": 10}


async def test_path(swagger_docs, aiohttp_client):
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
    swagger.add_route("GET", "/r/{param_id}", handler)

    client = await aiohttp_client(swagger._app)

    resp = await client.get("/r/10")
    assert resp.status == 200
    assert await resp.json() == {"param_id": 10}
