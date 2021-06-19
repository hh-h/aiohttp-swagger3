import pytest
from aiohttp import web

from .helpers import error_to_json


async def test_basic_auth(swagger_docs_with_components, aiohttp_client):
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

    swagger = swagger_docs_with_components()
    swagger.add_route("GET", "/r", handler)

    client = await aiohttp_client(swagger._app)

    authorization = "ZGVtbzpwQDU1dzByZA=="
    headers = {"Authorization": f"Basic {authorization}"}

    resp = await client.get("/r", headers=headers)
    assert resp.status == 200
    assert await resp.json() == {"authorization": authorization}


async def test_bearer_auth(swagger_docs_with_components, aiohttp_client):
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

    swagger = swagger_docs_with_components()
    swagger.add_route("GET", "/r", handler)

    client = await aiohttp_client(swagger._app)

    authorization = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ1"
    headers = {"Authorization": f"Bearer {authorization}"}

    resp = await client.get("/r", headers=headers)
    assert resp.status == 200
    assert await resp.json() == {"authorization": authorization}


async def test_api_key_header_auth(swagger_docs_with_components, aiohttp_client):
    async def handler(request):
        """
        ---
        security:
          - apiKeyHeaderAuth: []

        responses:
          '200':
            description: OK.

        """
        assert "X-API-KEY" not in request["data"]
        assert "x-api-key" in request["data"]
        return web.json_response({"api_key": request["data"]["x-api-key"]})

    swagger = swagger_docs_with_components()
    swagger.add_route("GET", "/r", handler)

    client = await aiohttp_client(swagger._app)

    api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ2"
    headers = {"X-API-KEY": api_key}

    resp = await client.get("/r", headers=headers)
    assert resp.status == 200
    assert await resp.json() == {"api_key": api_key}

    resp = await client.get("/r")
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"x-api-key": "is required"}

    resp = await client.get("/r", headers={"X-API-KEY": ""})
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"x-api-key": "value length should be more than 1"}


async def test_api_key_query_auth(swagger_docs_with_components, aiohttp_client):
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

    swagger = swagger_docs_with_components()
    swagger.add_route("GET", "/r", handler)

    client = await aiohttp_client(swagger._app)

    api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ3"
    params = {"api_key": api_key}

    resp = await client.get("/r", params=params)
    assert resp.status == 200
    assert await resp.json() == {"api_key": api_key}

    resp = await client.get("/r")
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"api_key": "is required"}

    resp = await client.get("/r", params={"api_key": ""})
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"api_key": "value length should be more than 1"}


async def test_api_key_cookie_auth(swagger_docs_with_components, aiohttp_client):
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

    swagger = swagger_docs_with_components()
    swagger.add_route("GET", "/r", handler)

    client = await aiohttp_client(swagger._app)

    api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ4"
    cookies = {"C-API-KEY": api_key}

    resp = await client.get("/r", cookies=cookies)
    assert resp.status == 200
    assert await resp.json() == {"api_key": api_key}

    resp = await client.get("/r")
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"C-API-KEY": "is required"}

    resp = await client.get("/r", cookies={"C-API-KEY": ""})
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"C-API-KEY": "value length should be more than 1"}


async def test_all_of_auth(swagger_docs_with_components, aiohttp_client):
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

    swagger = swagger_docs_with_components()
    swagger.add_route("GET", "/r", handler)

    client = await aiohttp_client(swagger._app)

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

    resp = await client.get("/r")
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"authorization": "is required"}


async def test_any_of_auth(swagger_docs_with_components, aiohttp_client):
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
        r = {}
        if "C-API-KEY" in request["data"]:
            r["api_key"] = request["data"]["C-API-KEY"]
        if "authorization" in request["data"]:
            r["authorization"] = request["data"]["authorization"]

        return web.json_response(r)

    swagger = swagger_docs_with_components()
    swagger.add_route("GET", "/r", handler)

    client = await aiohttp_client(swagger._app)

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
    assert resp.status == 200
    assert await resp.json() == {"authorization": authorization, "api_key": api_key}

    resp = await client.get("/r")
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"authorization": "no auth has been provided"}


