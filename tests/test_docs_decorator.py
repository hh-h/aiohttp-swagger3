from functools import wraps

import pytest
from aiohttp import web

from aiohttp_swagger3 import swagger_doc


async def test_decorated_handlers(swagger_docs, aiohttp_client):
    def decorator(fn):
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            return await fn(*args, **kwargs)

        return wrapper

    @decorator
    @swagger_doc("tests/testdata/route.yaml")
    async def after_deco_handler(request, param_id: int):
        return web.json_response({"param_id": param_id})

    @swagger_doc("tests/testdata/route.yaml")
    @decorator
    async def before_deco_handler(request, param_id: int):
        return web.json_response({"param_id": param_id})

    @swagger_doc("tests/testdata/route.yaml")
    async def simple_handler(request, param_id: int):
        return web.json_response({"param_id": param_id})

    class View(web.View):
        @swagger_doc("tests/testdata/route.yaml")
        async def get(self, param_id: int):
            return web.json_response({"param_id": param_id})

    routes = web.RouteTableDef()

    @routes.view("/r5/{param_id}")
    class OtherView(web.View):
        @swagger_doc("tests/testdata/route.yaml")
        async def get(self, param_id: int):
            return web.json_response({"param_id": param_id})

    swagger = swagger_docs()
    swagger.add_route("GET", "/r1/{param_id}", after_deco_handler)
    swagger.add_route("GET", "/r2/{param_id}", before_deco_handler)
    swagger.add_route("GET", "/r3/{param_id}", simple_handler)
    swagger.add_routes([web.view("/r4/{param_id}", View)])
    swagger.add_routes(routes)

    client = await aiohttp_client(swagger._app)

    for i in range(1, 6):
        resp = await client.get(f"/r{i}/10")
        assert resp.status == 200
        assert await resp.json() == {"param_id": 10}


async def test_docstring_and_decorator_collision(swagger_docs, aiohttp_client):

    with pytest.raises(Exception, match="cannot use decorator swagger_doc with docstring, function:"):

        @swagger_doc("tests/testdata/route.yaml")
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
