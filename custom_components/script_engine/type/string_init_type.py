
class StringInitType:
    def __init__(self, str):
        self.item = self.to_item(str)

    def to_item(self, str) -> str:
        raise NotImplementedError()

    def __hash__(self):
        return hash(self.item)

    def check_type(self, other):
        if not isinstance(other, StringInitType):
            return NotImplemented

    def __eq__(self, other):
        self.check_type(other=other)
        return self.item == other.item

    def __ne__(self, other):
        self.check_type(other=other)
        return self.item != other.item

    def __lt__(self, other):
        self.check_type(other=other)
        return self.item < other.item

    def __le__(self, other):
        self.check_type(other=other)
        return self.item <= other.item

    def __gt__(self, other):
        self.check_type(other=other)
        return self.item > other.item

    def __ge__(self, other):
        self.check_type(other=other)
        return self.item >= other.item

    def __repr__(self) -> str:
        return self.item.__repr__()

    def __str__(self) -> str:
        return self.item.__str__()

    def __add__(self, other):
        self.check_type(other=other)
        return self.item + other.item

    def __sub__(self, other):
        self.check_type(other=other)
        return self.item - other.item
