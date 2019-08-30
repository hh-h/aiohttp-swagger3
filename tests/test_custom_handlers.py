import re
from typing import Dict, Tuple

import pytest
from aiohttp import web

from aiohttp_swagger3 import SwaggerDocs


async def test_custom_media_type(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")

    async def custom_handler(request: web.Request) -> Tuple[Dict, bool]:
        # <key1>[value1]<key2>[value2]
        text = await request.text()
        return dict(re.findall(r"<(?P<key>.+?)>\[(?P<value>.+?)\]", text)), True

    s.register_media_type_handler("custom/handler", custom_handler)

    async def handler(request, body: Dict):
        """
        ---
        requestBody:
          required: true
          content:
            custom/handler:
              schema:
                type: object
                required:
                  - required
                properties:
                  required:
                    type: integer
                  optional:
                    type: integer

        responses:
          '200':
            description: OK.

        """
        return web.json_response(body)

    s.add_route("POST", "/r", handler)

    client = await aiohttp_client(app)

    resp = await client.post(
        "/r", data="<required>[10]", headers={"content-type": "custom/handler"}
    )
    assert resp.status == 200
    assert await resp.json() == {"required": 10}

    resp = await client.post(
        "/r",
        data="<required>[10]<optional>[20]",
        headers={"content-type": "custom/handler"},
    )
    assert resp.status == 200
    assert await resp.json() == {"required": 10, "optional": 20}


async def test_missing_custom_media_type(loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")

    async def handler(request, body: Dict):
        """
        ---
        requestBody:
          required: true
          content:
            custom/handler:
              schema:
                type: object

        responses:
          '200':
            description: OK.

        """
        return web.json_response(body)

    with pytest.raises(Exception) as exc_info:
        s.add_route("POST", "/r", handler)
    assert "register handler for custom/handler first" == str(exc_info.value)


async def test_file_upload(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")

    async def octet_stream_handler(request: web.Request) -> Tuple[bytes, bool]:
        return await request.read(), True

    s.register_media_type_handler("application/octet-stream", octet_stream_handler)

    async def handler(request, body: bytes):
        """
        ---
        requestBody:
          required: true
          content:
            application/octet-stream:
              schema:
                type: string
                format: binary

        responses:
          '200':
            description: OK.

        """
        return web.Response(body=body)

    s.add_route("POST", "/r", handler)

    client = await aiohttp_client(app)

    data = b"\x00Binary-data\x00"
    resp = await client.post("/r", data=data)
    assert resp.status == 200
    assert await resp.read() == data
