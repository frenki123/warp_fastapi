from __future__ import annotations

from enum import Enum, auto
from typing import TYPE_CHECKING

from .base import TemplateModel
from .exceptions import RelationshipException, RelMsgErr

if TYPE_CHECKING:
    from .app_object import AppObject


class RelationshipType(Enum):
    one_to_many = auto()
    many_to_one = auto()
    one_to_one = auto()
    many_to_many = auto()


one_to_many = RelationshipType.one_to_many
many_to_one = RelationshipType.many_to_one
one_to_one = RelationshipType.one_to_one
many_to_many = RelationshipType.many_to_many


class Relationship(TemplateModel):
    """
    A class representing a relationship between two objects.

    Args:
        name (str): The name of the relationship.
        obj (AppObject): The object that this relationship is associated with.
        type (RelationshipType): The type of relationship.
        optional (bool, optional): Whether the relationship is optional. Defaults to False.

    Raises:
        RelationshipException: If the relationship type is `many_to_many`.
    """

    related_object: AppObject
    relationship_type: RelationshipType
    optional: bool = False

    def __init__(
        self,
        name: str,
        obj: AppObject,
        type: RelationshipType,
        optional: bool = False,
    ) -> None:
        if type == many_to_many:
            raise RelationshipException(RelMsgErr.MANY_MANY_ERR)
        super().__init__(
            name=name,
            related_object=obj,
            relationship_type=type,
            optional=optional,
        )


class BackpopulatesRelationship(TemplateModel):
    """
    A class representing a backpopulates relationship between two objects.

    Args:
        name (str): The name of the relationship.
        obj (AppObject): The object that this relationship is associated with.
        type (RelationshipType): The type of relationship.
        back_populates_name (str): The name of the backpopulates relationship on the related object.
        back_populates_object (AppObject): The related object.
        optional (bool, optional): Whether the relationship is optional. Defaults to False.
    """

    related_object: AppObject
    relationship_type: RelationshipType
    optional: bool = False
    back_populates_name: str
    back_populates_object: AppObject

    def __init__(
        self,
        name: str,
        obj: AppObject,
        type: RelationshipType,
        back_populates_name: str,
        back_populates_object: AppObject,
        optional: bool = False,
    ) -> None:
        super().__init__(
            name=name,
            related_object=obj,
            relationship_type=type,
            optional=optional,
            back_populates_object=back_populates_object,
            back_populates_name=back_populates_name,
        )


def create_relationship(
    name: str,
    obj: AppObject,
    type: RelationshipType,
    back_populates_object: AppObject | None = None,
    back_populates_name: str | None = None,
    optional: bool = False,
) -> Relationship | BackpopulatesRelationship:
    """
    Creates a relationship between two objects.

    Args:
    name (str): The name of the relationship.
    obj (AppObject): The object that this relationship is associated with.
    type (RelationshipType): The type of relationship.
    back_populates_object (AppObject | None): The related object.
    back_populates_name (str | None): The name of the backpopulates relationship on the related object.
    optional (bool): Whether the relationship is optional. Defaults to False.

    Returns:
    Relationship | BackpopulatesRelationship: The created relationship.
    """
    if back_populates_name and back_populates_object:
        return BackpopulatesRelationship(name, obj, type, back_populates_name, back_populates_object, optional)
    return Relationship(name, obj, type)
