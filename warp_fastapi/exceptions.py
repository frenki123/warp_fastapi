from enum import Enum


class RelMsgErr(Enum):
    MANY_MANY_ERR = 'Relationship of type many_to_many must have backpopulates object!'
    MISSING_BACKPOPULATES = 'Both backpopulates object and backpopulates name needs to be provided!'


class RelationshipException(Exception):
    """This is my own custom exception."""

    def __init__(self, type: RelMsgErr):
        super().__init__(type.value)
