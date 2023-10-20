"""
Main module for definition of application objects. Contains AppObject and AppConfing.
"""
from __future__ import annotations

import re

from pydantic import BaseModel

from .attributes import (
    Attribute,
    DescriptionAttribute,
    EmailAttribute,
    NameAttribute,
    StringAttribute,
    UsernameAttribute,
)
from .base import TemplateModel
from .relationships import (
    BackpopulatesRelationship,
    Relationship,
    RelationshipType,
    create_relationship,
    many_to_many,
    many_to_one,
    one_to_many,
    one_to_one,
)


# TODO:add name validation for these attributes
class AppConfig(BaseModel):
    """
    A class representing the configuration of an app.

    Attributes:
        route_name (str | None): The route name for the app.
        table_name (str | None): The database table name for the app.
        class_name (str | None): The class name for the app.
        plural (str | None): The plural form of the app name.
        plural_class_name (str | None): The plural class name for the app.
    """

    route_name: str | None = None
    table_name: str | None = None
    class_name: str | None = None
    plural: str | None = None
    plural_class_name: str | None = None


class AppObject(TemplateModel):
    """
    A class representing an object in an application.
    Attributes:
        attributes (list[Attribute]): The attributes of the object.
        relationships (list[Relationship | BackpopulatesRelationship]): The relationships of the object.
        back_populates_relationships (list[BackpopulatesRelationship]): The backpopulates relationships of the object.
        config (AppConfig): The configuration of the object.
    """

    attributes: list[Attribute]
    relationships: list[Relationship | BackpopulatesRelationship] = []
    back_populates_relationships: list[BackpopulatesRelationship] = []
    config: AppConfig = AppConfig()
    secure: bool = False

    def __init__(
        self,
        name: str,
        *args: Attribute,
        config: AppConfig = AppConfig(),
        secure: bool = False,
    ):
        """
        Initializes an instance of the `AppObject` class.

        Args:
            name (str): The name of the object.
            *args: The attributes of the object.
            config (AppConfig): The configuration of the object.
        """
        super().__init__(name=name, attributes=args, config=config, secure=secure)

    def add_relationship(
        self,
        obj: AppObject,
        type: RelationshipType,
        name: str,
        back_populates_name: str | None = None,
        optional: bool = False,
    ) -> None:
        """
        Adds a relationship to the object.
        Args:
            obj (AppObject): The object that is related to this object.
            type (RelationshipType): The type of the relationship.
            name (str): The name of the relationship.
            back_populates_name (str | None): The name of the backpopulates relationship on the related object.
            optional (bool): Whether the relationship is optional.
        """
        # TODO: add validation to not have duplicated names in relationships and attributes
        rel = create_relationship(name, obj, type, self, back_populates_name, optional)
        self.relationships.append(rel)
        if isinstance(rel, BackpopulatesRelationship):
            rel.related_object.back_populates_relationships.append(rel)

    def add_one_to_one_rel(
        self,
        obj: AppObject,
        name: str,
        back_populates_name: str | None = None,
        optional: bool = False,
    ) -> None:
        """
        Adds a one to one relationship to the object.
        Args:
            obj (AppObject): The object that is related to this object.
            name (str): The name of the relationship.
            back_populates_name (str | None): The name of the backpopulates relationship on the related object.
            optional (bool): Whether the relationship is optional.
        """
        self.add_relationship(obj, one_to_one, name, back_populates_name, optional)

    def add_one_to_many_rel(
        self,
        obj: AppObject,
        name: str,
        back_populates_name: str | None = None,
        optional: bool = False,
    ) -> None:
        """
        Adds a one to many relationship to the object.
        Args:
            obj (AppObject): The object that is related to this object.
            name (str): The name of the relationship.
            back_populates_name (str | None): The name of the backpopulates relationship on the related object.
            optional (bool): Whether the relationship is optional.
        """
        self.add_relationship(obj, one_to_many, name, back_populates_name, optional)

    def add_many_to_one_rel(
        self,
        obj: AppObject,
        name: str,
        back_populates_name: str | None = None,
        optional: bool = False,
    ) -> None:
        """
        Adds a many to one relationship to the object.
        Args:
            obj (AppObject): The object that is related to this object.
            name (str): The name of the relationship.
            back_populates_name (str | None): The name of the backpopulates relationship on the related object.
            optional (bool): Whether the relationship is optional.
        """
        self.add_relationship(obj, many_to_one, name, back_populates_name, optional)

    def add_many_to_many_rel(
        self,
        obj: AppObject,
        name: str,
        back_populates_name: str | None = None,
        optional: bool = False,
    ) -> None:
        """
        Adds a many to many relationship to the object.
        Args:
            obj (AppObject): The object that is related to this object.
            name (str): The name of the relationship.
            back_populates_name (str | None): The name of the backpopulates relationship on the related object.
            optional (bool): Whether the relationship is optional.
        """
        self.add_relationship(obj, many_to_many, name, back_populates_name, optional)

    def add_attributes(self, *args: Attribute) -> None:
        """
        Adds attributes to the object.

        Args:
            *args: The attributes to add.
        """
        self.attributes += args

    def is_relationship_self(self, rel: Relationship | BackpopulatesRelationship) -> bool:
        """
        Checks if the relationship is a self-relationship.

        Args:
            rel (Relationship | BackpopulatesRelationship): The relationship to check.

        Returns:
            bool: Whether the relationship is a self-relationship.
        """
        self._check_rel(rel)
        return self.name == rel.related_object.name

    def is_relationship_multiple(self, relationship: Relationship | BackpopulatesRelationship) -> bool:
        """
        Checks if the relationship has multiple instances of the same object.

        Args:
            relationship (Relationship | BackpopulatesRelationship): The relationship to check.

        Returns:
            bool: Whether the relationship is multiple.
        """
        check_list: list[str] = [rel.related_object.name for rel in self.relationships]
        if self.is_rel_backref(relationship):
            check_list = [rel.back_populates_object.name for rel in self.back_populates_relationships]

        return check_list.count(relationship.related_object.name) > 1

    def is_relationship_many(self, relationship: Relationship | BackpopulatesRelationship) -> bool:
        """
        Checks if the relationship is many-to-one or many-to-many..

        Args:
            relationship (Relationship | BackpopulatesRelationship): The relationship to check.

        Returns:
            bool: Whether the relationship is multiple.
        """
        self._check_rel(relationship)
        if relationship in self.relationships:
            return relationship.relationship_type in (one_to_many, many_to_many)
        return relationship.relationship_type in (many_to_one, many_to_many)

    def is_rel_backref(self, relationship: Relationship | BackpopulatesRelationship) -> bool:
        """
        Checks if the relationship is backreferances.
        Args:
            relationship (Relationship | BackpopulatesRelationship): The relationship to check.

        Returns:
            bool: Whether the relationship is multiple.
        """
        self._check_rel(relationship)
        return relationship in self.back_populates_relationships

    def get_rel_name(self, rel: Relationship | BackpopulatesRelationship) -> str:
        """
        Gets the name of the relationship.

        Args:
            rel (Relationship | BackpopulatesRelationship): The relationship to get the name of.

        Returns:
            str: The name of the relationship.
        """
        if self.is_rel_backref(rel) and isinstance(rel, BackpopulatesRelationship):
            return rel.back_populates_name
        return rel.name

    def get_backpopulates_name(self, rel: BackpopulatesRelationship) -> str:
        """
        Gets the name of the backpopulates relationship.

        Args:
            rel (BackpopulatesRelationship): The relationship to get the name of.

        Returns:
            str: The name of the relationship.
        """
        if self.is_rel_backref(rel):
            return rel.name
        return rel.back_populates_name

    def get_rel_obj(self, rel: Relationship | BackpopulatesRelationship) -> AppObject:
        """
        Gets the AppObject of the relationship.

        Args:
            rel (Relationship | BackpopulatesRelationship): The relationship to get the name of.

        Returns:
            AppObject: AppObject of the relationship.
        """
        if self.is_rel_backref(rel) and isinstance(rel, BackpopulatesRelationship):
            return rel.back_populates_object
        return rel.related_object

    def _check_rel(self, rel: Relationship | BackpopulatesRelationship) -> None:
        """
        Checks if the relationship is associated with the object.

        Args:
            rel (Relationship | BackpopulatesRelationship): The relationship to check.

        Raises:
            AttributeError: If the relationship is not associated with the object.
        """
        if rel not in (self.relationships + self.back_populates_relationships):
            raise AttributeError('Relationship not associated with object!')

    @property
    def all_relationships(self) -> list[Relationship | BackpopulatesRelationship]:
        """
        Gets all the relationships of the object.

        Returns:
            list[Relationship | BackpopulatesRelationship]: The relationships of the object.
        """
        x: list[Relationship | BackpopulatesRelationship] = list(self.relationships)
        x.extend(self.back_populates_relationships)
        return x

    @staticmethod
    def _class_name(name: str) -> str:
        """
        Converts a name to a class name.

        Args:
            name (str): The name to convert.

        Returns:
            str: The class name.
        """
        splite_names = name.split('_')
        name = ''.join([split_name.capitalize() for split_name in splite_names])
        return name

    @property
    def _plural(self) -> str:
        """
        Gets the plural name of the object.

        Returns:
            str: The plural name of the object.
        """
        if self.config.plural:
            return self.config.plural
        word = self.name
        if re.search('[sxz]$', word) or re.search('[^aeioudgkprt]h$', word):
            return re.sub('$', 'es', word)
        if re.search('[^aeiou]y$', word):
            return re.sub('y$', 'ies', word)
        return word + 's'

    @property
    def plural_class_name(self) -> str:
        """
        Gets the plural class name of the object.

        Returns:
            str: The plural class name of the object.
        """
        if self.config.plural_class_name:
            return self.config.plural_class_name
        plural = self._plural
        return self._class_name(plural)

    @property
    def class_name(self) -> str:
        """
        Gets the class name of the object.

        Returns:
            str: The class name of the object.
        """
        if self.config.class_name:
            return self.config.class_name
        return self._class_name(self.name)

    @property
    def table_name(self) -> str:
        """
        Gets the table name of the object.

        Returns:
            str: The table name of the object.
        """
        if self.config.table_name:
            return self.config.table_name
        if self.config.plural:
            return self.config.plural
        return self._plural

    @property
    def route_name(self) -> str:
        """
        Gets the route name of the object.

        Returns:
            str: The route name of the object.
        """
        if self.config.route_name:
            return self.config.route_name
        if self.config.plural:
            return self.config.plural.replace('_', '-')
        return self._plural.replace('_', '-')


class AuthObject(AppObject):
    def __init__(
        self,
        name: str,
        *args: Attribute,
        config: AppConfig = AppConfig(),
        secure: bool = False,
    ):
        super().__init__(name, *args, config=config, secure=secure)


def BasicUser() -> AuthObject:
    """returns basic user as app object with attributes username and password"""
    return AuthObject(
        'user',
        UsernameAttribute(),
        StringAttribute('password'),
    )


def Role() -> AppObject:
    return AppObject('role', NameAttribute(default='user'))


def User() -> AuthObject:
    """Returns user as auth object with attributes username, password, first_name,
    last_name, email and relationship with roles. You need to create Role AppObject also.
    """
    user = AuthObject(
        'user',
        UsernameAttribute(),
        StringAttribute('password'),
        StringAttribute('first_name'),
        StringAttribute('last_name'),
        EmailAttribute(),
    )
    user.add_many_to_one_rel(Role(), 'role', 'users')
    return user


def Tag() -> AppObject:
    return AppObject('tag', NameAttribute(unique=True), DescriptionAttribute())
