from typing import Dict, List, Optional

import attr


@attr.attrs(
    slots=True, frozen=True, eq=False, hash=False, auto_attribs=True, kw_only=True
)
class SwaggerUiSettings:
    path: str
    # plugin
    layout: str = attr.attrib(
        default="StandaloneLayout",
        validator=attr.validators.in_(("BaseLayout", "StandaloneLayout")),
    )
    # display
    deepLinking: bool = attr.attrib(
        default=True, validator=attr.validators.instance_of(bool)
    )
    displayOperationId: bool = attr.attrib(
        default=False, validator=attr.validators.instance_of(bool)
    )
    defaultModelsExpandDepth: int = attr.attrib(
        default=1, validator=attr.validators.instance_of(int)
    )
    defaultModelExpandDepth: int = attr.attrib(
        default=1, validator=attr.validators.instance_of(int)
    )
    defaultModelRendering: str = attr.attrib(
        default="example", validator=attr.validators.in_(("example", "model")),
    )
    displayRequestDuration: bool = attr.attrib(
        default=False, validator=attr.validators.instance_of(bool)
    )
    docExpansion: str = attr.attrib(
        default="list", validator=attr.validators.in_(("list", "full", "none")),
    )
    filter: bool = attr.attrib(
        default=False, validator=attr.validators.instance_of(bool)
    )
    showExtensions: bool = attr.attrib(
        default=False, validator=attr.validators.instance_of(bool)
    )
    showCommonExtensions: bool = attr.attrib(
        default=False, validator=attr.validators.instance_of(bool)
    )
    # network
    supportedSubmitMethods: List[str] = attr.attrib(
        validator=attr.validators.deep_iterable(
            member_validator=attr.validators.in_(
                ("get", "put", "post", "delete", "options", "head", "patch", "trace")
            ),
            iterable_validator=attr.validators.instance_of(list),
        )
    )
    validatorUrl: Optional[str] = attr.attrib(
        default="https://validator.swagger.io/validator",
        validator=attr.validators.optional(attr.validators.instance_of(str)),  # type: ignore
    )

    withCredentials: bool = attr.attrib(
        default=False, validator=attr.validators.instance_of(bool)
    )

    @supportedSubmitMethods.default
    def _supported_submit_methods_default(self) -> List[str]:
        return ["get", "put", "post", "delete", "options", "head", "patch", "trace"]

    def to_settings(self) -> Dict:
        return attr.asdict(
            self, filter=attr.filters.exclude(attr.fields(SwaggerUiSettings).path)
        )
