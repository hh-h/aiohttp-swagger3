from aiohttp import web

from aiohttp_swagger3 import SwaggerContact, SwaggerDocs, SwaggerInfo, SwaggerLicense, SwaggerUiSettings


def main():
    app = web.Application()
    SwaggerDocs(
        app,
        info=SwaggerInfo(
            title="test app",
            version="2.2.2",
            description="test description",
            terms_of_service="https://example.com/terms",
            contact=SwaggerContact(name="user", url="https://example.com/contact", email="user@example.com"),
            license=SwaggerLicense(name="Apache 2.0", url="https://www.apache.org/licenses/LICENSE-2.0.html"),
        ),
        swagger_ui_settings=SwaggerUiSettings(path="/docs"),
    )
    web.run_app(app)


if __name__ == "__main__":
    main()
