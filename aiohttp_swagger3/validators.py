import base64
import enum
import ipaddress
import operator
import re
import uuid
from typing import Any, Dict, List, Optional, Pattern, Set, Union

import attr
import strict_rfc3339
from aiohttp import web

_EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
_HOSTNAME_REGEX = re.compile(r"(?!-)[a-z0-9-]{1,63}(?<!-)$", re.IGNORECASE)


class _MissingType:
    pass


MISSING = _MissingType()


@attr.attrs(slots=True, auto_attribs=True)
class ValidatorError(Exception):
    error: Union[str, Dict]


@attr.attrs(slots=True, frozen=True, auto_attribs=True)
class Validator:
    def validate(self, value: Any, raw: bool) -> Any:
        raise NotImplementedError


class IntegerFormat(enum.Enum):
    Int32 = "int32"
    Int64 = "int64"


class NumberFormat(enum.Enum):
    Float = "float"
    Double = "double"


class StringFormat(enum.Enum):
    Default = "default"
    Date = "date"
    Datetime = "date-time"
    Password = "password"
    Byte = "byte"
    Binary = "binary"
    Email = "email"
    Uuid = "uuid"
    Hostname = "hostname"
    IPv4 = "ipv4"
    IPv6 = "ipv6"


@attr.attrs(slots=True, frozen=True, eq=False, hash=False, auto_attribs=True)
class Integer(Validator):
    format: IntegerFormat = attr.attrib(converter=IntegerFormat)
    minimum: Optional[int] = None
    maximum: Optional[int] = None
    exclusiveMinimum: bool = False
    exclusiveMaximum: bool = False
    enum: Optional[List[int]] = None
    nullable: bool = False
    default: Optional[int] = None

    def validate(
        self, raw_value: Union[None, int, str, _MissingType], raw: bool
    ) -> Union[None, int, _MissingType]:
        if isinstance(raw_value, str):
            if not raw:
                raise ValidatorError("value should be type of int")
            try:
                value = int(raw_value)
            except ValueError:
                raise ValidatorError("value should be type of int")
        elif isinstance(raw_value, int) and not isinstance(raw_value, bool):
            value = raw_value
        elif raw_value is None:
            if self.nullable:
                return None
            raise ValidatorError("value should be type of int")
        elif isinstance(raw_value, _MissingType):
            if self.default is None:
                return raw_value
            value = self.default
        else:
            raise ValidatorError("value should be type of int")
        if (
            self.format == IntegerFormat.Int32
            and not -2_147_483_648 <= value <= 2_147_483_647
        ):
            raise ValidatorError("value out of bounds int32")

        if self.minimum is not None:
            op = operator.le if self.exclusiveMinimum else operator.lt
            if op(value, self.minimum):
                msg = "" if self.exclusiveMinimum else " or equal to"
                raise ValidatorError(f"value should be more than{msg} {self.minimum}")
        if self.maximum is not None:
            op = operator.ge if self.exclusiveMaximum else operator.gt
            if op(value, self.maximum):
                msg = "" if self.exclusiveMaximum else " or equal to"
                raise ValidatorError(f"value should be less than{msg} {self.maximum}")
        if self.enum is not None and value not in self.enum:
            raise ValidatorError(f"value should be one of {self.enum}")
        return value


@attr.attrs(slots=True, frozen=True, eq=False, hash=False, auto_attribs=True)
class Number(Validator):
    format: NumberFormat = attr.attrib(converter=NumberFormat)
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    exclusiveMinimum: bool = False
    exclusiveMaximum: bool = False
    enum: Optional[List[float]] = None
    nullable: bool = False
    default: Optional[float] = None

    def validate(
        self, raw_value: Union[None, int, float, str, _MissingType], raw: bool
    ) -> Union[None, float, _MissingType]:
        if isinstance(raw_value, str):
            if not raw:
                raise ValidatorError("value should be type of float")
            try:
                value = float(raw_value)
            except ValueError:
                raise ValidatorError("value should be type of float")
        elif isinstance(raw_value, float):
            value = raw_value
        elif isinstance(raw_value, int) and not isinstance(raw_value, bool):
            value = float(raw_value)
        elif raw_value is None:
            if self.nullable:
                return None
            raise ValidatorError("value should be type of float")
        elif isinstance(raw_value, _MissingType):
            if self.default is None:
                return raw_value
            value = self.default
        else:
            raise ValidatorError("value should be type of float")

        if self.minimum is not None:
            op = operator.le if self.exclusiveMinimum else operator.lt
            if op(value, self.minimum):
                msg = "" if self.exclusiveMinimum else " or equal to"
                raise ValidatorError(f"value should be more than{msg} {self.minimum}")
        if self.maximum is not None:
            op = operator.ge if self.exclusiveMaximum else operator.gt
            if op(value, self.maximum):
                msg = "" if self.exclusiveMaximum else " or equal to"
                raise ValidatorError(f"value should be less than{msg} {self.maximum}")
        if self.enum is not None and value not in self.enum:
            raise ValidatorError(f"value should be one of {self.enum}")
        return value


