__all__ = (
    "ReDocUiSettings",
    "SwaggerDocs",
    "SwaggerFile",
    "SwaggerUiSettings",
    "__version__",
)
__version__ = "0.3.5"
__author__ = "Valetov Konstantin"

from .swagger_docs import SwaggerDocs
from .swagger_file import SwaggerFile
from .ui_settings import ReDocUiSettings, SwaggerUiSettings
