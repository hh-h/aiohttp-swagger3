from aiohttp import web

from aiohttp_swagger3 import ValidatorError

from .helpers import error_to_json


async def test_unknown_string_format(swagger_docs, aiohttp_client):
    async def handler(request, query: str):
        """
        ---
        parameters:

          - name: query
            in: query
            required: true
            schema:
              type: string
              format: something_unknown

        responses:
          '200':
            description: OK.

        """
        return web.json_response({"query": query})

    swagger = swagger_docs()
    swagger.add_route("GET", "/r", handler)

    client = await aiohttp_client(swagger._app)

    params = {"query": "qqq"}
    resp = await client.get("/r", params=params)
    assert resp.status == 200
    assert await resp.json() == params


async def test_custom_string_format(swagger_docs, aiohttp_client):
    def my_custom_validator(value: str) -> None:
        if not value.startswith("my_"):
            raise ValidatorError("description why it's not valid")

    async def handler(request, query: str):
        """
        ---
        parameters:

          - name: query
            in: query
            required: true
            schema:
              type: string
              format: my_custom_sf

        responses:
          '200':
            description: OK.

        """
        return web.json_response({"query": query})

    swagger = swagger_docs()
    swagger.register_string_format_validator("my_custom_sf", my_custom_validator)
    swagger.add_route("GET", "/r", handler)

    client = await aiohttp_client(swagger._app)

    params = {"query": "my_custom_sf"}
    resp = await client.get("/r", params=params)
    assert resp.status == 200
    assert await resp.json() == params

    params = {"query": "invalid_custom_sf"}
    resp = await client.get("/r", params=params)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"query": "description why it's not valid"}


async def test_override_default_string_format(swagger_docs, aiohttp_client):
    def my_ipv4_validator(value: str) -> None:
        if value != "8.8.8.8":
            raise ValidatorError("invalid ipv4 address")

    async def handler(request, ip: str):
        """
        ---
        parameters:

          - name: ip
            in: query
            required: true
            schema:
              type: string
              format: ipv4

        responses:
          '200':
            description: OK.

        """
        return web.json_response({"ip": ip})

    swagger = swagger_docs()
    swagger.register_string_format_validator("ipv4", my_ipv4_validator)
    swagger.add_route("GET", "/r", handler)

    client = await aiohttp_client(swagger._app)

    params = {"ip": "8.8.8.8"}
    resp = await client.get("/r", params=params)
    assert resp.status == 200
    assert await resp.json() == params

    params = {"ip": "1.1.1.1"}
    resp = await client.get("/r", params=params)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"ip": "invalid ipv4 address"}
