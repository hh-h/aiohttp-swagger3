from typing import List

from aiohttp import web

from .helpers import error_to_json


async def test_query_array(swagger_docs, aiohttp_client):
    async def handler(request, query1: List[int], query2: List[int] = None):
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

    swagger = swagger_docs()
    swagger.add_route("POST", "/r", handler)

    client = await aiohttp_client(swagger._app)

    query1 = [1, 2, 3, 4, 5]
    params = {"query1": ",".join(str(x) for x in query1)}
    resp = await client.post("/r", params=params)
    assert resp.status == 200
    assert await resp.json() == {"query1": query1, "query2": None}


async def test_array(swagger_docs, aiohttp_client):
    async def handler(request, array: List[int]):
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

    swagger = swagger_docs()
    swagger.add_route("GET", "/r", handler)

    client = await aiohttp_client(swagger._app)
    a = [1, 2, -10, 15, 999, 0]
    resp = await client.get("/r", params={"array": ",".join(str(x) for x in a)})
    assert resp.status == 200
    assert await resp.json() == a

    a = []
    resp = await client.get("/r", params={"array": ",".join(str(x) for x in a)})
    assert resp.status == 200
    assert await resp.json() == a


async def test_enum(swagger_docs, aiohttp_client):
    async def handler(request, integer: int, string: str, number: float):
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
        return web.json_response(
            {"integer": integer, "string": string, "number": number}
        )

    swagger = swagger_docs()
    swagger.add_route("GET", "/r", handler)

    client = await aiohttp_client(swagger._app)
    integer = 10
    string = "abc"
    number = 10.1
    params = {"integer": integer, "string": string, "number": str(number)}
    resp = await client.get("/r", params=params)
    assert resp.status == 200
    assert await resp.json() == {"integer": integer, "string": string, "number": number}

    integer = 100
    string = "abcd"
    number = 10.3
    params = {"integer": integer, "string": string, "number": str(number)}
    resp = await client.get("/r", params=params)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {
        "integer": "value should be one of [1, 5, 10]",
        "string": "value should be one of ['abc', 'bca']",
        "number": "value should be one of [10.1, 10.2]",
    }


async def test_primitives(swagger_docs, aiohttp_client):
    async def handler(
        request,
        integer: int,
        int32: int,
        int64: int,
        number: float,
        float1: float,
        double: float,
        string: str,
        boolean: bool,
    ):
        """
        ---
        parameters:

          - name: integer
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

          - name: float1
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
                "integer": integer,
                "int32": int32,
                "int64": int64,
                "number": number,
                "float1": float1,
                "double": double,
                "string": string,
                "boolean": boolean,
            }
        )

    swagger = swagger_docs()
    swagger.add_route("GET", "/r", handler)

    client = await aiohttp_client(swagger._app)
    integer = 42
    int32 = 32
    int64 = 64
    number = 333.333
    float1 = 10.111_111
    double = 20.222_222_222_222
    string = "1string1"
    boolean = False
    resp = await client.get(
        "/r",
        params={
            "integer": integer,
            "int32": int32,
            "int64": int64,
            "number": str(number),
            "float1": str(float1),
            "double": str(double),
            "string": string,
            "boolean": str(boolean).lower(),
        },
    )
    assert resp.status == 200
    assert await resp.json() == {
        "integer": integer,
        "int32": int32,
        "int64": int64,
        "number": number,
        "float1": float1,
        "double": double,
        "string": string,
        "boolean": boolean,
    }


async def test_string_formats(swagger_docs, aiohttp_client):
    async def handler(
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

    swagger = swagger_docs()
    swagger.add_route("GET", "/r", handler)

    client = await aiohttp_client(swagger._app)

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
    assert await resp.json() == {
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
    error = error_to_json(await resp.text())
    assert error == {
        "date": "value should be date format",
        "datetime": "value should be datetime format",
        "byte": "value should be base64-encoded string",
        "email": "value should be valid email",
        "uuid": "value should be uuid",
        "hostname": "value should be valid hostname",
        "ipv4": "value should be valid ipv4 address",
        "ipv6": "value should be valid ipv6 address",
    }

    resp = await client.get(
        "/r",
        params={
            "date": "",
            "datetime": "",
            "password": "",
            "byte": "",
            "binary": "",
            "email": "",
            "uuid": "",
            "hostname": "",
            "ipv4": "",
            "ipv6": "",
        },
    )
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {
        "date": "value should be date format",
        "datetime": "value should be datetime format",
        "email": "value should be valid email",
        "uuid": "value should be uuid",
        "hostname": "value should be valid hostname",
        "ipv4": "value should be valid ipv4 address",
        "ipv6": "value should be valid ipv6 address",
    }


async def test_corner_cases(swagger_docs, aiohttp_client):
    async def handler(request, int32: int, int64: int, float1: float, double: float):
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

          - name: float1
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
            {"int32": int32, "int64": int64, "float1": float1, "double": double}
        )

    swagger = swagger_docs()
    swagger.add_route("POST", "/r", handler)

    client = await aiohttp_client(swagger._app)

    params = {"int32": "abc", "int64": "cca", "float1": "bca", "double": "bba"}
    resp = await client.post("/r", params=params)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {
        "int32": "value should be type of int",
        "int64": "value should be type of int",
        "float1": "value should be type of float",
        "double": "value should be type of float",
    }


async def test_string_pattern(swagger_docs, aiohttp_client):
    async def handler(request, string: str):
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

    swagger = swagger_docs()
    swagger.add_route("GET", "/r", handler)

    client = await aiohttp_client(swagger._app)

    string = "123"
    resp = await client.get("/r", params={"string": string})
    assert resp.status == 200
    assert await resp.json() == {"string": string}

    string = "asd"
    resp = await client.get("/r", params={"string": string})
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"string": "value should match regex pattern '^\\d{3}$'"}


async def test_decorated_routes(swagger_docs, aiohttp_client):

    routes = web.RouteTableDef()

    @routes.get("/r")
    async def handler(request, int32: int):
        """
        ---
        parameters:

          - name: int32
            in: query
            required: true
            schema:
              type: integer

        responses:
          '200':
            description: OK.
        """
        return web.json_response({"int32": int32})

    swagger = swagger_docs()
    swagger.add_routes(routes)

    client = await aiohttp_client(swagger._app)

    params = {"int32": 15}
    resp = await client.get("/r", params=params)
    assert resp.status == 200
    assert await resp.json() == params


async def test_missing_query_parameter(swagger_docs, aiohttp_client):
    async def handler(request):
        """
        ---
        parameters:

          - name: variable
            in: query
            required: true
            schema:
              type: integer

        responses:
          '200':
            description: OK.

        """
        return web.json_response()

    swagger = swagger_docs()
    swagger.add_route("GET", "/r", handler)

    client = await aiohttp_client(swagger._app)
    resp = await client.get("/r")
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"variable": "is required"}


async def test_wrong_item_in_array(swagger_docs, aiohttp_client):
    async def handler(request):
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

        responses:
          '200':
            description: OK.

        """
        return web.json_response()

    swagger = swagger_docs()
    swagger.add_route("POST", "/r", handler)

    client = await aiohttp_client(swagger._app)

    params = {"array": ",".join(str(x) for x in [1, "abc", 3, True, 5])}
    resp = await client.post("/r", params=params)
    assert resp.status == 400
    error = error_to_json(await resp.text())
    assert error == {"array": {"1": "value should be type of int"}}
