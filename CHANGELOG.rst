Changelog
=========

0.5.4 (dd-mm-yyyy)
------------------

- detailed error info for allOf
- bump rapidoc ui to 8.4.9
- bump redoc ui to v2.0.0-rc.50

0.5.3 (14-01-2021)
------------------

- allOf, oneOf, anyOf can be nullable
- readOnly should affect only properties

0.5.2 (31-12-2020)
------------------

- Happy New Year!
- added required readOnly support
- bump rapidoc ui to 8.4.3
- bump swagger ui to 3.38.0

0.5.1 (28-11-2020)
------------------

- added readOnly support
- bump swagger ui to 3.37.2

0.5.0 (31-10-2020)
------------------

- added aiohttp 3.7 support
- bump swagger ui to 3.36.1
- bump rapidoc ui to 8.3.0
- bump redoc ui to v2.0.0-rc.40

0.4.4 (30-06-2020)
------------------

- raise more verbose exception if schema failed to validate
- bump swagger ui to 3.28.0
- bump rapidoc ui to 8.1.1
- bump redoc ui to v2.0.0-rc.31

0.4.3 (13-03-2020)
------------------

- some optimizations, it should parse request a little bit faster

0.4.2 (11-03-2020)
------------------

- added ability to register custom string formats. Closes `#53 <https://github.com/hh-h/aiohttp-swagger3/issues/53>`_

0.4.1 (09-03-2020)
------------------

- allow for unknown string formats. Closes `#51 <https://github.com/hh-h/aiohttp-swagger3/issues/51>`_

0.4.0 (07-03-2020)
------------------

- raise custom exception when validation fails. Closes `#49 <https://github.com/hh-h/aiohttp-swagger3/issues/49>`_
- finally added documentation
- bump Swagger UI to 3.25.0
- bump RapiDoc UI to 7.4.0
- bump ReDoc UI to v2.0.0-rc23
- removed deprecated ``up_path`` parameter from ``SwaggerDocs`` and ``SwaggerFile``

0.3.6 (21-01-2020)
------------------

- added ability to disable validation per route. Closes `#29 <https://github.com/hh-h/aiohttp-swagger3/issues/29>`_
- added discriminator support. Closes `#34 <https://github.com/hh-h/aiohttp-swagger3/issues/34>`_
- added RapiDoc UI. Closes `#39 <https://github.com/hh-h/aiohttp-swagger3/issues/39>`_

0.3.5 (18-12-2019)
------------------

- one more attempt to fix fonts

0.3.4 (18-12-2019)
------------------

- required files must be in wheel too

0.3.3 (18-12-2019)
------------------

- added missing fonts for ReDoc UI

0.3.2 (18-12-2019)
------------------

- migrated to fastjsonschema

0.3.1 (17-12-2019)
------------------

- added ReDoc UI. Closes `#33 <https://github.com/hh-h/aiohttp-swagger3/issues/33>`_

0.3.0 (10-12-2019)
------------------

- fixed server error when passed hostname is empty. Closes `#35 <https://github.com/hh-h/aiohttp-swagger3/issues/35>`_
- fixed KeyError when no swagger routes defined. Closes `#28 <https://github.com/hh-h/aiohttp-swagger3/issues/28>`_
- added ability to bind Swagger UI to root "/". Closes `#31 <https://github.com/hh-h/aiohttp-swagger3/issues/31>`_
- added optional authentication support. Closes `#36 <https://github.com/hh-h/aiohttp-swagger3/issues/36>`_
- swagger UI is now customizable and can be disabled. Closes `#30 <https://github.com/hh-h/aiohttp-swagger3/issues/30>`_

0.2.5 (27-11-2019)
------------------

- use anyOf instead of oneOf for security validation. Closes `#23 <https://github.com/hh-h/aiohttp-swagger3/issues/23>`_

0.2.4 (16-11-2019)
------------------

- requestBody can be optional. Closes `#19 <https://github.com/hh-h/aiohttp-swagger3/issues/19>`_
- bump swagger ui to 3.24.2

0.2.3 (16-09-2019)
------------------

- fixed TypeError during rendering swagger docs. Closes `#17 <https://github.com/hh-h/aiohttp-swagger3/issues/17>`_

0.2.2 (30-08-2019)
------------------

- fixed string/binary doesn't allow bytes as input
- bump swagger ui to 3.23.6

0.2.1 (29-06-2019)
------------------

- added cookie parameters support
- added authentication
- headers now stored in request in lowercase

0.2.0 (27-06-2019)
------------------

- added ability to handle empty arrays in query parameters
- added class based view
- added METH\_ANY support
- fixed incorrect validate=False behaviour

0.1.8 (27-06-2019)
------------------

- bump swagger ui to 3.23.1

0.1.7 (11-04-2019)
------------------

- fixed bug when object inside object couldn't be optional
- fixed bug when allow\_head was ignored

0.1.6 (30-03-2019)
------------------

- added ability to skip validation

0.1.5 (15-03-2019)
------------------

- use yaml's safe\_load instead of load
- bump swagger ui to 3.21.0
- fixed compatibility with aiohttp>3

0.1.4 (31-01-2019)
------------------

- ability to set key where validated data stored in request
- bump swagger ui to 3.20.5

0.1.3 (14-01-2019)
------------------

- fixed forgot to pass named resources for GET methods

0.1.2 (27-12-2018)
------------------

- added support for application/x-www-form-urlencoded (only primitives)

0.1.1 (25-12-2018)
------------------

- fixed detection of content-type
- added ability to work with handler decorators
- type annotations are checked in strict mode now
- fixed error when route wasn't in spec file

0.1 (22-12-2018)
----------------

- first public version

