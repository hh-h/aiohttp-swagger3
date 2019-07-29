from aiohttp import web

from aiohttp_swagger3 import SwaggerDocs

from .helpers import error_to_json


async def test_basic_auth(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs", components="tests/testdata/components.yaml")

    async def handler(request):
        """
        ---
        security:
          - basicAuth: []

        responses:
          '200':
            description: OK.

        """
        assert "authorization" in request["data"]
        return web.json_response({"authorization": request["data"]["authorization"]})

    s.add_route("GET", "/r", handler)

    client = await aiohttp_client(app)

    authorization = "ZGVtbzpwQDU1dzByZA=="
    headers = {"Authorization": f"Basic {authorization}"}

    resp = await client.get("/r", headers=headers)
    assert resp.status == 200
    assert await resp.json() == {"authorization": authorization}


async def test_bearer_auth(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs", components="tests/testdata/components.yaml")

    async def handler(request):
        """
        ---
        security:
          - bearerAuth: []

        responses:
          '200':
            description: OK.

        """
        assert "authorization" in request["data"]
        return web.json_response({"authorization": request["data"]["authorization"]})

    s.add_route("GET", "/r", handler)

    client = await aiohttp_client(app)

    authorization = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ1"
    headers = {"Authorization": f"Bearer {authorization}"}

    resp = await client.get("/r", headers=headers)
    assert resp.status == 200
    assert await resp.json() == {"authorization": authorization}


async def test_api_key_header_auth(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs", components="tests/testdata/components.yaml")

    async def handler(request):
        """
        ---
        security:
          - apiKeyHeaderAuth: []

        responses:
          '200':
            description: OK.

        """
        assert "X-API-KEY" in request["data"]
        return web.json_response({"api_key": request["data"]["X-API-KEY"]})

    s.add_route("GET", "/r", handler)

    client = await aiohttp_client(app)

    api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ2"
    headers = {"X-API-KEY": api_key}

    resp = await client.get("/r", headers=headers)
    assert resp.status == 200
    assert await resp.json() == {"api_key": api_key}


async def test_api_key_query_auth(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs", components="tests/testdata/components.yaml")

    async def handler(request):
        """
        ---
        security:
          - apiKeyQueryAuth: []

        responses:
          '200':
            description: OK.

        """
        assert "api_key" in request["data"]
        return web.json_response({"api_key": request["data"]["api_key"]})

    s.add_route("GET", "/r", handler)

    client = await aiohttp_client(app)

    api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ3"
    params = {"api_key": api_key}

    resp = await client.get("/r", params=params)
    assert resp.status == 200
    assert await resp.json() == {"api_key": api_key}


async def test_api_key_cookie_auth(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs", components="tests/testdata/components.yaml")

    async def handler(request):
        """
        ---
        security:
          - apiKeyCookieAuth: []

        responses:
          '200':
            description: OK.

        """
        assert "C-API-KEY" in request["data"]
        return web.json_response({"api_key": request["data"]["C-API-KEY"]})

    s.add_route("GET", "/r", handler)

    client = await aiohttp_client(app)

    api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ4"
    cookies = {"C-API-KEY": api_key}

    resp = await client.get("/r", cookies=cookies)
    assert resp.status == 200
    assert await resp.json() == {"api_key": api_key}


async def test_all_of_auth(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs", components="tests/testdata/components.yaml")

    async def handler(request):
        """
        ---
        security:
          - basicAuth: []
            apiKeyCookieAuth: []

        responses:
          '200':
            description: OK.

        """
        assert "C-API-KEY" in request["data"]
        assert "authorization" in request["data"]
        return web.json_response(
            {
                "api_key": request["data"]["C-API-KEY"],
                "authorization": request["data"]["authorization"],
            }
        )

    s.add_route("GET", "/r", handler)

    client = await aiohttp_client(app)

    api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ4"
    cookies = {"C-API-KEY": api_key}

    authorization = "ZGVtbzpwQDU1dzByZA=="
    headers = {"Authorization": f"Basic {authorization}"}

    resp = await client.get("/r", headers=headers, cookies=cookies)
    assert resp.status == 200
    assert await resp.json() == {"api_key": api_key, "authorization": authorization}

    resp = await client.get("/r", cookies=cookies)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"authorization": "is required"}

    resp = await client.get("/r", headers=headers)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"C-API-KEY": "is required"}


async def test_one_of_auth(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs", components="tests/testdata/components.yaml")

    async def handler(request):
        """
        ---
        security:
          - bearerAuth: []
          - apiKeyCookieAuth: []

        responses:
          '200':
            description: OK.

        """
        assert not (
            "C-API-KEY" in request["data"] and "authorization" in request["data"]
        )
        r = {}
        if "C-API-KEY" in request["data"]:
            assert "authorization" not in request["data"]
            r["api_key"] = request["data"]["C-API-KEY"]
        else:
            assert "authorization" in request["data"]
            assert "C-API-KEY" not in request["data"]
            r["authorization"] = request["data"]["authorization"]

        return web.json_response(r)

    s.add_route("GET", "/r", handler)

    client = await aiohttp_client(app)

    api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ4"
    cookies = {"C-API-KEY": api_key}

    resp = await client.get("/r", cookies=cookies)
    assert resp.status == 200
    assert await resp.json() == {"api_key": api_key}

    authorization = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ1"
    headers = {"Authorization": f"Bearer {authorization}"}

    resp = await client.get("/r", headers=headers)
    assert resp.status == 200
    assert await resp.json() == {"authorization": authorization}

    resp = await client.get("/r", cookies=cookies, headers=headers)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == "Only one auth must be provided"

    resp = await client.get("/r")
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == "One auth must be provided"
