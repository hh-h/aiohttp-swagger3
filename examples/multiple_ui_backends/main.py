from aiohttp import web

from aiohttp_swagger3 import RapiDocUiSettings, ReDocUiSettings, SwaggerDocs, SwaggerUiSettings


async def handler(request):
    """
    ---
    responses:
      '200':
        description: OK.

    """
    return web.json_response()


def main():
    app = web.Application()
    s = SwaggerDocs(
        app,
        swagger_ui_settings=SwaggerUiSettings(path="/swagger"),
        redoc_ui_settings=ReDocUiSettings(path="/redoc"),
        rapidoc_ui_settings=RapiDocUiSettings(path="/rapidoc"),
    )
    s.add_routes([web.get("/", handler, allow_head=True)])
    web.run_app(app)


if __name__ == "__main__":
    main()
