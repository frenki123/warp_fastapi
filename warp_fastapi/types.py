from enum import Enum, auto

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

    def __init__(self, python_type: type, db_type: type, pydantic_type: type | None = None):
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
            db_type=db_type.__name__,
            db_module=db_type.__module__,
        )
        if pydantic_type:
            self.add_pydantic_type(pydantic_type)

    def add_pydantic_type(self, t: type) -> None:
        """
        Adds the given Pydantic type to the data type.

        Args:
            t (type): The Pydantic type to add.
        """
        self.pydantic_type = t.__name__


class SchemaType(Enum):
    create = auto()
    edit = auto()
    read = auto()
    db = auto()


create_schema = SchemaType.create
edit_schema = SchemaType.edit
read_schema = SchemaType.read
db_schema = SchemaType.db

all_schemas = [SchemaType.create, SchemaType.edit, SchemaType.read, SchemaType.db]
