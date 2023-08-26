from datetime import date, datetime, time, timedelta
from decimal import Decimal

from pydantic import EmailStr
from sqlalchemy.types import (
    BigInteger,
    Boolean,
    Date,
    DateTime,
    Float,
    Integer,
    Interval,
    Numeric,
    String,
    Text,
    Time,
    Unicode,
)

from .types import DataType

int_type = DataType(int, Integer)

"""The `int_type` variable is a shortcut for creating a `DataType` object
that represents the `int` Python type and the `Integer` database type.

The `pydantic_type` attribute of the `int_type` variable is set to `None`.
"""

bigint_type = DataType(int, BigInteger)

"""The `bigint_type` variable is a shortcut for creating a `DataType`
object that represents the `int` Python type and the `BigInteger` database type.

The `pydantic_type` attribute of the `bigint_type` variable is set to `None`.
"""

string_type = DataType(str, String)

"""
The `string_type` variable is a shortcut for creating a `DataType`
object that represents the `str` Python type and the `String` database type.

The `pydantic_type` attribute of the `string_type` variable is set to `None`.
"""

float_type = DataType(float, Float)

"""
The `float_type` variable is a shortcut for creating a `DataType`
object that represents the `float` Python type and the `Float` database type.

The `pydantic_type` attribute of the `float_type` variable is set to `None`.
"""

decimal_type = DataType(Decimal, Numeric)

"""
The `decimal_type` variable is a shortcut for creating a `DataType`
object that represents the `Decimal` Python type and the `Numeric` database type.

The `pydantic_type` attribute of the `decimal_type` variable is set to `None`.
"""

bool_type = DataType(bool, Boolean)

"""
The `bool_type` variable is a shortcut for creating a `DataType`
 that represents the `bool` Python type and the `Boolean` database type.

The `pydantic_type` attribute of the `bool_type` variable is set to `None`.
"""

date_only_type = DataType(date, Date)

"""
The `date_only_type` variable is a shortcut for creating a `DataType`
object that represents the `date` Python type and the `Date` database type.

The `pydantic_type` attribute of the `date_only_type` variable is set to `None`.
"""

date_time_type = DataType(datetime, DateTime)

"""
The `date_time_type` variable is a shortcut for creating a `DataType`
 that represents the `datetime` Python type and the `DateTime` database type.

The `pydantic_type` attribute of the `date_time_type` variable is set to `None`.
"""

timedelta_type = DataType(timedelta, Interval)

"""
The `timedelta_type` variable is a shortcut for creating a `DataType`
object that represents the `timedelta` Python type and the `Interval` database type.

The `pydantic_type` attribute of the `timedelta_type` variable is set to `None`.
"""

time_type = DataType(time, Time)

"""
The `time_type` variable is a shortcut for creating a `DataType`
object that represents the `time` Python type and the `Time` database type.

The `pydantic_type` attribute of the `time_type` variable is set to `None`.
"""

text_type = DataType(str, Text)

"""
The `text_type` variable is a shortcut for creating a `DataType`
object that represents the `str` Python type and the `Text` database type.

The `pydantic_type` attribute of the `text_type` variable is set to `None`.
"""

unicode_type = DataType(str, Unicode)

"""
The `unicode_type` variable is a shortcut for creating a `DataType`
object that represents the `str` Python type and the `Unicode` database type.

The `pydantic_type` attribute of the `unicode_type` variable is set to `None`.
"""

email_type = DataType(str, String, EmailStr)
