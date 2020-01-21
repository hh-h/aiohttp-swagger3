import re
from typing import Dict, List, Optional, Union

import attr

HEX_COLOR_REGEX = re.compile(
    r"^#([a-f0-9]{3,4}|[a-f0-9]{4}(?:[a-f0-9]{2}){1,2})$", re.IGNORECASE
)


@attr.attrs(
    slots=True, frozen=True, eq=False, hash=False, auto_attribs=True, kw_only=True
)
class _UiSettings:
    path: str

    def to_settings(self) -> Dict:
        return attr.asdict(
            self, filter=attr.filters.exclude(attr.fields(_UiSettings).path)
        )


@attr.attrs(
    slots=True, frozen=True, eq=False, hash=False, auto_attribs=True, kw_only=True
)
class SwaggerUiSettings(_UiSettings):
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

    # noinspection PyUnresolvedReferences
    @supportedSubmitMethods.default
    def _supported_submit_methods_default(self) -> List[str]:
        return ["get", "put", "post", "delete", "options", "head", "patch", "trace"]


@attr.attrs(
    slots=True, frozen=True, eq=False, hash=False, auto_attribs=True, kw_only=True
)
class ReDocUiSettings(_UiSettings):
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

    # noinspection PyUnresolvedReferences
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

    # noinspection PyUnresolvedReferences
    @jsonSampleExpandLevel.validator
    def _json_sample_expand_level_validator(
        self, _: "attr.Attribute[Union[int, str]]", value: Union[int, str]
    ) -> None:
        if isinstance(value, str) and value != "all":
            raise ValueError(
                f"jsonSampleExpandLevel must be either 'all' or integer, got '{value}'"
            )


