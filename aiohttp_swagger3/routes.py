import datetime
import json
from typing import Any

from aiohttp import web

_SWAGGER_INDEX_HTML = "SWAGGER_INDEX_HTML"
_SWAGGER_SPECIFICATION = "SWAGGER_SPECIFICATION"


class CustomEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


async def _swagger_home(request: web.Request) -> web.Response:
    return web.Response(text=request.app[_SWAGGER_INDEX_HTML], content_type="text/html")


async def _swagger_spec(request: web.Request) -> web.Response:
    return web.json_response(
        request.app[_SWAGGER_SPECIFICATION],
        dumps=lambda obj: json.dumps(obj, cls=CustomEncoder),
    )


async def _redirect(request: web.Request) -> web.Response:
    return web.HTTPMovedPermanently(f"{request.path}/")
