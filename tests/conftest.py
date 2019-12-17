import pytest
from aiohttp import web

from aiohttp_swagger3 import (
    ReDocUiSettings,
    SwaggerDocs,
    SwaggerFile,
    SwaggerUiSettings,
)

pytest_plugins = ["aiohttp.pytest_plugin"]


@pytest.fixture
def swagger_ui_settings():
    def _swagger_ui_settings(**kwargs):
        if "path" not in kwargs:
            kwargs["path"] = "/docs"
        return SwaggerUiSettings(**kwargs)

    return _swagger_ui_settings


@pytest.fixture
def redoc_ui_settings():
    def _redoc_ui_settings(**kwargs):
        if "path" not in kwargs:
            kwargs["path"] = "/docs"
        return ReDocUiSettings(**kwargs)

    return _redoc_ui_settings


@pytest.fixture
def swagger_docs_with_components():
    def _swagger_docs_with_components(**kwargs):
        app = web.Application()
        return SwaggerDocs(app, components="tests/testdata/components.yaml", **kwargs,)

    return _swagger_docs_with_components


@pytest.fixture
def swagger_docs():
    def _swagger_docs(**kwargs):
        app = web.Application()
        return SwaggerDocs(app, **kwargs)

    return _swagger_docs


@pytest.fixture
def swagger_file():
    def _swagger_file(**kwargs):
        app = web.Application()
        return SwaggerFile(app, spec_file="tests/testdata/petstore.yaml", **kwargs,)

    return _swagger_file
