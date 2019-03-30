# aiohttp-swagger3
[![Build Status](https://travis-ci.com/hh-h/aiohttp-swagger3.svg?branch=master)](https://travis-ci.com/hh-h/aiohttp-swagger3)
[![Code Coverage](https://img.shields.io/codecov/c/github/hh-h/aiohttp-swagger3/master.svg?style=flat)](https://codecov.io/github/hh-h/aiohttp-swagger3?branch=master)
[![PyPI version](https://badge.fury.io/py/aiohttp-swagger3.svg)](https://badge.fury.io/py/aiohttp-swagger3)
[![Python version](https://img.shields.io/badge/python-3.6%2B-brightgreen.svg)](https://img.shields.io/badge/python-3.6%2B-brightgreen.svg)
[![Code Style](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/ambv/black)
[![License](https://img.shields.io/pypi/l/aiohttp-swagger3.svg)](https://www.apache.org/licenses/LICENSE-2.0)

## !!! Testers are needed !!!
Feel free to try this library and raise an issue if it does not work as expected, thanks!

# About
Package for displaying swagger docs and optionally validating/parsing aiohttp requests using swagger specification 3.0 only.  
It's marked as pre-alpha on pypi.org, but that's because I haven't decided architecture yet. However, we use it in production :)

# Disable validation
Okay, just pass `validate=False` to `SwaggerDocs`/`SwaggerFile` class, default is `True`

# Requirements
- python3.6+
- aiohttp>=3
- pyyaml
- attrs
- openapi-spec-validator
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
from aiohttp_swagger3 import SwaggerDocs

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
    s = SwaggerDocs(app, '/docs', title="Swagger Petstore", version="1.0.0", components="components.yaml")
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

- ### aiohttp specific
- [ ] class based view
- [ ] METH_ANY (*) routes

- ### swagger specific
- [ ] cookies
- [ ] multipleOf
- [ ] not 
- [ ] allowEmptyValue
- [ ] Common Parameters for All Methods of a Path (spec file only)
- [ ] readOnly, writeOnly
- [ ] more serialization methods, see: [https://swagger.io/docs/specification/serialization/](https://swagger.io/docs/specification/serialization/)
- [ ] encoding
- [ ] form data serialization (array, object)
- [ ] default (array, object)
