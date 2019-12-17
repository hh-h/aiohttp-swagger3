from typing import Dict, Union

import attr


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