def _re_compile(pattern: Optional[str]) -> Optional[Pattern]:
    if pattern is None:
        return None
    return re.compile(pattern)


@attr.attrs(slots=True, frozen=True, eq=False, hash=False, auto_attribs=True)
class String(Validator):
    format: StringFormat = attr.attrib(converter=StringFormat)
    pattern: Optional[Pattern] = attr.attrib(converter=_re_compile)
    minLength: Optional[int] = None
    maxLength: Optional[int] = None
    enum: Optional[List[str]] = None
    nullable: bool = False
    default: Optional[str] = None

    def validate(
        self, raw_value: Union[None, str, bytes, _MissingType], raw: bool
    ) -> Union[None, str, bytes, _MissingType]:
        if isinstance(raw_value, (str, bytes)):
            value = raw_value
        elif raw_value is None:
            if self.nullable:
                return None
            raise ValidatorError("value should be type of str")
        elif isinstance(raw_value, _MissingType):
            if self.default is None:
                return raw_value
            value = self.default
        else:
            raise ValidatorError("value should be type of str")

        if self.minLength is not None and len(value) < self.minLength:
            raise ValidatorError(f"value length should be more than {self.minLength}")
        if self.maxLength is not None and len(value) > self.maxLength:
            raise ValidatorError(f"value length should be less than {self.maxLength}")
        if self.enum is not None and value not in self.enum:
            raise ValidatorError(f"value should be one of {self.enum}")

        if self.format not in (
            StringFormat.Default,
            StringFormat.Password,
            StringFormat.Binary,
        ):
            assert isinstance(value, str)
            if self.format == StringFormat.Uuid:
                try:
                    uuid.UUID(value)
                except ValueError:
                    raise ValidatorError("value should be uuid")
            elif self.format == StringFormat.Datetime:
                if not strict_rfc3339.validate_rfc3339(value):
                    raise ValidatorError("value should be datetime format")
            elif self.format == StringFormat.Date:
                if not strict_rfc3339.validate_rfc3339(f"{value}T00:00:00Z"):
                    raise ValidatorError("value should be date format")
            elif self.format == StringFormat.Email:
                if not _EMAIL_REGEX.match(value):
                    raise ValidatorError("value should be valid email")
            elif self.format == StringFormat.Byte:
                try:
                    base64.b64decode(value)
                except ValueError:
                    raise ValidatorError("value should be base64-encoded string")
            elif self.format == StringFormat.IPv4:
                try:
                    ipaddress.IPv4Address(value)
                except ValueError:
                    raise ValidatorError("value should be valid ipv4 address")
            elif self.format == StringFormat.IPv6:
                try:
                    ipaddress.IPv6Address(value)
                except ValueError:
                    raise ValidatorError("value should be valid ipv6 address")
            elif self.format == StringFormat.Hostname:
                hostname = value[:-1] if value[-1] == "." else value
                if len(hostname) > 255 or not all(
                    _HOSTNAME_REGEX.match(x) for x in hostname.split(".")
                ):
                    raise ValidatorError("value should be valid hostname")

        if (
            self.format != StringFormat.Binary
            and self.pattern
            and not self.pattern.search(value)
        ):
            raise ValidatorError(
                f"value should match regex pattern '{self.pattern.pattern}'"
            )

        return value


@attr.attrs(slots=True, frozen=True, eq=False, hash=False, auto_attribs=True)
class Boolean(Validator):
    nullable: bool = False
    default: Optional[bool] = None

    def validate(
        self, raw_value: Union[None, bool, str, _MissingType], raw: bool
    ) -> Union[None, bool, _MissingType]:
        if isinstance(raw_value, str):
            if not raw:
                raise ValidatorError("value should be type of bool")
            if raw_value == "true":
                value = True
            elif raw_value == "false":
                value = False
            else:
                raise ValidatorError("value should be type of bool")
        elif isinstance(raw_value, bool):
            value = raw_value
        elif raw_value is None:
            if self.nullable:
                return None
            raise ValidatorError("value should be type of bool")
        elif isinstance(raw_value, _MissingType):
            if self.default is None:
                return raw_value
            value = self.default
        else:
            raise ValidatorError("value should be type of bool")
        return value


