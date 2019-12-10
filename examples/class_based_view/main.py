from typing import Dict

from aiohttp import web

from aiohttp_swagger3 import SwaggerDocs, SwaggerUiSettings


class View(web.View):
    async def get(self, param_id: int):
        """
        ---
        parameters:

          - name: param_id
            in: path
            required: true
            schema:
              type: integer

        responses:
          '200':
            description: OK.

        """
        return web.json_response({"param_id": param_id})

    async def post(self, param_id: int, body: Dict):
        """
        ---
        parameters:

          - name: param_id
            in: path
            required: true
            schema:
              type: integer

        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  integer:
                    type: integer

        responses:
          '200':
            description: OK.

        """
        return web.json_response({"param_id": param_id, "body": body})


def main():
    app = web.Application()
    s = SwaggerDocs(app, swagger_ui_settings=SwaggerUiSettings(path="/docs"))
    s.add_routes([web.view("/r/{param_id}", View)])
    web.run_app(app)


if __name__ == "__main__":
    main()
