from aiohttp import web

from aiohttp_swagger3 import SwaggerDocs, SwaggerUiSettings


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
        swagger_ui_settings=SwaggerUiSettings(
            path="/docs",
            layout="BaseLayout",
            deepLinking=False,
            displayOperationId=True,
            defaultModelsExpandDepth=5,
            defaultModelExpandDepth=5,
            defaultModelRendering="model",
            displayRequestDuration=True,
            docExpansion="list",
            filter=True,
            showExtensions=True,
            showCommonExtensions=True,
            supportedSubmitMethods=["get"],
            validatorUrl=None,
            withCredentials=True,
        ),
    )
    s.add_routes([web.get("/", handler, allow_head=True)])
    web.run_app(app)


if __name__ == "__main__":
    main()
