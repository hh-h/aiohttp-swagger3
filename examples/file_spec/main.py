from typing import Dict, Optional

from aiohttp import web

from aiohttp_swagger3 import SwaggerFile, SwaggerUiSettings


class PetFactory:
    id = 1

    def create(self, name: str, tag: Optional[str]) -> Dict:
        pet = {"id": self.id, "name": name}
        if tag is not None:
            pet["tag"] = tag
        self.id += 1
        return pet


PET_FACTORY = PetFactory()


async def get_all_pets(request: web.Request) -> web.Response:
    return web.json_response(list(request.app["storage"].values()))


async def create_pet(request: web.Request, body: Dict) -> web.Response:
    # or access to body via request['data']['body']
    pet = PET_FACTORY.create(body["name"], body.get("tag"))
    request.app["storage"][pet["id"]] = pet
    return web.json_response(pet, status=201)


async def get_one_pet(request: web.Request, pet_id: int) -> web.Response:
    if pet_id not in request.app["storage"]:
        raise web.HTTPNotFound()
    return web.json_response(request.app["storage"][pet_id])


async def delete_one_pet(request: web.Request, pet_id: int) -> web.Response:
    if pet_id not in request.app["storage"]:
        raise web.HTTPNotFound()
    del request.app["storage"][pet_id]
    return web.json_response(status=204)


def main():
    app = web.Application()
    s = SwaggerFile(
        app,
        spec_file="petstore.yaml",
        swagger_ui_settings=SwaggerUiSettings(path="/docs"),
    )
    s.add_routes(
        [
            web.get("/pets", get_all_pets),
            web.get("/pets/{pet_id}", get_one_pet),
            web.delete("/pets/{pet_id}", delete_one_pet),
            web.post("/pets", create_pet),
        ]
    )
    app["storage"] = {}
    web.run_app(app)


if __name__ == "__main__":
    main()