@attr.attrs(slots=True, frozen=True, eq=False, hash=False, auto_attribs=True)
class Array(Validator):
    validator: Validator
    uniqueItems: bool
    minItems: Optional[int] = None
    maxItems: Optional[int] = None
    nullable: bool = False

    def validate(
        self, raw_value: Union[None, str, List, _MissingType], raw: bool
    ) -> Union[None, List, _MissingType]:
        if isinstance(raw_value, str):
            if not raw:
                raise ValidatorError("value should be type of list")
            items = []
            index = 0
            if raw_value:
                try:
                    for i, value in enumerate(raw_value.split(",")):
                        index = i
                        items.append(self.validator.validate(value, raw))
                except ValidatorError as e:
                    raise ValidatorError({index: e.error})
        elif isinstance(raw_value, list):
            items = []
            index = 0
            try:
                for i, value in enumerate(raw_value):
                    index = i
                    items.append(self.validator.validate(value, raw))
            except ValidatorError as e:
                raise ValidatorError({index: e.error})
        elif raw_value is None:
            if self.nullable:
                return None
            raise ValidatorError("value should be type of list")
        elif isinstance(raw_value, _MissingType):
            return raw_value
        else:
            raise ValidatorError("value should be type of list")

        if self.minItems is not None and len(items) < self.minItems:
            raise ValidatorError(f"number or items must be more than {self.minItems}")
        if self.maxItems is not None and len(items) > self.maxItems:
            raise ValidatorError(f"number or items must be less than {self.maxItems}")
        if self.uniqueItems and len(items) != len(set(items)):
            raise ValidatorError("all items must be unique")
        return items


@attr.attrs(slots=True, frozen=True, eq=False, hash=False, auto_attribs=True)
class Object(Validator):
    properties: Dict[str, Validator]
    required: Set[str]
    minProperties: Optional[int] = None
    maxProperties: Optional[int] = None
    additionalProperties: Union[bool, Validator] = True
    nullable: bool = False

    def validate(
        self, raw_value: Union[None, Dict, _MissingType], raw: bool
    ) -> Union[None, Dict, _MissingType]:
        if raw_value is None:
            if self.nullable:
                return None
            raise ValidatorError("value should be type of dict")
        elif not isinstance(raw_value, dict):
            if isinstance(raw_value, _MissingType):
                return raw_value
            raise ValidatorError("value should be type of dict")
        value = {}
        errors: Dict = {}
        for name in self.required:
            if name not in raw_value:
                errors[name] = "required property"
        if errors:
            raise ValidatorError(errors)

        for name, validator in self.properties.items():
            prop = raw_value.get(name, MISSING)
            try:
                val = validator.validate(prop, raw)
                if val != MISSING:
                    value[name] = val
            except ValidatorError as e:
                errors[name] = e.error
        if errors:
            raise ValidatorError(errors)

        if isinstance(self.additionalProperties, bool):
            if not self.additionalProperties:
                additional_properties = raw_value.keys() - value.keys()
                if additional_properties:
                    raise ValidatorError(
                        {
                            k: "additional property not allowed"
                            for k in additional_properties
                        }
                    )
            else:
                for key in raw_value.keys() - value.keys():
                    value[key] = raw_value[key]
        else:
            for name in raw_value.keys() - value.keys():
                validator = self.additionalProperties
                value[name] = validator.validate(raw_value[name], raw)
        if self.minProperties is not None and len(value) < self.minProperties:
            raise ValidatorError(
                f"number or properties must be more than {self.minProperties}"
            )
        if self.maxProperties is not None and len(value) > self.maxProperties:
            raise ValidatorError(
                f"number or properties must be less than {self.maxProperties}"
            )
        return value


@attr.attrs(slots=True, frozen=True, eq=False, hash=False, auto_attribs=True)
class OneOf(Validator):
    validators: List[Validator]

    def validate(self, raw_value: Any, raw: bool) -> Any:
        found = False
        value = None
        for validator in self.validators:
            try:
                value = validator.validate(raw_value, raw)
            except ValidatorError:
                continue
            if found:
                raise ValidatorError("fail to validate oneOf")
            found = True
        if not found:
            raise ValidatorError("fail to validate oneOf")
        return value


