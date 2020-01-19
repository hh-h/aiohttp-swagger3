from ast import literal_eval
from typing import Dict

from aiohttp import web

from .helpers import error_to_json


async def test_one_of_discriminator(swagger_docs, aiohttp_client):
    async def handler(request, body: Dict):
        """
        ---
        requestBody:
          required: true
          content:
            application/json:
              schema:
                oneOf:
                  - $ref: '#/components/schemas/Cat'
                  - $ref: '#/components/schemas/Dog'
                  - $ref: '#/components/schemas/Lizard'
                discriminator:
                  propertyName: petType
                  mapping:
                    cat_full: '#/components/schemas/Cat'
                    cat_short: Cat

        responses:
          '200':
            description: OK.
        """
        return web.json_response(body)

    swagger = swagger_docs(components="tests/testdata/discriminator.yaml")
    swagger.add_post("/r", handler)

    client = await aiohttp_client(swagger._app)

    data = {"petType": "Cat", "name": "misty"}
    resp = await client.post("/r", json=data)
    assert resp.status == 200
    assert await resp.json() == data

    data = {"petType": "cat_full", "name": "misty"}
    resp = await client.post("/r", json=data)
    assert resp.status == 200
    assert await resp.json() == data

    data = {"petType": "cat_short", "name": "misty"}
    resp = await client.post("/r", json=data)
    assert resp.status == 200
    assert await resp.json() == data

    data = {"petType": "Cat", "name": "misty", "bark": "woof"}
    resp = await client.post("/r", json=data)
    assert resp.status == 200
    assert await resp.json() == data

    data = {"petType": "Dog", "name": "misty", "bark": "woof"}
    resp = await client.post("/r", json=data)
    assert resp.status == 200
    assert await resp.json() == data

    data = {"petType": "Dog", "name": "misty"}
    resp = await client.post("/r", json=data)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"body": "fail to validate oneOf"}


async def test_any_of_discriminator(swagger_docs, aiohttp_client):
    async def handler(request, body: Dict):
        """
        ---
        requestBody:
          required: true
          content:
            application/json:
              schema:
                anyOf:
                  - $ref: '#/components/schemas/Cat'
                  - $ref: '#/components/schemas/Dog'
                  - $ref: '#/components/schemas/Lizard'
                discriminator:
                  propertyName: petType
                  mapping:
                    cat_full: '#/components/schemas/Cat'
                    cat_short: Cat

        responses:
          '200':
            description: OK.
        """
        return web.json_response(body)

    swagger = swagger_docs(components="tests/testdata/discriminator.yaml")
    swagger.add_post("/r", handler)

    client = await aiohttp_client(swagger._app)

    data = {"petType": "Cat", "name": "misty"}
    resp = await client.post("/r", json=data)
    assert resp.status == 200
    assert await resp.json() == data

    data = {"petType": "cat_full", "name": "misty"}
    resp = await client.post("/r", json=data)
    assert resp.status == 200
    assert await resp.json() == data

    data = {"petType": "cat_short", "name": "misty"}
    resp = await client.post("/r", json=data)
    assert resp.status == 200
    assert await resp.json() == data

    data = {"petType": "Cat", "name": "misty", "bark": "woof"}
    resp = await client.post("/r", json=data)
    assert resp.status == 200
    assert await resp.json() == data

    data = {"petType": "Dog", "name": "misty", "bark": "woof"}
    resp = await client.post("/r", json=data)
    assert resp.status == 200
    assert await resp.json() == data

    data = {"petType": "Dog", "name": "misty"}
    resp = await client.post("/r", json=data)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"body": "fail to validate anyOf"}


async def test_invalid_discriminator(swagger_docs, aiohttp_client):
    async def handler(request, body: Dict):
        """
        ---
        requestBody:
          required: true
          content:
            application/json:
              schema:
                oneOf:
                  - $ref: '#/components/schemas/Cat'
                  - $ref: '#/components/schemas/Dog'
                  - $ref: '#/components/schemas/Lizard'
                discriminator:
                  propertyName: petType

        responses:
          '200':
            description: OK.
        """
        return web.json_response(body)

    swagger = swagger_docs(components="tests/testdata/discriminator.yaml")
    swagger.add_post("/r", handler)

    client = await aiohttp_client(swagger._app)

    # no discriminator
    data = {"name": "misty"}
    resp = await client.post("/r", json=data)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"body": {"petType": "is required"}}

    # invalid discriminator
    data = {"petType": "Dino", "name": "misty"}
    resp = await client.post("/r", json=data)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    msg = error["body"]["petType"]
    assert msg.startswith("must be one of ")
    schemas = set(literal_eval(msg.replace("must be one of ", "")))
    assert schemas == {"Cat", "Dog", "Lizard"}

    # wrong type
    data = ["hi"]
    resp = await client.post("/r", json=data)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"body": "value should be type of dict"}
