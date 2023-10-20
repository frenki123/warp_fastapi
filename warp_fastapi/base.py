from __future__ import annotations

import re
from abc import ABC
from typing import Any

from pydantic import BaseModel, field_validator


class TemplateModel(BaseModel, ABC):
    """
    Abstract class for Attribute, Relationship, BackpopulatesRelationship, AppObject and Project.

    Attributes:
        name (str): The name of the model. Name should be snake_case.

    Methods:
        __str__(): Returns a string representation of the model.
        __init__(**kwargs): Initializes the model with the given keyword arguments.

    Raises:
        ValueError: If name doesn't follow snake case rulle.
    """

    name: str

    @field_validator('name')
    @classmethod
    def _snake_case_validator(cls, name: str) -> str:
        pattern = r'^[a-z][a-z\d]*(_[a-z\d]+)*$'
        if re.search(pattern, name):
            return name
        raise ValueError('Name most follow snake_case rule.')

    def __str__(self) -> str:
        return f'{type(self).__name__}({super().__str__()})'

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    class ConfigDict:
        underscore_attrs_are_private = True
