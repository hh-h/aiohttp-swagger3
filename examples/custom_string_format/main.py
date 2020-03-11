from aiohttp import web

from aiohttp_swagger3 import SwaggerDocs, ValidatorError


async def handler(request, query: str):
    """
    ---
    parameters:

      - name: query
        in: query
        required: true
        schema:
          type: string
          format: my_custom_sf

    responses:
      '200':
        description: OK.

    """
    return web.json_response({"query": query})


# your validator should accept only string and return nothing
# all exceptions must be converted to ValidatorError
def my_custom_validator(value: str) -> None:
    if not value.startswith("my_"):
        raise ValidatorError("description why it's not valid")


def main():
    app = web.Application()
    s = SwaggerDocs(app)
    # register your custom string format validator
    s.register_string_format_validator("my_custom_sf", my_custom_validator)
    s.add_routes([web.get("/p", handler)])
    web.run_app(app)


if __name__ == "__main__":
    main()