@attr.attrs(slots=True, frozen=True, eq=False, hash=False, auto_attribs=True)
class AnyOf(Validator):
    validators: List[Validator]

    def validate(self, raw_value: Any, raw: bool) -> Any:
        for validator in self.validators:
            try:
                return validator.validate(raw_value, raw)
            except ValidatorError:
                pass
        raise ValidatorError("fail to validate anyOf")


@attr.attrs(slots=True, frozen=True, eq=False, hash=False, auto_attribs=True)
class AllOf(Validator):
    validators: List[Validator]

    def validate(self, raw_value: Any, raw: bool) -> Any:
        value: Dict = {}
        for validator in self.validators:
            try:
                value.update(validator.validate(raw_value, raw))
            except ValidatorError:
                raise ValidatorError("fail to validate allOf")
        return value


@attr.attrs(slots=True, frozen=True, eq=False, hash=False, auto_attribs=True)
class AuthBasic(Validator):
    name: str = "authorization"

    def validate(self, request: web.Request, _: bool) -> Dict[str, str]:
        try:
            value = request.headers.getone(self.name)
        except KeyError:
            raise ValidatorError({self.name: "is required"})

        if not value.startswith("Basic "):
            raise ValidatorError({self.name: "value should start with 'Basic' word"})
        return {self.name: value.replace("Basic ", "")}


@attr.attrs(slots=True, frozen=True, eq=False, hash=False, auto_attribs=True)
class AuthBearer(Validator):
    name: str = "authorization"

    def validate(self, request: web.Request, _: bool) -> Dict[str, str]:
        try:
            value = request.headers.getone(self.name)
        except KeyError:
            raise ValidatorError({self.name: "is required"})

        if not value.startswith("Bearer "):
            raise ValidatorError({self.name: "value should start with 'Bearer' word"})
        return {self.name: value.replace("Bearer ", "")}


@attr.attrs(slots=True, frozen=True, eq=False, hash=False, auto_attribs=True)
class AuthApiKeyHeader(Validator):
    name: str

    def validate(self, request: web.Request, _: bool) -> Dict[str, str]:
        try:
            value = request.headers.getone(self.name)
        except KeyError:
            raise ValidatorError({self.name: "is required"})

        if len(value) == 0:
            raise ValidatorError({self.name: "value length should be more than 1"})
        return {self.name: value}


@attr.attrs(slots=True, frozen=True, eq=False, hash=False, auto_attribs=True)
class AuthApiKeyQuery(Validator):
    name: str

    def validate(self, request: web.Request, _: bool) -> Dict[str, str]:
        try:
            value = request.rel_url.query.getone(self.name)
        except KeyError:
            raise ValidatorError({self.name: "is required"})

        if len(value) == 0:
            raise ValidatorError({self.name: "value length should be more than 1"})
        return {self.name: value}


@attr.attrs(slots=True, frozen=True, eq=False, hash=False, auto_attribs=True)
class AuthApiKeyCookie(Validator):
    name: str

    def validate(self, request: web.Request, _: bool) -> Dict[str, str]:
        try:
            value = request.cookies[self.name]
        except KeyError:
            raise ValidatorError({self.name: "is required"})

        if len(value) == 0:
            raise ValidatorError({self.name: "value length should be more than 1"})
        return {self.name: value}


@attr.attrs(slots=True, frozen=True, eq=False, hash=False, auto_attribs=True)
class AnyOfAuth(Validator):
    validators: List[Validator]

    def validate(self, request: web.Request, raw: bool) -> Dict[str, str]:
        for validator in self.validators:
            try:
                value: Dict[str, str] = validator.validate(request, raw)
                return value
            except ValidatorError:
                continue
        raise ValidatorError("no auth has been provided")


@attr.attrs(slots=True, frozen=True, eq=False, hash=False, auto_attribs=True)
class AllOfAuth(Validator):
    validators: List[Validator]

    def validate(self, request: web.Request, raw: bool) -> Dict[str, str]:
        value: Dict[str, str] = {}
        for validator in self.validators:
            value.update(validator.validate(request, raw))
        return value


