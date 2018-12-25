from typing import Dict, Tuple

from aiohttp import web

from .validators import ValidatorError


async def application_json(request: web.Request) -> Tuple[Dict, bool]:
    try:
        return await request.json(), False
    except ValueError as e:
        raise ValidatorError(str(e))
