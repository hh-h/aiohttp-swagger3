from aiohttp import web

from aiohttp_swagger3 import RequestValidationFailed


async def test_validation_exception_middleware(swagger_docs, aiohttp_client):
    @web.middleware
    async def middleware(request, handler):
        try:
            return await handler(request)
        except RequestValidationFailed as exc:
            assert exc.errors == {"query": "value should be type of int"}
            raise exc

    async def handler(request):
        """
        ---
        parameters:

          - name: query
            in: query
            required: true
            schema:
              type: integer

        responses:
          '200':
            description: OK.
        """
        return web.json_response()

    swagger = swagger_docs()
    swagger._app.middlewares.append(middleware)
    swagger.add_get("/r", handler)

    client = await aiohttp_client(swagger._app)

    params = {"query": "abc"}
    resp = await client.get("/r", params=params)
    assert resp.status == 400
