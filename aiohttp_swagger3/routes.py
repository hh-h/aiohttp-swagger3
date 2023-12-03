import datetime
import json
from typing import Any

from aiohttp import web


class CustomEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


async def _ui(ui_text: str, request: web.Request) -> web.Response:
    return web.Response(text=ui_text, content_type="text/html")


async def _swagger_spec(spec: Any, request: web.Request) -> web.Response:
    return web.json_response(
        spec,
        dumps=lambda obj: json.dumps(obj, cls=CustomEncoder),
    )


async def _redirect(request: web.Request) -> web.Response:
    return web.HTTPMovedPermanently(f"{request.path}/")
