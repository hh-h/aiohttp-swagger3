from ast import literal_eval
from typing import Dict, List, Optional, Union

from aiohttp import web

from aiohttp_swagger3 import SwaggerDocs, SwaggerFile


def error_to_json(error: str) -> Dict:
    return literal_eval(error.replace("400: ", ""))


async def no_doc_handler(request):
    return web.json_response()


async def minimum_maximum_handler(
    request,
    path_int: int,
    path_float: float,
    query_int: int,
    query_float: float,
    body: Dict,
):
    """
    ---
    parameters:

      - name: query_int
        in: query
        required: true
        schema:
          type: integer
          minimum: 10
          maximum: 20

      - name: query_float
        in: query
        required: true
        schema:
          type: number
          minimum: 10.1
          maximum: 19.9

      - name: path_int
        in: path
        required: true
        schema:
          type: integer
          minimum: 10
          maximum: 20

      - name: path_float
        in: path
        required: true
        schema:
          type: number
          minimum: 10.1
          maximum: 19.9

    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - int
              - float
            properties:
              int:
                type: integer
                minimum: 10
                maximum: 20
              float:
                type: number
                minimum: 10.1
                maximum: 19.9

    responses:
      '200':
        description: OK.

    """
    return web.json_response(
        {
            "query_int": query_int,
            "query_float": query_float,
            "path_int": path_int,
            "path_float": path_float,
            "body": body,
        }
    )


