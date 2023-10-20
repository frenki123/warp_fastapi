from __future__ import annotations

from collections.abc import Callable
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from typing import Any

from pydantic import EmailStr, validate_call

from .base import TemplateModel
from .data_types import (
    DataType,
    bool_type,
    date_only_type,
    date_time_type,
    decimal_type,
    email_type,
    float_type,
    int_type,
    string_type,
    time_type,
    timedelta_type,
)


class Attribute(TemplateModel):
    """
    A class that represents an attribute in a template model.

    Attributes:
        name: str: The name of the model. Name should be snake_case. From TemplateModel
        type: DataType: The type of the attribute.
        default: Any|None: The default value of the attribute. Defaults to None.
        unique: bool: Whether or not the attribute is unique. Defaults to False.
        optional: bool: Whether or not the attribute is optional. Defaults to False.
        validation: list[Callable[[Any],Any]]: Not implemented.
    """

    type: DataType
    default: Any | None = None
    unique: bool = False
    optional: bool = False
    validation: list[Callable[[Any], Any]] = []

    # TODO: add validation for type and default value
    def __init__(
        self,
        name: str,
        type: DataType,
        default: Any = None,
        unique: bool = False,
        optional: bool = False,
        validation_rules: list[Callable[[Any], Any]] = [],
    ) -> None:
        """
        Initializes the attribute with the given arguments.

        Args:
            name: str: The name of the attribute.
            type: DataType: The type of the attribute.
            default: Any: The default value of the attribute. Defaults to None.
            unique: bool: Whether or not the attribute is unique. Defaults to False.
            optional: bool: Whether or not the attribute is optional. Defaults to False.
            validation_rules: list[Callable[[Any],Any]]: Not implemented.
        """
        super().__init__(
            name=name,
            type=type,
            default=default,
            unique=unique,
            optional=optional,
            validation_rules=validation_rules,
        )


@validate_call
def StringAttribute(name: str, default: str | None = None, unique: bool = False, optional: bool = False) -> Attribute:
    """Creates string type attribute with DataType string_type"""
    return Attribute(name, string_type, default, unique, optional)


@validate_call
def IntAttribute(name: str, default: int | None = None, unique: bool = False, optional: bool = False) -> Attribute:
    """Creates int type attribute with DataType int_type"""
    return Attribute(name, int_type, default, unique, optional)


@validate_call
def FloatAttribute(name: str, default: float | None = None, unique: bool = False, optional: bool = False) -> Attribute:
    """Creates float type attribute with DataType float_type"""
    return Attribute(name, float_type, default, unique, optional)


@validate_call
def DecimalAttribute(
    name: str, default: Decimal | None = None, unique: bool = False, optional: bool = False
) -> Attribute:
    """Creates Decimal type attribute with DataType decimal_type"""
    return Attribute(name, decimal_type, default, unique, optional)


@validate_call
def BoolAttribute(name: str, default: bool | None = None, unique: bool = False, optional: bool = False) -> Attribute:
    """Creates bool type attribute with DataType bool_type"""
    return Attribute(name, bool_type, default, unique, optional)


@validate_call
def DateAttribute(name: str, default: date | None = None, unique: bool = False, optional: bool = False) -> Attribute:
    """Creates date type attribute with DataType date_only_type"""
    return Attribute(name, date_only_type, default, unique, optional)


@validate_call
def DateTimeAttribute(
    name: str, default: datetime | None = None, unique: bool = False, optional: bool = False
) -> Attribute:
    """Creates datetime type attribute with DataType date_time_type"""
    return Attribute(name, date_time_type, default, unique, optional)


@validate_call
def TimeAttribute(name: str, default: time | None = None, unique: bool = False, optional: bool = False) -> Attribute:
    """Creates time type attribute with DataType time_type"""
    return Attribute(name, time_type, default, unique, optional)


@validate_call
def TimeDeltaAttribute(
    name: str, default: timedelta | None = None, unique: bool = False, optional: bool = False
) -> Attribute:
    """Creates timedelata type attribute with DataType timedelta_type"""
    return Attribute(name, timedelta_type, default, unique, optional)


@validate_call
def EmailAttribute(
    name: str = 'email', default: EmailStr | None = None, unique: bool = True, optional: bool = False
) -> Attribute:
    """Creates email type attribute with DataType email_type. Default attribute name is email and it is set as unique"""
    return Attribute(name, email_type, default, unique, optional)


@validate_call
def NameAttribute(default: str | None = None, unique: bool = False, optional: bool = False) -> Attribute:
    """Creates string type attribute with DataType string_type. Default attribute name is name"""
    return Attribute('name', string_type, default, unique, optional)


def UsernameAttribute() -> Attribute:
    """Creates string type attribute with DataType string_type. Default attribute name is username.
    Attribute is always unique and it is not optional without default value."""
    return Attribute('username', string_type, default=None, unique=True, optional=False)


@validate_call
def DescriptionAttribute(default: str | None = None, unique: bool = False, optional: bool = False) -> Attribute:
    """Creates string type attribute with DataType string_type. Default attribute name is description."""
    return Attribute('description', string_type, default, unique, optional)
