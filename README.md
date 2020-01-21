# aiohttp-swagger3
[![Build Status](https://travis-ci.com/hh-h/aiohttp-swagger3.svg?branch=master)](https://travis-ci.com/hh-h/aiohttp-swagger3)
[![Code Coverage](https://img.shields.io/codecov/c/github/hh-h/aiohttp-swagger3/master.svg?style=flat)](https://codecov.io/github/hh-h/aiohttp-swagger3?branch=master)
[![PyPI version](https://badge.fury.io/py/aiohttp-swagger3.svg)](https://badge.fury.io/py/aiohttp-swagger3)
[![Python version](https://img.shields.io/badge/python-3.6%2B-brightgreen.svg)](https://img.shields.io/badge/python-3.6%2B-brightgreen.svg)
[![Code Style](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/ambv/black)
[![License](https://img.shields.io/pypi/l/aiohttp-swagger3.svg)](https://www.apache.org/licenses/LICENSE-2.0)

# About
Package for displaying swagger docs via different UI backends and optionally validating/parsing aiohttp requests using swagger specification 3.0, known as OpenAPI3.  

# UI backends
Multiple UI backends can be used or UI backend can be disabled at all if only needed validation without being able to view documentation.  
## Supported UI backends ##  
* Swagger UI - https://github.com/swagger-api/swagger-ui
* ReDoc - https://github.com/Redocly/redoc
* RapiDoc - https://github.com/mrin9/RapiDoc  

# Disable validation
Pass `validate=False` to `SwaggerDocs`/`SwaggerFile` class, the default is `True`  
Also, sometimes validation has to be disabled for a route, to do this you have to pass `validate=False` during the initialization of the route.  
ex. `web.post("/route", handler, validate=False)`, the default is `True`

# Requirements
- python3.6+
- aiohttp >= 3.5.4
- pyyaml
- attrs
- python-fastjsonschema
- strict_rfc3339

# Limitations
- only application/json and application/x-www-form-urlencoded supported for now, but you can create own [handler](https://github.com/hh-h/aiohttp-swagger3/tree/master/examples/custom_handler)
- header/query parameters only supported simple/form array serialization, e.g. 1,2,3,4
- see TODO below

# Installation
`pip install aiohttp-swagger3`

# Example
```python
from aiohttp import web
from aiohttp_swagger3 import SwaggerDocs, SwaggerUiSettings

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
    s = SwaggerDocs(
        app,
        swagger_ui_settings=SwaggerUiSettings(path="/docs/"),
        title="Swagger Petstore",
        version="1.0.0",
        components="components.yaml"
    )
    s.add_routes([
        web.get("/pets/{pet_id}", get_one_pet),
    ])
    app['storage'] = {}
    web.run_app(app)
```
More [examples](https://github.com/hh-h/aiohttp-swagger3/tree/master/examples)

# Features
- [x] application/json
- [x] application/x-www-form-urlencoded (except array and object)
- [x] items
- [x] properties
- [x] pattern
- [x] required
- [x] enum
- [x] minimum
- [x] maximum
- [x] exclusiveMinimum
- [x] exclusiveMaximum
- [x] minLength
- [x] maxLength
- [x] minItems
- [x] maxItems
- [x] uniqueItems
- [x] minProperties
- [x] maxProperties
- [x] default (only primitives)
- [x] additionalProperties
- [x] nullable
- [x] allOf
- [x] oneOf
- [x] anyOf
- [x] string formats: date, date-time, password, byte, binary, email, uuid, hostname, ipv4, ipv6

# TODO (raise an issue if needed)

- ### swagger specific
- [ ] multipleOf
- [ ] not 
- [ ] allowEmptyValue
- [ ] Common Parameters for All Methods of a Path (spec file only)
- [ ] readOnly, writeOnly
- [ ] more serialization methods, see: [https://swagger.io/docs/specification/serialization/](https://swagger.io/docs/specification/serialization/)
- [ ] encoding
- [ ] form data serialization (array, object)
- [ ] default (array, object)