async def query_array(request, query1: List[int], query2: List[int] = None):
    """
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


async def exclusive_minimum_maximum_handler(
    request,
    path_int: int,
    path_float: float,
    query_int: int,
    query_float: float,
    body: Dict,
):
    """
    ---
    parameters:

      - name: query_int
        in: query
        required: true
        schema:
          type: integer
          minimum: 10
          maximum: 20
          exclusiveMinimum: true
          exclusiveMaximum: true

      - name: query_float
        in: query
        required: true
        schema:
          type: number
          minimum: 10.1
          maximum: 19.9
          exclusiveMinimum: true
          exclusiveMaximum: true

      - name: path_int
        in: path
        required: true
        schema:
          type: integer
          minimum: 10
          maximum: 20
          exclusiveMinimum: true
          exclusiveMaximum: true

      - name: path_float
        in: path
        required: true
        schema:
          type: number
          minimum: 10.1
          maximum: 19.9
          exclusiveMinimum: true
          exclusiveMaximum: true

    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - int
              - float
            properties:
              int:
                type: integer
                minimum: 10
                maximum: 20
                exclusiveMinimum: true
                exclusiveMaximum: true
              float:
                type: number
                minimum: 10.1
                maximum: 19.9
                exclusiveMinimum: true
                exclusiveMaximum: true

    responses:
      '200':
        description: OK.

    """
    return web.json_response(
        {
            "query_int": query_int,
            "query_float": query_float,
            "path_int": path_int,
            "path_float": path_float,
            "body": body,
        }
    )


async def int32_bounds_handler(request, path: int, query: int, body: Dict):
    """
    ---
    parameters:

      - name: query
        in: query
        required: true
        schema:
          type: integer
          format: int32

      - name: path
        in: path
        required: true
        schema:
          type: integer
          format: int32

    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - int
            properties:
              int:
                type: integer
                format: int32

    responses:
      '200':
        description: OK.

    """
    return web.json_response({"query": query, "path": path, "body": body})


async def float_as_int_handler(request, body: Dict):
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


async def corner_cases_handler(
    request, int32: int, int64: int, float: float, double: float
):
    """
    ---
    parameters:

      - name: int32
        in: query
        required: true
        schema:
          type: integer
          format: int32

      - name: int64
        in: query
        required: true
        schema:
          type: integer
          format: int64

      - name: float
        in: query
        required: true
        schema:
          type: number
          format: float

      - name: double
        in: query
        required: true
        schema:
          type: number
          format: double

    responses:
      '200':
        description: OK.

    """
    return web.json_response(
        {"int32": int32, "int64": int64, "float": float, "double": double}
    )


async def min_max_properties_handler(request, body: Dict):
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


async def min_max_items_handler(
    request, header: List[int], query: List[int], body: Dict
):
    """
    ---
    parameters:

      - name: header
        in: header
        required: true
        schema:
          type: array
          items:
            type: integer
          minItems: 2
          maxItems: 5

      - name: query
        in: query
        required: true
        schema:
          type: array
          items:
            type: integer
          minItems: 2
          maxItems: 5

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
                minItems: 2
                maxItems: 5

    responses:
      '200':
        description: OK.

    """
    return web.json_response({"query": query, "header": header, "body": body})


async def unique_items_handler(
    request, header: List[int], query: List[int], body: Dict
):
    """
    ---
    parameters:

      - name: header
        in: header
        required: true
        schema:
          type: array
          items:
            type: integer
          uniqueItems: true

      - name: query
        in: query
        required: true
        schema:
          type: array
          items:
            type: integer
          uniqueItems: true

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
                uniqueItems: true

    responses:
      '200':
        description: OK.

    """
    return web.json_response({"query": query, "header": header, "body": body})


async def min_max_length_handler(
    request, header: str, path: str, query: str, body: Dict
):
    """
    ---
    parameters:

      - name: header
        in: header
        required: true
        schema:
          type: string
          minLength: 5
          maxLength: 10

      - name: query
        in: query
        required: true
        schema:
          type: string
          minLength: 5
          maxLength: 10

      - name: path
        in: path
        required: true
        schema:
          type: string
          minLength: 5
          maxLength: 10

    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - str
            properties:
              str:
                type: string
                minLength: 5
                maxLength: 10

    responses:
      '200':
        description: OK.

    """
    return web.json_response(
        {"header": header, "query": query, "path": path, "body": body}
    )


async def parameter_ref_handler(request, month: int):
    """
    ---
    parameters:

      - $ref: '#/components/parameters/Month'

    responses:
      '200':
        description: OK.

    """
    return web.json_response({"month": month})


async def body_handler(request, body: Dict):
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


async def body_with_optional_properties_handler(request, body: Dict):
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


async def body_with_additional_properties_handler(request, body: Dict):
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


async def body_with_no_additional_properties_handler(request, body: Dict):
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


async def body_with_object_additional_properties_handler(request, body: Dict):
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


async def deep_nested_body_handler(request, body: Dict):
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


async def nullable_handler(request, body: Dict):
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


async def one_of_basic_handler(request, int_or_bool: Union[int, bool], body: Dict):
    """
    ---
    parameters:

      - name: int_or_bool
        in: query
        required: true
        schema:
          oneOf:
            - type: integer
            - type: boolean

    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - int_or_bool
            properties:
              int_or_bool:
                oneOf:
                  - type: integer
                  - type: boolean

    responses:
      '200':
        description: OK.

    """
    return web.json_response({"int_or_bool": int_or_bool, "body": body})


async def one_of_object_handler(request, body: Dict):
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


async def any_of_object_handler(request, body: Dict):
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


async def all_of_object_handler(request, body: Dict):
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


async def int32_array_handler(request, array: List[int]):
    """
    ---
    parameters:

      - name: array
        in: query
        required: true
        schema:
          type: array
          items:
            type: integer
            format: int32

    responses:
      '200':
        description: OK.

    """
    return web.json_response(array)


async def array_in_object_handler(request, body: Dict):
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


async def enum_handler(request, integer: int, string: str, number: float):
    """
    ---
    parameters:

      - name: integer
        in: query
        required: true
        schema:
          type: integer
          enum: [1, 5, 10]

      - name: string
        in: query
        required: true
        schema:
          type: string
          enum: [abc, bca]

      - name: number
        in: query
        required: true
        schema:
          type: number
          enum: [10.1, 10.2]

    responses:
      '200':
        description: OK.

    """
    return web.json_response({"integer": integer, "string": string, "number": number})


async def body_ref_handler(request, body: Dict):
    """
    ---
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Pet'

    responses:
      '200':
        description: OK.

    """
    return web.json_response(body)


async def primitives_handler(
    request,
    int: int,
    int32: int,
    int64: int,
    number: float,
    float: float,
    double: float,
    string: str,
    boolean: bool,
):
    """
    ---
    parameters:

      - name: int
        in: query
        required: true
        schema:
          type: integer

      - name: int32
        in: query
        required: true
        schema:
          type: integer
          format: int32

      - name: int64
        in: query
        required: true
        schema:
          type: integer
          format: int64

      - name: number
        in: query
        required: true
        schema:
          type: number

      - name: float
        in: query
        required: true
        schema:
          type: number
          format: float

      - name: double
        in: query
        required: true
        schema:
          type: number
          format: double

      - name: string
        in: query
        required: true
        schema:
          type: string

      - name: boolean
        in: query
        required: true
        schema:
          type: boolean

    responses:
      '200':
        description: OK.

    """
    return web.json_response(
        {
            "int": int,
            "int32": int32,
            "int64": int64,
            "number": number,
            "float": float,
            "double": double,
            "string": string,
            "boolean": boolean,
        }
    )


async def string_formats_handler(
    request,
    date: str,
    datetime: str,
    password: str,
    byte: str,
    binary: str,
    email: str,
    uuid: str,
    hostname: str,
    ipv4: str,
    ipv6: str,
):
    """
    ---
    parameters:

      - name: date
        in: query
        required: true
        schema:
          type: string
          format: date

      - name: datetime
        in: query
        required: true
        schema:
          type: string
          format: date-time

      - name: password
        in: query
        required: true
        schema:
          type: string
          format: password

      - name: byte
        in: query
        required: true
        schema:
          type: string
          format: byte

      - name: binary
        in: query
        required: true
        schema:
          type: string
          format: binary

      - name: email
        in: query
        required: true
        schema:
          type: string
          format: email

      - name: uuid
        in: query
        required: true
        schema:
          type: string
          format: uuid

      - name: hostname
        in: query
        required: true
        schema:
          type: string
          format: hostname

      - name: ipv4
        in: query
        required: true
        schema:
          type: string
          format: ipv4

      - name: ipv6
        in: query
        required: true
        schema:
          type: string
          format: ipv6

    responses:
      '200':
        description: OK.

    """
    return web.json_response(
        {
            "date": date,
            "datetime": datetime,
            "password": password,
            "byte": byte,
            "binary": binary,
            "email": email,
            "uuid": uuid,
            "hostname": hostname,
            "ipv4": ipv4,
            "ipv6": ipv6,
        }
    )


async def default_handler(
    request, integer: int, number: float, string: str, boolean: bool, body: Dict
):
    """
    ---
    parameters:

      - name: integer
        in: query
        schema:
          type: integer
          default: 15

      - name: number
        in: query
        schema:
          type: number
          default: 15.5

      - name: string
        in: query
        schema:
          type: string
          default: string

      - name: boolean
        in: query
        schema:
          type: boolean
          default: True

    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              integer:
                type: integer
                default: 15
              number:
                type: number
                default: 15.5
              string:
                type: string
                default: string
              boolean:
                type: boolean
                default: true

    responses:
      '200':
        description: OK.

    """
    return web.json_response(
        {
            "integer": integer,
            "number": number,
            "string": string,
            "boolean": boolean,
            "body": body,
        }
    )


async def optional_handler(
    request,
    body: Dict,
    integer: Optional[int] = None,
    number: Optional[float] = None,
    string: Optional[str] = None,
    boolean: Optional[bool] = None,
):
    """
    ---
    parameters:

      - name: integer
        in: query
        schema:
          type: integer

      - name: number
        in: query
        schema:
          type: number

      - name: string
        in: query
        schema:
          type: string

      - name: boolean
        in: query
        schema:
          type: boolean

    requestBody:
      required: true
      content:
        application/json:
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
    resp = {"body": body}
    if integer is not None:
        resp["integer"] = integer
    if number is not None:
        resp["number"] = number
    if string is not None:
        resp["string"] = string
    if boolean is not None:
        resp["boolean"] = boolean

    return web.json_response(resp)


