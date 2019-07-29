from aiohttp import web

from aiohttp_swagger3 import SwaggerDocs


async def handler(request):
    """
    ---
    security:
      - bearerAuth: []
      - apiKeyAuth: []

    responses:
      '200':
        description: OK.

    """
    r = {}
    if "x-api-key" in request["data"]:
        r["api_key"] = request["data"]["x-api-key"]
    else:
        r["authorization"] = request["data"]["authorization"]

    return web.json_response(r)


def main():
    app = web.Application()
    s = SwaggerDocs(app, "/docs", components="components.yaml")
    s.add_routes([web.get("/", handler, allow_head=False)])
    web.run_app(app)


if __name__ == "__main__":
    main()
