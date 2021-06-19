from typing import List

from aiohttp import web

from aiohttp_swagger3 import SwaggerDocs, SwaggerUiSettings, swagger_doc


async def docstring_handler(request, query1: List[int], query2: List[int] = None):
    """
    some docstring
    ---
    parameters:

      - name: query1
        in: query
        required: true
        schema:
          type: array
          items:
            type: integer
          uniqueItems: true
          minItems: 1

      - name: query2
        in: query
        schema:
          type: array
          items:
            type: integer
          uniqueItems: true
          minItems: 1

    responses:
      '200':
        description: OK.

    """
    return web.json_response({"query1": query1, "query2": query2})


@swagger_doc("swagger_schemas/get.yaml")
async def decorator_handler(request, query1: List[int], query2: List[int] = None):
    """
    some docstring
    """
    return web.json_response({"query1": query1, "query2": query2})


def main():
    app = web.Application()
    s = SwaggerDocs(
        app,
        title="Example",
        version="1.0.0",
        swagger_ui_settings=SwaggerUiSettings(path="/docs"),
    )
    s.add_routes(
        [
            web.get("/docstring", docstring_handler, allow_head=False),
            web.get("/decorator", decorator_handler, allow_head=False),
        ]
    )
    web.run_app(app)


if __name__ == "__main__":
    main()
