import json
from typing import Dict, Optional

from aiohttp import web

from .helpers import error_to_json


async def test_body(swagger_docs, aiohttp_client):
    async def handler(request, body: Dict):
        """
        ---
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                required:
                  - int
                  - int32
                  - int64
                  - number
                  - float
                  - double
                  - string
                  - boolean
                  - array
                  - object
                properties:
                  int:
                    type: integer
                  int32:
                    type: integer
                    format: int32
                  int64:
                    type: integer
                    format: int64
                  number:
                    type: number
                  float:
                    type: number
                    format: float
                  double:
                    type: number
                    format: double
                  string:
                    type: string
                  boolean:
                    type: boolean
                  array:
                    type: array
                    items:
                      type: integer
                      format: int32
                  object:
                    type: object
                    required:
                      - field
                    properties:
                      field:
                        type: integer

        responses:
          '200':
            description: OK.

        """
        return web.json_response(body)

    swagger = swagger_docs()
    swagger.add_route("POST", "/r", handler)

    client = await aiohttp_client(swagger._app)
    int = 42
    int32 = 32
    int64 = 64
    number = 333.333
    float = 10.111_111
    double = 20.222_222_222_222
    string = "1string1"
    boolean = False
    array = [1, 2, -10, 15, 999, 0]
    object = {"field": 10}
    body = {
        "int": int,
        "int32": int32,
        "int64": int64,
        "number": number,
        "float": float,
        "double": double,
        "string": string,
        "boolean": boolean,
        "array": array,
        "object": object,
    }
    resp = await client.post("/r", json=body)
    assert resp.status == 200
    assert await resp.json() == body

    body = {}
    resp = await client.post("/r", json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    msg = "required property"
    assert error == {
        "body": {
            "int": msg,
            "int32": msg,
            "int64": msg,
            "number": msg,
            "float": msg,
            "double": msg,
            "string": msg,
            "boolean": msg,
            "array": msg,
            "object": msg,
        }
    }

    body = {
        "int": "123",
        "int32": "321",
        "int64": "333",
        "number": "abc",
        "float": "ccc",
        "double": "bca",
        "string": 10,
        "boolean": "false",
        "array": "89",
        "object": 10,
    }
    resp = await client.post("/r", json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {
        "body": {
            "int": "value should be type of int",
            "int32": "value should be type of int",
            "int64": "value should be type of int",
            "number": "value should be type of float",
            "float": "value should be type of float",
            "double": "value should be type of float",
            "string": "value should be type of str",
            "boolean": "value should be type of bool",
            "array": "value should be type of list",
            "object": "value should be type of dict",
        }
    }

    body = {
        "int": None,
        "int32": None,
        "int64": None,
        "number": None,
        "float": None,
        "double": None,
        "string": None,
        "boolean": None,
        "array": None,
        "object": None,
    }
    resp = await client.post("/r", json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {
        "body": {
            "int": "value should be type of int",
            "int32": "value should be type of int",
            "int64": "value should be type of int",
            "number": "value should be type of float",
            "float": "value should be type of float",
            "double": "value should be type of float",
            "string": "value should be type of str",
            "boolean": "value should be type of bool",
            "array": "value should be type of list",
            "object": "value should be type of dict",
        }
    }

    body = {
        "int": {},
        "int32": "10.1",
        "int64": 10.1,
        "number": [],
        "float": "10",
        "double": "bbb",
        "string": 10.1,
        "boolean": 11,
        "array": {},
        "object": [],
    }
    resp = await client.post("/r", json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {
        "body": {
            "int": "value should be type of int",
            "int32": "value should be type of int",
            "int64": "value should be type of int",
            "number": "value should be type of float",
            "float": "value should be type of float",
            "double": "value should be type of float",
            "string": "value should be type of str",
            "boolean": "value should be type of bool",
            "array": "value should be type of list",
            "object": "value should be type of dict",
        }
    }

    body = {
        "int": True,
        "int32": False,
        "int64": True,
        "number": True,
        "float": True,
        "double": False,
        "string": True,
        "boolean": 1,
        "array": True,
        "object": True,
    }
    resp = await client.post("/r", json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {
        "body": {
            "int": "value should be type of int",
            "int32": "value should be type of int",
            "int64": "value should be type of int",
            "number": "value should be type of float",
            "float": "value should be type of float",
            "double": "value should be type of float",
            "string": "value should be type of str",
            "boolean": "value should be type of bool",
            "array": "value should be type of list",
            "object": "value should be type of dict",
        }
    }


async def test_body_with_additional_properties(swagger_docs, aiohttp_client):
    async def handler(request, body: Dict):
        """
        ---
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                additionalProperties: true
                required:
                  - required
                properties:
                  required:
                    type: integer
                  optional:
                    type: integer

        responses:
          '200':
            description: OK.

        """
        return web.json_response(body)

    swagger = swagger_docs()
    swagger.add_route("POST", "/r", handler)

    client = await aiohttp_client(swagger._app)
    body = {"required": 10, "optional": 15, "str": "str", "int": 10}
    resp = await client.post("/r", json=body)
    assert resp.status == 200
    assert await resp.json() == body


async def test_body_with_no_additional_properties(swagger_docs, aiohttp_client):
    async def handler(request, body: Dict):
        """
        ---
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                additionalProperties: false
                required:
                  - required
                properties:
                  required:
                    type: integer
                  optional:
                    type: integer

        responses:
          '200':
            description: OK.

        """
        return web.json_response(body)

    swagger = swagger_docs()
    swagger.add_route("POST", "/r", handler)

    client = await aiohttp_client(swagger._app)
    body = {"required": 10, "optional": 15, "str": "str", "int": 10}
    resp = await client.post("/r", json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {
        "body": {
            "int": "additional property not allowed",
            "str": "additional property not allowed",
        }
    }


async def test_body_with_object_additional_properties(swagger_docs, aiohttp_client):
    async def handler(request, body: Dict):
        """
        ---
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                additionalProperties:
                  type: integer
                required:
                  - required
                properties:
                  required:
                    type: integer
                  optional:
                    type: integer

        responses:
          '200':
            description: OK.

        """
        return web.json_response(body)

    swagger = swagger_docs()
    swagger.add_route("POST", "/r", handler)

    client = await aiohttp_client(swagger._app)
    body = {"required": 10, "optional": 15, "str": 999, "int": 10}
    resp = await client.post("/r", json=body)
    assert resp.status == 200
    assert await resp.json() == body


async def test_deep_nested(swagger_docs, aiohttp_client):
    async def handler(request, body: Dict):
        """
        ---
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                required:
                  - obj1
                  - obj2
                  - arr1
                  - arr2
                properties:
                  obj1:
                    type: object
                    required:
                      - a
                    properties:
                      a:
                        type: array
                        items:
                          type: object
                          required:
                            - b
                          properties:
                            b:
                              type: string
                  obj2:
                    type: object
                    required:
                      - a
                    properties:
                      a:
                        type: object
                        required:
                          - b
                        properties:
                          b:
                            type: object
                            required:
                              - c
                            properties:
                              c:
                                type: string
                  arr1:
                    type: array
                    items:
                      type: array
                      items:
                        type: boolean
                  arr2:
                    type: array
                    items:
                      type: object
                      required:
                        - b
                      properties:
                        b:
                          type: string

        responses:
          '200':
            description: OK.

        """
        return web.json_response(body)

    swagger = swagger_docs()
    swagger.add_route("POST", "/r", handler)

    client = await aiohttp_client(swagger._app)
    body = {
        "obj1": {"a": [{"b": "str1"}, {"b": "str2"}]},
        "obj2": {"a": {"b": {"c": "str"}}},
        "arr1": [[True, False, False], [False, True, True]],
        "arr2": [{"b": "str1"}, {"b": "str2"}],
    }
    resp = await client.post("/r", json=body)
    assert resp.status == 200
    assert await resp.json() == body


async def test_nullable(swagger_docs, aiohttp_client):
    async def handler(request, body: Dict):
        """
        ---
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                nullable: true
                required:
                  - int
                  - int32
                  - int64
                  - number
                  - float
                  - double
                  - string
                  - boolean
                  - array
                  - object
                properties:
                  int:
                    type: integer
                    nullable: true
                  int32:
                    type: integer
                    format: int32
                    nullable: true
                  int64:
                    type: integer
                    format: int64
                    nullable: true
                  number:
                    type: number
                    nullable: true
                  float:
                    type: number
                    format: float
                    nullable: true
                  double:
                    type: number
                    format: double
                    nullable: true
                  string:
                    type: string
                    nullable: true
                  boolean:
                    type: boolean
                    nullable: true
                  array:
                    type: array
                    nullable: true
                    items:
                      type: integer
                      format: int32
                  object:
                    type: object
                    nullable: true
                    required:
                      - field
                    properties:
                      field:
                        type: integer

        responses:
          '200':
            description: OK.

        """
        return web.json_response(body)

    swagger = swagger_docs()
    swagger.add_route("POST", "/r", handler)

    client = await aiohttp_client(swagger._app)

    body = {
        "int": 10,
        "int32": 15,
        "int64": 20,
        "number": 10.1,
        "float": 10.2,
        "double": 10.3,
        "string": "abc",
        "boolean": True,
        "array": [1, 2],
        "object": {"field": 10},
    }
    resp = await client.post("/r", json=body)
    assert resp.status == 200
    assert await resp.json() == body

    body = {
        "int": None,
        "int32": None,
        "int64": None,
        "number": None,
        "float": None,
        "double": None,
        "string": None,
        "boolean": None,
        "array": None,
        "object": None,
    }
    resp = await client.post("/r", json=body)
    assert resp.status == 200
    assert await resp.json() == body


async def test_one_of_object(swagger_docs, aiohttp_client):
    async def handler(request, body: Dict):
        """
        ---
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                required:
                  - object
                properties:
                  object:
                    oneOf:
                      - type: object
                        required:
                          - id
                        properties:
                          id:
                            type: integer
                      - type: object
                        required:
                          - name
                        properties:
                          name:
                            type: string

        responses:
          '200':
            description: OK.

        """
        return web.json_response(body)

    swagger = swagger_docs()
    swagger.add_route("POST", "/r", handler)

    client = await aiohttp_client(swagger._app)

    body = {"object": {"id": 10}}
    resp = await client.post("/r", json=body)
    assert resp.status == 200
    assert await resp.json() == body

    body = {"object": {"name": "string"}}
    resp = await client.post("/r", json=body)
    assert resp.status == 200
    assert await resp.json() == body

    body = {"object": {"test": "value"}}
    resp = await client.post("/r", json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"body": {"object": "fail to validate oneOf"}}

    body = {"object": {"id": "string"}}
    resp = await client.post("/r", json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"body": {"object": "fail to validate oneOf"}}

    body = {"object": {"name": 10}}
    resp = await client.post("/r", json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"body": {"object": "fail to validate oneOf"}}

    body = {"object": {"id": 10, "name": "string"}}
    resp = await client.post("/r", json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"body": {"object": "fail to validate oneOf"}}


async def test_any_of_object(swagger_docs, aiohttp_client):
    async def handler(request, body: Dict):
        """
        ---
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                required:
                  - object
                properties:
                  object:
                    anyOf:
                      - type: object
                        required:
                          - id
                        properties:
                          id:
                            type: integer
                          rank:
                            type: string
                      - type: object
                        required:
                          - name
                        properties:
                          name:
                            type: string
                          age:
                            type: integer

        responses:
          '200':
            description: OK.

        """
        return web.json_response(body)

    swagger = swagger_docs()
    swagger.add_route("POST", "/r", handler)

    client = await aiohttp_client(swagger._app)

    body = {"object": {"id": 10}}
    resp = await client.post("/r", json=body)
    assert resp.status == 200
    assert await resp.json() == body

    body = {"object": {"name": "string"}}
    resp = await client.post("/r", json=body)
    assert resp.status == 200
    assert await resp.json() == body

    body = {"object": {"id": 10, "name": "string", "rank": "123"}}
    resp = await client.post("/r", json=body)
    assert resp.status == 200
    assert await resp.json() == body

    body = {"object": {"test": "value"}}
    resp = await client.post("/r", json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"body": {"object": "fail to validate anyOf"}}

    body = {"object": {"id": "string"}}
    resp = await client.post("/r", json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"body": {"object": "fail to validate anyOf"}}

    body = {"object": {"name": 10}}
    resp = await client.post("/r", json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"body": {"object": "fail to validate anyOf"}}

    body = {"object": {"rank": "321"}}
    resp = await client.post("/r", json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"body": {"object": "fail to validate anyOf"}}

    body = {"object": {"age": 15}}
    resp = await client.post("/r", json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"body": {"object": "fail to validate anyOf"}}


async def test_all_of_object(swagger_docs, aiohttp_client):
    async def handler(request, body: Dict):
        """
        ---
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                required:
                  - object
                properties:
                  object:
                    allOf:
                      - type: object
                        required:
                          - id
                        properties:
                          id:
                            type: integer
                          rank:
                            type: string
                      - type: object
                        required:
                          - name
                        properties:
                          name:
                            type: string
                          age:
                            type: integer

        responses:
          '200':
            description: OK.

        """
        return web.json_response(body)

    swagger = swagger_docs()
    swagger.add_route("POST", "/r", handler)

    client = await aiohttp_client(swagger._app)

    body = {"object": {"id": 10, "name": "string", "age": 15, "rank": "123"}}
    resp = await client.post("/r", json=body)
    assert resp.status == 200
    assert await resp.json() == body

    body = {
        "object": {
            "id": 10,
            "name": "string",
            "age": 15,
            "rank": "123",
            "not_in_schema": "definitely",
        }
    }
    resp = await client.post("/r", json=body)
    assert resp.status == 200
    assert await resp.json() == body

    body = {"object": {"id": 10, "name": "string"}}
    resp = await client.post("/r", json=body)
    assert resp.status == 200
    assert await resp.json() == body

    body = {"object": {"id": 10}}
    resp = await client.post("/r", json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"body": {"object": {"name": "required property"}}}

    body = {"object": {"name": "string"}}
    resp = await client.post("/r", json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"body": {"object": {"id": "required property"}}}

    body = {"object": {"test": "value"}}
    resp = await client.post("/r", json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"body": {"object": {"id": "required property"}}}

    body = {"object": {"id": 10, "name": "string", "age": 10.1}}
    resp = await client.post("/r", json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"body": {"object": {"age": "value should be type of int"}}}

    body = {"object": {"rank": "321"}}
    resp = await client.post("/r", json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"body": {"object": {"id": "required property"}}}

    body = {"object": {"age": 15}}
    resp = await client.post("/r", json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"body": {"object": {"id": "required property"}}}


async def test_array_in_object(swagger_docs, aiohttp_client):
    async def handler(request, body: Dict):
        """
        ---
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                required:
                  - array
                properties:
                  array:
                    type: array
                    items:
                      type: integer

        responses:
          '200':
            description: OK.

        """
        return web.json_response(body)

    swagger = swagger_docs()
    swagger.add_route("POST", "/r", handler)

    client = await aiohttp_client(swagger._app)

    body = {"array": []}
    resp = await client.post("/r", json=body)
    assert resp.status == 200
    assert await resp.json() == body

    body = {"array": [1, 2, 3]}
    resp = await client.post("/r", json=body)
    assert resp.status == 200
    assert await resp.json() == body

    body = {"array": ["1", 2, 3]}
    resp = await client.post("/r", json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"body": {"array": {"0": "value should be type of int"}}}

    body = {"array": [1, 2.2, 3]}
    resp = await client.post("/r", json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"body": {"array": {"1": "value should be type of int"}}}

    body = {"array": [1, 2, True]}
    resp = await client.post("/r", json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"body": {"array": {"2": "value should be type of int"}}}


async def test_float_as_int(swagger_docs, aiohttp_client):
    async def handler(request, body: Dict):
        """
        ---
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                required:
                  - int_float
                  - int_double
                properties:
                  int_float:
                    type: number
                    format: float
                  int_double:
                    type: number
                    format: double

        responses:
          '200':
            description: OK.

        """
        return web.json_response(body)

    swagger = swagger_docs()
    swagger.add_route("POST", "/r", handler)

    client = await aiohttp_client(swagger._app)

    int_float = 10
    int_double = 20
    body = {"int_float": int_float, "int_double": int_double}
    resp = await client.post("/r", json=body)
    assert resp.status == 200
    assert await resp.json() == body


async def test_min_max_properties(swagger_docs, aiohttp_client):
    async def handler(request, body: Dict):
        """
        ---
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                minProperties: 2
                maxProperties: 5

        responses:
          '200':
            description: OK.

        """
        return web.json_response(body)

    swagger = swagger_docs()
    swagger.add_route("POST", "/r", handler)

    client = await aiohttp_client(swagger._app)

    body = {"str1": "str1", "str2": "str1", "str3": "str1"}
    resp = await client.post("/r", json=body)
    assert resp.status == 200
    assert await resp.json() == body

    body = {"str1": "str1"}
    resp = await client.post("/r", json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"body": "number or properties must be more than 2"}

    body = {
        "str1": "str1",
        "str2": "str1",
        "str3": "str1",
        "str4": "str1",
        "str5": "str1",
        "str6": "str1",
    }
    resp = await client.post("/r", json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"body": "number or properties must be less than 5"}


async def test_body_with_optional_properties(swagger_docs, aiohttp_client):
    async def handler(request, body: Dict):
        """
        ---
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                required:
                  - required
                properties:
                  required:
                    type: integer
                  optional:
                    type: integer

        responses:
          '200':
            description: OK.

        """
        return web.json_response(body)

    swagger = swagger_docs()
    swagger.add_route("POST", "/r", handler)

    client = await aiohttp_client(swagger._app)
    body = {"required": 10}
    resp = await client.post("/r", json=body)
    assert resp.status == 200
    assert await resp.json() == body

    body = {"required": 10, "optional": 15}
    resp = await client.post("/r", json=body)
    assert resp.status == 200
    assert await resp.json() == body


async def test_media_type_with_charset(swagger_docs, aiohttp_client):
    async def handler(request, body: Dict):
        """
        ---
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                required:
                  - required
                properties:
                  required:
                    type: integer
                  optional:
                    type: integer

        responses:
          '200':
            description: OK.

        """
        return web.json_response(body)

    swagger = swagger_docs()
    swagger.add_route("POST", "/r", handler)

    client = await aiohttp_client(swagger._app)

    body = {"required": 10}
    resp = await client.post(
        "/r",
        data=json.dumps(body),
        headers={"content-type": "application/json; charset=UTF-8"},
    )
    assert resp.status == 200
    assert await resp.json() == body


async def test_incorrect_json_body(swagger_docs, aiohttp_client):
    async def handler(request, body: Dict):
        """
        ---
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                required:
                  - required
                properties:
                  required:
                    type: integer
                  optional:
                    type: integer

        responses:
          '200':
            description: OK.

        """
        return web.json_response(body)

    swagger = swagger_docs()
    swagger.add_route("POST", "/r", handler)

    client = await aiohttp_client(swagger._app)

    resp = await client.post("/r", data="{{", headers={"content-type": "application/json"})
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"body": "Expecting property name enclosed in double quotes: line 1 column 2 (char 1)"}


async def test_form_data(swagger_docs, aiohttp_client):
    async def handler(request, body: Dict):
        """
        ---
        requestBody:
          required: true
          content:
            application/x-www-form-urlencoded:
              schema:
                type: object
                properties:
                  integer:
                    type: integer
                  number:
                    type: number
                  string:
                    type: string
                  boolean:
                    type: boolean

        responses:
          '200':
            description: OK.

        """
        return web.json_response(body)

    swagger = swagger_docs()
    swagger.add_route("POST", "/r", handler)

    client = await aiohttp_client(swagger._app)

    integer = 15
    number = 15.5
    string = "string"
    boolean = True
    data = {
        "integer": integer,
        "number": number,
        "string": string,
        "boolean": str(boolean).lower(),
    }
    resp = await client.post("/r", data=data)
    assert resp.status == 200
    assert await resp.json() == {
        "integer": integer,
        "number": number,
        "string": string,
        "boolean": boolean,
    }


async def test_object_can_have_optional_props(swagger_docs, aiohttp_client):
    routes = web.RouteTableDef()

    @routes.post("/r")
    async def handler(request, body: Dict):
        """
        ---
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  integer:
                    type: integer
                  string:
                    type: string
                  array:
                    type: array
                    items:
                      type: string
                  object:
                    type: object

        responses:
          '200':
            description: OK.
        """
        return web.json_response(body)

    swagger = swagger_docs()
    swagger.add_routes(routes)

    client = await aiohttp_client(swagger._app)

    resp = await client.post("/r", json={})
    assert resp.status == 200
    assert await resp.json() == {}


async def test_no_content_type(swagger_docs, aiohttp_client):
    async def handler(request, body: Optional[Dict] = None):
        """
        ---
        requestBody:
          content:
            application/json:
              schema:
                type: object
                required:
                  - required
                properties:
                  required:
                    type: integer

        responses:
          '200':
            description: OK.

        """
        return web.json_response(body)

    swagger = swagger_docs()
    swagger.add_route("POST", "/r", handler)

    client = await aiohttp_client(swagger._app)

    resp = await client.post("/r", skip_auto_headers=("Content-Type",))
    assert resp.status == 200
    assert await resp.json() is None


async def test_no_content_type_body_required(swagger_docs, aiohttp_client):
    async def handler(request, body: Dict):
        """
        ---
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                required:
                  - required
                properties:
                  required:
                    type: integer

        responses:
          '200':
            description: OK.

        """
        return web.json_response(body)

    swagger = swagger_docs()
    swagger.add_route("POST", "/r", handler)

    client = await aiohttp_client(swagger._app)

    resp = await client.post("/r", skip_auto_headers=("Content-Type",))
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"body": "is required"}

    resp = await client.post("/r", skip_auto_headers=("Content-Type",), data="payload")
    assert resp.status == 400
    assert error == {"body": "is required"}


async def test_required_no_content_type(swagger_docs, aiohttp_client):
    async def handler(request, body: Dict):
        """
        ---
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                required:
                  - required
                properties:
                  required:
                    type: integer

        responses:
          '200':
            description: OK.

        """
        return web.json_response(body)

    swagger = swagger_docs()
    swagger.add_route("POST", "/r", handler)

    client = await aiohttp_client(swagger._app)

    resp = await client.post("/r", skip_auto_headers=("Content-Type",))
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"body": "is required"}


async def test_no_handler(swagger_docs, aiohttp_client):
    async def handler(request, body: Optional[Dict] = None):
        """
        ---
        requestBody:
          content:
            application/x-www-form-urlencoded:
              schema:
                type: object
                required:
                  - required
                properties:
                  required:
                    type: integer

        responses:
          '200':
            description: OK.

        """
        return web.json_response(body)

    swagger = swagger_docs()
    swagger.add_route("POST", "/r", handler)

    client = await aiohttp_client(swagger._app)

    body = {"required": 10}
    resp = await client.post("/r", json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"body": "no handler for application/json"}


async def test_wrong_body(swagger_docs, aiohttp_client):
    async def handler(request, body: Dict):
        """
        ---
        requestBody:
          required: true
          content:
            application/x-www-form-urlencoded:
              schema:
                type: object
                required:
                  - required
                properties:
                  required:
                    type: integer

        responses:
          '200':
            description: OK.

        """
        return web.json_response(body)

    swagger = swagger_docs()
    swagger.add_route("POST", "/r", handler)

    client = await aiohttp_client(swagger._app)

    body = {"required": 10}
    resp = await client.post("/r", json=body)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"body": "no handler for application/json"}


async def test_nullable_ref(swagger_docs_with_components, aiohttp_client):
    routes = web.RouteTableDef()

    @routes.post("/r")
    async def handler(request, body: Dict):
        """
        ---
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                required:
                  - pet
                properties:
                  pet:
                    nullable: true
                    allOf:
                      - $ref: '#/components/schemas/Pet'

        responses:
          '200':
            description: OK.
        """
        return web.json_response(body)

    swagger = swagger_docs_with_components()
    swagger.add_routes(routes)

    client = await aiohttp_client(swagger._app)

    body = {
        "pet": None,
    }
    resp = await client.post("/r", json=body)
    assert resp.status == 200
    assert await resp.json() == body

    body = {
        "pet": {
            "name": "lizzy",
            "age": 12,
        }
    }
    resp = await client.post("/r", json=body)
    assert resp.status == 200
    assert await resp.json() == body


async def test_optional_body_implicit(swagger_docs, aiohttp_client):
    async def handler(request, body: Optional[Dict]):
        """
        ---
        requestBody:
          content:
            application/json:
              schema:
                type: object
                required:
                  - required
                properties:
                  required:
                    type: integer

        responses:
          '200':
            description: OK.

        """
        return web.json_response(body)

    swagger = swagger_docs()
    swagger.add_route("POST", "/r", handler)

    client = await aiohttp_client(swagger._app)

    resp = await client.post("/r")
    assert resp.status == 200
    assert await resp.json() is None

    body = {"required": 10}
    resp = await client.post("/r", json=body)
    assert resp.status == 200
    assert await resp.json() == body


async def test_optional_body_explicit(swagger_docs, aiohttp_client):
    async def handler(request, body: Optional[Dict]):
        """
        ---
        requestBody:
          required: false
          content:
            application/json:
              schema:
                type: object
                required:
                  - required
                properties:
                  required:
                    type: integer

        responses:
          '200':
            description: OK.

        """
        return web.json_response(body)

    swagger = swagger_docs()
    swagger.add_route("POST", "/r", handler)

    client = await aiohttp_client(swagger._app)

    resp = await client.post("/r")
    assert resp.status == 200
    assert await resp.json() is None

    body = {"required": 10}
    resp = await client.post("/r", json=body)
    assert resp.status == 200
    assert await resp.json() == body
