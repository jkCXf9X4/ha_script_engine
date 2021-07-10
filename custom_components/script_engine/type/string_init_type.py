
class StringInitType:
    def __init__(self, str):
        self.item = self.to_item(str)

    def to_item(self, str) -> str:
        raise NotImplementedError()

    def __hash__(self):
        return hash(self.item)

    def __eq__(self, other):
        if not isinstance(other, StringInitType):
            return NotImplemented
        return self.item == other.item

    def __ne__(self, other):
        if not isinstance(other, StringInitType):
            return NotImplemented
        return self.item != other.item

    def __lt__(self, other):
        if not isinstance(other, StringInitType):
            return NotImplemented
        return self.item < other.item

    def __le__(self, other):
        if not isinstance(other, StringInitType):
            return NotImplemented
        return self.item <= other.item

    def __gt__(self, other):
        if not isinstance(other, StringInitType):
            return NotImplemented
        return self.item > other.item

    def __ge__(self, other):
        if not isinstance(other, StringInitType):
            return NotImplemented
        return self.item >= other.item

    def __repr__(self) -> str:
        return self.item.__repr__()

    def __str__(self) -> str:
        return self.item.__str__()

    def __add__(self, other):
        if not isinstance(other, StringInitType):
            return NotImplemented
        return self.item + other.item

    def __sub__(self, other):
        if not isinstance(other, StringInitType):
            return NotImplemented
        return self.item - other.item
