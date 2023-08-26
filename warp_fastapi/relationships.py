from enum import Enum, auto


class RelationshipType(Enum):
    one_to_many = auto()
    many_to_one = auto()
    one_to_one = auto()
    many_to_many = auto()


one_to_many = RelationshipType.one_to_many
many_to_one = RelationshipType.many_to_one
one_to_one = RelationshipType.one_to_one
many_to_many = RelationshipType.many_to_many
