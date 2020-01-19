from typing import Dict, List, Optional, Union

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


@attr.attrs(
    slots=True, frozen=True, eq=False, hash=False, auto_attribs=True, kw_only=True
)
class ReDocUiSettings:
    path: str
    disableSearch: bool = attr.attrib(
        default=False, validator=attr.validators.instance_of(bool)
    )
    expandDefaultServerVariables: bool = attr.attrib(
        default=False, validator=attr.validators.instance_of(bool)
    )
    expandResponses: str = attr.attrib(
        default="", validator=attr.validators.instance_of(str)
    )
    hideDownloadButton: bool = attr.attrib(
        default=False, validator=attr.validators.instance_of(bool)
    )
    hideHostname: bool = attr.attrib(
        default=False, validator=attr.validators.instance_of(bool)
    )
    hideLoading: bool = attr.attrib(
        default=False, validator=attr.validators.instance_of(bool)
    )
    hideSingleRequestSampleTab: bool = attr.attrib(
        default=False, validator=attr.validators.instance_of(bool)
    )
    jsonSampleExpandLevel: Union[int, str] = attr.attrib(
        default=2, validator=attr.validators.instance_of((int, str))
    )
    menuToggle: bool = attr.attrib(
        default=True, validator=attr.validators.instance_of(bool)
    )
    nativeScrollbars: bool = attr.attrib(
        default=False, validator=attr.validators.instance_of(bool)
    )
    noAutoAuth: bool = attr.attrib(
        default=False, validator=attr.validators.instance_of(bool)
    )
    onlyRequiredInSamples: bool = attr.attrib(
        default=False, validator=attr.validators.instance_of(bool)
    )
    pathInMiddlePanel: bool = attr.attrib(
        default=False, validator=attr.validators.instance_of(bool)
    )
    requiredPropsFirst: bool = attr.attrib(
        default=False, validator=attr.validators.instance_of(bool)
    )
    scrollYOffset: int = attr.attrib(
        default=0, validator=attr.validators.instance_of(int)
    )
    showExtensions: bool = attr.attrib(
        default=False, validator=attr.validators.instance_of(bool)
    )
    sortPropsAlphabetically: bool = attr.attrib(
        default=False, validator=attr.validators.instance_of(bool)
    )
    suppressWarnings: bool = attr.attrib(
        default=False, validator=attr.validators.instance_of(bool)
    )
    payloadSampleIdx: int = attr.attrib(
        default=0, validator=attr.validators.instance_of(int)
    )
    untrustedSpec: bool = attr.attrib(
        default=False, validator=attr.validators.instance_of(bool)
    )

    @expandResponses.validator
    def _expand_responses_validator(self, _: "attr.Attribute[str]", value: str) -> None:
        if value == "all" or value == "":
            return
        raw_codes = value.split(",")
        for raw_code in raw_codes:
            try:
                int(raw_code)
            except ValueError:
                raise ValueError(
                    "expandResponses must be either 'all' or "
                    f"comma-separated list of http codes, got '{raw_code}'"
                )

    @jsonSampleExpandLevel.validator
    def _json_sample_expand_level_validator(
        self, _: "attr.Attribute[Union[int, str]]", value: Union[int, str]
    ) -> None:
        if isinstance(value, str) and value != "all":
            raise ValueError(
                f"jsonSampleExpandLevel must be either 'all' or integer, got '{value}'"
            )

    def to_settings(self) -> Dict:
        return attr.asdict(
            self, filter=attr.filters.exclude(attr.fields(ReDocUiSettings).path)
        )