@attr.attrs(
    slots=True, frozen=True, eq=False, hash=False, auto_attribs=True, kw_only=True
)
class RapiDocUiSettings(_UiSettings):
    # General
    sort_tags: bool = attr.attrib(
        default=False, validator=attr.validators.instance_of(bool)
    )
    heading_text: Optional[str] = attr.attrib(
        default=None,
        validator=attr.validators.optional(attr.validators.instance_of(str)),
    )
    # UI Colors and Fonts
    theme: str = attr.attrib(
        default="light", validator=attr.validators.in_(("light", "dark")),
    )
    bg_color: str = attr.attrib(validator=attr.validators.instance_of(str))
    text_color: str = attr.attrib(validator=attr.validators.instance_of(str))
    header_color: str = attr.attrib(
        default="#444444", validator=attr.validators.instance_of(str),
    )
    primary_color: str = attr.attrib(
        default="#FF791A", validator=attr.validators.instance_of(str),
    )
    # Navigation bar colors
    nav_bg_color: Optional[str] = attr.attrib(
        default=None,
        validator=attr.validators.optional(attr.validators.instance_of(str)),
    )
    nav_text_color: Optional[str] = attr.attrib(
        default=None,
        validator=attr.validators.optional(attr.validators.instance_of(str)),
    )
    nav_hover_bg_color: Optional[str] = attr.attrib(
        default=None,
        validator=attr.validators.optional(attr.validators.instance_of(str)),
    )
    nav_hover_text_color: Optional[str] = attr.attrib(
        default=None,
        validator=attr.validators.optional(attr.validators.instance_of(str)),
    )
    nav_accent_color: Optional[str] = attr.attrib(
        default=None,
        validator=attr.validators.optional(attr.validators.instance_of(str)),
    )
    # UI Layout & Placement
    layout: str = attr.attrib(
        default="row", validator=attr.validators.in_(("row", "column")),
    )
    render_style: str = attr.attrib(
        default="view", validator=attr.validators.in_(("read", "view")),
    )
    schema_style: str = attr.attrib(
        default="tree", validator=attr.validators.in_(("tree", "table")),
    )
    schema_expand_level: int = attr.attrib(
        default=999, validator=attr.validators.instance_of(int)
    )
    schema_description_expanded: bool = attr.attrib(
        default=False, validator=attr.validators.instance_of(bool)
    )
    default_schema_tab: str = attr.attrib(
        default="model", validator=attr.validators.in_(("model", "example")),
    )
    api_list_style: str = attr.attrib(
        default="group-by-tag",
        validator=attr.validators.in_(("group-by-tag", "group-by-path")),
    )
    # Hide/Show Sections
    show_info: bool = attr.attrib(
        default=True, validator=attr.validators.instance_of(bool)
    )
    show_header: bool = attr.attrib(
        default=True, validator=attr.validators.instance_of(bool)
    )
    allow_authentication: bool = attr.attrib(
        default=True, validator=attr.validators.instance_of(bool)
    )
    allow_spec_url_load: bool = attr.attrib(
        default=True, validator=attr.validators.instance_of(bool)
    )
    allow_spec_file_load: bool = attr.attrib(
        default=True, validator=attr.validators.instance_of(bool)
    )
    allow_search: bool = attr.attrib(
        default=True, validator=attr.validators.instance_of(bool)
    )
    allow_try: bool = attr.attrib(
        default=True, validator=attr.validators.instance_of(bool)
    )
    allow_server_selection: bool = attr.attrib(
        default=True, validator=attr.validators.instance_of(bool)
    )
    allow_api_list_style_selection: bool = attr.attrib(
        default=True, validator=attr.validators.instance_of(bool)
    )
    # API Server
    api_key_name: str = attr.attrib(
        default="Authorization", validator=attr.validators.instance_of(str),
    )
    api_key_value: Optional[str] = attr.attrib(
        default=None,
        validator=attr.validators.optional(attr.validators.instance_of(str)),
    )
    api_key_location: str = attr.attrib(
        default="header", validator=attr.validators.in_(("header", "query")),
    )
    server_url: Optional[str] = attr.attrib(
        default=None,
        validator=attr.validators.optional(attr.validators.instance_of(str)),
    )
    default_api_server: Optional[str] = attr.attrib(
        default=None,
        validator=attr.validators.optional(attr.validators.instance_of(str)),
    )

    # noinspection PyUnresolvedReferences
    @bg_color.validator
    def _bg_color_validator(self, _: "attr.Attribute[str]", value: str) -> None:
        if not HEX_COLOR_REGEX.match(value):
            raise ValueError("bg_color must be valid HEX color")

    # noinspection PyUnresolvedReferences
    @bg_color.default
    def _bg_color_default(self) -> str:
        if self.theme == "light":
            return "#fff"
        return "#333"

    # noinspection PyUnresolvedReferences
    @text_color.validator
    def _text_color_validator(self, _: "attr.Attribute[str]", value: str) -> None:
        if not HEX_COLOR_REGEX.match(value):
            raise ValueError("text_color must be valid HEX color")

    # noinspection PyUnresolvedReferences
    @text_color.default
    def _text_color_default(self) -> str:
        if self.theme == "light":
            return "#444"
        return "#bbb"

    @nav_bg_color.validator
    def _nav_bg_color_validator(
        self, _: "attr.Attribute[Optional[str]]", value: Optional[str]
    ) -> None:
        if value is not None and not HEX_COLOR_REGEX.match(value):
            raise ValueError("nav_bg_color must be valid HEX color")

    @nav_text_color.validator
    def _nav_text_color_validator(
        self, _: "attr.Attribute[Optional[str]]", value: Optional[str]
    ) -> None:
        if value is not None and not HEX_COLOR_REGEX.match(value):
            raise ValueError("nav_text_color must be valid HEX color")

    @nav_hover_bg_color.validator
    def _nav_hover_bg_color_validator(
        self, _: "attr.Attribute[Optional[str]]", value: Optional[str]
    ) -> None:
        if value is not None and not HEX_COLOR_REGEX.match(value):
            raise ValueError("nav_hover_bg_color must be valid HEX color")

    @nav_hover_text_color.validator
    def _nav_hover_text_color_validator(
        self, _: "attr.Attribute[Optional[str]]", value: Optional[str]
    ) -> None:
        if value is not None and not HEX_COLOR_REGEX.match(value):
            raise ValueError("nav_hover_text_color must be valid HEX color")

    @nav_accent_color.validator
    def _nav_accent_color_validator(
        self, _: "attr.Attribute[Optional[str]]", value: Optional[str]
    ) -> None:
        if value is not None and not HEX_COLOR_REGEX.match(value):
            raise ValueError("nav_accent_color must be valid HEX color")

    def to_settings(self) -> Dict:
        settings = {}
        attrs = attr.fields(self.__class__)
        for attribute in attrs:
            if attribute.name == "path":
                continue
            value = getattr(self, attribute.name)
            if value is None:
                continue
            settings[attribute.name.replace("_", "-")] = value
        return settings
