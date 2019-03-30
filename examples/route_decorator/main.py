from aiohttp import web
from aiohttp_swagger3 import SwaggerDocs

routes = web.RouteTableDef()

@routes.get('/pets/{pet_id}', allow_head=False)
async def get_one_pet(request: web.Request, pet_id: int) -> web.Response:
    """
    Optional route description
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

def main():
    app = web.Application()
    s = SwaggerDocs(app, '/docs', "petstore.yaml")
    s.add_routes(routes)
    web.run_app(app)