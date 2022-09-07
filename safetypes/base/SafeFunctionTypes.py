from enum import unique, Enum


@unique
class SafeFunctionTypes(Enum):
    UNKNOWN = 0
    FUNCTION = 1
    STATIC_METHOD = 2
    CLASS_METHOD = 3
    INSTANCE_METHOD = 4
