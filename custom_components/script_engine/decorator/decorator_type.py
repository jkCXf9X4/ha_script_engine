
from enum import Enum

# ABC is for type check, if not overwritten this should cause an error

class DecoratorType(Enum):
    PRE = 1
    BOOLEAN = 2
    OPERAND = 3
    POST = 4
    OTHER = 0
    ABC = -1