def _type_to_validator(schema: Dict, components: Dict) -> Validator:
    if "type" not in schema:
        raise KeyError("type is required")
    if schema["type"] == "integer":
        return Integer(
            nullable=schema.get("nullable", False),
            minimum=schema.get("minimum"),
            maximum=schema.get("maximum"),
            exclusiveMinimum=schema.get("exclusiveMinimum", False),
            exclusiveMaximum=schema.get("exclusiveMaximum", False),
            enum=schema.get("enum"),
            format=schema.get("format", IntegerFormat.Int64),
            default=schema.get("default"),
        )
    elif schema["type"] == "number":
        return Number(
            nullable=schema.get("nullable", False),
            minimum=schema.get("minimum"),
            maximum=schema.get("maximum"),
            exclusiveMinimum=schema.get("exclusiveMinimum", False),
            exclusiveMaximum=schema.get("exclusiveMaximum", False),
            enum=schema.get("enum"),
            format=schema.get("format", NumberFormat.Double),
            default=schema.get("default"),
        )
    elif schema["type"] == "string":
        return String(
            format=schema.get("format", StringFormat.Default),
            nullable=schema.get("nullable", False),
            minLength=schema.get("minLength"),
            maxLength=schema.get("maxLength"),
            enum=schema.get("enum"),
            default=schema.get("default"),
            pattern=schema.get("pattern"),
        )
    elif schema["type"] == "boolean":
        return Boolean(
            nullable=schema.get("nullable", False), default=schema.get("default")
        )
    elif schema["type"] == "array":
        return Array(
            nullable=schema.get("nullable", False),
            validator=schema_to_validator(schema["items"], components),
            uniqueItems=schema.get("uniqueItems", False),
            minItems=schema.get("minItems"),
            maxItems=schema.get("maxItems"),
        )
    elif schema["type"] == "object":
        # TODO move this logic to class?
        properties = {
            k: schema_to_validator(v, components)
            for k, v in schema.get("properties", {}).items()
        }
        raw_additional_properties = schema.get("additionalProperties", True)
        if isinstance(raw_additional_properties, dict):
            additional_properties = schema_to_validator(
                raw_additional_properties, components
            )
        else:
            additional_properties = raw_additional_properties
        return Object(
            nullable=schema.get("nullable", False),
            properties=properties,
            required=set(schema.get("required", [])),
            minProperties=schema.get("minProperties"),
            maxProperties=schema.get("maxProperties"),
            additionalProperties=additional_properties,
        )
    else:
        raise Exception(f"Unknown type '{schema['type']}'")


def schema_to_validator(schema: Dict, components: Dict) -> Validator:
    if "$ref" in schema:
        if not components:
            raise Exception("file with components definitions is missing")
        # #/components/schemas/Pet
        *_, section, obj = schema["$ref"].split("/")
        schema = components[section][obj]
    if "oneOf" in schema:
        return OneOf(
            validators=[schema_to_validator(sch, components) for sch in schema["oneOf"]]
        )
    elif "anyOf" in schema:
        return AnyOf(
            validators=[schema_to_validator(sch, components) for sch in schema["anyOf"]]
        )
    elif "allOf" in schema:
        return AllOf(
            validators=[schema_to_validator(sch, components) for sch in schema["allOf"]]
        )
    else:
        return _type_to_validator(schema, components)


def _security_to_validator(sec_name: str, components: Dict) -> Validator:
    if sec_name not in components["securitySchemes"]:
        raise Exception(f"security schema {sec_name} must be defined in components")
    sec_def = components["securitySchemes"][sec_name]
    if sec_def["type"] == "http":
        if sec_def["scheme"] == "basic":
            return AuthBasic()
        elif sec_def["scheme"] == "bearer":
            return AuthBearer()
        else:
            raise Exception(f"Unknown scheme {sec_def['scheme']} in {sec_name}")
    elif sec_def["type"] == "apiKey":
        if sec_def["in"] == "header":
            return AuthApiKeyHeader(name=sec_def["name"].lower())
        elif sec_def["in"] == "query":
            return AuthApiKeyQuery(name=sec_def["name"])
        elif sec_def["in"] == "cookie":
            return AuthApiKeyCookie(name=sec_def["name"])
        else:
            raise Exception(f"Unknown value of in {sec_def['in']} in {sec_name}")
    else:
        raise Exception(f"Unsupported auth type {sec_def['type']}")


def security_to_validator(schema: List[Dict], components: Dict) -> Validator:
    if "securitySchemes" not in components:
        raise Exception("securitySchemes must be defined in components")
    if len(schema) > 1:
        validators = []
        for security in schema:
            if len(security) > 1:
                validator: Validator = AllOfAuth(
                    validators=[
                        _security_to_validator(sec_name, components)
                        for sec_name in security
                    ]
                )
            else:
                validator = _security_to_validator(next(iter(security)), components)
            validators.append(validator)
        return AnyOfAuth(validators=validators)
    else:
        security = schema[0]
        if len(security) > 1:
            return AllOfAuth(
                validators=[
                    _security_to_validator(sec_name, components)
                    for sec_name in security
                ]
            )
        else:
            return _security_to_validator(next(iter(security)), components)
