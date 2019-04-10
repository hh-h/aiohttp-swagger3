import re
from typing import Dict, Tuple

from aiohttp import web

from aiohttp_swagger3 import SwaggerDocs


async def create_pet(request: web.Request, body: Dict) -> web.Response:
    """
    some docs
    ---
    summary: Create a pet
    tags:
      - pets
    requestBody:
      required: true
      content:
        my_cool/type:
          schema:
            type: object
            required:
              - name
            properties:
              name:
                type: string
              tag:
                type: string
    responses:
      '201':
        description: new pet
    """
    # or access to body via request['data']['body']
    pet = {"id": 1, "name": body["name"]}
    if "tag" in body:
        pet["tag"] = body["tag"]
    return web.json_response(pet, status=201)


regex = re.compile(r"<(?P<key>.+?)>\[(?P<value>.+?)\]")


# your handler must return tuple of two values:
# first one is actual parsed value
# second one is a boolean, does your first value have raw data or not
# i.e. json doesn't have raw values, but this example should return True
# because there're can be integers as strings, and they should be converted
async def my_cool_handler(request: web.Request) -> Tuple[Dict, bool]:
    # imaging that keys are wrapped with <> and values with []
    # <name>[lessie]<tag>[dog]
    return dict(regex.findall(await request.text())), True


def main():
    app = web.Application()
    s = SwaggerDocs(app, "/docs", title="Swagger Petstore", version="1.0.0")
    # register your handler before registering routes
    s.register_media_type_handler("my_cool/type", my_cool_handler)
    s.add_routes([web.post("/pets", create_pet)])
    web.run_app(app)


if __name__ == "__main__":
    main()
