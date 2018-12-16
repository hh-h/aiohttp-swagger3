import attr

from .validators import Validator


@attr.attrs(slots=True, auto_attribs=True)
class Parameter:
    name: str
    validator: Validator
    required: bool
