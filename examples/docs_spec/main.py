from typing import Dict, Optional

from aiohttp import web
from aiohttp_swagger3 import SwaggerDocs


class PetFactory:
    id = 1

    def create(self, name: str, tag: Optional[str]) -> Dict:
        pet = {
            'id': self.id,
            'name': name,
        }
        if tag is not None:
            pet['tag'] = tag
        self.id += 1
        return pet


PET_FACTORY = PetFactory()


async def get_all_pets(request: web.Request) -> web.Response:
    """
    some docs
    ---
    summary: List all pets
    tags:
      - pets
    responses:
      '200':
        description: An array of pets
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/Pets"
    """
    return web.json_response(list(request.app['storage'].values()))


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
        application/json:
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
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/Pet"
    """
    # or access to body via request['data']['body']
    pet = PET_FACTORY.create(body['name'], body.get('tag'))
    request.app['storage'][pet['id']] = pet
    return web.json_response(pet, status=201)


async def get_one_pet(request: web.Request, pet_id: int) -> web.Response:
    """
    ---
    summary: Info for a specific pet
    tags:
      - pets
    parameters:
      - name: pet_id
        in: path
        required: true
        description: The id of the pet to retrieve
        schema:
          type: integer
          format: int32
    responses:
      '200':
        description: Expected response to a valid request
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/Pet"
    """
    if pet_id not in request.app['storage']:
        raise web.HTTPNotFound()
    return web.json_response(request.app['storage'][pet_id])


async def delete_one_pet(request: web.Request, pet_id: int) -> web.Response:
    """
    ---
    summary: Deletes specific pet
    tags:
      - pets
    parameters:
      - name: pet_id
        in: path
        required: true
        description: The id of the pet to delete
        schema:
          type: integer
          format: int32
    responses:
      '204':
        description: Null response
    """
    if pet_id not in request.app['storage']:
        raise web.HTTPNotFound()
    del request.app['storage'][pet_id]
    return web.json_response(status=204)


def main():
    app = web.Application()
    s = SwaggerDocs(app, '/docs', title="Swagger Petstore", version="1.0.0", components="components.yaml")
    s.add_routes([
        web.get("/pets", get_all_pets),
        web.get("/pets/{pet_id}", get_one_pet),
        web.delete("/pets/{pet_id}", delete_one_pet),
        web.post("/pets", create_pet),
    ])
    app['storage'] = {}
    web.run_app(app)


if __name__ == '__main__':
    main()
