# Changelog

## 0.3.1 (17-12-2019)
- added ReDoc UI. Closes [#33](https://github.com/hh-h/aiohttp-swagger3/issues/33)

## 0.3.0 (10-12-2019)
- fixed server error when passed hostname is empty. Closes [#35](https://github.com/hh-h/aiohttp-swagger3/issues/35)
- fixed KeyError when no swagger routes defined. Closes [#28](https://github.com/hh-h/aiohttp-swagger3/issues/28)
- added ability to bind Swagger UI to root "/". Closes [#31](https://github.com/hh-h/aiohttp-swagger3/issues/31)
- added optional authentication support. Closes [#36](https://github.com/hh-h/aiohttp-swagger3/issues/36)
- swagger UI is now customizable and can be disabled. Closes [#30](https://github.com/hh-h/aiohttp-swagger3/issues/30)

## 0.2.5 (27-11-2019)
- use anyOf instead of oneOf for security validation. Closes [#23](https://github.com/hh-h/aiohttp-swagger3/issues/23)

## 0.2.4 (16-11-2019)
- requestBody can be optional. Closes [#19](https://github.com/hh-h/aiohttp-swagger3/issues/19)
- bump swagger ui to 3.24.2

## 0.2.3 (16-09-2019)
- fixed TypeError during rendering swagger docs. Closes [#17](https://github.com/hh-h/aiohttp-swagger3/issues/17)

## 0.2.2 (30-08-2019)
- fixed string/binary doesn't allow bytes as input
- bump swagger ui to 3.23.6

## 0.2.1 (29-06-2019)
- added cookie parameters support
- added authentication
- headers now stored in request in lowercase

## 0.2.0 (27-06-2019)
- added ability to handle empty arrays in query parameters
- added class based view
- added METH_ANY support
- fixed incorrect validate=False behaviour

## 0.1.8 (27-06-2019)
- bump swagger ui to 3.23.1

## 0.1.7 (11-04-2019)
- fixed bug when object inside object couldn't be optional
- fixed bug when allow_head was ignored

## 0.1.6 (30-03-2019)
- added ability to skip validation

## 0.1.5 (15-03-2019)
- use yaml's safe_load instead of load
- bump swagger ui to 3.21.0
- fixed compatibility with aiohttp>3

## 0.1.4 (31-01-2019)
- ability to set key where validated data stored in request
- bump swagger ui to 3.20.5

## 0.1.3 (14-01-2019)
- fixed forgot to pass named resources for GET methods

## 0.1.2 (27-12-2018)
- added support for application/x-www-form-urlencoded (only primitives)

## 0.1.1 (25-12-2018)
- fixed detection of content-type
- added ability to work with handler decorators
- type annotations are checked in strict mode now
- fixed error when route wasn't in spec file

## 0.1 (22-12-2018)
- first public version