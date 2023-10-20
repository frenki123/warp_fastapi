from datetime import date, datetime, time, timedelta
from decimal import Decimal

from pydantic import BaseModel


class DataType(BaseModel):
    """
    DataType object used in fastapiez

    Attributes:
        python_type (str): The Python type of the data type.
        python_module (str): The module that the Python type belongs to.
        db_type (str): The database type of the data type.
        db_module (str): The module that the database type belongs to.
        pydantic_type (str): The Pydantic type of the data type.

    Methods:
        add_pydantic_type(t): Adds the given Pydantic type to the data type.
    """

    python_type: str
    python_module: str
    db_type: str
    db_module: str
    pydantic_type: str | None = None

    def __init__(self, python_type: type, db_type: str, db_module: str, pydantic_type: str | None = None):
        """
        Initializes a new `DataType` instance.
        Args:
            python_type (type): The Python type of the data type.
            db_type (type): The database type of the data type.
            pydantic_type (type, optional): The Pydantic type of the data type. Defaults to None.
        """
        super().__init__(
            python_type=python_type.__name__,
            python_module=python_type.__module__,
            db_type=db_type,
            db_module=db_module,
        )
        if pydantic_type:
            self.add_pydantic_type(pydantic_type)

    def add_pydantic_type(self, t: str) -> None:
        """
        Adds the given Pydantic type to the data type.

        Args:
            t (type): The Pydantic type to add.
        """
        self.pydantic_type = t


int_type = DataType(int, 'Integer', 'sqlalchemy.types')

"""The `int_type` variable is a shortcut for creating a `DataType` object
that represents the `int` Python type and the `Integer` database type.

The `pydantic_type` attribute of the `int_type` variable is set to `None`.
"""

bigint_type = DataType(int, 'BigInteger', 'sqlalchemy.types')

"""The `bigint_type` variable is a shortcut for creating a `DataType`
object that represents the `int` Python type and the `BigInteger` database type.

The `pydantic_type` attribute of the `bigint_type` variable is set to `None`.
"""

string_type = DataType(str, 'String', 'sqlalchemy.types')

"""
The `string_type` variable is a shortcut for creating a `DataType`
object that represents the `str` Python type and the `String` database type.

The `pydantic_type` attribute of the `string_type` variable is set to `None`.
"""

float_type = DataType(float, 'Float', 'sqlalchemy.types')

"""
The `float_type` variable is a shortcut for creating a `DataType`
object that represents the `float` Python type and the `Float` database type.

The `pydantic_type` attribute of the `float_type` variable is set to `None`.
"""

decimal_type = DataType(Decimal, 'Numeric', 'sqlalchemy.types')

"""
The `decimal_type` variable is a shortcut for creating a `DataType`
object that represents the `Decimal` Python type and the `Numeric` database type.

The `pydantic_type` attribute of the `decimal_type` variable is set to `None`.
"""

bool_type = DataType(bool, 'Boolean', 'sqlalchemy.types')

"""
The `bool_type` variable is a shortcut for creating a `DataType`
 that represents the `bool` Python type and the `Boolean` database type.

The `pydantic_type` attribute of the `bool_type` variable is set to `None`.
"""

date_only_type = DataType(date, 'Date', 'sqlalchemy.types')

"""
The `date_only_type` variable is a shortcut for creating a `DataType`
object that represents the `date` Python type and the `Date` database type.

The `pydantic_type` attribute of the `date_only_type` variable is set to `None`.
"""

date_time_type = DataType(datetime, 'DateTime', 'sqlalchemy.types')

"""
The `date_time_type` variable is a shortcut for creating a `DataType`
 that represents the `datetime` Python type and the `DateTime` database type.

The `pydantic_type` attribute of the `date_time_type` variable is set to `None`.
"""

timedelta_type = DataType(timedelta, 'Interval', 'sqlalchemy.types')

"""
The `timedelta_type` variable is a shortcut for creating a `DataType`
object that represents the `timedelta` Python type and the `Interval` database type.

The `pydantic_type` attribute of the `timedelta_type` variable is set to `None`.
"""

time_type = DataType(time, 'Time', 'sqlalchemy.types')

"""
The `time_type` variable is a shortcut for creating a `DataType`
object that represents the `time` Python type and the `Time` database type.

The `pydantic_type` attribute of the `time_type` variable is set to `None`.
"""

text_type = DataType(str, 'Text', 'sqlalchemy.types')

"""
The `text_type` variable is a shortcut for creating a `DataType`
object that represents the `str` Python type and the `Text` database type.

The `pydantic_type` attribute of the `text_type` variable is set to `None`.
"""

unicode_type = DataType(str, 'Unicode', 'sqlalchemy.types')

"""
The `unicode_type` variable is a shortcut for creating a `DataType`
object that represents the `str` Python type and the `Unicode` database type.

The `pydantic_type` attribute of the `unicode_type` variable is set to `None`.
"""

email_type = DataType(str, 'String', 'sqlalchemy.types', 'EmailStr')
"""
The `email_type` variable is a shortcut for creating a `DataType`
object that represents the `str` Python type and the `String` database type.

The `pydantic_type` attribute of the `email_type` variable is set to `EmailStr`.
"""