async def test_missing_basic_word_in_auth(swagger_docs_with_components, aiohttp_client):
    async def handler(request):
        """
        ---
        security:
          - basicAuth: []

        responses:
          '200':
            description: OK.

        """
        return web.json_response()

    swagger = swagger_docs_with_components()
    swagger.add_route("GET", "/r", handler)

    client = await aiohttp_client(swagger._app)

    authorization = "ZGVtbzpwQDU1dzByZA=="
    headers = {"Authorization": authorization}

    resp = await client.get("/r", headers=headers)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"authorization": "value should start with 'Basic' word"}


async def test_missing_bearer_word_in_auth(swagger_docs_with_components, aiohttp_client):
    async def handler(request):
        """
        ---
        security:
          - bearerAuth: []

        responses:
          '200':
            description: OK.

        """
        return web.json_response()

    swagger = swagger_docs_with_components()
    swagger.add_route("GET", "/r", handler)

    client = await aiohttp_client(swagger._app)

    authorization = "ZGVtbzpwQDU1dzByZA=="
    headers = {"Authorization": authorization}

    resp = await client.get("/r", headers=headers)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"authorization": "value should start with 'Bearer' word"}


async def test_unknown_security(swagger_docs_with_components):
    async def handler(request):
        """
        ---
        security:
          - wrongAuth: []

        responses:
          '200':
            description: OK.

        """
        return web.json_response()

    swagger = swagger_docs_with_components()
    with pytest.raises(Exception) as exc_info:
        swagger.add_route("GET", "/r", handler)
    assert "security schema wrongAuth must be defined in components" == str(exc_info.value)


async def test_complex_auth(swagger_docs_with_components, aiohttp_client):
    async def handler(request):
        """
        ---
        security:
          - basicAuth: []
            apiKeyCookieAuth: []
          - bearerAuth: []
            apiKeyHeaderAuth: []

        responses:
          '200':
            description: OK.

        """
        assert "C-API-KEY" in request["data"] or "x-api-key" in request["data"]
        api_key = request["data"]["C-API-KEY"] if "C-API-KEY" in request["data"] else request["data"]["x-api-key"]
        authorization = request["data"]["authorization"]
        return web.json_response({"http": authorization, "api_key": api_key})

    swagger = swagger_docs_with_components()
    swagger.add_route("GET", "/r", handler)

    client = await aiohttp_client(swagger._app)

    option1_http = "111ZGVtbzpwQDU1dzByZA=="
    option1_api_key = "111eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ4"
    option1 = {
        "cookies": {"C-API-KEY": option1_api_key},
        "headers": {"Authorization": f"Basic {option1_http}"},
    }

    option2_http = "222ZGVtbzpwQDU1dzByZA=="
    option2_api_key = "222eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ4"
    option2 = {
        "headers": {
            "Authorization": f"Bearer {option2_http}",
            "X-API-KEY": option2_api_key,
        }
    }

    resp = await client.get("/r", **option1)
    assert resp.status == 200
    assert await resp.json() == {"api_key": option1_api_key, "http": option1_http}

    resp = await client.get("/r", **option2)
    assert resp.status == 200
    assert await resp.json() == {"api_key": option2_api_key, "http": option2_http}


async def test_optional_any_of_auth(swagger_docs_with_components, aiohttp_client, loop):
    async def handler(request):
        """
        ---
        security:
          - bearerAuth: []
          - {}

        responses:
          '200':
            description: OK.

        """
        has_auth = "authorization" in request["data"]
        return web.json_response({"has_auth": has_auth})

    swagger = swagger_docs_with_components()
    swagger.add_route("GET", "/r", handler)

    client = await aiohttp_client(swagger._app)

    authorization = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ1"
    headers = {"Authorization": f"Bearer {authorization}"}

    resp = await client.get("/r", headers=headers)
    assert resp.status == 200
    assert await resp.json() == {"has_auth": True}

    resp = await client.get("/r")
    assert resp.status == 200
    assert await resp.json() == {"has_auth": False}


async def test_disabled_security(swagger_docs_with_components, aiohttp_client):
    async def handler(request):
        """
        ---
        security: []

        responses:
          '200':
            description: OK.

        """
        return web.json_response()

    swagger = swagger_docs_with_components()
    swagger.add_route("GET", "/r", handler)

    client = await aiohttp_client(swagger._app)

    resp = await client.get("/r")
    assert resp.status == 200