async def headers_handler(request):
    """
    ---
    parameters:

      - name: x-request-id
        in: header
        required: true
        schema:
          type: string

    responses:
      '200':
        description: OK.

    """
    return web.json_response({"x-request-id": request["data"]["x-request-id"]})


async def pattern_handler(request, string: str):
    """
    ---
    parameters:

      - name: string
        in: query
        required: true
        schema:
          type: string
          pattern: ^\\d{3}$

    responses:
      '200':
        description: OK.

    """
    return web.json_response({"string": string})


async def path_handler(request, param_id: int):
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


async def get_all_pets(request, limit: Optional[int] = None):
    pets = []
    for i in range(limit or 3):
        pets.append({"id": i, "name": f"pet_{i}", "tag": f"tag_{i}"})
    return web.json_response(pets)


async def create_pet(request):
    return web.json_response(status=201)


async def get_one_pet(request, pet_id: int):
    if pet_id in (1, 2, 3):
        return web.json_response(
            {"id": pet_id, "name": f"pet_{pet_id}", "tag": f"tag_{pet_id}"}
        )
    return web.json_response(
        {"code": 10, "message": f"pet with ID '{pet_id}' not found"}, status=500
    )


async def test_primitives(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")
    s.add_route("GET", "/r", primitives_handler)

    client = await aiohttp_client(app)
    int = 42
    int32 = 32
    int64 = 64
    number = 333.333
    float = 10.111_111
    double = 20.222_222_222_222
    string = "1string1"
    boolean = False
    resp = await client.get(
        "/r",
        params={
            "int": int,
            "int32": int32,
            "int64": int64,
            "number": str(number),
            "float": str(float),
            "double": str(double),
            "string": string,
            "boolean": str(boolean).lower(),
        },
    )
    assert resp.status == 200
    json = await resp.json()
    assert json == {
        "int": int,
        "int32": int32,
        "int64": int64,
        "number": number,
        "float": float,
        "double": double,
        "string": string,
        "boolean": boolean,
    }


async def test_default(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")
    s.add_route("GET", "/r", default_handler)

    client = await aiohttp_client(app)
    resp = await client.get("/r", json={})
    assert resp.status == 200
    json = await resp.json()
    assert json == {
        "integer": 15,
        "number": 15.5,
        "string": "string",
        "boolean": True,
        "body": {"integer": 15, "number": 15.5, "string": "string", "boolean": True},
    }


async def test_optional(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")
    s.add_route("GET", "/r", optional_handler)

    client = await aiohttp_client(app)
    resp = await client.get("/r", json={})
    assert resp.status == 200
    json = await resp.json()
    assert json == {"body": {}}

    params = {
        "integer": 15,
        "number": str(15.5),
        "string": "string",
        "boolean": str(True).lower(),
    }
    body = {"integer": 15, "number": 15.5, "string": "string", "boolean": True}

    resp = await client.get("/r", params=params, json=body)
    assert resp.status == 200
    json = await resp.json()
    assert json == {
        "integer": 15,
        "number": 15.5,
        "string": "string",
        "boolean": True,
        "body": {"integer": 15, "number": 15.5, "string": "string", "boolean": True},
    }


async def test_body(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")
    s.add_route("GET", "/r", body_handler)

    client = await aiohttp_client(app)
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
    resp = await client.get("/r", json=body)
    assert resp.status == 200
    json = await resp.json()
    assert json == body

    body = {}
    resp = await client.get("/r", json=body)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    msg = "required property"
    assert json == {
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
    resp = await client.get("/r", json=body)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    assert json == {
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
    resp = await client.get("/r", json=body)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    assert json == {
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
    resp = await client.get("/r", json=body)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    assert json == {
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
    resp = await client.get("/r", json=body)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    assert json == {
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


async def test_deep_nested(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")
    s.add_route("GET", "/r", deep_nested_body_handler)

    client = await aiohttp_client(app)
    body = {
        "obj1": {"a": [{"b": "str1"}, {"b": "str2"}]},
        "obj2": {"a": {"b": {"c": "str"}}},
        "arr1": [[True, False, False], [False, True, True]],
        "arr2": [{"b": "str1"}, {"b": "str2"}],
    }
    resp = await client.get("/r", json=body)
    assert resp.status == 200
    json = await resp.json()
    assert json == body


async def test_array(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")
    s.add_route("GET", "/r", int32_array_handler)

    client = await aiohttp_client(app)
    a = [1, 2, -10, 15, 999, 0]
    resp = await client.get("/r", params={"array": ",".join(str(x) for x in a)})
    assert resp.status == 200
    json = await resp.json()
    assert json == a


async def test_ref(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs", components="tests/testdata/components.yaml")
    s.add_route("GET", "/r", body_ref_handler)

    client = await aiohttp_client(app)
    body = {"name": "pet", "age": 15}
    resp = await client.get("/r", json=body)
    assert resp.status == 200
    json = await resp.json()
    assert json == body


async def test_nullable(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")
    s.add_route("GET", "/r", nullable_handler)

    client = await aiohttp_client(app)

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
    resp = await client.get("/r", json=body)
    assert resp.status == 200
    json = await resp.json()
    assert json == body

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
    resp = await client.get("/r", json=body)
    assert resp.status == 200
    json = await resp.json()
    assert json == body


async def test_one_of_basic(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")
    s.add_route("GET", "/r", one_of_basic_handler)

    client = await aiohttp_client(app)
    params = {"int_or_bool": 10}
    body = {"int_or_bool": True}
    resp = await client.get("/r", params=params, json=body)
    assert resp.status == 200
    json = await resp.json()
    assert json == {"int_or_bool": 10, "body": body}

    params = {"int_or_bool": "true"}
    body = {"int_or_bool": 10}
    resp = await client.get("/r", params=params, json=body)
    assert resp.status == 200
    json = await resp.json()
    assert json == {"int_or_bool": True, "body": body}

    params = {"int_or_bool": "abc"}
    body = {"int_or_bool": "bca"}
    resp = await client.get("/r", params=params, json=body)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    assert json == {
        "int_or_bool": "fail to validate oneOf",
        "body": {"int_or_bool": "fail to validate oneOf"},
    }


async def test_one_of_object(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")
    s.add_route("GET", "/r", one_of_object_handler)

    client = await aiohttp_client(app)

    body = {"object": {"id": 10}}
    resp = await client.get("/r", json=body)
    assert resp.status == 200
    json = await resp.json()
    assert json == body

    body = {"object": {"name": "string"}}
    resp = await client.get("/r", json=body)
    assert resp.status == 200
    json = await resp.json()
    assert json == body

    body = {"object": {"test": "value"}}
    resp = await client.get("/r", json=body)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    assert json == {"body": {"object": "fail to validate oneOf"}}

    body = {"object": {"id": "string"}}
    resp = await client.get("/r", json=body)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    assert json == {"body": {"object": "fail to validate oneOf"}}

    body = {"object": {"name": 10}}
    resp = await client.get("/r", json=body)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    assert json == {"body": {"object": "fail to validate oneOf"}}

    body = {"object": {"id": 10, "name": "string"}}
    resp = await client.get("/r", json=body)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    assert json == {"body": {"object": "fail to validate oneOf"}}


async def test_any_of_object(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")
    s.add_route("GET", "/r", any_of_object_handler)

    client = await aiohttp_client(app)

    body = {"object": {"id": 10}}
    resp = await client.get("/r", json=body)
    assert resp.status == 200
    json = await resp.json()
    assert json == body

    body = {"object": {"name": "string"}}
    resp = await client.get("/r", json=body)
    assert resp.status == 200
    json = await resp.json()
    assert json == body

    body = {"object": {"id": 10, "name": "string", "rank": "123"}}
    resp = await client.get("/r", json=body)
    assert resp.status == 200
    json = await resp.json()
    assert json == body

    body = {"object": {"test": "value"}}
    resp = await client.get("/r", json=body)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    assert json == {"body": {"object": "fail to validate anyOf"}}

    body = {"object": {"id": "string"}}
    resp = await client.get("/r", json=body)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    assert json == {"body": {"object": "fail to validate anyOf"}}

    body = {"object": {"name": 10}}
    resp = await client.get("/r", json=body)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    assert json == {"body": {"object": "fail to validate anyOf"}}

    body = {"object": {"rank": "321"}}
    resp = await client.get("/r", json=body)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    assert json == {"body": {"object": "fail to validate anyOf"}}

    body = {"object": {"age": 15}}
    resp = await client.get("/r", json=body)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    assert json == {"body": {"object": "fail to validate anyOf"}}


async def test_all_of_object(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")
    s.add_route("GET", "/r", all_of_object_handler)

    client = await aiohttp_client(app)

    body = {"object": {"id": 10, "name": "string", "age": 15, "rank": "123"}}
    resp = await client.get("/r", json=body)
    assert resp.status == 200
    json = await resp.json()
    assert json == body

    body = {
        "object": {
            "id": 10,
            "name": "string",
            "age": 15,
            "rank": "123",
            "not_in_schema": "definitely",
        }
    }
    resp = await client.get("/r", json=body)
    assert resp.status == 200
    json = await resp.json()
    assert json == body

    body = {"object": {"id": 10, "name": "string"}}
    resp = await client.get("/r", json=body)
    assert resp.status == 200
    json = await resp.json()
    assert json == body

    body = {"object": {"id": 10}}
    resp = await client.get("/r", json=body)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    assert json == {"body": {"object": "fail to validate allOf"}}

    body = {"object": {"name": "string"}}
    resp = await client.get("/r", json=body)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    assert json == {"body": {"object": "fail to validate allOf"}}

    body = {"object": {"test": "value"}}
    resp = await client.get("/r", json=body)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    assert json == {"body": {"object": "fail to validate allOf"}}

    body = {"object": {"id": 10, "name": "string", "age": 10.1}}
    resp = await client.get("/r", json=body)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    assert json == {"body": {"object": "fail to validate allOf"}}

    body = {"object": {"rank": "321"}}
    resp = await client.get("/r", json=body)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    assert json == {"body": {"object": "fail to validate allOf"}}

    body = {"object": {"age": 15}}
    resp = await client.get("/r", json=body)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    assert json == {"body": {"object": "fail to validate allOf"}}


async def test_body_with_optional_properties(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")
    s.add_route("GET", "/r", body_with_optional_properties_handler)

    client = await aiohttp_client(app)
    body = {"required": 10}
    resp = await client.get("/r", json=body)
    assert resp.status == 200
    json = await resp.json()
    assert json == body

    body = {"required": 10, "optional": 15}
    resp = await client.get("/r", json=body)
    assert resp.status == 200
    json = await resp.json()
    assert json == body


async def test_body_with_additional_properties(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")
    s.add_route("GET", "/r", body_with_additional_properties_handler)

    client = await aiohttp_client(app)
    body = {"required": 10, "optional": 15, "str": "str", "int": 10}
    resp = await client.get("/r", json=body)
    assert resp.status == 200
    json = await resp.json()
    assert json == body


async def test_body_with_no_additional_properties(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")
    s.add_route("GET", "/r", body_with_no_additional_properties_handler)

    client = await aiohttp_client(app)
    body = {"required": 10, "optional": 15, "str": "str", "int": 10}
    resp = await client.get("/r", json=body)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    assert json == {
        "body": {
            "int": "additional property not allowed",
            "str": "additional property not allowed",
        }
    }


async def test_body_with_object_additional_properties(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")
    s.add_route("GET", "/r", body_with_object_additional_properties_handler)

    client = await aiohttp_client(app)
    body = {"required": 10, "optional": 15, "str": 999, "int": 10}
    resp = await client.get("/r", json=body)
    assert resp.status == 200
    json = await resp.json()
    assert json == body


async def test_enum(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")
    s.add_route("GET", "/r", enum_handler)

    client = await aiohttp_client(app)
    integer = 10
    string = "abc"
    number = 10.1
    params = {"integer": integer, "string": string, "number": str(number)}
    resp = await client.get("/r", params=params)
    assert resp.status == 200
    json = await resp.json()
    assert json == {"integer": integer, "string": string, "number": number}

    integer = 100
    string = "abcd"
    number = 10.3
    params = {"integer": integer, "string": string, "number": str(number)}
    resp = await client.get("/r", params=params)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    assert json == {
        "integer": "value should be one of [1, 5, 10]",
        "string": "value should be one of ['abc', 'bca']",
        "number": "value should be one of [10.1, 10.2]",
    }


async def test_header(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")
    s.add_route("GET", "/r", headers_handler)

    client = await aiohttp_client(app)

    headers = {"x-request-id": "some_request_id"}
    resp = await client.get("/r", headers=headers)
    assert resp.status == 200
    json = await resp.json()
    assert json == headers


async def test_path(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")
    s.add_route("GET", "/r/{param_id}", path_handler)

    client = await aiohttp_client(app)

    resp = await client.get("/r/10")
    assert resp.status == 200
    json = await resp.json()
    assert json == {"param_id": 10}


async def test_ref_parameter(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs", components="tests/testdata/components.yaml")
    s.add_route("GET", "/r", parameter_ref_handler)

    client = await aiohttp_client(app)

    params = {"month": 5}
    resp = await client.get("/r", params=params)
    assert resp.status == 200
    json = await resp.json()
    assert json == params


async def test_minimum_maximum(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")
    s.add_route("POST", "/r/{path_int}/{path_float}", minimum_maximum_handler)

    client = await aiohttp_client(app)

    int_param = 15
    float_param = 15.5
    body = {"int": int_param, "float": float_param}
    params = {"query_int": int_param, "query_float": str(float_param)}
    resp = await client.post(f"/r/{int_param}/{float_param}", params=params, json=body)
    assert resp.status == 200
    json = await resp.json()
    assert json == {
        "query_int": int_param,
        "query_float": float_param,
        "path_int": int_param,
        "path_float": float_param,
        "body": body,
    }

    int_param = 10
    float_param = 10.1
    body = {"int": int_param, "float": float_param}
    params = {"query_int": int_param, "query_float": str(float_param)}
    resp = await client.post(f"/r/{int_param}/{float_param}", params=params, json=body)
    assert resp.status == 200
    json = await resp.json()
    assert json == {
        "query_int": int_param,
        "query_float": float_param,
        "path_int": int_param,
        "path_float": float_param,
        "body": body,
    }

    int_param = 20
    float_param = 19.9
    body = {"int": int_param, "float": float_param}
    params = {"query_int": int_param, "query_float": str(float_param)}
    resp = await client.post(f"/r/{int_param}/{float_param}", params=params, json=body)
    assert resp.status == 200
    json = await resp.json()
    assert json == {
        "query_int": int_param,
        "query_float": float_param,
        "path_int": int_param,
        "path_float": float_param,
        "body": body,
    }

    int_param = 5
    float_param = 5.5
    body = {"int": int_param, "float": float_param}
    params = {"query_int": int_param, "query_float": str(float_param)}
    resp = await client.post(f"/r/{int_param}/{float_param}", params=params, json=body)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    msg_int = "value should be more than or equal to 10"
    msg_float = "value should be more than or equal to 10.1"
    assert json == {
        "query_int": msg_int,
        "query_float": msg_float,
        "body": {"int": msg_int, "float": msg_float},
        "path_int": msg_int,
        "path_float": msg_float,
    }

    int_param = 25
    float_param = 25.5
    body = {"int": int_param, "float": float_param}
    params = {"query_int": int_param, "query_float": str(float_param)}
    resp = await client.post(f"/r/{int_param}/{float_param}", params=params, json=body)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    msg_int = "value should be less than or equal to 20"
    msg_float = "value should be less than or equal to 19.9"
    assert json == {
        "query_int": msg_int,
        "query_float": msg_float,
        "body": {"int": msg_int, "float": msg_float},
        "path_int": msg_int,
        "path_float": msg_float,
    }


async def test_exclusive_minimum_maximum(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")
    s.add_route("POST", "/r/{path_int}/{path_float}", exclusive_minimum_maximum_handler)

    client = await aiohttp_client(app)

    int_param = 10
    float_param = 10.1
    body = {"int": int_param, "float": float_param}
    params = {"query_int": int_param, "query_float": str(float_param)}
    resp = await client.post(f"/r/{int_param}/{float_param}", params=params, json=body)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    msg_int = "value should be more than 10"
    msg_float = "value should be more than 10.1"
    assert json == {
        "query_int": msg_int,
        "query_float": msg_float,
        "body": {"int": msg_int, "float": msg_float},
        "path_int": msg_int,
        "path_float": msg_float,
    }

    int_param = 20
    float_param = 19.9
    body = {"int": int_param, "float": float_param}
    params = {"query_int": int_param, "query_float": str(float_param)}
    resp = await client.post(f"/r/{int_param}/{float_param}", params=params, json=body)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    msg_int = "value should be less than 20"
    msg_float = "value should be less than 19.9"
    assert json == {
        "query_int": msg_int,
        "query_float": msg_float,
        "body": {"int": msg_int, "float": msg_float},
        "path_int": msg_int,
        "path_float": msg_float,
    }


async def test_int32_bounds(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")
    s.add_route("POST", "/r/{path}", int32_bounds_handler)

    client = await aiohttp_client(app)

    body_param = -2_147_483_649
    body = {"int": body_param}
    query_param = -2_147_483_649
    params = {"query": query_param}
    path_param = -2_147_483_649
    resp = await client.post(f"/r/{path_param}", params=params, json=body)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    msg = "value out of bounds int32"
    assert json == {"query": msg, "body": {"int": msg}, "path": msg}

    body_param = 2_147_483_648
    body = {"int": body_param}
    query_param = 2_147_483_648
    params = {"query": query_param}
    path_param = 2_147_483_648
    resp = await client.post(f"/r/{path_param}", params=params, json=body)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    msg = "value out of bounds int32"
    assert json == {"query": msg, "body": {"int": msg}, "path": msg}


async def test_min_max_length(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")
    s.add_route("POST", "/r/{path}", min_max_length_handler)

    client = await aiohttp_client(app)

    header_param = "string"
    headers = {"header": header_param}
    body_param = "string"
    body = {"str": body_param}
    query_param = "string"
    params = {"query": query_param}
    path_param = "string"
    resp = await client.post(
        f"/r/{path_param}", headers=headers, params=params, json=body
    )
    assert resp.status == 200
    json = await resp.json()
    assert json == {
        "header": header_param,
        "query": query_param,
        "path": path_param,
        "body": body,
    }

    header_param = "str"
    headers = {"header": header_param}
    body_param = "str"
    body = {"str": body_param}
    query_param = "str"
    params = {"query": query_param}
    path_param = "str"
    resp = await client.post(
        f"/r/{path_param}", headers=headers, params=params, json=body
    )
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    msg = "value length should be more than 5"
    assert json == {"query": msg, "body": {"str": msg}, "header": msg, "path": msg}

    header_param = "long_string"
    headers = {"header": header_param}
    body_param = "long_string"
    body = {"str": body_param}
    query_param = "long_string"
    params = {"query": query_param}
    path_param = "long_string"
    resp = await client.post(
        f"/r/{path_param}", headers=headers, params=params, json=body
    )
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    msg = "value length should be less than 10"
    assert json == {"query": msg, "body": {"str": msg}, "header": msg, "path": msg}


async def test_min_max_properties(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")
    s.add_route("POST", "/r", min_max_properties_handler)

    client = await aiohttp_client(app)

    body = {"str1": "str1", "str2": "str1", "str3": "str1"}
    resp = await client.post(f"/r", json=body)
    assert resp.status == 200
    json = await resp.json()
    assert json == body

    body = {"str1": "str1"}
    resp = await client.post(f"/r", json=body)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    assert json == {"body": "number or properties must be more than 2"}

    body = {
        "str1": "str1",
        "str2": "str1",
        "str3": "str1",
        "str4": "str1",
        "str5": "str1",
        "str6": "str1",
    }
    resp = await client.post(f"/r", json=body)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    assert json == {"body": "number or properties must be less than 5"}


async def test_min_max_items(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")
    s.add_route("POST", "/r", min_max_items_handler)

    client = await aiohttp_client(app)

    header_param = [1, 2, 3]
    headers = {"header": ",".join(str(x) for x in header_param)}
    body_param = [1, 2, 3]
    body = {"array": body_param}
    query_param = [1, 2, 3]
    params = {"query": ",".join(str(x) for x in query_param)}
    resp = await client.post(f"/r", headers=headers, params=params, json=body)
    assert resp.status == 200
    json = await resp.json()
    assert json == {"header": header_param, "query": query_param, "body": body}

    header_param = [1]
    headers = {"header": ",".join(str(x) for x in header_param)}
    body_param = [1]
    body = {"array": body_param}
    query_param = [1]
    params = {"query": ",".join(str(x) for x in query_param)}
    resp = await client.post(f"/r", headers=headers, params=params, json=body)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    msg = "number or items must be more than 2"
    assert json == {"query": msg, "body": {"array": msg}, "header": msg}

    header_param = [1, 2, 3, 4, 5, 6, 7]
    headers = {"header": ",".join(str(x) for x in header_param)}
    body_param = [1, 2, 3, 4, 5, 6, 7]
    body = {"array": body_param}
    query_param = [1, 2, 3, 4, 5, 6, 7]
    params = {"query": ",".join(str(x) for x in query_param)}
    resp = await client.post(f"/r", headers=headers, params=params, json=body)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    msg = "number or items must be less than 5"
    assert json == {"query": msg, "body": {"array": msg}, "header": msg}


async def test_unique_items(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")
    s.add_route("POST", "/r", unique_items_handler)

    client = await aiohttp_client(app)

    header_param = [1, 2, 3]
    headers = {"header": ",".join(str(x) for x in header_param)}
    body_param = [1, 2, 3]
    body = {"array": body_param}
    query_param = [1, 2, 3]
    params = {"query": ",".join(str(x) for x in query_param)}
    resp = await client.post(f"/r", headers=headers, params=params, json=body)
    assert resp.status == 200
    json = await resp.json()
    assert json == {"header": header_param, "query": query_param, "body": body}

    header_param = [1, 1]
    headers = {"header": ",".join(str(x) for x in header_param)}
    body_param = [1, 1]
    body = {"array": body_param}
    query_param = [1, 1]
    params = {"query": ",".join(str(x) for x in query_param)}
    resp = await client.post(f"/r", headers=headers, params=params, json=body)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    msg = "all items must be unique"
    assert json == {"query": msg, "body": {"array": msg}, "header": msg}


async def test_float_as_int(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")
    s.add_route("POST", "/r", float_as_int_handler)

    client = await aiohttp_client(app)

    int_float = 10
    int_double = 20
    body = {"int_float": int_float, "int_double": int_double}
    resp = await client.post(f"/r", json=body)
    assert resp.status == 200
    json = await resp.json()
    assert json == body


async def test_corner_cases(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")
    s.add_route("POST", "/r", corner_cases_handler)

    client = await aiohttp_client(app)

    params = {"int32": "abc", "int64": "cca", "float": "bca", "double": "bba"}
    resp = await client.post(f"/r", params=params)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    assert json == {
        "int32": "value should be type of int",
        "int64": "value should be type of int",
        "float": "value should be type of float",
        "double": "value should be type of float",
    }


async def test_query_array(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")
    s.add_route("POST", "/r", query_array)

    client = await aiohttp_client(app)

    query1 = [1, 2, 3, 4, 5]
    params = {"query1": ",".join(str(x) for x in query1)}
    resp = await client.post(f"/r", params=params)
    assert resp.status == 200
    json = await resp.json()
    assert json == {"query1": query1, "query2": None}


async def test_string_formats(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")
    s.add_route("GET", "/r", string_formats_handler)

    client = await aiohttp_client(app)

    date = "2017-07-21"
    datetime = "2017-07-21T00:00:00Z"
    password = "password"
    byte = "Oik="
    binary = "âPNGIHDRdlú±9bKGDˇˇˇ†ΩßìpHYs..."
    email = "me@me.com"
    uuid = "550e8400-e29b-41d4-a716-446655440001"
    hostname = "test.example.com"
    ipv4 = "127.0.0.1"
    ipv6 = "2001:db8::ff00:42:8329"
    resp = await client.get(
        "/r",
        params={
            "date": date,
            "datetime": datetime,
            "password": password,
            "byte": byte,
            "binary": binary,
            "email": email,
            "uuid": uuid,
            "hostname": hostname,
            "ipv4": ipv4,
            "ipv6": ipv6,
        },
    )
    assert resp.status == 200
    json = await resp.json()
    assert json == {
        "date": date,
        "datetime": datetime,
        "password": password,
        "byte": byte,
        "binary": binary,
        "email": email,
        "uuid": uuid,
        "hostname": hostname,
        "ipv4": ipv4,
        "ipv6": ipv6,
    }

    date = "20170721"
    datetime = "2017-07-21B00:00:00Z"
    password = "password"
    byte = "something"
    binary = "âPNGIHDRdlú±9bKGDˇˇˇ†ΩßìpHYs..."
    email = "me.me@com"
    uuid = "446655440001"
    hostname = "test.ex#ample.com"
    ipv4 = "10"
    ipv6 = "10"
    resp = await client.get(
        "/r",
        params={
            "date": date,
            "datetime": datetime,
            "password": password,
            "byte": byte,
            "binary": binary,
            "email": email,
            "uuid": uuid,
            "hostname": hostname,
            "ipv4": ipv4,
            "ipv6": ipv6,
        },
    )
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    assert json == {
        "date": "value should be date format",
        "datetime": "value should be datetime format",
        "byte": "value should be base64-encoded string",
        "email": "value should be valid email",
        "uuid": "value should be uuid",
        "hostname": "value should be valid hostname",
        "ipv4": "value should be valid ipv4 address",
        "ipv6": "value should be valid ipv6 address",
    }


async def test_string_pattern(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")
    s.add_route("GET", "/r", pattern_handler)

    client = await aiohttp_client(app)

    string = "123"
    resp = await client.get("/r", params={"string": string})
    assert resp.status == 200
    json = await resp.json()
    assert json == {"string": string}

    string = "asd"
    resp = await client.get("/r", params={"string": string})
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    assert json == {"string": "value should match regex pattern '^\\d{3}$'"}


async def test_incorrent_json_body(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")
    s.add_route("GET", "/r", body_with_optional_properties_handler)

    client = await aiohttp_client(app)

    resp = await client.get(
        "/r", data="{{", headers={"content-type": "application/json"}
    )
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    assert json == {
        "body": "Expecting property name enclosed in double quotes: line 1 column 2 (char 1)"
    }


async def test_array_in_object(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")
    s.add_route("GET", "/r", array_in_object_handler)

    client = await aiohttp_client(app)

    body = {"array": []}
    resp = await client.get("/r", json=body)
    assert resp.status == 200
    json = await resp.json()
    assert json == body

    body = {"array": [1, 2, 3]}
    resp = await client.get("/r", json=body)
    assert resp.status == 200
    json = await resp.json()
    assert json == body

    body = {"array": ["1", 2, 3]}
    resp = await client.get("/r", json=body)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    assert json == {"body": {"array": {0: "value should be type of int"}}}

    body = {"array": [1, 2.2, 3]}
    resp = await client.get("/r", json=body)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    assert json == {"body": {"array": {1: "value should be type of int"}}}

    body = {"array": [1, 2, True]}
    resp = await client.get("/r", json=body)
    assert resp.status == 400
    error = await resp.text()
    json = error_to_json(error)
    assert json == {"body": {"array": {2: "value should be type of int"}}}


async def test_no_docs(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerDocs(app, "/docs")
    s.add_route("GET", "/r", no_doc_handler)

    client = await aiohttp_client(app)
    resp = await client.get("/r", json={"array": "whatever"})
    assert resp.status == 200


async def test_spec_file(aiohttp_client, loop):
    app = web.Application(loop=loop)
    s = SwaggerFile(app, "/docs", "tests/testdata/petstore.yaml")
    s.add_routes(
        [
            web.get("/pets", get_all_pets),
            web.get("/pets/{pet_id}", get_one_pet),
            web.post("/pets", create_pet),
        ]
    )

    client = await aiohttp_client(app)

    resp = await client.get("/pets", params={"limit": 1})
    assert resp.status == 200
    json = await resp.json()
    assert json == [{"id": 0, "name": "pet_0", "tag": "tag_0"}]

    resp = await client.get("/pets")
    assert resp.status == 200
    json = await resp.json()
    assert json == [
        {"id": 0, "name": "pet_0", "tag": "tag_0"},
        {"id": 1, "name": "pet_1", "tag": "tag_1"},
        {"id": 2, "name": "pet_2", "tag": "tag_2"},
    ]

    resp = await client.post("/pets")
    assert resp.status == 201

    resp = await client.get("/pets/1")
    assert resp.status == 200
    json = await resp.json()
    assert json == {"id": 1, "name": "pet_1", "tag": "tag_1"}

    resp = await client.get(f"/pets/1")
    assert resp.status == 200
    json = await resp.json()
    assert json == {"id": 1, "name": "pet_1", "tag": "tag_1"}

    resp = await client.get(f"/pets/100")
    assert resp.status == 500
    json = await resp.json()
    assert json == {"code": 10, "message": f"pet with ID '100' not found"}
