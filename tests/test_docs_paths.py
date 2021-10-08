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


async def test_path_with_regex(swagger_docs, aiohttp_client):
    async def handler(request, first_param_id: int, second_param_id: int):
        """
        ---
        parameters:

          - name: first_param_id
            in: path
            required: true
            schema:
              type: integer

          - name: second_param_id
            in: path
            required: true
            schema:
              type: integer

        responses:
          '200':
            description: OK.

        """
        return web.json_response({"first_param_id": first_param_id, "second_param_id": second_param_id})

    swagger = swagger_docs()
    swagger.add_route("GET", r"/r/{first_param_id:\d+}/r/{second_param_id:\d+}", handler)

    client = await aiohttp_client(swagger._app)

    resp = await client.get("/r/10/r/11")
    assert resp.status == 200
    assert await resp.json() == {"first_param_id": 10, "second_param_id": 11}
